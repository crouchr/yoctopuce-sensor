# This is copied from metfuncs which is the MASTER

import math

# http://www.sciencebits.com/SnowProbCalc?calc=yes
# Based on the analysis of whether falling snow will melt as it descends, it is possible to estimate the
# probability with which falling precipitation will be snow.
# The calculator calculates the melting temperature associated with the given relative humidity.
# Below this temperature, snow cannot melt because of evaporation.
# At higher temperatures, it may snow, with a decreasing probability.
# Original code in php written by Nir Shaviv <nir.shaviv@mail.huji.ac.il>
# This code cannot be distributed
# Prof. Nir Shaviv
#
# Racah Institute of Physics
# The Hebrew University of Jerusalem
# T +972.54.4738555 | W +972.2.6585807 | F +972.5611519
# Email nir.shaviv@mail.huji.ac.il | Skype nirshaviv


def calc_snow_probability(air_temp_c, humidity):
    """
    Calculate the probability that precipitation will be snow

    :param air_temp_c: in degrees C
    :param humidity: relative humidity (percent)
    :return:
    """

    rh = float(humidity/100)
    frozen_temp_c = 10.49 * (1-rh)      # frozen_temp_c a.k.a. melting air temperature

    for i in range(1, 10):
        frozen_temp_c = 10.49 * (1-rh * math.exp(17.27 * frozen_temp_c / (238.3+frozen_temp_c)))

    x = float(air_temp_c - frozen_temp_c)
    prob = 0.5 + 0.5 * math.tanh((1 - x) * 1.8)

    prob_percent = int(prob * 100)

    if x < 0.0:
        prognosis_text = 'It will snow'
    elif x > 0.0 and x < 1.6 :
        prognosis_text = 'Probability for any precipitation to be snow is ' + prob_percent.__str__() + ' %'
    elif x > 1.6 and x < 2.2:
        prognosis_text = 'Very slim change of snow'
    else:
        prognosis_text = 'No chance of snow'

    return prognosis_text, round(frozen_temp_c, 1), prob_percent

# using rh = 80%
# 3 = slim chance of snow
# 2 = probability of snow = 72 %
# 1 = it will snow


if __name__ == '__main__':
    air_temp_c = 1
    humidity = 80
    prognosis_text, frozen_temp_c, prob_percent = calc_snow_probability(air_temp_c, humidity)
    print('Melting air temperature : ' + frozen_temp_c.__str__() + ' C')
    print('Probability of precipitation being snow : ' + prob_percent.__str__() + ' %')
    print(' => ' + prognosis_text)
