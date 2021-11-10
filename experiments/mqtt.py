def write_to_mqtt(broker_host, broker_port, topic, pressure, temp_c, humidity):
    mqtt_msg = {}
    mqtt_msg['pressure'] = pressure

    print('wrote data to MQTT server OK')

    return True

# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import paho.mqtt.client as paho
# broker="192.168.1.184"
# port=1883
# def on_publish(client,userdata,result):             #create function for callback
#     print("data published \n")
#     pass
# client1= paho.Client("control1")                           #create client object
# client1.on_publish = on_publish                          #assign function to callback
# client1.connect(broker,port)                                 #establish connection
# ret= client1.publish("house/bulb1","on")

# Not sure I even need this
# def on_publish(client, userdata, result):             #create function for callback
#     print("data published\n")
#     pass


# test harness
if __name__ == '__main__':
    import random
    import time
    import json

    metrics = {}

    broker = "192.168.1.5"  # kube = dev machine
    port = 1883
    client1 = paho.Client("control1")                           #create client object
    # client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker, port)                                 #establish connection

    while True:
        random_temp = int(20 * random.random())
        temp_str = 'temp=' + random_temp.__str__()

        metrics['temp'] = random_temp
        metrics['humidity'] = 34.8
        metrics['pressure'] = 1022.9

        # ret = client1.publish("house/bulb1","on")
        MQTT_MSG = json.dumps(metrics)

        ret = client1.publish("meteo/metrics", MQTT_MSG)

        print(ret.__str__())
        time.sleep(3)