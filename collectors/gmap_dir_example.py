#!/usr/bin/python3
import googlemaps
import os
from datetime import datetime
import pprint
import json
gmaps = googlemaps.Client(key=os.environ['DIRECTIONS_API_KEY'])

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()

#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="driving",
#                                     departure_time=now)

directions_result = gmaps.directions(" 800 Macleod Trail SE, Calgary ",
                                     "2000 Airport Rd NE, Calgary",
                                     mode="driving",
                                     departure_time=now)

f = open('result_data.json', 'w')
f.write(json.dumps(directions_result))
f.close()

print(directions_result[0]['legs'][0]['distance']['text'])
print(directions_result[0]['legs'][0]['duration']['text'])
print(len(directions_result[0]['legs'][0]['steps']))
#print(type(directions_result[0]['legs'][0]['steps']))
numsteps = len(directions_result[0]['legs'][0]['steps'])
for steps in range(0, numsteps) :
    # meters
    distance = directions_result[0]['legs'][0]['steps'][steps]['distance']['value']
    distance_km = distance/1000
    #seconds
    duration = directions_result[0]['legs'][0]['steps'][steps]['duration']['value']
    duration_hours = duration/3600
    travelmode = directions_result[0]['legs'][0]['steps'][steps]['travel_mode']
    instructions = directions_result[0]['legs'][0]['steps'][steps]['html_instructions']
    print ('step #'+ str(steps) +
        ' distance: '+ str(distance) + 
        ' duration: ' + str(duration) + 
        ' = ' + str(distance_km/duration_hours) +' kmph ' + travelmode + ' ' +instructions)