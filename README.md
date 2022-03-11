README
======
- Code for reading data from Yoctopuce met v2 
temp, pressure, humidity sensor and sending to MQTT topic for downstream processing

- Calculate derived values as well

- Provide smoothed values for critical parameters

- Ensure that any 'tweakable' values can be changed without restarting the container


TODO
----
- Add the crhuda values - and smoothed versions of

- run as a service on PI https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

RASP PI
=======
This has the drivers copied across - i.e. not imported

https://linuxhint.com/about-arm64-armel-armhf/