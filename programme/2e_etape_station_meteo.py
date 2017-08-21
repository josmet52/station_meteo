#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------------------------------------------------------------

"""
Programme : 
Auteur : 
Version : 
Date : 

Ce programme interroge le site internet www.wunderground.com/api pour obtenir les prévisions météo de Sion et les affiche
"""

#---------------------------------------------------------------------------------------------------------------------------------
# importation des librairies nécessaires
import json
import requests
import time
import Adafruit_CharLCD as LCD


# assignation du display à la variable lcdDisplay 
lcdDisplay = LCD.Adafruit_CharLCDPlate()

#---------------------------------------------------------------------------------------------------------------------------------
# interrogation du site wunderground,com
#r = requests.get("introduisez ici la commande que vous avez testé à l'étape précédente")
r = requests.get("http://api.wunderground.com/api/d49b0a2fb656398f/forecast/lang:FR/q/CH/Sion.json")
sForecast = r.json()

# boucle pour parcourir les prévisions jour (day) après jour (4 jours pour forecast)
for day in sForecast['forecast']['simpleforecast']['forecastday']:

    print "Prevision meteo pour Sion le " + day['date']['weekday_short'] + " " + str(day['date']['day']) + " " + day['date']['monthname_short'] + " " + str(day['date']['year'])
    print "Temperature min prevue : " + day['low']['celsius']
    print "Temperature max prevue : " + day['high']['celsius']
    print "Prevision meteo : " + day['conditions']
    print "-----------------------------------------------------"

    str1 = day['date']['weekday_short'] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius']
    str2 = day['conditions']
    lcdDisplay.clear()
    lcdDisplay.message(str1 + "\n" + str2)

    time.sleep(2)
    
# Fin du programme
#---------------------------------------------------------------------------------------------------------------------------------
