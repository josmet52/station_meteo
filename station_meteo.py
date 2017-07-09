#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()




r = requests.get("http://api.wunderground.com/api/67b3e8dedd282c83/forecast/lang:FR/q/CH/Sion.json")
data = r.json()

for day in data['forecast']['simpleforecast']['forecastday']:

    wDay = day['date']['weekday'][0:2]
    dDay = day['date']['day']
    tempMin = int(day['low']['celsius'])
    tempMax = int(day['high']['celsius'])

    if tempMin < 0 :
        lcd.set_color(0,0,1) # temp min < 0 -> color = blue
    elif tempMax > 30 :
        lcd.set_color(1,0,0) # temp max > 30 -> color = red
    else :
        lcd.set_color(0,1,0) # else color =) green
            
    
#    str1 = wDay + ' ' + str(dDay) + ' : T=' + day['low']['celsius'] + '-' + day['high']['celsius']
    str2 = day['conditions'][0:16]
#    str = str1 + '\n' + str2

    lcd.message(str2)
    time.sleep(3)

    lcd.clear()
