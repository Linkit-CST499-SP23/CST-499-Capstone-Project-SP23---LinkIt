import re

"""

The get_confidence_score() function takes in a csv column name and column values 
passed in as a list and returns a confidence score by taking an average
on how likely each item in the column is of generic text type.

input: string, string list
output: double

"""
def get_confidence_score(col_name, col_vals):
    scores = []
    col_vals = remove_null(col_vals) 

    for c in col_vals:
        scores.append(get_elem_score(c))

    scores = remove_outliers(scores)

    if (len(scores) == 0):
        return 0.0
    else:
        return sum(scores) / len(scores)



"""
The get_elem_score() function takes one element from the column list
and returns a confidence score on
how well the element is of generic text type.

input: string
output: double

"""
def get_elem_score(elem):
   if (re.search("[a-zA-Z]", elem)):
       num_time_indicators = len(re.findall('AST|ADT|EST|EDT|CST|CDT|PST|PDT|AKST|AKDT|HST|HDT|UTC|PM|AM', elem))
       num_date_month_indicators = len(re.findall('JAN|FEB|MARCH|APRIL|MAY|JUNE|JULY|AUG|SEPT|OCT|NOV|DEC\
                                                  |Jan|Feb|March|April|May|June|July|Aug|Sept|Oct|Nov|Dec', elem)) 
       num_date_day_indicators = len(re.findall('MON|TUES|WED|THURS|FRI|SAT|SUN\
                                                |Mon|Tues|Wed|Thurs|Fri|Sat|Sun', elem)) 
       return 100.0 - (2.0 * (num_time_indicators + num_date_month_indicators + num_date_day_indicators))
   else:
       return 0.0
    

"""
The remove_null() function removes any null elements that may be in the column list.

input: string list
output: string list

"""
def remove_null(col_vals):
    col_vals = [elem for elem in col_vals if (elem is not None and elem != '')] # remove None and empty string values
    return col_vals


"""
The remove_outliers() function removes any elements that could be skewing the average
(elements that are 2 standard deviations away from the mean).

input: double list
output: double list

"""
def remove_outliers(scores):
    if (len(scores) == 0):
        return scores
    
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
    