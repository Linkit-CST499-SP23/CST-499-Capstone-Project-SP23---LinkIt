import re

"""

The get_confidence_score() function takes in a csv column name and column values 
passed in as a list and returns a confidence score by taking an average
on how likely each item in the column is of generic number type.

input: string, string list
output: double

"""
def get_confidence_score(col_name, col_vals):
    scores = []
    col_vals = remove_lead_trail_space(col_vals)
    col_vals = remove_null(col_vals) 

    for c in col_vals:
        scores.append(get_elem_score(c))
    scores = remove_outliers(scores)
    return sum(scores) / len(scores)


"""
The get_elem_score() function takes one element from the column list
and returns a confidence score on
how well the element is of generic number type.

input: string
output: double

"""
def get_elem_score(elem):
   if (re.fullmatch("(\d+(\.\d+)?)|(\.\d+)|(\d{1,3},\d{3}(,\d{3})*(\.\d+)?)", elem)):
       return 100.0 
   elif (re.fullmatch("(\d+(\.\d+)?%)|(\.\d+%)", elem)):
       return 90.0
   elif (re.fullmatch("\d+/\d+", elem)):
       return 40.0
   else:
       return 0.0
    

"""
The remove_null() function removes any null elements that may be in the column list.

input: string list
output: string list

"""
def remove_null(col_vals):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a', '']
    col_vals = [elem for elem in col_vals if elem is not None] # remove None values
    col_vals = [elem for elem in col_vals if elem not in null_strings] # remove any strings denoting null values
    return col_vals


"""
The remove_lead_trail_space() function removes any leading and trailing spaces that may be in the strings of the column list.

input: string list
output: string list

"""
def remove_lead_trail_space(col_vals):
    col_vals = [elem.strip() for elem in col_vals] # remove leading and trailing spaces
    return col_vals


"""
The remove_outliers() function removes any elements that could be skewing the average
(elements that are 2 standard deviations away from the mean).

input: double list
output: double list

"""
def remove_outliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
    