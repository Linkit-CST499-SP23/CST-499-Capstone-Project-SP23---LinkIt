import usaddress
import re
import math

def get_confidence_score(column_name, address_list):
    scores = []
    regex = re.compile("(street|address|destination|origin)", re.IGNORECASE)
    address_list = remove_null(address_list)
    for address in address_list:
        scores.append(get_elem_score(address))

    if len(scores) > 15:
        scores = remove_outliers(scores)
    
    avg_score = sum(scores) / len(scores) if len(scores) > 0 else 0
    if regex.match(column_name):
        avg_score *= 1.1
    else:
        avg_score *= .9
    if avg_score > 100:
        avg_score = max(100.0, math.floor(avg_score / 100.0) * 100.0)
    return avg_score
def get_elem_score(string):
    regex = re.compile("(street|address|destination|origin)", re.IGNORECASE)
    addrComps = ['AddressNumber', 'StreetName', 'StreetNamePostType']
    currentAddr = []
    score = 0
    try:
        parsed_address = usaddress.parse(string)
        for (value,component) in parsed_address:
            currentAddr.append(component)
        
        if len(set(currentAddr) & set(addrComps)) == 3:
            score = 100.0/1
        elif len(set(currentAddr) & set(addrComps)) == 2:
            score = 100.0/2
        elif len(set(currentAddr) & set(addrComps)) == 1:
            score = 100.0/4
        elif len(set(currentAddr) & set(addrComps)) == 0:
            score = 0.0

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



