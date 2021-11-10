
import sys
import time
import json
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import paho.mqtt.client as paho

import get_env_app
import meteo2_sensor


def main():

    metrics = {}

    # broker = "192.168.1.5"  # kube = dev machine
    # port = 1883
    broker = get_env_app.get_mqttd_host()
    port = get_env_app.get_mqttd_port()
    topic = get_env_app.get_mqttd_topic()
    poll_secs = get_env_app.get_poll_secs()

    print('MQTT broker IP : ' + broker)
    print(f'MQTT broker port : {port}')
    print('MQTT topic : ' + topic)
    print(f'poll_secs : {poll_secs}')

    client1 = paho.Client("control1")  # create client object
    # client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker, port)

    hum_sensor, press_sensor, temperature_sensor, status_msg = meteo2_sensor.register_meteo2_sensor()
    print(status_msg)
    #
    if status_msg != 'Meteo sensor registered OK':
        sys.exit('Exiting, unable to register Meteo sensor')

    while True:
        humidity, pressure, temperature = meteo2_sensor.get_meteo_values(hum_sensor, press_sensor, temperature_sensor)
        metrics['epoch'] = time.time()       # time the message was sent
        metrics['timestamp'] = time.ctime()
        metrics['temp'] = temperature
        metrics['humidity'] = humidity
        metrics['pressure'] = pressure

        MQTT_MSG = json.dumps(metrics)

        # publish data to MQTT topic
        # ret = client1.publish(topic, MQTT_MSG)

        # print(ret.__str__())

        time.sleep(poll_secs)


if __name__ == '__main__':
    main()

