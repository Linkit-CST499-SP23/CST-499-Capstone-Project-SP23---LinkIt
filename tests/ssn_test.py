import unittest
from SSN import SSN_confidence_score,remove_null_values

class TestSSNConfidenceScore(unittest.TestCase):

    def test_empty_column(self):
        col_name = "SSN"
        column_val = []
        expected_score = 0.0
        actual_score = SSN_confidence_score(col_name, column_val)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_null_values(self):
        col_name = "SSN"
        column_val = [None, "123-45-6789", "N/A", "987-65-4321"]
        expected_score = 50.0
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_no_ssn_values(self):
        col_name = "SSN"
        column_val = ["123-45-y789", "123-45-678A", "N/A"]
        expected_score = 0.0
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_all_ssn_values_with_dashes(self):
        col_name = "SSN"
        column_val = ["123-45-6789", "987-65-4321", "831-12-3456"]
        expected_score = 66.67
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_mixed_ssn_values_with_dashes(self):
        col_name = "SSN"
        column_val = ["123-45-6789", "987-65-4321", "123-45-y789", "N/A"]
        expected_score = round(33.33,2)
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_all_ssn_values_without_dashes(self):
        col_name = "SSN"
        column_val = ["123456789", "987654321", "831123456"]
        expected_score = round(33.33,2)
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_mixed_ssn_values_with_and_without_dashes(self):
        col_name = "SSN"
        column_val = ["123-45-6789", "123456789", "987-65-4321", "831123456", "N/A"]
        expected_score = 50.0
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

    def test_ssn_values_with_invalid_first_three_digits(self):
        col_name = "SSN"
        column_val = ["000-12-3456", "666-12-3456", "900-12-3456", "999-12-3456"]
        expected_score = 0.0
        cleaned_column = remove_null_values(column_val)
        actual_score = SSN_confidence_score(col_name, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score, places=2)

if __name__ == '__main__':
    unittest.main()