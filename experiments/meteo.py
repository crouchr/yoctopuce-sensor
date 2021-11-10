# Fake a Yoctopuce Meteo v2 by pulling data from phase 1 Aercus and then 2 OpenWeather API (COWES/YARMOUTH)
import beep

# artifacts (metrestapi)
import cumulus_comms
# artifacts (metfuncs)
import mean_sea_level_pressure


# TODO : remove endpoint as a function parameter
def get_meteo_data(endpoint, site_height_m):
    """

    :param endpoint:
    :param site_height_m: Elevation of the AWS station above sea-level
    :return:
    """

    try:
        status_code, response_dict = cumulus_comms.call_rest_api(endpoint, query=None)

        # pprint(response_dict)
        # if status_code != 200:
        #     data_connection_up = 0                      # indicates any sort of comms error
        #     beep.warning(num_beeps = 3, sound=3)
        #     raise ValueError('Error : Failed to contact CumulusMX API, status_code=' + status_code.__str__())
        #
        # data_connection_alarm = response_dict['DataStopped']
        # if data_connection_alarm:       # true = connection failed
        #     data_connection_up = 0
        #     beep.warning(num_beeps=3, sound=3)
        #     raise ValueError('Error : WMR base station serial connection is not connected to CumulusMX')
        # else:
        #     data_connection_up = 1

        # Note : only numbers can be sent to Grafana
        # last_data_read = response_dict['LastDataRead']      # 13:09:32

        # unreliable on my WMR unit
        temp_c = round(float(response_dict['OutdoorTemp']), 1)
        humidity = round(float(response_dict['OutdoorHum']), 1)

        # Burt says to record pressure adjusted to MSL (Mean Sea Level)
        pressure = round(float(response_dict['Pressure']), 1)
        pressure = pressure + mean_sea_level_pressure.msl_k_factor(site_height_m, temp_c)

        pressure_trend = round(float(response_dict['PressTrend']), 1)
        cumulusmx_build = int(response_dict['Build'])                   # e.g. a Jenkins build number ?

        return data_connection_up, last_data_read, temp_c, humidity, pressure, pressure_trend, cumulusmx_build

    except Exception as e:
        print('get_meteo_data() : error=' + e.__str__())
        return data_connection_up, None, None, None, None, None, None
