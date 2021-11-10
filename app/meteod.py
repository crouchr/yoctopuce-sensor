
import sys
import time
import json
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import traceback

import paho.mqtt.client as paho
from pprint import pprint

import get_env_app
import meteo2_sensor
import moving_averages

def main():
    try:
        metrics = {}

        broker = get_env_app.get_mqttd_host()
        port = get_env_app.get_mqttd_port()
        topic = get_env_app.get_mqttd_topic()
        poll_secs = get_env_app.get_poll_secs()
        window_len = get_env_app.get_window_len()

        print('MQTT broker IP : ' + broker)
        print(f'MQTT broker port : {port}')
        print('MQTT topic : ' + topic)
        print(f'poll_secs : {poll_secs}')
        print(f'window_len : {window_len}')

        pressure_smoothed = moving_averages.MovingAverage(window_len)
        temperature_smoothed = moving_averages.MovingAverage(window_len)
        humidity_smoothed = moving_averages.MovingAverage(window_len)

        client1 = paho.Client("control1")  # create client object
        # client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker, port)

        hum_sensor, press_sensor, temperature_sensor, status_msg = meteo2_sensor.register_meteo2_sensor()
        print(status_msg)

        if status_msg != 'Meteo sensor registered OK':
            sys.exit('Exiting, unable to register Meteo sensor')

        while True:
            humidity, pressure, temperature = meteo2_sensor.get_meteo_values(hum_sensor, press_sensor, temperature_sensor)

            pressure_smoothed.add(pressure)
            humidity_smoothed.add(humidity)
            temperature_smoothed.add(temperature)

            # meta information
            metrics['epoch'] = time.time()              # time the message was sent
            metrics['timestamp'] = time.ctime()
            metrics['elevation_m'] = 0
            metrics['window_len'] = window_len
            metrics['poll_secs'] = poll_secs

            # raw data
            metrics['temp_c'] = temperature               # sensor height above sea-level
            metrics['humidity'] = humidity
            metrics['pressure_abs'] = pressure     # absolute i.e. not sea level
            metrics['pressure_sea'] = -10          # not yet supported

            # derived data
            metrics['temp_c_smoothed'] = temperature_smoothed.get_moving_average()
            metrics['humidity_smoothed'] = humidity_smoothed.get_moving_average()
            metrics['pressure_abs_smoothed'] = pressure_smoothed.get_moving_average()

            MQTT_MSG = json.dumps(metrics)
            pprint(metrics)

            # publish payload to MQTT topic
            ret = client1.publish(topic=topic, payload=MQTT_MSG)
            print(ret.__str__())

            time.sleep(poll_secs)

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()
