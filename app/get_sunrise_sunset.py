# copied from metmini-misc
# Access external API at https://sunrise-sunset.org/api
import requests
import json


def convert_to_24_hour(time_str):
    """

    :param time_str: e.g. '7:23:23 PM'
    :return: '19:23:23'

    """
    parts = time_str.split(':')
    hours = int(parts[0])
    mins = int(parts[1])
    secs = int(parts[2].split(' ')[0])

    if 'PM' in time_str and hours != 12:
        hours += 12

    time_24_hour = "%02d" % hours + ':' + "%02d" % mins + ':' + "%02d" % secs    # add leading zero

    return time_24_hour


def get_solar_info_api1(lat, lon):
    """
    Call external API and get sunrise/sunset etc. and convert to 24 hour format
    :param lat:
    :param lon:
    :return:
    >>> get_solar_info_api1(51.4146, -1.3749)

    """
    answer = {}

    url = "https://api.sunrise-sunset.org/json?" +\
        "lat=" + lat.__str__() + \
        "&lng=" + lon.__str__() + \
        "&date=today"

    response = requests.get(url)

    if response.status_code != 200:
        return response.status_code, None

    response_dict = json.loads(response.content.decode('utf-8'))

    answer['civil_twilight_begin'] = convert_to_24_hour(response_dict['results']['civil_twilight_begin'])
    answer['sunrise'] =  convert_to_24_hour(response_dict['results']['sunrise'])
    answer['solar_noon'] = convert_to_24_hour(response_dict['results']['solar_noon'])
    answer['sunset'] =  convert_to_24_hour(response_dict['results']['sunset'])
    answer['civil_twilight_end'] = convert_to_24_hour(response_dict['results']['civil_twilight_end'])
    answer['day_length'] = response_dict['results']['day_length']

    return response.status_code, answer


# testing
if __name__ == '__main__':

    my_lat = 51.4146
    my_lon = -1.3749

    print('lat = ' + my_lat.__str__())
    print('lon = ' + my_lon.__str__())

    status_code, response = get_solar_info_api1(my_lat, my_lon)

    if status_code != 200:
        print('status_code=' + status_code.__str__())

    print('civil_twilight_begin = ' + response['civil_twilight_begin'])
    print('sunrise = ' + response['sunrise'])
    print('solar_noon = ' + response['solar_noon'])
    print('sunset = ' + response['sunset'])
    print('civil_twilight_end = ' + response['civil_twilight_end'])
    print('day_length = ' + response['day_length'])

    print('finished')



