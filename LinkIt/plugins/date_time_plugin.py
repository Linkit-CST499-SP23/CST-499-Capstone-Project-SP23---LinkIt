import re
import numpy as np
from datetime import datetime

class DTEP:
    def __init__(self):
        self.null_values = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a', '', ' ', 'none', 'None', 'NULL', 'null']
        self.datetime_regex = [
            (re.compile(r"^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$"), 0.75),
            (re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$"), 0.75),
            (re.compile(r"^\d{1,2}[-/]\d{1,2}[-/]\d{2,4} \d{1,2}:\d{2}:\d{2}$"), 1.0),
            (re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2} \d{1,2}:\d{2}:\d{2}$"), 0.75),
            (re.compile(r"^\d{4}-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])$"), 0.75)
        ]

    def get_confidence_score(self, col_name, col_vals):
        if len(col_vals) == 0:
            return "The input list is empty."

        date_time_name_check = 'date' in col_name.lower() or 'time' in col_name.lower()
        scores = []

        col_vals = self.remove_lead_trail_space(col_vals)
        col_vals = self.remove_null(col_vals)

        for elem in col_vals:
            scores.append(self.get_elem_score(date_time_name_check, elem))

        scores = self.remove_outliers(scores)

        if len(scores) > 0:
            return np.mean(scores)
        else:
            return 0.0

    def get_elem_score(self, strict, elem):
        """
        Calculate the score of an element based on the strictness and the pattern matches.

        Parameters:
        strict (bool): Whether or not to use strict pattern matching.
        elem (str): The element to calculate the score for.

        Returns:
        float: The score of the element.
        """
        if strict:
            if self.is_strict_pattern(elem):
                return 1.0
            else:
                return 0.0
        else:
            scores = []
            for pattern, score in self.datetime_regex:
                if self.is_pattern_match(pattern, elem):
                    scores.append(score)
            if len(scores) == 0:
                return 0.0
            else:
                return sum(scores) / len(scores)






    def remove_null(self, col_vals):
        return [val for val in col_vals if val not in self.null_values]

    def remove_lead_trail_space(self, col_vals):
        return [val.strip() for val in col_vals]

    def remove_outliers(self, scores):
        if len(scores) == 0:
            return scores
        mean = np.mean(scores)
        std_dev = np.std(scores)

        return [score for score in scores if (mean - 2 * std_dev) <= score <= (mean + 2 * std_dev)]
    
    def is_strict_pattern(self, elem):
        """Check if an element matches a strict date pattern."""
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        return bool(re.match(pattern, elem))
    
    def is_pattern_match(self, pattern, elem):
        if not bool(re.match(pattern, elem)):
            return False
        try:
            datetime.strptime(elem, '%Y-%m-%d')
            return True
        except ValueError:
            return False

