import re

"""

The get_confidence_score() function takes in a list of names and returns a 
confidence score by taking an average on how likely each name is a valid name.

input: string list
output: double

"""
def get_confidence_score(col_name, names):
    scores = []
    names = remove_lead_trail_space(names)
    names = remove_null(names) 

    for name in names:
        scores.append(get_name_score(name))
    scores = remove_outliers(scores)

    if (len(scores) == 0):
        return 0.0
    else:
        return sum(scores) / len(scores)


"""
The get_name_score() function takes one name and returns a confidence score on
how well the name is a valid name.

input: string
output: double

"""
def get_name_score(name):
    if (re.fullmatch("[A-Z][a-z]* [A-Z][a-z]*", name)):
        return 100.0 
    elif (re.fullmatch("[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*", name)):
        return 80.0
    else:
        return 0.0
    

"""
The remove_null() function removes any null elements that may be in the list of names.

input: string list
output: string list

"""
def remove_null(names):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    names = [name for name in names if name is not None] # remove None values
    names = [name for name in names if name not in null_strings] # remove any strings denoting null values
    return names


"""
The remove_lead_trail_space() function removes any leading and trailing spaces that may be in the strings of the list of names.

input: string list
output: string list

"""
def remove_lead_trail_space(names):
    names = [name.strip() for name in names] # remove leading and trailing spaces
    return names


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
