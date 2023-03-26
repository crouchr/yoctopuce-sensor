import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = int(os.environ['POLL_SECS'])
    else:
        poll_secs = 60

    return poll_secs


def get_window_len():
    """
    Moving average window length
    :return:
    """
    if 'WINDOW_LEN' in os.environ:
        window_len = int(os.environ['WINDOW_LEN'])
    else:
        window_len = int(15 * 60 / get_poll_secs())    # 15 minutes is the window

    return window_len


# Actual wind vane height to allow for multiplier
def get_vane_height_m():
    if 'VANE_HEIGHT' in os.environ:
        vane_height = os.environ['VANE_HEIGHT']
    else:
        #vane_height = 3.7       # Aercus weather station on top of shed
        vane_height = 1.0       # Yoctopuce sensor on side of shed

    return vane_height


# Solar multiplier = theoretical / measured on a cloudless day at noon
# def get_solar_multiplier():
#     if 'SOLAR_MULTIPLIER' in os.environ:
#         solar_multiplier = os.environ['SOLAR_MULTIPLIER']
#     else:
#         solar_multiplier = 1.7       # value in Ermin Street
#
#     return solar_multiplier


# def get_snow_prob():
#     if 'SNOW_PROBABILITY' in os.environ:
#         snow_prob_level = os.environ['SNOW_PROBABILITY']
#     else:
#         snow_prob_level = 80       # 80%
#
#     return float(snow_prob_level)


# fudge factor used by CRHUDA rain prediction algorithm
def get_rain_k_factor():
    if 'RAIN_K_FACTOR' in os.environ:
        rain_k_factor = os.environ['RAIN_K_FACTOR']
    else:
        rain_k_factor = 0.167

    return rain_k_factor

# This is internal name
def get_sensor_name():
    if 'SENSOR_NAME' in os.environ:
        sensor_name = os.environ['SENSOR_NAME']
    else:
        sensor_name = 'dev_test_sensor_1'

    return sensor_name

def get_public_sensor_name():
    """
    Return the public name of the sensor - may be less detailed than sensor_name
    e.g. preserve privacy
    :return:
    """
    if 'PUBLIC_SENSOR_NAME' in os.environ:
        public_sensor_name = os.environ['PUBLIC_SENSOR_NAME']
    else:
        public_sensor_name = 'Stockcross Public Sensor'

    return public_sensor_name

def get_sensor_city():
    if 'SENSOR_CITY' in os.environ:
        sensor_city = os.environ['SENSOR_CITY']
    else:
        sensor_city = 'Stockcross'

    return sensor_city
def get_sensor_location():
    if 'SENSOR_LOCATION' in os.environ:
        sensor_location = os.environ['SENSOR_LOCATION']
    else:
        sensor_location = 'Top room lab'

    return sensor_location

def get_sensor_notes():
    if 'SENSOR_NOTES' in os.environ:
        sensor_notes = os.environ['SENSOR_NOTES']
    else:
        sensor_notes = 'Here are some notes about this sensor'

    return sensor_notes

def get_sensor_postcode():
    if 'SENSOR_POSTCODE' in os.environ:
        sensor_postcode = os.environ['SENSOR_POSTCODE'].upper()
    else:
        sensor_postcode = 'rg20 8LH'.upper()

    return sensor_postcode
def get_sensor_latitude():
    if 'SENSOR_LATITUDE' in os.environ:
        sensor_latitude = os.environ['SENSOR_LATITUDE']
    else:
        sensor_latitude = '51.4151'

    return sensor_latitude
def get_sensor_longitude():
    if 'SENSOR_LONGITUDE' in os.environ:
        sensor_longitude = os.environ['SENSOR_LONGITUDE']
    else:
        sensor_longitude = '-1.3667'

    return sensor_longitude

# elevation in metres
def get_site_elevation():
    if 'SITE_ELEVATION' in os.environ:
        site_elevation = os.environ['SITE_ELEVATION']
    else:
        # FIXME : the mean_sea_level function cannot handle 0 - so fix it and return to default here of 0m
        site_elevation = 90      # default is sea-level - i.e. running on a boat at sea
    return site_elevation



# Use j1900 for live
def get_mqttd_host():
    """
    Determine the hostname that hosts the MQTT Daemon
    :return:
    """
    if 'STAGE' in os.environ and os.environ['STAGE'] == 'PRD':
        mqttd_host = 'mqttd'    # name of 'mqttd' container
    else:
        mqttd_host = 'j1900'    # IP of mqttd

    return mqttd_host


def get_mqttd_port():
    mqttd_port = 1883

    return mqttd_port


def get_mqttd_topic():
    topic = "meteo/metrics"

    return topic
