# -*- coding: utf-8 -*-

import urllib2
import json
import requests

r = requests.get("http://api.wunderground.com/api/67b3e8dedd282c83/forecast10day/q/CH/Sion.json")
data = r.json()

for day in data['forecast']['simpleforecast']['forecastday']:
    print day['date']['weekday'] + ' ' + str(day['date']['day']) + " : " + day['conditions']
    print "High: ", day['high']['celsius'] + "C", "Low: ", day['low']['celsius'] + "C", ''
    print

