train-data--kvv--LCD-pi-python
==============================

using an 20x2 LCD display to show time, date and departure of next train into city (due to small screen only one direction)
if there are less then 3min until departure, next train is shown instead
script wait and backlight of LCD is turned off when i'm not at home or sleep, measured by pinging computer, smartphone etc in local network
data is collected from live.kvv.de via json

to do: get road works / disruption / changes of train route from kvv
to do: turn LCD complete off when away



to get it work: install python with json, urllib2, Adafruit_CharLCD and RPi.GPIO libraries and make empty file "ping.txt" in same folder with r/w access
