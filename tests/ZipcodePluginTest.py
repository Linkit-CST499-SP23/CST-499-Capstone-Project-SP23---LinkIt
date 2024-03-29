import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.ZipcodePlugin import *

class TestGetConfidenceScore(unittest.TestCase):

    def test_colnames_zip(self):
        col_name = "Zip Code"
        col_values = ["90210", "90210-1234", "Not a zip code"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 93.33)
    def test_colnames_post(self):
        col_name = "Postal Code"
        col_values = ["90210", "90210-1234", "Not a zip code"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 93.33)
    def test_colnames_rand(self):
        col_name = "random"
        col_values = ["90210", "90210-1234", "Not a zip code"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 66.67)
        
    def test_null_values(self):
        col_name = "name"
        col_values = ["90210", "90210-1234", "Not a zip code", "", "nan", "NA"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 66.67)
    
    def test_spaces(self):
        col_name = "name"
        col_values = ["   90210", "90210-1234   ", "Not a zip code"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 66.67)
    
    def test_formats(self):
        col_name = "name"
        col_values = ["90210", "90210-1234", "Will", "AI231", "404", "831-112-4321"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 33.33)

    def test_api(self):
        col_name = "name"
        col_values = ["90210", "90210-1234", "Not a zip code"]
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 66.67)

if __name__ == '__main__':
    unittest.main()