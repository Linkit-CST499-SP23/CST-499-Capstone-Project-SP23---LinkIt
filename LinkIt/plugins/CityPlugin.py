
import statistics
from fuzzywuzzy import fuzz
import random

import sys
sys.path.append("..")

from internal_databases.state_city_database import us_cities

#US cities databease with ver 108,000 cities and towns from all 50 states
#cities_df = pd.read_csv('plugins/us_cities.csv')
#city_names = set(cities_df['city'].str.lower())

"""
The get_confidence_score() function takes in column name as a string value
and a csv column as a list and returns a confidence score on how likely each value 
in the column is a valid US City.

input: string list, string value
output: double 

"""
def get_confidence_score(col_name, col_values):
     if(len(col_values>50)):
        sample_values= random.sample(col_values,50)
     else:
         sample_values=col_values
    
     
     #column name check
     colcheck= ("city" in col_name.lower() or "cities" in col_name.lower())
     #Remove null values
     sample_values= remove_null(sample_values)
     #Remove spaces
     sample_values= remove_spaces(sample_values)

     scores= []
     for c in sample_values:
        valid_city_check= valid_city(c)

        if colcheck and valid_city_check:
            scores.append(100)
        if colcheck and not valid_city_check:
            scores.append(60)
        if not colcheck and valid_city_check:
            scores.append(40)
        if not colcheck and not valid_city_check:
            scores.append(0)
     scores= remove_outliers(scores)
     return float(statistics.median(scores))
        

def valid_city(city_name):
    #check match or close match from the database
    # Andrew: checking for debug
    if any(city_name.lower() in us_cities or fuzz.token_set_ratio(x, city_name) >= 70 for x in us_cities):
        return True
    else:
        #check common city suffixes
        city_suffix= ['ville', 'town', 'burg', 'burgh', 'ford', 'field', 'ston', 'port', 'view', 'beach', 'crest', 'land', 'heights', 'island']
        if city_name in city_suffix:
            return True
        return False
    
    
def remove_null(sample_values):
     null_values= ["", "NAN", "NaN","nan", "Null", None, "NA", "N/A", "na","n/a", "null", "NULL", ]
     sample_values= [elem for elem in sample_values if elem not in null_values]
     return sample_values

def remove_spaces(sample_values):
    sample_values = [elem.strip() for elem in sample_values] 
    return sample_values

def remove_outliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
