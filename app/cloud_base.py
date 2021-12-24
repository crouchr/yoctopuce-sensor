# https://en.wikipedia.org/wiki/Cloud_base
# This is copied from metfuncs which is the MASTER
def calc_cloud_base_ft(temp_c, dew_point_c):
    """
    Return an estimate of the cloud_base
    A cloud base (or the base of the cloud) is the lowest altitude of the visible portion of a cloud
    :param temp_c:
    :param dew_point_c:
    :return:
    """
    cloud_base_ft = 1000 * (abs(temp_c - dew_point_c) / 2.5)
    return int(cloud_base_ft)
