#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
from Adafruit_CharLCD import Adafruit_CharLCD
from Adafruit_MCP230xx import MCP230XX_GPIO
from subprocess import *
import time
from datetime import datetime
import os



# bus = 1         # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
# address = 0x20  # I2C address of the MCP230xx chip.
# gpio_count = 16  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.
# Create MCP230xx GPIO adapter.
# mcp = MCP230XX_GPIO(bus, address, gpio_count)
mcp = MCP230XX_GPIO(1, 0x20, 16) #hardcoded bus,adress and number of pins (16 for mcp23017)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp) #pins A1-A6, A0 and A7 unused, D4 lcd = A3 mpc, D5 lcd = A4 mcp, ...



# prüfen ob schon da ist
os.system('ls /sys/class/gpio | grep "gpio4" > /var/tmpram/gpio4.txt')
with open('/var/tmpram/gpio4.txt') as f:
		blubb = f.readlines()
		print blubb
		if blubb == []:
			os.system('sudo echo 4 > /sys/class/gpio/export') #pin 4 Pi means Pin7 board
os.system('sudo echo out > /sys/class/gpio/gpio4/direction')

running = True
while running:
	#light out when i'm home, tested by ping my computer and gadgets in home-network
	os.system('ping 192.168.178.52 -w 2| grep "ttl" > /var/tmpram/ping.txt') #my tablet
	os.system('ping 192.168.178.53 -w 2| grep "ttl" >> /var/tmpram/ping.txt') #my tower-pc
	os.system('ping 192.168.178.61 -w 2| grep "ttl" >> /var/tmpram/ping.txt') #my smartphone
	with open('/var/tmpram/ping.txt') as f:
		bla = f.readlines()
		if bla == []:
			print "lightoff"
			os.system('sudo echo 0 > /sys/class/gpio/gpio4/value') #licht aus
			lcd.clear()
			# lcd.message(datetime.now().strftime('%H:%M   %d.%m.%y\n')) # print time & date
			# lcd.message('ping fail')

		else:
			print "lighton"
			url = "http://live.kvv.de/webapp/departures/bystop/de:8212:404?maxInfos=3&key=377d840e54b59adbe53608ba1aad70e8"	
			jsonstring = urllib2.urlopen(url).read()
			kvvdata = json.loads(jsonstring)
			
			if 'departures' in kvvdata:
				for i in range (0 , 3):
					# print kvvdata['departures'][i]['direction']
					# print 'das oben ist die richtung'
					kvvdata['departures'][i]['direction']
					if kvvdata['departures'][i]['direction'] == u'1': #direction 1 = into city, written as u'number' in jsondata
						linie = kvvdata['departures'][i]['route']
						ziel = kvvdata['departures'][i]['destination']
						restzeit = kvvdata['departures'][i]['time']
						# print restzeit
						if restzeit == u'0': #if less then 3min left, print next
							continue
						if restzeit == u'1 min':
							continue
						if restzeit == u'2 min':
							continue
						if restzeit == u'3 min':
							continue
						# print "route"
						os.system('sudo echo 1 > /sys/class/gpio/gpio4/value') #licht an
						lcd.clear()
						lcd.message(datetime.now().strftime('%H:%M   %d.%m.%y\n')) # print time & date
						if linie == u'S2':
							lcd.message('{0} {1} {2}'.format(linie,ziel[0:7],restzeit))
						else:				
							lcd.message('{0} {1} {2}'.format(linie,ziel[0:8],restzeit))
						# dazu noch len(restzeit) wenn mehr als 10min noch passt einbauen (nur 0:30uhr irgendwie)
						
			else:
				lcd.clear()
				lcd.message(datetime.now().strftime('%H:%M   %d.%m.%y\n')) # print time & date
				lcd.message('KVV error')
	time.sleep(15)		
	
os.system('sudo echo 4 > /sys/class/gpio/unexport')
			

# error:  File "./kvv2.py", line 53, in <module>
		# # print 'das oben ist die richtung' um 02:30 uhr, S2 rheinstetten um 03:18
		# IndexError: list index out of range

