# functions related to solar radiation

def convert_lux_to_watts(lux):
    """

    :param lux:
    :return:
    """
    watts = lux * 0.0079

    return watts


def convert_watts_to_lux(watts):
    """

    :param watts:
    :return:
    """
    lux = watts * (1 / 0.0079)

    return lux


# fixme : add time so that 'sunset/sunrise' can be added
# fixme - full moon is not reliable
def map_lux_to_sky_condition(lux):
    """

    :param lux:
    :return:
    >>> map_lux_to_sky_condition(0.1)
    'dark'
    >>> map_lux_to_sky_condition(8.0)
    'twilight'
    >>> map_lux_to_sky_condition(100.0)
    'overcast'
    >>> map_lux_to_sky_condition(10000.0)
    'daylight'
    >>> map_lux_to_sky_condition(50000.0)
    'bright sky'
    """
    if lux <= 1:
        condition = 'dark'
    elif lux <= 10:
        condition = 'twilight'
    elif lux <= 1000:
        condition = 'overcast'
    elif lux <= 30000:
        condition = 'daylight'
    elif lux <= 100000:
        condition = 'bright sky'

    return condition
