import pandas as pd
import statistics
from fuzzywuzzy import fuzz
from state_city_database import us_cities

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
     
     #column name check
     colcheck= ("city" in col_name.lower() or "cities" in col_name.lower())

     #Remove null values
     col_values= remove_null(col_values)
     #Remove spaces
     col_values= remove_spaces(col_values)

     scores= []
     for c in col_values:
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
    if city_name.lower() in us_cities:
        return True
    else:
        # check if close match
        for x in us_cities:
            if fuzz.token_set_ratio(x, city_name) >= 70:
                return True
        #check common city suffixes
        city_suffix= ['ville', 'town', 'burg', 'burgh', 'ford', 'field', 'ston', 'port', 'view', 'beach', 'crest', 'land', 'heights']
        if city_suffix in city_name:
            return True
        return False
    
    
def remove_null(col_values):
     null_values= ["", "NAN", "NaN","nan", "Null", None, "NA", "N/A", "na","n/a", "null", "NULL", ]
     col_values= [elem for elem in col_values if elem not in null_values]
     return col_values

def remove_spaces(col_values):
    col_values = [elem.strip() for elem in col_values] 
    return col_values

def remove_outliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
