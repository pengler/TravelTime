#!/usr/bin/python3

import pandas as pd
import pickle
import sys

# Simple script that takes in the Canada Post .add file 
# and outputs a pickled data frame. 
#
# Input/Output files must be specified on the command line
# convert_canada_add.py input_file output_file
#
# File must conform to specification located at: 
# https://www.canadapost.ca/cpo/mc/assets/pdf/business/postalcodetechspecs_en.pdf

#TODOs

street_name_conv = {'DR':('Drive')}
street_name_conv2 = {'AL':'Alley', 'AV':'Avenue', 'BA':	'Bay', 'BV':'Boulevard', 'CA':'Cape', 
'CE':'Centre', 'CI':'Circle', 'CL':'Close', 'CM':'Common', 'CO':'Court', 'CR':'Crescent', 
'CV':'Cove', 'DR':'Drive', 'GA':'Gate', 'GD':'Gardens', 'GR':'Green', 'GV':'Grove', 
'HE':'Heath', 'HI':'Highway', 'HL':'Hill', 'HT':'Heights', 'IS':'Island', 'LD':'Landing', 
'LI':'Link', 'LN':'Lane', 'ME':'Mews', 'MR':'Manor', 'MT':'Mount', 'PA':'Park', 
'PH':'Path', 'PL':'Place', 'PR':'Parade', 'PS':'Passage', 'PT':'Point', 'PY':'Parkway', 
'PZ':'Plaza', 'RD':'Road', 'RI':'Rise', 'RO':'Row', 'SQ':'Square', 'ST':'Street', 
'TC':'Terrace', 'TR':'Trail', 'VI':'Villas', 'VW':'View', 'WK':'Walk', 'WY':'Way'}

col_types={'latitude':object, 'longitude':object}
if len (sys.argv) != 3 :
    print ('Input/Output files must be specified on the command line')
    print ('# convert_canada_add.py input_file output_file')
    exit(-1)

parcels = pd.read_csv(sys.argv[1], float_precision='high', dtype=col_types)
#parcels['STREET_TYPE_EXTENDED'] = parcels['STREET_TYPE'].apply( lambda x: street_name_conv2[x]).str.upper()
#parcels['ADDRESS_EXTENDED'] = parcels['ADDRESS'].apply( lambda x: )
#print (parcels.head(10))
#print (parcels.info())
pickle.dump( parcels, open( sys.argv[2], "wb" ) )