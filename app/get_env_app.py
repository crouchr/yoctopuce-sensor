import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 300     # same as polling OpenWeather API

    return poll_secs


# Actual wind vane height to allow for multiplier
# def get_vane_height_m():
#     if 'VANE_HEIGHT' in os.environ:
#         vane_height = os.environ['VANE_HEIGHT']
#     else:
#         vane_height = 3.7       # value in Ermin Street
#
#     return vane_height


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


# elevation in metres
# def get_site_elevation():
#     if 'SITE_ELEVATION' in os.environ:
#         site_elevation = os.environ['SITE_ELEVATION']
#     else:
#         site_elevation = 0      # default is sea-level - i.e. running on a boat at sea
#
#     return site_elevation


# elevation in metres
# def get_rain_k_factor():
#     if 'RAIN_K_FACTOR' in os.environ:
#         rain_k_factor = os.environ['RAIN_K_FACTOR']
#     else:
#         rain_k_factor = 0.167
#
#     return rain_k_factor


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
