import unittest
import sys
sys.path.append("..")

from LinkIt.plugins.NamePlugin import *


class TestNamePlugin(unittest.TestCase):

    def test_remove_lead_trail_space(self):
        input_list = [' John ', '   Marry  ', '  Joe   ']
        expected_output = ['John', 'Marry', 'Joe']
        self.assertEqual(remove_lead_trail_space(input_list), expected_output)

    def test_remove_null(self):
        input_list = ['John', None, 'Marry', 'N/A', 'Joe']
        expected_output = ['John', 'Marry', 'Joe']
        self.assertEqual(remove_null(input_list), expected_output)

    def test_remove_outliers(self):
        input_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 100.0]
        expected_output = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        self.assertEqual(remove_outliers(input_list), expected_output)

    def test_get_confidence_score(self):
        valid_names = ["John Doe", "Jane Smith"]
        invalid_names = ["Johhny", "Smithy"]
        input_list = valid_names + invalid_names
        expected_output = len(valid_names) / len(input_list) * 100.0
        self.assertAlmostEqual(get_confidence_score(input_list), expected_output, delta=0.1)

if __name__ == '__main__':
    unittest.main()
