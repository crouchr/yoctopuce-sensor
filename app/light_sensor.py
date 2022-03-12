
from yocto_lightsensor import *

def register_light_sensor(target='any'):
    try:
        print('entered register_light_sensor()')

        errmsg = YRefParam()

        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            msg = "Error : light sensor init error" + errmsg.value
            return None, msg

        if target == 'any':
            # retrieve any Light sensor
            sensor = YLightSensor.FirstLightSensor()
            if sensor is None:
                msg = 'Error : check light sensor USB cable'
                return None, msg
        else:
            sensor = YLightSensor.FindLightSensor(target + '.lightSensor')

        if not (sensor.isOnline()):
            msg = 'Error : light sensor device not connected'
            return None, msg

        print('light sensor registered OK')
        return sensor, 'light sensor registered OK'

    except Exception as e:
        print(e.__str__())
        YAPI.FreeAPI()
        return None


def get_lux(sensor):
    """
    Read light level (in Lux) from light sensor
    :param sensor:
    :return:
    """

    if sensor.isOnline():
        lux = sensor.get_currentValue()
        if lux < 0.1:
            lux = 0.0           # headlights of passing cars ?
        return lux
    else:
        return None
