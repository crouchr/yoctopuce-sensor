# This is copied from metfuncs which is the MASTER

# https://stackoverflow.com/questions/50508262/using-look-up-tables-in-python

# See Table 7.2 Burt book
# Stockcross 90m - not confirmed
# Currently using 50m to see if it lines up better with OpenWeatherAPI
# TODO : Could make more even accurate by adding interpolation
def msl_k_factor(height, temp_c):
    """
    See Burt Table 7.2 p.177
    :param height: of the site above sea level, e.g. Stockcross (metres)
    :param temp: external air temperature
    :return: correction factor
    """

    press_map = {
        0: [1.0, 1.0, 1.0, 1.0, 1.0],
        10: [1.3, 1.3, 1.2, 1.2, 1.1],
        20: [2.6, 2.5, 2.4, 2.3, 2.3],
        50: [6.5, 6.3, 6.0, 5.8, 5.6],
        90: [11.7, 11.3, 10.9, 10.5, 10.2]
    }

    height_rounded = int(round(height/10)*10)
    temp_rounded = int(round(temp_c/10)*10)

    col = int((temp_rounded + 10) / 10)

    row_list = press_map[height_rounded]

    k_factor = row_list[col]

    return k_factor


if __name__ == '__main__':
    height = 90
    temp_c = 9

    msl = msl_k_factor(height, temp_c)
    print(msl)
