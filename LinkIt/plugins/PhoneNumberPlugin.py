import re

"""

The get_confidence_score() function takes in a csv column name and column values 
passed in as a list and returns a confidence score by taking an average
on how likely each item in the column is a phone number.

input: string, string list
output: double

"""
def get_confidence_score(col_name, col_vals):
    col_name_check= ("phone" in col_name.lower())

    scores = []
    col_vals = remove_lead_trail_space(col_vals)
    col_vals = remove_null(col_vals) 

    for c in col_vals:
        scores.append(get_elem_score(col_name_check, c))

    scores = remove_outliers(scores)

    if (len(scores) == 0):
        return 0.0
    else:
        return sum(scores) / len(scores)



"""
The get_elem_score() function takes in a boolean denoting
whether 'phone' was found in the column name and 
one element from the column list and returns a confidence score on
how the element is a phone number.

input: bool, string
output: double

"""
def get_elem_score(col_name_check, elem):
    og_elem_length = len(elem)

    if col_name_check:
        score_boost = 1.1
    else:
        score_boost = 1.0

    # matches '(555)555-555' or '(555) 555-5555'
    if (match := re.search("\(\d{3}\)\s?\d{3}-\d{4}", elem)) is not None:
        return (100.00 - (5.0 * (og_elem_length - (match.end(0) - match.start(0))))) * score_boost
    # matches '+1555555555' or '+1 555.555.5555' or '+555-555-5555'
    elif (match := re.search("(\+1?\s?\d{3}[\.-]\d{3}[\.-]\d{4})|(\+1\d{10})", elem)) is not None:
        return (90.0 - (5.0 * (og_elem_length - (match.end(0) - match.start(0))))) * score_boost
    # matches '555-555-5555' or '555.555.5555' or '1-555-555-5555'
    elif (match := re.search("(1-\d{3}-\d{3}-\d{4})|(\d{3}[\.-]\d{3}[\.-]\d{4})", elem)) is not None:
        return (80.0 - (5.0 * (og_elem_length - (match.end(0) - match.start(0))))) * score_boost
    # matches '555 555 5555'
    elif (match := re.search("\d{3}\s\d{3}\s\d{4}", elem)) is not None:
        return (40.0 - (5.0 * (og_elem_length - (match.end(0) - match.start(0))))) * score_boost
    # matches '5555555555'
    elif (match := re.search("\d{10}", elem)) is not None:
        return (20.0 - (5.0 * (og_elem_length - (match.end(0) - match.start(0))))) * score_boost
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
    