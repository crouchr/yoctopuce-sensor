README
======
- Code for reading data from Yoctopuce met v2 
temp, pressure, humidity sensor and sending to MQTT topic for downstream processing

- Calculate derived values as well

- Provide smoothed values for critical parameters

- Ensure that any 'tweakable' values can be changed without restarting the container


PRINCIPLES
----------
- This container must not connect to any Internet services - its focus is on publishing to MQRR

TODO
----
- Add the crhuda values - and smoothed versions of

TESTING
-------
- check that crhuda values can all be tweaked without interrupting container
- check that container can be built on Rasp Pi - if not it may mean keeping only the most basic of metrics
