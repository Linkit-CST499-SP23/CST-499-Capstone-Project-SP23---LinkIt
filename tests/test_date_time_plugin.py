import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.DateTimePlugin import *

class TestDTEP(unittest.TestCase):

    def test_get_elem_score(self):
        self.assertEqual(get_elem_score(True, "2022-12-12"), 100.0)
        self.assertAlmostEqual(get_elem_score(False, "2022-12-12"), 50.0, delta = 0.2)
        self.assertEqual(get_elem_score(True, "random text"), 0.0)
        self.assertEqual(get_elem_score(False, "2022-13-12"), 0.0)  # Invalid date
        self.assertEqual(get_elem_score(False, "2022-12-32"), 0.0)  # Invalid date
        self.assertEqual(get_elem_score(False, "2022-12-12 24:00:00"), 0.0)  # Invalid time

    def test_remove_null(self):
        test_list = ["NA", "N/A", "na", "n/a", "Na", "N/a", '', ' ', 'none', 'None', 'NULL', 'null', "2022-12-12"]
        self.assertEqual(remove_null(test_list), ["2022-12-12"])
        self.assertEqual(remove_null([]), [])

    def test_remove_lead_trail_space(self):
        test_list = ["   2022-12-12", "2022-12-12   ", "   2022-12-12   ", "2022-12-12"]
        self.assertEqual(remove_lead_trail_space(test_list), ["2022-12-12", "2022-12-12", "2022-12-12", "2022-12-12"])
        self.assertEqual(remove_lead_trail_space([]), [])

    def test_remove_outliers(self):
        test_scores = [1.0, 0.75, 0.0, 0.75, 1.0, 0.75, 1.0, 100]
        self.assertEqual(remove_outliers(test_scores), [1.0, 0.75, 0.0, 0.75, 1.0, 0.75, 1.0])
        self.assertEqual(remove_outliers([1.0]), [1.0])
        self.assertEqual(remove_outliers([]), [])
        def test_get_confidence_score(self):
            col_name = "OrderDate"
            col_vals = ["2022-12-12", "12/12/2022", "N/A", "   2022/12/12 12:12:12   ", "random text"]
            self.assertEqual(get_confidence_score(col_name, col_vals), 0.75)
            self.assertEqual(get_confidence_score(col_name, []), "The input list is empty.")
            self.assertEqual(get_confidence_score("", col_vals), 0.75)  # Empty column name
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "12/13/2022"]), 0.625)  # Invalid date
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "2022-12-32"]), 0.75)  # Invalid date, but different regex matches
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", ""]), 0.75)  # Empty string
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", " "]), 0.75)  # String with space only
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", None]), 0.75)  # None value
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "2022-12-12 12:12:12"]), 1.0)  # Full datetime
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "12/12/2022", "2022-12-12 12:12:12", None]), 0.9375)  # Mixture of valid and null values
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "2022-12-12 12:12:12", "2022-12-12 13:13:13"]), 1.0)  # Two valid values
            self.assertEqual(get_confidence_score(col_name, ["2022-12-12", "2022-12-12 12:12:12", "2022-12-12 13:13:13", "2022-12-12 14:14:14"]), 0.9375)  # Three valid values and one outlier
    
if __name__ == '__main__':
    unittest.main()