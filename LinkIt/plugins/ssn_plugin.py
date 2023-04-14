import re

# confidence score 
def SSN_confidence_score(col_name,column_val):
    ssn_regex = r'^\d{3}-\d{2}-\d{4}$'
    total_score = 0
    count = 0
    
    for item in column_val:
        if re.match(ssn_regex, item):
            total_score += 1
        count += 1
    
    return (total_score / count) * 100 if count > 0 else 0

def remove_null_values(column_val):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    column_val = [elem for elem in column_val if elem is not None] # remove None values
    column_val = [elem for elem in column_val if elem not in null_strings] # remove any strings denoting null values
    return column_val