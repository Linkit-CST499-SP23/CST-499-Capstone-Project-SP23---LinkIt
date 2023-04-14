import re
import math

def get_confidence_score(col_name, col_list):      
    scores = []
    col = remove_null(col_list)
    
    
    for c in col:
        scores.append(get_elem_score(c))

    scores = remove_outliers(scores)
    confidence_score = math.floor(sum(scores) / len(scores))
    # matches possible column names case insensitive
    if re.match(r'\b(?:url|link\s*(?:s)?|website\s*(?:s)?|web\s*address(?:es)?|urls?|site\s*URL\s*(?:s)?|hyperlink\s*(?:s)?|web\s+site)(?:s)?\b', col_name):
        confidence_score += 10
    return confidence_score     

def get_elem_score(string):
    
    # matches URLs that begin "http", "https", "ftp"
    if re.match(r'^(https?|ftp|sftp|file|mailto|tel|sms|data):\/\/', string):
        score = 100.0
    # Second, check if the string has a top-level domain (e.g. .com, .org, .net)
    elif re.search(r'(^|\s)([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*\.(?:com|net|org|edu|gov|io|co|biz|info|me|tv|us|ca|uk|au|de|jp))(?:\/[^\s?#]*)?(?:\?[^#\s]*)?(?:#[^\s]*)?(\s|$)', string):
        score = 90.0
    # Third, check if the string has a subdomain (e.g. www) also needs a domain and tld
    elif re.search(r'^(www|blog|mail|smtp|pop|imap|ftp)\.[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}(\/[^\s?#]*)?(\?[^#\s]*)?(#[^\s]*)?$', string):
        score = 80.0
    # Fourth, check if the string is an IP address
    elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', string):
        score = 40.0
    # Fifth, checks if string is formatted like a url but doesnt include scheme, common tlds, or subdomains 
    elif re.search(r'^\S{2,}\.\S{2,}(\.\S{2,})?(?:\/\S{2,})?$', string):
        score = 20.0
    # If none of the above conditions are met, assign a score of 0
    else:
        score = 0.0
    
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

