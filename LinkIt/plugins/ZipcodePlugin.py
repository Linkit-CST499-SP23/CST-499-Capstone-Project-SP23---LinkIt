
from opencage.geocoder import OpenCageGeocode
import re
import os 
import statistics
import random
"""
The get_confidence_score() function takes in column name as a string value
and a csv column as a list and returns a confidence score on how likely each value 
in the column is a valid US zipcode.

The plugin calculates the score based on three parameters: 
column name, format of value passed and external api

input: string list, string value
output: double 
"""

def get_confidence_score(col_name, col_values):
     if(len(col_values>50)):
        sample_values= random.sample(col_values,50)
     else:
         sample_values=col_values
     
     #column name check
     colcheck_1= ("zipcode" in col_name.lower() or "zip code" in col_name.lower() or "postalcode" in col_name.lower() or "postalcode" in col_name.lower())
     colcheck_2= ("zip" in col_name.lower() or "postal" in col_name.lower())
     colcheck=""
     if(colcheck_1 and colcheck_2):
        colcheck= "Yes"
     elif(not colcheck_1 and colcheck_2):
         colcheck="Maybe"
     else:
         colcheck="No"

     #Remove null values
     sample_values= remove_null(sample_values)
     #Remove spaces
     sample_values= remove_spaces(sample_values)

     scores= []
     for c in sample_values:
        
        format_check, api_check= None, None
        format_check= get_format(c)
        # format True colcheck yes
        if format_check and colcheck=="Yes":
            scores.append(100)
        #format True colcheck maybe
        if format_check and colcheck=="Maybe":
            scores.append(100)
        #format True colcheck no
        if format_check and colcheck=="No":
            api_check= get_api_value(c)
            if api_check==True:
                scores.append(100)
            else:
                scores.append(0)
        #format False colcheck yes
        if not format_check and colcheck=="Yes":
            api_check= get_api_value(c)
            if api_check==True:
                scores.append(100)
            else:
                scores.append(0)
        #format False colcheck maybe
        if not format_check and colcheck=="Maybe":
            api_check= get_api_value(c)
            if api_check==True:
                scores.append(100)
            else:
                scores.append(0)
        #format False colcheck no
        if not format_check and colcheck=="No":
            scores.append(0)

     if scores:
        return float(statistics.median(scores))
     else:
        return 0.0
     
def remove_null(sample_values):
     null_values= ["", "NAN", "NaN","nan", "Null", None, "NA", "N/A", "na","n/a", "null", "NULL", ]
     sample_values= [elem for elem in sample_values if elem not in null_values]
     return sample_values

def remove_spaces(sample_values):
    sample_values = [elem.strip() for elem in sample_values] 
    return sample_values

def get_format(c):
    if (re.match(r"^\d{5}$", c) is not None or re.match(r"^\d{5}-\d{4}$", c) is not None):
        return True
    else:
        return False
    
def get_api_value(c):

    api_key = os.environ.get('OPENCAGE_API_KEY')
    geocoder = OpenCageGeocode(api_key)
    api_result=''

    api_json = geocoder.geocode(c)
    if(api_json!= []):
        api_result= api_json[0]['components']['_type']

    if(api_result=='postcode'):
        return True
    else:
        return False
    