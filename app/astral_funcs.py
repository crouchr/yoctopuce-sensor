# https://github.com/sffjunkie/astral/blob/master/src/docs/index.rst
# TODO : dusk etc

import datetime
from astral import moon


# FIXME : use current time
def get_moon_days():
    moon_days = round(moon.phase(datetime.date(2018, 1, 1)),2)
    return moon_days


if __name__ == '__main__':
    get_moon_days()
