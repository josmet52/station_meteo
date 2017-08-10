#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()

sPays = "ES"
sVille = "la Garriga"
sLang = "lang:SP"
##sPays = "CH"
##sVille = "Sion"
##sLang = "lang:FR"
##sPays = "IT"
##sVille = "Todi"
##sLang = "lang:IT"
sKey = "67b3e8dedd282c83"
sDemand = "forecast10day"
sUrl = "http://api.wunderground.com/api"
sRequest = sUrl + "/" + sKey + "/" + sDemand + "/" + sLang + "/q/" + sPays + "/" + sVille +".json"
sTooLong =["Partiellement", "Parzialmente", "Possibilita", "Parcialmente", "Probabilidad"]

j=0
while True:
    r = requests.get(sRequest)
    data = r.json()
    i=0
    j += 1
    for day in data['forecast']['simpleforecast']['forecastday']:
        
        str1 = day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius']
        str2 = strip_accents(day['conditions'])
        str3 = str2.split()[0]
        for x in sTooLong :
           if x == str3 :
              str2 = str3[0:4] + "." + str2[len(str3):]
        strx = str1 + "\n" + str2
        strx = strip_accents(strx)

        print str1, " -> low = ", day['low']['celsius'], " / high = ", day['high']['celsius'], " -> ", str2

        tempMin = int(day['low']['celsius'])
        tempMax = int(day['high']['celsius'])
        
        if i == 1 :
            stry = strx
            tempMiny = tempMin
            tempMaxy = tempMax

        if tempMin < 0 :
            lcd.set_color(0,0,1) # temp min < 0 -> color = blue
        elif tempMax > 30 :
            lcd.set_color(1,0,0) # temp max > 30 -> color = red
        else :
            lcd.set_color(0,1,0) # else color -> color = green

            
        lcd.message(strx)
        time.sleep(3)
        lcd.clear()
        
        i += 1

    if tempMiny < 0 :
       lcd.set_color(0,0,1) # temp min < 0 -> color = blue
    elif tempMaxy > 30 :
       lcd.set_color(1,0,0) # temp max > 30 -> color = red
    else :
       lcd.set_color(0,1,0) # else color -> color = green
         
    lcd.message(stry)
    
    print 'passe : ' + str(j) + " -> " + time.strftime('%d.%m.%Y %H:%M',time.localtime())
    print sPays + " -> " + sVille
    print stry
    print '----------------------------------'

    time.sleep(1200)
