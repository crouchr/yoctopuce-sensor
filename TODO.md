TODO
====

PRIORITY 
---------
- eliminate all use of artifacts - have all the source in the project and mark up the sources to indicate this
- test container can be built on Rasp Pi

OTHER
-----
- add some logging to papertrail ?
- add moonrise and moonset times
- add okta calculation
- add evapotranspiration metric 
- add is_day, is_night, is_full_moon
- add a function 'full_moon in x days'
- add is_freezing
- is_spring_tide, is_neap_tide
- add last_freezing_days_ago - i.e. when can plants be planted out ?
- add is_foggy (set wind_speed = 0)
- serial_number = module.get_module()         # FIXME : add to metrics
- product_name = module.get_productName()     # FIXME : add to metrics
- add three hour pressure trend - like cumulus 'rising quickly' - e.g. met office style
- add three hour pressure trend - quantitative - e.g. met office style
- add forecast based on pressure trend
- theoretical solar charging watts ? - is there a calculation on internet ?

DONE
----
- add sunrise and sunset times - done but need to test with network failures
- add fog prediction - done

CHAOS MONKEYS
-------------
- Test case where both sensors are unplugged at random 
- Ensure the event is loggable, trapped by exception, recoverable 

BUGS
----
- handle cases where data returned by the sensors may be 'None' - e.g.
vane_height_m : 1.0
sensor_elevation_m : 91.0
rain_k_factor : 0.167
Traceback (most recent call last):
  File "/home/crouchr/PycharmProjects/yoctopuce-sensor/app/meteod.py", line 120, in main
    sea_level_pressure = pressure + mean_sea_level_pressure.msl_k_factor(sensor_elevation_m, temperature)
  File "/usr/lib/python3.10/site-packages/mean_sea_level_pressure.py", line 24, in msl_k_factor
    temp_rounded = int(round(temp_c/10)*10)
TypeError: unsupported operand type(s) for /: 'NoneType' and 'int'

