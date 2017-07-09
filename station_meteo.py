#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()

while True:
    r = requests.get("http://api.wunderground.com/api/67b3e8dedd282c83/forecast/lang:FR/q/CH/Sion.json")
    data = r.json()
    i=0
    for day in data['forecast']['simpleforecast']['forecastday']:
        i+=1
        
        str1 = day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius']
        str2 = day['conditions']
        if str2[0:13] == 'Partiellement' :
            str2 = 'Part. ' + str2[14:]
        strx = str1 + "\n" + str2
        if i == 2 :
            stry = strx
        

        tempMin = int(day['low']['celsius'])
        tempMax = int(day['high']['celsius'])

        if tempMin < 0 :
            lcd.set_color(0,0,1) # temp min < 0 -> color = blue
        elif tempMax > 30 :
            lcd.set_color(1,0,0) # temp max > 30 -> color = red
        else :
            lcd.set_color(1,1,0) # else color -> color = green
            
        lcd.message(strx)
        time.sleep(3)
        lcd.clear()

    lcd.set_color(1,1,1) # else color -> blanc
    lcd.message(stry)

    time.sleep(1200)
    print '...bye...'
    
