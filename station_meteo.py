# -*- coding: utf-8 -*-

import urllib2
import json
import requests

f =requests.get ('http://api.wunderground.com/api/67b3e8dedd282c83/forecast/q/CH/Sion.json')
data = f.json
print data["forecast"]["simpleforecast"]

