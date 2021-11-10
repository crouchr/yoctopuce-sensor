# See https://www.yoctopuce.com/EN/products/yocto-meteo-v2/doc/METEOMK2.usermanual.html#CHAP5SEC1

from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *


# Must be root to register the sensor
# SerialNumber: METEOMK2-18FD45
def register_meteo2_sensor(target='any'):
    """

    :param target:
    :return:
    """
    try:
        print('entered register_meteo2_sensor()')

        errmsg = YRefParam()

        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            msg = "Error : Meteo sensor init error : " + errmsg.value
            print(msg)
            return None, None, None, msg

        if target == 'any':
            # retrieve any sensor
            sensor = YHumidity.FirstHumidity()
            if sensor is None:
                msg = 'Error : check Meteo sensor USB cable'
                print(msg)
                return None, None, None, msg
            m = sensor.get_module()
            target = m.get_serialNumber()

        hum_sensor = YHumidity.FindHumidity(target + '.humidity')
        temp_sensor = YTemperature.FindTemperature(target + '.temperature')
        press_sensor = YPressure.FindPressure(target + '.pressure')

        if not (m.isOnline()):
            msg = 'Error : Meteo sensor not connected'
            print(msg)
            return None, None, None, msg

        print('Meteo sensor registered OK')
        print(hum_sensor.__str__())
        print(press_sensor.__str__())
        print(temp_sensor.__str__())

        return hum_sensor, press_sensor, temp_sensor, 'Meteo sensor registered OK'

    except Exception as e:
        print('register_meteo2_sensor() : exception : ' + e.__str__())
        YAPI.FreeAPI()
        return None, None, None, e.__str__()


def get_meteo_values(hum_sensor, press_sensor, temperature_sensor):
    """

    :param hum_sensor:
    :param press_sensor:
    :param temperature_sensor:
    :return:
    """

    if hum_sensor.isOnline():
        humidity = hum_sensor.get_currentValue()
        pressure = press_sensor.get_currentValue()
        temperature = temperature_sensor.get_currentValue()
    else:
        humidity = None
        pressure = None
        temperature = None

    return humidity, pressure, temperature


# Simple test loop
if __name__ == '__main__':
    hum_sensor, press_sensor, temperature_sensor, status_msg = register_meteo2_sensor()
    print(status_msg)

    if status_msg != 'Meteo sensor registered OK':
        sys.exit('Exiting, unable to register Meteo sensor')

    while True:
        print('---')
        humidity, pressure, temperature = get_meteo_values(hum_sensor, press_sensor, temperature_sensor)
        print('humidity=' + humidity.__str__())
        print('pressure=' + pressure.__str__())
        print('temperature=' + temperature.__str__())
        time.sleep(15)
