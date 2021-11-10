# Re-usable code for subscribing to a topic

import time
import paho.mqtt.client as mqttClient
import get_env_app

Connected = False   # global variable for the state of the connection


def connect_mqtt(client_id) -> mqttClient:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected to MQTT Broker OK")
        else:
            print("failed to connect !, return code %d\n", rc)

    broker_host = get_env_app.get_mqttd_host()
    broker_port = get_env_app.get_mqttd_port()

    print('broker_host=' + broker_host.__str__())
    print('broker_port=' + broker_port.__str__())

    client = mqttClient.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker_host, broker_port)

    return client


# common funcs
def on_connect(client, userdata, flags, rc):
    # print('entered on_connect()')
    if rc == 0:
        print(time.ctime() + " : connected to MQTT Broker OK")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("connection to MQTT Broker failed !")