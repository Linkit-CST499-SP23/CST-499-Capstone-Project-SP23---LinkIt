import re
from us_states import us_states
import statistics

"""
The get_confidence_score() function takes in column name as a string value
and a csv column as a list and returns a confidence score on how likely each value 
in the column is a valid US State.

input: string list, string value
output: double 

"""
def get_confidence_score(col_name, col_values):
     
     #column name check
     colcheck= ("state" in col_name.lower() or "states" in col_name.lower())

     #Remove null values
     col_values= remove_null(col_values)
     #Remove spaces
     col_values= remove_spaces(col_values)

     scores= []
     for c in col_values:
        valid_state_check= valid_state(c)

        if colcheck and valid_state_check:
            scores.append(100)
        if colcheck and not valid_state_check:
            scores.append(60)
        if not colcheck and valid_state_check:
            scores.append(40)
        if not colcheck and not valid_state_check:
            scores.append(0)

     scores= remove_outliers(scores)
     print(scores)
     return float(statistics.median(scores))

# checks valid US state names/abberevations  from us_states.py- a dictionary of all US states
def valid_state(state_name):
    if state_name.title() in us_states or state_name.upper() in us_states.values():
        return True
    else:
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

