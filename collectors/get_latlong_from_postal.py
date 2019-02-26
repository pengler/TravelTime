#!/usr/bin/env python3

#Example code to search for the location of a postal code
#and print out the formatted address, lat and long 
import pickle
import sys
import pandas as pd
import os
import googlemaps
import json

MAX_CODES=60000
gmaps = googlemaps.Client(key=os.environ['DIRECTIONS_API_KEY'])

# read the data file
postal_codes = pickle.load(open(sys.argv[1], 'rb'))

distinct_codes = postal_codes.loc[:,"POSTAL_CODE"].unique()

for code in distinct_codes[:MAX_CODES]:
    #print (postal_codes[postal_codes['POSTAL_CODE'] == code] )

    place_result = gmaps.find_place(input = code,
                                    input_type="textquery",
                                     fields=set(["geometry","formatted_address"])
                                     )
    if place_result['status'] != 'OK':
        print (code + " missing")
    else:   
        #print(json.dumps(place_result, indent=4, sort_keys=True))
        print(code)
        postal_codes.loc[postal_codes['POSTAL_CODE'] == code, 'LATITUDE'] = place_result['candidates'][0]['geometry']['location']['lat']
        postal_codes.loc[postal_codes['POSTAL_CODE'] == code, 'LONGITUDE'] = place_result['candidates'][0]['geometry']['location']['lng']
        postal_codes.loc[postal_codes['POSTAL_CODE'] == code, 'FORMATTED_ADDR'] = place_result['candidates'][0]['formatted_address']

    #print (place_result['candidates'][0]['formatted_address'])
    #print (place_result['candidates'][0]['geometry']['location']['lat'])
    #print (place_result['candidates'][0]['geometry']['location']['lng'])
    
    #print (json.dumps(place_result, indent=4, sort_keys=True))
    
    #print (type(distinct_codes))
    #print (distinct_codes)

#Save the extended data to a new pickle file   
#pd.set_option('display.max_columns', None)
#print (postal_codes.head(30))
pickle.dump( postal_codes, open( sys.argv[2], "wb" ) )



