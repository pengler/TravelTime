#!/usr/bin/python3

import os
import urllib.request
import json
import pprint

DIRECTIONS_API_KEY = os.environ['DIRECTIONS_API_KEY']

REQUEST='https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key='+DIRECTIONS_API_KEY

resource = urllib.request.urlopen(REQUEST)

content =  resource.read()
json = json.loads(content.decode('utf-8'))
pprint.pprint(json)

