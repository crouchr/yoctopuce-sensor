import sys
import time
import json
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import traceback

import paho.mqtt.client as paho
from pprint import pprint

import get_env
import get_env_app

# 2 x Yoctopuce sensors
import meteo2_sensor
import light_sensor

# artifacts (metfuncs)
import mean_sea_level_pressure
import dew_point
import wet_bulb
import cloud_base
import moon_phase
import solar_funcs
import solar_rad_expected
import snow_probability

# artifacts (metminifuncs)
import moving_averages

import simple_fog
import get_sunrise_sunset

def main():
    try:
        metrics = {}

        bypass_sensor = False    # i.e. set to True if no sensor attached during development

        version = get_env.get_version()
        broker = get_env_app.get_mqttd_host()
        port = get_env_app.get_mqttd_port()
        topic = get_env_app.get_mqttd_topic()
        poll_secs = get_env_app.get_poll_secs()
        window_len = get_env_app.get_window_len()
        sensor_started_timestamp = time.ctime()
        sensor_started_epoch = time.time()

        # Sensor information
        sensor_name = get_env_app.get_sensor_name()
        public_sensor_name = get_env_app.get_public_sensor_name()
        sensor_city = get_env_app.get_sensor_city()
        sensor_location = get_env_app.get_sensor_location()
        sensor_postcode = get_env_app.get_sensor_postcode()
        sensor_latitude = float(get_env_app.get_sensor_latitude())
        sensor_longitude = float(get_env_app.get_sensor_longitude())

        # smoothed values
        pressure_smoothed = moving_averages.MovingAverage(window_len)
        sea_level_pressure_smoothed = moving_averages.MovingAverage(window_len)
        temperature_smoothed = moving_averages.MovingAverage(window_len)
        humidity_smoothed = moving_averages.MovingAverage(window_len)
        s1_m_avg = moving_averages.MovingAverage(window_len)
        s2_m_avg = moving_averages.MovingAverage(window_len)

        print('MQTT broker IP : ' + broker)
        print(f'MQTT broker port : {port}')
        print('MQTT topic : ' + topic)
        print(f'poll_secs : {poll_secs}')
        print(f'window_len : {window_len}')

        client1 = paho.Client("control1")  # create client object
        # client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker, port)
        s2_avg_last = 0

        # Get the raw data from the Met sensor
        hum_sensor, press_sensor, temperature_sensor, meteo_status_msg = meteo2_sensor.register_meteo2_sensor()
        print("meteo sensor : " + meteo_status_msg)
        lux_sensor, lux_status_msg = light_sensor.register_light_sensor()
        print("light sensor : " + lux_status_msg)

        if meteo_status_msg != 'meteo sensor registered OK':
            sys.exit('Exiting, unable to register Yoctopuce meteo sensor')
        if lux_status_msg != 'light sensor registered OK':
            sys.exit('Exiting, unable to register Yoctopuce light sensor')

        while True:
            vane_height_m = float(get_env_app.get_vane_height_m())
            site_elevation_m = float(get_env_app.get_site_elevation())
            sensor_elevation_m = float(site_elevation_m) + float(vane_height_m)
            sensor_notes = get_env_app.get_sensor_notes()
            rain_k_factor = float(get_env_app.get_rain_k_factor())  # can tweak without restarting container
            print(f'site_elevation_m : {site_elevation_m}')
            print(f'vane_height_m : {vane_height_m}')
            print(f'sensor_elevation_m : {sensor_elevation_m}') # sensor elevation
            print(f'rain_k_factor : {rain_k_factor}')

            # date info
            utc_epoch = time.time()
            # local_time = time.ctime(utc_epoch)
            time_struct = time.gmtime(utc_epoch)  # gm = UTC
            tm_month = time_struct.tm_mon
            tm_year = time_struct.tm_year
            tm_day = time_struct.tm_mday
            tm_daylight_savings_time = time_struct.tm_isdst
            tm_zone = time_struct.tm_zone
            sensor_uptime_secs = int(utc_epoch - sensor_started_epoch) # seconds
            sensor_uptime_days = int(sensor_uptime_secs / (3600 * 24))

            # moon-related
            moon_phase_tuple = moon_phase.moon_phase(tm_month, tm_day, tm_year)
            moon_phase_description = moon_phase_tuple[1]
            moon_light_percent = moon_phase_tuple[2]

            # Read raw data from meteo sensor
            humidity, pressure, temperature = meteo2_sensor.get_meteo_values(hum_sensor, press_sensor, temperature_sensor, bypass_sensor=bypass_sensor)

            # Read raw data from light sensor
            lux = light_sensor.get_lux(lux_sensor)

            # Calculate derived data
            sea_level_pressure = pressure + mean_sea_level_pressure.msl_k_factor(sensor_elevation_m, temperature)
            dew_point_c = dew_point.get_dew_point(temperature, humidity)
            wet_bulb_c = wet_bulb.get_wet_bulb(temperature, pressure, dew_point_c)
            cloud_base_ft = cloud_base.calc_cloud_base_ft(temperature, dew_point_c)
            solar_watts = round(solar_funcs.convert_lux_to_watts(lux), 2)
            azimuth = solar_rad_expected.calc_azimuth(sensor_latitude, sensor_longitude)
            altitude = solar_rad_expected.calc_altitude(sensor_latitude, sensor_longitude)
            solar_watts_theoretical = round(solar_rad_expected.get_solar_radiation_theoretical(altitude), 2)
            sky_condition = solar_funcs.map_lux_to_sky_condition(lux)
            snow_prognosis_text, _, snow_prob_percent = snow_probability.calc_snow_probability(temperature, humidity)

            # Fog prediction
            predict_fog = simple_fog.fog_algo_yocto(temperature, dew_point_c, wet_bulb_c, humidity)


            # solar-related information - this uses external API - replace with local calculation
            # Add some error handling here - dodgy Internet etc
            status_code, response = get_sunrise_sunset.get_solar_info_api1(sensor_latitude, sensor_longitude)
            if status_code != 200:
                print('error : failed to get sunrise/set information, status_code=' + status_code.__str__())

            civil_twilight_begin = response['civil_twilight_begin']
            civil_twilight_end = response['civil_twilight_end']
            sunrise = response['sunrise']
            solar_noon = response['solar_noon']
            sunset = response['sunset']

            day_length = response['day_length']

            # CRHUDA model https://www.researchgate.net/publication/337236701_Algorithm_to_Predict_the_Rainfall_Starting_Point_as_a_Function_of_Atmospheric_Pressure_Humidity_and_Dewpoint
            # This metric calculation should be moved OUT of cloudmetricsd
            if dew_point_c < 1.0:
                crhuda_dew = 1.0
            else:
                crhuda_dew = dew_point_c
            s1 = humidity
            # s2_raw = round(pressure / crhuda_dew, 1)
            s2 = round(rain_k_factor * (pressure / crhuda_dew), 1)

            if s2 > 150.0:
                s2 = 150.0

            s1_m_avg.add(s1)
            s2_m_avg.add(s2)

            s1_avg = s1_m_avg.get_moving_average()
            s2_avg = s2_m_avg.get_moving_average()

            # s2 slope -
            s2_delta = s2_avg - s2_avg_last
            s2_avg_last = s2_avg

            # add this metric in here once good values have been determined in a downstream daemon
            # in phase waiting for S2 to increase and cross S1
            # if s2_avg < s1_avg:
            #     crhuda_primed = 10.0
            # else:
            #     crhuda_primed = 0.0
            # end of CRHUDA

            # Smoothed data
            pressure_smoothed.add(pressure)
            sea_level_pressure_smoothed.add(sea_level_pressure)
            humidity_smoothed.add(humidity)
            temperature_smoothed.add(temperature)

            # meta information
            metrics['epoch'] = time.time()              # time the message was sent
            metrics['timestamp'] = time.ctime()
            metrics['window_len'] = window_len
            metrics['poll_secs'] = poll_secs
            metrics['topic'] = topic
            metrics['version'] = version
            metrics['sensor_uptime_secs'] = sensor_uptime_secs
            metrics['sensor_uptime_days'] = sensor_uptime_days
            metrics['sensor_started_epoch'] = sensor_started_epoch
            metrics['sensor_started_timestamp'] = sensor_started_timestamp

            # sensor information
            metrics['sensor_name'] = sensor_name
            metrics['sensor_notes'] = sensor_notes
            metrics['public_sensor_name'] = public_sensor_name
            metrics['sensor_city'] = sensor_city
            metrics['sensor_location'] = sensor_location
            metrics['sensor_postcode'] = sensor_postcode
            metrics['sensor_latitude'] = sensor_latitude
            metrics['sensor_longitude'] = sensor_longitude
            metrics['sensor_elevation_m'] = sensor_elevation_m

            # Moon information
            metrics['moon_phase_description'] = moon_phase_description
            metrics['moon_light_percent'] = moon_light_percent

            # Sun information
            metrics['solar_azimuth'] = azimuth
            metrics['solar_altitude'] = altitude
            metrics['solar_watts_theoretical'] = solar_watts_theoretical

            # More solar information - via Internet API
            metrics['civil_twilight_begin'] = civil_twilight_begin
            metrics['civil_twilight_end'] = civil_twilight_end
            metrics['sunrise'] = sunrise
            metrics['solar_noon'] = solar_noon
            metrics['sunset'] = sunset
            metrics['day_length'] = day_length

            # Snow information
            metrics['snow_prognosis_text'] = snow_prognosis_text
            metrics['snow_probability_percent'] = snow_prob_percent

            # Meteo sensor reading data
            metrics['temp_c'] = temperature                 # sensor height above sea-level
            metrics['humidity'] = humidity
            metrics['pressure_abs'] = pressure              # absolute i.e. not sea level
            metrics['lux'] = lux
            metrics['solar_watts'] = solar_watts

            # derived data
            metrics['pressure_sea'] = sea_level_pressure    #
            metrics['dew_point'] = dew_point_c
            metrics['wet_bulb'] = wet_bulb_c
            metrics['sky_condition'] = sky_condition
            metrics['cloud_base_ft'] = cloud_base_ft
            metrics['crhuda_primed'] = -10      # To be added in the future

            # predictions
            metrics['predict_fog'] = predict_fog

            # smoothed data
            metrics['temp_c_smoothed'] = temperature_smoothed.get_moving_average()
            metrics['humidity_smoothed'] = humidity_smoothed.get_moving_average()
            metrics['pressure_abs_smoothed'] = pressure_smoothed.get_moving_average()
            metrics['pressure_sea_smoothed'] = sea_level_pressure_smoothed.get_moving_average()
            metrics['crhuda_s1'] = s1_avg
            metrics['crhuda_s2'] = s2_avg
            metrics['crhuda_s2_delta'] = s2_delta

            MQTT_MSG = json.dumps(metrics)
            pprint(metrics)

            # publish payload to MQTT topic
            ret = client1.publish(topic=topic, payload=MQTT_MSG)
            print('mqtt publish status : ' + ret.__str__())

            time.sleep(poll_secs)

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()
