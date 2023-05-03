import re

def get_confidence_score(col_name,column_val):
    ssn_regex = r'^(?!000|666)[0-8]\d{2}(-?)\d{2}\1\d{4}$'
    total_score = 0
    count = 0

    column_val = remove_null_values(column_val)

    for item in column_val:
        if re.match(ssn_regex, item):
            if '-' not in item:
                total_score += 0.5
            else:
                total_score += 1
        count += 1

    return (total_score / count) * 100 if count > 0 else 0

def remove_null_values(column_val):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    column_val = [elem for elem in column_val if elem is not None]
    column_val = [elem for elem in column_val if elem not in null_strings]
    column_val = [elem for elem in column_val if elem]
    return column_val

