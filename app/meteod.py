
import sys
import time
import json
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import traceback

import paho.mqtt.client as paho
from pprint import pprint

import get_env_app
import meteo2_sensor


# artifacts (metfuncs)
# import mean_sea_level_pressure
# import dew_point
# import wet_bulb
# import cloud_base

# artifacts (metminifuncs)
# import moving_averages


def main():
    try:
        metrics = {}

        broker = get_env_app.get_mqttd_host()
        port = get_env_app.get_mqttd_port()
        topic = get_env_app.get_mqttd_topic()
        poll_secs = get_env_app.get_poll_secs()
        window_len = get_env_app.get_window_len()

        # pressure_smoothed = moving_averages.MovingAverage(window_len)
        # sea_level_pressure_smoothed = moving_averages.MovingAverage(window_len)
        # temperature_smoothed = moving_averages.MovingAverage(window_len)
        # humidity_smoothed = moving_averages.MovingAverage(window_len)
        # s1_m_avg = moving_averages.MovingAverage(window_len)
        # s2_m_avg = moving_averages.MovingAverage(window_len)

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
        hum_sensor, press_sensor, temperature_sensor, status_msg = meteo2_sensor.register_meteo2_sensor()
        print(status_msg)

        if status_msg != 'Meteo sensor registered OK':
            sys.exit('Exiting, unable to register Meteo sensor')

        while True:
            vane_height_m = float(get_env_app.get_vane_height_m())
            site_elevation_m = float(get_env_app.get_site_elevation())
            sensor_elevation_m = float(site_elevation_m) + float(vane_height_m)
            rain_k_factor = float(get_env_app.get_rain_k_factor())

            print(f'site_elevation_m : {site_elevation_m}')
            print(f'vane_height_m : {vane_height_m}')
            print(f'sensor_elevation_m : {sensor_elevation_m}') # sensor elevation
            print(f'rain_k_factor : {rain_k_factor}')

            # Read raw data from sensors
            humidity, pressure, temperature = meteo2_sensor.get_meteo_values(hum_sensor, press_sensor, temperature_sensor)

            # Calculate derived data
            # sea_level_pressure = pressure + mean_sea_level_pressure.msl_k_factor(sensor_elevation_m, temperature)
            # dew_point_c = dew_point.get_dew_point(temperature, humidity)
            # wet_bulb_c = wet_bulb.get_wet_bulb(temperature, pressure, dew_point_c)
            # cloud_base_ft = cloud_base.calc_cloud_base_ft(temperature, dew_point_c)

            # CRHUDA model https://www.researchgate.net/publication/337236701_Algorithm_to_Predict_the_Rainfall_Starting_Point_as_a_Function_of_Atmospheric_Pressure_Humidity_and_Dewpoint
            # This metric calculation should be moved OUT of cloudmetricsd
            # if dew_point_c < 1.0:
            #     crhuda_dew = 1.0
            # else:
            #     crhuda_dew = dew_point_c
            # s1 = humidity
            # s2_raw = round(pressure / crhuda_dew, 1)
            # s2 = round(rain_k_factor * (pressure / crhuda_dew), 1)
            #
            # if s2 > 150.0:
            #     s2 = 150.0
            #
            # s1_m_avg.add(s1)
            # s2_m_avg.add(s2)
            #
            # s1_avg = s1_m_avg.get_moving_average()
            # s2_avg = s2_m_avg.get_moving_average()

            # s2 slope -
            # s2_delta = s2_avg - s2_avg_last
            # s2_avg_last = s2_avg

            # add this metric in here once good values have been determined in a downstream daemon
            # in phase waiting for S2 to increase and cross S1
            # if s2_avg < s1_avg:
            #     crhuda_primed = 10.0
            # else:
            #     crhuda_primed = 0.0
            # end of CRHUDA

            # Smoothed data
            # pressure_smoothed.add(pressure)
            # sea_level_pressure_smoothed.add(sea_level_pressure)
            # humidity_smoothed.add(humidity)
            # temperature_smoothed.add(temperature)

            # meta information
            metrics['epoch'] = time.time()              # time the message was sent
            metrics['timestamp'] = time.ctime()
            metrics['window_len'] = window_len
            metrics['poll_secs'] = poll_secs
            metrics['topic'] = topic
            metrics['sensor_elevation_m'] = sensor_elevation_m

            # raw data
            metrics['temp_c'] = temperature                 # sensor height above sea-level
            metrics['humidity'] = humidity
            metrics['pressure_abs'] = pressure              # absolute i.e. not sea level

            # derived data
            # metrics['pressure_sea'] = sea_level_pressure    #
            # metrics['dew_point'] = dew_point_c
            # metrics['wet_bulb'] = wet_bulb_c
            # metrics['cloud_base_ft'] = cloud_base_ft
            # metrics['crhuda_primed'] = -10 # To be added in the future

            # smoothed data
            # metrics['temp_c_smoothed'] = temperature_smoothed.get_moving_average()
            # metrics['humidity_smoothed'] = humidity_smoothed.get_moving_average()
            # metrics['pressure_abs_smoothed'] = pressure_smoothed.get_moving_average()
            # metrics['pressure_sea_smoothed'] = sea_level_pressure_smoothed.get_moving_average()
            # metrics['crhuda_s1'] = s1_avg
            # metrics['crhuda_s2'] = s2_avg
            # metrics['crhuda_s2_delta'] = s2_delta

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
