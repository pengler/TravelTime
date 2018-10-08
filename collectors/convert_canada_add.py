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
titles = ['Record_Type_Code','Address_Type_Code','Province_Code','Directory_Area_Name',
          'Street_Name','Street_Type_Code','Street_Direction_Code','Street_Address_Sequence_Code',
          'Street_Address_To_Number','Street_Address_Number_Suffix_To_Code','Suite_To_Number',
          'Filler1','Street_Address_From_Number','Street_Address_Number_Suffix_From_Code',
          'Suite_From_Number','Municipality_Name','Filler2','Province_Accent_Indicator',
          'Directory_Area_Name_Accent_Indicator','Municipality_Name_Accent_Indicator',
          'Street_Name_Accent_Indicator','Filler3','Postal_Code','Delivery_Installation_Postal_Code',
          'Action_Code']
to_catagorical = ['Record_Type_Code','Address_Type_Code','Province_Code','Directory_Area_Name',
          'Street_Name','Street_Type_Code','Street_Direction_Code','Street_Address_Sequence_Code',
          'Street_Address_Number_Suffix_To_Code', 'Street_Address_Number_Suffix_From_Code',
          'Municipality_Name', 'Delivery_Installation_Postal_Code','Action_Code']
to_delete = ['Filler1','Filler2','Province_Accent_Indicator', 'Directory_Area_Name_Accent_Indicator',
             'Municipality_Name_Accent_Indicator', 'Street_Name_Accent_Indicator','Filler3']          
to_numeric = ['Street_Address_To_Number','Street_Address_From_Number','Suite_To_Number','Suite_From_Number']

titles = [t.upper() for t in titles]
to_catagorical = [c.upper() for c in to_catagorical]
to_delete = [d.upper() for d in to_delete]
to_numeric = [w.upper() for w in to_numeric]

split_points = [0,1,2,4,34,64,70,72,73,79,80,86,99,105,106,112,142,161,162,163,164,164,167,173,179]
my_list = []
with open(sys.argv[1],'r') as file:
    for line in file:
        split_list = list(map(lambda x :line[slice(*x)], zip(split_points, split_points[1:]+[None])))
        if split_list[0] == '1': 
            for x in range(0,len(split_list)):
                split_list[x] = split_list[x].strip()
            my_list.append(dict(zip(titles,split_list)))

postal_code = pd.DataFrame(my_list)
# for debugging
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)
#print(addresses['Suite_To_Number'])

postal_code = postal_code.rename(str.upper, axis='columns')

#Clear out columns that won't be used
postal_code = postal_code.drop(to_delete, axis=1)

#Convert to catagorical
for col in to_catagorical:                               
    postal_code[col] = postal_code[col].astype('category')

#Convert to numeric
for num in to_numeric:
    postal_code[num] = pd.to_numeric(postal_code[num], downcast='integer', errors='coerce')

#Create a Forward Sortation Area Catagory
postal_code['FORWARD_SORTATION_AREA'] = postal_code.POSTAL_CODE.str[:3].astype('category')

#Save the dataframe
pickle.dump( postal_code, open( sys.argv[2], "wb" ) )
