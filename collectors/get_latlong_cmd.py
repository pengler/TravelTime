#!/usr/bin/env python3

# Get one postal code from the command line
# Example ./get_latlong_cmd A1B2C3

import sys
import os
import googlemaps
import json

gmaps = googlemaps.Client(key=os.environ['DIRECTIONS_API_KEY'])

code = sys.argv[1]

print(code)

place_result = gmaps.find_place(input = code,
                                input_type="textquery",
                                fields=set(["geometry","formatted_address"])
                                )
if place_result['status'] != 'OK':
    print ("whoops")
else:   
    print(json.dumps(place_result, indent=4, sort_keys=True))
    
