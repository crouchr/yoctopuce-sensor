# copied from display-generator AND modified to return 0 or 1
# Simplified version for use with Yoctopuce

# algorithms for predicting fog
# find the range that contains all three values and it must be less than a threshold I can adjust
# This will work with data calculated with an AWS
# add lux in as < 10K ?
def fog_algo_yocto(temp_c, dew_point_c, wet_bulb_c, humidity, permitted_range=0.1):
    """
    :param temp_c:
    :param dew_point_c:
    :param wet_bulb_c:
    :param wind_knots_2m: Wind speed at 2m high (not 10m)
    :param solar: Watts (integer)
    :param humidity: relative humidity
    :param permitted_range: All 3 temperatures must be within this range
    :return:
    """

    # fog won't form if wind speed is too high - this is from my own observations - not seen a rule
    # if wind_knots_2m >= 8.0:
    #     return False

    if humidity < 100.0:
        return 0

    # if solar >= 80:      # too light for fog i.e. sun starting to burn off ?
    #     return False

    temps = [temp_c, dew_point_c, wet_bulb_c]

    max_temp = max(temps)
    min_temp = min(temps)

    temp_range = max_temp - min_temp

    if temp_range <= permitted_range:
        return 1
    else:
        return 0
