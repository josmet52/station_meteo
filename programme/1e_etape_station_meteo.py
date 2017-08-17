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

#---------------------------------------------------------------------------------------------------------------------------------
# questionnement du site wunderground,com
r = requests.get("http://api.wunderground.com/api/d49b0a2fb656398f/forecast/lang:FR/q/CH/Sion.json")
sForecast = r.json()

# boucle pour parcourir les prévisions jour (day) après jour (4 jours pour forecast)
for day in sForecast['forecast']['simpleforecast']['forecastday']:

  print day['date']['weekday_short'] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius']
  print day['conditions']
  print "------------------------------"

# Fin du programme
#---------------------------------------------------------------------------------------------------------------------------------
