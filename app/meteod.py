# wet-bulb needs numpy
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/

import sys
import time
import json

import traceback
import random
import paho.mqtt.client as paho
from pprint import pprint
import platform

import get_env
import get_env_app
import meteo2_sensor
import dew_point
import frost_point

# The MASTER of these files are in artifacts (metfuncs)
import mean_sea_level_pressure
import cloud_base
import snow_probability

# artifacts (metminifuncs)
# import moving_averages

client_id = 'meteod-' + str(random.randint(0, 1000))
print(f'client_id : {client_id}')


def connect_mqtt(broker_ip, port):

    client = paho.Client(client_id)  # create client object
    client.on_log = on_log
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.connect(broker_ip, port)
    return client


def on_connect(client, userdata, flags, rc):
    print(time.ctime() + f' on_connect() : CONNACK received with code {rc}')


def on_publish(client, userdata, mid):
    print(time.ctime() + f" on_publish() : Mid: {mid}")


def on_disconnect(client, userdata, rc):
    print(time.ctime() + " on_disconnect() : client disconnected ok")


def on_log(client, userdata, level, buf):
    print(time.ctime() + " on_log() => ", buf)


def main():
    try:
        metrics = {}
        msg_num = 0

        stage = get_env.get_stage()
        broker_ip = get_env_app.get_mqttd_host()
        port = get_env_app.get_mqttd_port()
        topic = get_env_app.get_mqttd_topic()
        poll_secs = get_env_app.get_poll_secs()
        window_len = get_env_app.get_window_len()
        my_node_name = platform.node()

        if stage == 'DEV':
            emulate = True
        else:
            emulate = False

        # pressure_smoothed = moving_averages.MovingAverage(window_len)
        # sea_level_pressure_smoothed = moving_averages.MovingAverage(window_len)
        # temperature_smoothed = moving_averages.MovingAverage(window_len)
        # humidity_smoothed = moving_averages.MovingAverage(window_len)
        # s1_m_avg = moving_averages.MovingAverage(window_len)
        # s2_m_avg = moving_averages.MovingAverage(window_len)

        print('MQTT broker IP : ' + broker_ip)
        print(f'MQTT broker port : {port}')
        print('MQTT topic : ' + topic)
        print(f'poll_secs : {poll_secs}')
        print(f'window_len : {window_len}')
        print(f'stage : {stage}')

        client = connect_mqtt(broker_ip, port)
        client.loop_start()

        # client_id = 'meteod-' + str(random.randint(0, 100))
        # client1 = paho.Client(client_id)  # create client object
        # client1.on_log = on_log
        # client1.connect(broker, port)

        s2_last = 0

        # Get the raw data from the Met sensor
        hum_sensor, press_sensor, temperature_sensor, status_msg = meteo2_sensor.register_meteo2_sensor(emulate=emulate)
        print(status_msg)

        if status_msg != 'Meteo sensor registered OK':
            sys.exit('Exiting, unable to register Yoctopuce Meteo sensor')

        while True:
            try:
                vane_height_m = float(get_env_app.get_vane_height_m())
                site_elevation_m = float(get_env_app.get_site_elevation())
                sensor_elevation_m = float(site_elevation_m) + float(vane_height_m)
                crhuda_s1_coeff = float(get_env_app.get_crhuda_s1_coeff())
                crhuda_s2_offset = get_env_app.get_crhuda_s2_offset()

                print(f'site_elevation_m : {site_elevation_m}')
                print(f'vane_height_m : {vane_height_m}')
                print(f'sensor_elevation_m : {sensor_elevation_m}') # sensor elevation
                print(f'crhuda_s1_coeff : {crhuda_s1_coeff}')
                print(f'crhuda_s2_offset : {crhuda_s2_offset}')

                msg_num = msg_num + 1
                if msg_num > 99999:
                    msg_num=0

                # Read raw data from sensors
                humidity, pressure, temperature = meteo2_sensor.get_meteo_values(hum_sensor, press_sensor, temperature_sensor, emulate=emulate)

                # Calculate derived data
                sea_level_pressure = round(pressure + mean_sea_level_pressure.msl_k_factor(sensor_elevation_m, temperature), 1)
                dew_point_c = round(dew_point.calc_dew_point(temperature, humidity), 1)
                # wet_bulb_c = wet_bulb.get_wet_bulb(temperature, pressure, dew_point_c)
                cloud_base_ft = cloud_base.calc_cloud_base_ft(temperature, dew_point_c)
                snow_probability_val = snow_probability.calc_snow_probability(temperature, humidity)
                frost_point_c = round(frost_point.calc_frost_point_c(temperature, dew_point_c), 1)

                # CRHUDA model https://www.researchgate.net/publication/337236701_Algorithm_to_Predict_the_Rainfall_Starting_Point_as_a_Function_of_Atmospheric_Pressure_Humidity_and_Dewpoint
                # This metric calculation should be moved OUT of cloudmetricsd
                if dew_point_c < 1.0:
                    crhuda_dew = 1.0
                else:
                    crhuda_dew = dew_point_c

                # rain_k_factor : the paper mentions scaling humidity
                s1 = round(humidity * crhuda_s1_coeff, 1)
                s2_raw = round(pressure / crhuda_dew, 1)

                s2 = s2_raw + crhuda_s2_offset

                #
                if s2 > 150.0:
                    s2 = 150.0

                # s1_m_avg.add(s1)
                # s2_m_avg.add(s2)
                #
                # s1_avg = s1_m_avg.get_moving_average()
                # s2_avg = s2_m_avg.get_moving_average()

                # s2 slope -
                s2_delta = round(s2 - s2_last, 1)
                s2_last = s2

                # add this metric in here once good values have been determined in a downstream daemon
                # in phase waiting for S2 to increase and cross S1
                # if s2 < s1:
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
                metrics['publisher'] = my_node_name
                metrics['msg_num'] = msg_num
                metrics['timestamp'] = time.ctime()
                metrics['topic'] = topic

                # environment variables information
                metrics['window_len'] = window_len
                metrics['poll_secs'] = poll_secs
                metrics['sensor_elevation_m'] = sensor_elevation_m
                metrics['crhuda_s1_coeff'] = crhuda_s1_coeff
                metrics['crhuda_s2_offset'] = crhuda_s2_offset

                # raw metrics
                metrics['temp_c'] = temperature                 # sensor height above sea-level
                metrics['humidity'] = humidity
                metrics['pressure_abs'] = pressure              # absolute i.e. not sea level

                # derived metrics
                metrics['pressure_sea'] = sea_level_pressure    #
                metrics['dew_point'] = dew_point_c
                metrics['frost_point'] = frost_point_c
                metrics['snow_probability'] = snow_probability_val[2]
                metrics['cloud_base_ft'] = cloud_base_ft

                # Needs more work to get to work on Pi
                # metrics['wet_bulb'] = wet_bulb_c
                # metrics['crhuda_primed'] = crhuda_primed

                # smoothed data
                # metrics['temp_c_smoothed'] = temperature_smoothed.get_moving_average()
                # metrics['humidity_smoothed'] = humidity_smoothed.get_moving_average()
                # metrics['pressure_abs_smoothed'] = pressure_smoothed.get_moving_average()
                # metrics['pressure_sea_smoothed'] = sea_level_pressure_smoothed.get_moving_average()
                # metrics['crhuda_s1'] = s1_avg
                # metrics['crhuda_s2'] = s2_avg
                # metrics['crhuda_s2_delta'] = s2_delta

                metrics['crhuda_s1'] = s1
                metrics['crhuda_s2_raw'] = s2_raw
                metrics['crhuda_s2_tuned'] = s2
                metrics['crhuda_s2_delta'] = s2_delta

                MQTT_MSG = json.dumps(metrics)
                pprint(metrics)

                # publish payload to MQTT topic
                ret = client.publish(topic=topic, payload=MQTT_MSG, qos=1)
                publish_status = ret[0]
                msg_num = ret[1]
                # print('mqtt publish_status : ' + publish_status.__str__())
                # print('mqtt msg_num : ' + msg_num.__str__())

                # Try a single retry : FIXME : make this exponential backoff
                if publish_status != 0:
                    backoff = 30
                    print(f'publish failed, publish_status={publish_status}, waiting {backoff} secs to re-connect...')
                    time.sleep(backoff)
                    client = connect_mqtt(broker_ip, port)
                    client.publish(topic=topic, payload=MQTT_MSG, qos=1)

                time.sleep(poll_secs)

            except Exception as e:
                backoff = 30
                print(f'exception={e}')
                traceback.print_exc()
                print(f'waiting {backoff} secs to re-connect...')
                time.sleep(backoff)
                client = connect_mqtt(broker_ip, port)
                continue

    except Exception as e:
        print(f'fatal exception={e}, aborting...')
        traceback.print_exc()
        sys.exit(-1)


if __name__ == '__main__':
    main()
