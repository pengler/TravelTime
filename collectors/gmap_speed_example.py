#!/usr/bin/python3
# Simple example to extract speed from the Google Maps Directions API
# Would use the speed API but that is a premium service and trying to do this on the cheap


import googlemaps
import os
import datetime
import pprint
import json
gmaps = googlemaps.Client(key=os.environ['DIRECTIONS_API_KEY'])

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
departTime = datetime.datetime(2019, 8, 5, 2, 0)

# Get a sample route
#directions_result = gmaps.directions(" 800 Macleod Trail SE, Calgary ",
#                                     "2000 Airport Rd NE, Calgary",
#                                     mode="driving",
#                                     traffic_model="pessimistic",
#                                     departure_time=departTime)

#sample route from burbs to downtown
directions_result = gmaps.directions("5228 Barron Dr NW, Calgary ",
                                     "410 6 Ave SW, Calgary",
                                     mode="driving",
                                     traffic_model="pessimistic",
                                     departure_time=departTime)

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