# See https://www.yoctopuce.com/EN/products/yocto-meteo-v2/doc/METEOMK2.usermanual.html#CHAP5SEC1

from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *


# Must be root to register the sensor
# SerialNumber: METEOMK2-18FD45
def register_meteo2_sensor(target='any', bypass_sensor=False):
    """

    :param target:
    :return:
    """
    try:
        print('Entered register_meteo2_sensor()')
        if bypass_sensor:
            return None, None, None, 'Emulated that Meteo sensor registered OK'

        errmsg = YRefParam()

        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            msg = "Error : meteo sensor init error : " + errmsg.value
            print(msg)
            return None, None, None, msg
        else:
            print('meteo sensor registered OK')

        module = YModule.FirstModule()
        serial_number = module.get_module()         # FIXME : add to metrics
        product_name = module.get_productName()     # FIXME : add to metrics
        print("serial_number is " + serial_number.__str__())
        print("product_name is " + product_name.__str__())

        if target == 'any':
            # retrieve any sensor
            sensor = YHumidity.FirstHumidity()
            if sensor is None:
                msg = 'Error : Check Meteo sensor USB cable'
                print(msg)
                return None, None, None, msg
            m = sensor.get_module()
            target = m.get_serialNumber()

        hum_sensor = YHumidity.FindHumidity(target + '.humidity')
        temp_sensor = YTemperature.FindTemperature(target + '.temperature')
        press_sensor = YPressure.FindPressure(target + '.pressure')

        if not (m.isOnline()):
            msg = 'Error : meteo sensor not connected'
            print(msg)
            return None, None, None, msg

        print('Meteo sensor registered OK')
        print(hum_sensor.__str__())
        print(press_sensor.__str__())
        print(temp_sensor.__str__())

        return hum_sensor, press_sensor, temp_sensor, 'meteo sensor registered OK'

    except Exception as e:
        print('register_meteo2_sensor() : exception : ' + e.__str__())
        YAPI.FreeAPI()
        return None, None, None, e.__str__()


def get_meteo_values(hum_sensor, press_sensor, temperature_sensor, bypass_sensor=False):
    """

    :param hum_sensor:
    :param press_sensor:
    :param temperature_sensor:
    :return:
    """

    if bypass_sensor:
        return 60.0, 990.0, 25.0
    recovered = False

    while True:
        try:
            if hum_sensor.isOnline():
                humidity = hum_sensor.get_currentValue()
                pressure = press_sensor.get_currentValue()
                temperature = temperature_sensor.get_currentValue()
                if humidity is not None and pressure is not None and temperature is not None:
                    if recovered:
                        print('get_meteo_values() : yoctopuce sensor recovered')
                    return humidity, pressure, temperature
            else:
                print('get_meteo_values() : error : failed to read met data from yoctopuce, so sleeping...')
                recovered = True
                time.sleep(5)
        except Exception as e:
            print(f"get_meteo_values() : exception : {e}, so sleeping...")
            recovered = True
            time.sleep(5)


# Simple test loop
if __name__ == '__main__':
    hum_sensor, press_sensor, temperature_sensor, status_msg = register_meteo2_sensor()
    print(status_msg)

    if status_msg != 'meteo sensor registered OK':
        sys.exit('Exiting, unable to register Meteo sensor')

    while True:
        print('---')
        print(time.ctime())
        humidity, pressure, temperature = get_meteo_values(hum_sensor, press_sensor, temperature_sensor)
        print('humidity=' + humidity.__str__())
        print('pressure=' + pressure.__str__())
        print('temperature=' + temperature.__str__())
        time.sleep(15)
