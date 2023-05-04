import re
import numpy as np
from scipy.stats import zscore

class SMEP:
    def __init__(self):
        self.null_values = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a', '', ' ', 'none', 'None', 'NULL', 'null']
        self.social_media_regex = [
            (re.compile(r"(http(s)?:\/\/)?(www\.)?twitter\.com\/[A-Za-z0-9_]+"), 1.0),
            (re.compile(r"(http(s)?:\/\/)?(www\.)?facebook\.com\/[A-Za-z0-9_\.]+"), 0.9),
            (re.compile(r"(http(s)?:\/\/)?(www\.)?instagram\.com\/[A-Za-z0-9_\.]+"), 0.9),
            (re.compile(r"(http(s)?:\/\/)?(www\.)?linkedin\.com\/(in\/)?[A-Za-z0-9_\-]+"), 0.9),
            (re.compile(r"(http(s)?:\/\/)?(www\.)?youtube\.com\/(channel\/|user\/)?[A-Za-z0-9_\-]+"), 0.9)
        ]

    def get_confidence_score(self, col_name, col_vals):
        if len(col_vals) == 0:
            return "The input list is empty."

        sm_name_check = any(name in col_name.lower() for name in ['social', 'media', 'twitter', 'facebook', 'instagram', 'linkedin', 'youtube'])
        scores = []

        col_vals = self.remove_lead_trail_space(col_vals)
        col_vals = self.remove_null(col_vals)

        for elem in col_vals:
            scores.append(self.get_elem_score(sm_name_check, elem))

        if len(scores) > 0:
            return np.mean(self.remove_outliers(np.array(scores)))
        else:
            return 0.0

    def get_elem_score(self, sm_name_check, elem):
        for regex, score in self.social_media_regex:
            if regex.match(elem):
                return score if sm_name_check else score * 0.75

        return 0.0

    def remove_null(self, col_vals):
        return [val for val in col_vals if val not in self.null_values]

    def remove_lead_trail_space(self, col_vals):
        return [val.strip() for val in col_vals]

    def remove_outliers(self, scores):
        if len(scores) < 3:
            return scores

        Q1 = np.percentile(scores, 25)
        Q3 = np.percentile(scores, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        return [score for score in scores if lower_bound <= score <= upper_bound]

