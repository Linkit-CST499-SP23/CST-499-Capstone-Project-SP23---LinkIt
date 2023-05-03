import re

# confidence scores
def get_confidence_score(column_name, column_values):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    total_score = 0
    count = 0
    
    for item in column_values:
        if re.match(email_regex, item):
            total_score += 1
        count += 1
    
    return (total_score / count)*100 if count > 0 else 0

def remove_null(column_val):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    column_val = [elem for elem in column_val if elem is not None] # remove None values
    column_val = [elem for elem in column_val if elem not in null_strings] # remove any strings denoting null values
    return column_val