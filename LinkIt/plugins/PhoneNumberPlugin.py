import re

"""

The getConfidenceScore() function takes in a csv column passed in as a list
and returns a confidence score by taking an average
on how likely each item in the column is a phone number.

input: string list
output: double

"""
def get_confidence_score(col):
    scores = []
    col = removeNull(col) 

    for c in col:
        scores.append(getElemScore(c))

    scores = removeOutliers(scores)
    return sum(scores) / len(scores)



"""
The getElemScore() function takes one element from the column list
and returns a confidence score on
how the element is a phone number.

input: string
output: double

"""
def getElemScore(elem):
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
    

"""
The removeNull() function removes any null elements that may be in the column list.

input: string list
output: string list

"""
def removeNull(col):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    col = [elem for elem in col if elem is not None] # remove None values
    col = [elem for elem in col if elem not in null_strings] # remove any strings denoting null values
    return col


"""
The removeOutliers() function removes any elements that could be skewing the average
(elements that are 2 standard deviations away from the mean).

input: double list
output: double list

"""
def removeOutliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
    