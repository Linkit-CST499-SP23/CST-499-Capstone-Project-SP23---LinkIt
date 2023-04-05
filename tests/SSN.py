import re

# def IsSSN(column):
#     pattern = r"^\d{3}-\d{2}-\d{4}$"
#     count = 0
#     confidence_score = 0
#     for item in column:
#         if re.match(pattern, item):
#             print(f"Matched: {item}")  # Debugging output
#             count += 1
#             confidence_score += 1
#         else:
            
#             print(f"Not matched: {item}")  # Debugging output
#     if count > 0:
#         confidence_score = (confidence_score / count) * 100
#     else:
#         confidence_score = 0
#     return confidence_score

def IsSSN(column):
    ssn_regex = r'^\d{3}-\d{2}-\d{4}$'
    total_score = 0
    count = 0
    
    for item in column:
        if re.match(ssn_regex, item):
            total_score += 1
        count += 1
    
    return (total_score / count) * 100 if count > 0 else 0

column = ['123-45-y789', '123-45-678A', '987-65-4321', 'abc-12-3456']
confidence_score = IsSSN(column)
print(confidence_score)