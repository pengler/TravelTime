#!/usr/bin/python3
# Simple script that takes in the Canada Post .add file 
# and outputs a pickled data frame. 
#
# Input/Output files must be specified on the command line
# convert_canada_add.py input_file output_file
#
# File must conform to specification located at: 
# https://www.canadapost.ca/cpo/mc/assets/pdf/business/postalcodetechspecs_en.pdf

#TODOs
# Clean up the ugly loop in the middle - break out to functions
# Assumptions about type 1 record 
# Expand the abbreviated street name to full names as per mapping in tech document 

import sys
import pandas as pd
import pickle

if len (sys.argv) != 3 :
    exit(-1)

# 0 indexed vs 1 indexed documentation
# We are only interester in Civic addresses - (Record_Type_Code == 1)
add_titles=['Record_Type_Code','Address_Type_Code','Province_Code','Directory_Area_Name',
           'Street_Name','Street_Type_Code','Street_Direction_Code','Street_Address_Sequence_Code',
           'Street_Address_To_Number','Street_Address_Number_Suffix_To_Code','Suite_To_Number',
           'Filler1','Street_Address_From_Number','Street_Address_Number_Suffix_From_Code',
           'Suite_From_Number','Municipality_Name','Filler2','Province_Accent_Indicator',
           'Directory_Area_Name_Accent_Indicator','Municipality_Name_Accent_Indicator',
           'Street_Name_Accent_Indicator','Filler3','Postal_Code','Delivery_Installation_Postal_Code',
           'Action_Code']
numeric_cols=['Street_Address_To_Number','Street_Address_From_Number','Suite_To_Number','Suite_From_Number']
addresses = pd.DataFrame(columns=add_titles)
split_points = [0,1,2,4,34,64,70,72,73,79,80,86,99,105,106,112,142,161,162,163,164,164,167,173,179]
zz=0
with open(sys.argv[1],'r') as file:
    for line in file:
        split_list = list(map(lambda x :line[slice(*x)], zip(split_points, split_points[1:]+[None])))
        if split_list[0] == '1': 
            for x in range(0,len(split_list)):
                split_list[x] = split_list[x].strip()
        
            my_dict = dict(zip(add_titles,split_list)) 
            addresses = addresses.append(my_dict, ignore_index=True)
        zz = zz+1
        print(zz)

# for debugging
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)

print(addresses['Suite_To_Number'])
for num in numeric_cols:
    addresses[num] = pd.to_numeric(addresses[num], downcast='integer', errors='coerce')

pickle.dump( addresses, open( sys.argv[2], "wb" ) )
