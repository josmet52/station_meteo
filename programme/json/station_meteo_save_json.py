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

##sPays = "ES"
##sVille = "la Garriga"
##sLang = "lang:SP"
sPays = "CH"
sVille = "Sion"
sLang = "lang:FR"
##sPays = "IT"
##sVille = "Todi"
##sLang = "lang:IT"
sKey = "d49b0a2fb656398f"
sDemand = "forecast10day"
sUrl = "http://api.wunderground.com/api"
sRequest = sUrl + "/" + sKey + "/" + sDemand + "/" + sLang + "/q/" + sPays + "/" + sVille +".json"
sTooLong =["Partiellement", "Parzialmente", "Possibilita", "Parcialmente", "Probabilidad"]

print "started"
r = requests.get(sRequest)
print r.json()

# Open a file in witre mode
myf = open("wunderground_json_data.txt","w") 
myf.write(str(r.json())) 
myf.close() 

print "finished"
