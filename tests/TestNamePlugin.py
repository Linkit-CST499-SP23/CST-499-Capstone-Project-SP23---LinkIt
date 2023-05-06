import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.NamePlugin import *

class TestNamesPlugin(unittest.TestCase):

    def test_get_name_score(self):
        self.assertEqual(get_name_score("John Smith"), 100.0)
        self.assertEqual(get_name_score("John S Smith"), 80.0)
        self.assertEqual(get_name_score("John"), 90.0)
        self.assertEqual(get_name_score("John$%Smith"), 0.0)

    def test_remove_null(self):
        names = ["NA", "John Smith", None, "", "n/a"]
        self.assertEqual(remove_null(names), ["John Smith"])

    def test_remove_lead_trail_space(self):
        names = ["  John Smith  ", "  John S Smith "]
        self.assertEqual(remove_lead_trail_space(names), ["John Smith", "John S Smith"])

    def test_remove_outliers(self):
        scores = [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2, 100, 150]
        self.assertEqual(sorted(remove_outliers(scores)), [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2, 100])

    def test_get_confidence_score(self):
        names = ["John Smith", "Jane Doe", "Robert Johnson", "Lisa Baker"]
        self.assertAlmostEqual(get_confidence_score("name", names), 100.0)

        names = ["John Smith", "Jane Doe", "Robert Johnson", "John S Smith", "Lisa Baker", "Joe Johnson"]
        self.assertAlmostEqual(get_confidence_score("name", names), 100.0)

        names = ["john smith", "Jane Doe", "Robert Johnson", "LISA BAKER", "john S smith"]
        self.assertAlmostEqual(get_confidence_score("name", names), 40.0)

        names = ["John Smith", "Jane Doe", "John", "Robert Johnson", "Lisa Baker", "john Smith", "N/A"]
        self.assertAlmostEqual(get_confidence_score("name", names), 98.0)

        names = []
        self.assertAlmostEqual(get_confidence_score("name", names), 0.0)

        names = ["Robert Johnson", "john smith", "Amanda Cook", "Lisa Baker", "N/a", "Jane Doe"]
        self.assertAlmostEqual(get_confidence_score("name", names), 80.0)


if __name__ == '__main__':
    unittest.main()
