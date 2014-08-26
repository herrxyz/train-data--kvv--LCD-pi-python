#!/usr/bin/python
import urllib2
import json
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
import time
from datetime import datetime
import RPi.GPIO as GPIO
import os


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 1000)  # channel=7 frequency=1000Hz
p.start(0) # 0-100, 30= prozent 


lcd = Adafruit_CharLCD()
lcd.begin(16, 1)

running = True
while running:
	#light out when i'm home, tested by ping my computer and gadgets in home-network
	os.system('ping 192.168.178.52 -w 2| grep "ttl" > ping.txt') #julian tablet
	os.system('ping 192.168.178.53 -w 2| grep "ttl" >> ping.txt') #julian tower-pc
	os.system('ping 192.168.178.61 -w 2| grep "ttl" >> ping.txt') #julian smartphone
	with open('ping.txt') as f:
		bla = f.readlines()
		if bla == []:
			print "lightoff"
			p.ChangeDutyCycle(0)	

		else:
			# print "lighton"
			p.ChangeDutyCycle(70)
			
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
			
p.stop()
GPIO.cleanup()
