import usaddress
import re
import math

def get_confidence_score(column_name, address_list):
    scores = []
    
    # if address_list is empty return 0
    if len(address_list) == 0:
        return 0

    # matches possible column name case insensitive
    regex = re.compile("(street|address|destination|origin)", re.IGNORECASE)
    address_list = remove_null(address_list)

    for address in address_list:
        scores.append(get_elem_score(address))

    if len(scores) > 15:
        scores = remove_outliers(scores)
    
    avg_score = sum(scores) / len(scores) if len(scores) > 0 else 0
    # if column name matches likely names multiply score by 1.1
    if regex.match(column_name):
        avg_score *= 1.1
    # if column name does not match likely names multiply by 0.9
    else:
        avg_score *= .9
    # if the average score is about 100 round it down to 100
    if avg_score > 100:
        avg_score = max(100.0, math.floor(avg_score / 100.0) * 100.0)
    return avg_score
    
def get_elem_score(string):
    # Main componentes of a street address
    addrComps = ['AddressNumber', 'StreetName', 'StreetNamePostType']
    currentAddr = []
    score = 0
    try:
        parsed_address = usaddress.parse(string)
        for (value,component) in parsed_address:
            currentAddr.append(component)
        # First check, if the 3 of 3 main components of a street address match add 100 to list
        if len(set(currentAddr) & set(addrComps)) == 3:
            score = 100.0/1
        # Second check, if the 2 of 3 main components of a street address match add 50 to list
        elif len(set(currentAddr) & set(addrComps)) == 2:
            score = 100.0/2
        # Third check, if the 1 of 3 main components of a street address match add 25 to list
        elif len(set(currentAddr) & set(addrComps)) == 1:
            score = 100.0/4
        # Fourth check, if the 0 of 3 main components of a street address match add 0 to list
        elif len(set(currentAddr) & set(addrComps)) == 0:
            score = 0.0
    # error raised when a string is likely not a valid address that could be tested or tokens were labeled incorrectly
    except usaddress.RepeatedLabelError:
        pass
    return score

def remove_null(col):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    col = [elem for elem in col if elem is not None] # remove None values
    col = [elem for elem in col if elem not in null_strings] # remove any strings denoting null values
    return col
def remove_outliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores: 
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
