import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Linkit', 'plugins')))
from stAddrPlugin import *
class TestGetConfidenceScore(unittest.TestCase):

    def test_valid_street_addr_list(self):
        column_name = "Address"
        address_list = [
            "123 Main St",
            "456 High St Apt 1",
            "789 Elm St",
            "1011 Maple Ave Apt B",
            "1314 Oak St",
        ]
        expected_score = 100.0
        
        result = get_confidence_score(column_name, address_list)
        
        self.assertAlmostEqual(result, expected_score, places=1)


    def test_invalid_street_addr_list(self):
        column_name = "nostreett"
        address_list = [
            "123main st", #2/3 -> +50
            "123mainst", #0/3 -> +0
            "1223 4536 7849", # 0/3 -> +0
            "not address", # 0/3 -> +0
            "St 123 Main", # 1/3 -> +25
        ]
        expected_score = 13.5
        
        result = get_confidence_score(column_name, address_list)
        
        self.assertAlmostEqual(result, expected_score, places=1)
    def test_empty_street_addr_list(self):
        column_name = "Address"
        address_list = [
            
        ]
        expected_score = 0
        
        result = get_confidence_score(column_name, address_list)
        
        self.assertAlmostEqual(result, expected_score, places=1)
        
    def test_100_score_phone_number_formats(self):
        actual = get_elem_score('123 Main St, Apt 12')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('456 Maple Ave')
        excepted = 100.0
        self.assertEqual(actual, excepted)

    def test_50_score_phone_number_formats(self):
        actual = get_elem_score('123 Main')
        excepted = 50.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('Oak St, Apt 12')
        excepted = 50.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('789 Central')
        excepted = 50.0
        self.assertEqual(actual, excepted)

    def test_25_score_phone_number_formats(self):
        actual = get_elem_score('street')
        excepted = 25.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('Main')
        excepted = 25.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('drive')
        excepted = 25.0
        self.assertEqual(actual, excepted)

    def test_0_score_phone_number_formats(self):
        actual = get_elem_score('California')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('94016')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('string')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('Google')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('community college')
        excepted = 0.0
        self.assertEqual(actual, excepted)

if __name__ == '__main__':
    unittest.main()
        
