import re

"""

The IsPhoneNumber function takes in a csv column passed in as a list
and returns a confidence score by taking an average
on how likely each item in the column is a phone number.

input: list
output: double

"""
def IsPhoneNumber(col):
    scores = []
    for c in col:
        scores.append(ConfidenceScore(c))
    return sum(scores) / len(scores)


"""
The ConfidenceScore function takes one element from the column list
and returns a confidence score on
how the element is a phone number.

input: string
output: double

"""
def ConfidenceScore(elem):
    # matches '(555)555-555' or '(555) 555-5555'
    if (re.search("^\(\d{3}\)\s?\d{3}-\d{4}$", elem)): 
        return 100.00
    # matches '+1555555555' or '+1 555.555.5555' or '+555-555-5555'
    elif (re.search("^\+1?\s?\d{3}[\.-]\d{3}[\.-]\d{4}$|^\+1\d{10}$", elem)):
        return 80.0
    # matches '555-555-5555' or '555.555.5555' or '1-555-555-5555'
    elif (re.search("^(1-)?\d{3}[\.-]\d{3}[\.-]\d{4}$", elem)):
        return 60.0
    # matches '555 555 5555'
    elif (re.search("^\d{3}\s\d{3}\s\d{4}$", elem)):
        return 40.0
    # matches '5555555555'
    elif (re.search("^\d{10}$", elem)):
        return 20.0
    else:
        return 0.0
    