import random

"""
Exists purely to test API's ability to dynamically call functions from multiple plugins
retruns a random confidence score between 0 and 100
"""

def get_confidence_score(col):
    scores = []
    for c in col:
        scores.append(random.randint(0.0, 100.00))
    return sum(scores) / len(scores)

