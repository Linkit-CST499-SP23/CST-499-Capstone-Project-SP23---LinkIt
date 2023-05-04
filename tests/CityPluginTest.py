import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.CityPlugin import *

class TestGetConfidenceScore(unittest.TestCase):

#types of tests
#different col and values
#valid city check
#valid city with spelling errors
#valid city with sufix

    def test_colname(self):
        col_name = "city"
        col_values = ['New York City, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Miami, FL']
        self.assertAlmostEqual(get_confidence_score(col_name, col_values), 100.0)

if __name__ == '__main__':
    unittest.main()