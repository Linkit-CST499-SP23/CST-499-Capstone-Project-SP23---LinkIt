import unittest

import sys
sys.path.append("..")

from plugins.GenericNumberPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests valid generic number cases.
    """
    def test_valid_number_list(self):
        # tests each number format once
        validNumList1 = ['12345', '45678.56789000', '.456789', '67,564', '89,890,890.89089898',
                        '98%', '98.56%', '.53%', '34/434']
        actual = get_confidence_score(validNumList1)
        expected = 96.25 # 40 is an outlier and should be removed from the final score 
        self.assertEqual(actual, expected)

        # tests a mix of formats that range between a confidence score of 100 and 90
        validNumList2 = ['12345', '3', '78.5678', '.09', '7,504', '78,980', '890,888.8', 
                        '98%', '98.56%', '.53%', '.004%', '0.007%', '51%']
        actual = get_confidence_score(validNumList2)
        expected = 95.0 
        self.assertAlmostEqual(actual, expected, delta=0.9)

        # tests a mix of formats that range between a confidence score of 90 and 40
        validNumList3 = ['98%', '98.56%', '.53%', '.004%', '0.007%',
                        '51%', '12/21', '45/4434', '1231/56', 
                        '535/535', '555/89']
        actual = get_confidence_score(validNumList3)
        expected = 67.0 
        self.assertAlmostEqual(actual, expected, delta=0.9)

        # tests formats with a 100 confidence score and one 40 confidence score outlier
        # the outlier should be removed before calculation of the final confidence score
        validNumList4 = ['12345', '3', '78.5678', '.09', '7,504', '78,980', '890,888.8', 
                        '.78', '456,789', '0.098', 
                        '100', '4/34']
        actual = get_confidence_score(validNumList4)
        expected = 100.0 
        self.assertEqual(actual, expected)

        # tests formats with a 40 confidence score and two 100 confidence score outliers
        # the outliers should be removed before calculation of the final confidence score
        validNumList5 = ['51/76', '12/21', '45/4434', '1231/56', 
                        '535/535', '555/89', '1/1', '22/32', '1/65', '24/2', 
                        '2124314', '2124567890']
        actual = get_confidence_score(validNumList5)
        expected = 40.0 
        self.assertEqual(actual, expected)


    """
    Tests invalid generic number formats.
    """
    def test_invalid_number_list(self):
        # tests strings that guarantee a 0 confidence score
        invalidNumList = ['string', 's7987498f', '.22.2.456.789.', '56,44,44',
                        '67%/78%']
        actual = get_confidence_score(invalidNumList)
        excepted = 0.0
        self.assertEqual(actual, excepted)

    """
    Tests the get_elem_score() function.
    More specifically, tests each number format.
    """
    def test_100_score_number_formats(self):
        actual = get_elem_score('12345')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('45678.56789000')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('.456789')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('67,564')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('89,890,890.89089898')
        excepted = 100.0
        self.assertEqual(actual, excepted)

    def test_90_score_number_formats(self):
        actual = get_elem_score('98%')
        excepted = 90.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('98.56%')
        excepted = 90.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('.53%')
        excepted = 90.0
        self.assertEqual(actual, excepted)

    def test_40_score_number_formats(self):
        actual = get_elem_score('34/343')
        excepted = 40.0
        self.assertEqual(actual, excepted)

    # The 0 score is for all invalid cases.
    def test_0_score_number_formats(self):
        actual = get_elem_score('string')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('s7987498f')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('.22.2.456.789.')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('56,44,44')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = get_elem_score('67%/78%')
        excepted = 0.0
        self.assertEqual(actual, excepted)


    """
    Tests the remove_outliers() function.
    """
    def test_remove_outlier(self):
        scores = [100, 100, 100, 100, 100, 0] # 0 is not within 2 standard deviations from the mean
        actual = remove_outliers(scores)
        expected = [100, 100, 100, 100, 100] 
        self.assertEqual(actual, expected)
        

    """
    Tests the remove_null() function.
    """
    def test_remove_null(self):
        col = ['435345345', '34534.345', None, '345,453', None, None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a'] 
        actual = remove_null(col)
        expected = ['435345345', '34534.345', '345,453']
        self.assertEqual(actual, expected)


    """
    Tests the remove_lead_trail_space() function.
    """
    def test_lead_trail_space(self):
        col = ['      345345', '345345      ', '       4534534      '] 
        actual = remove_lead_trail_space(col)
        expected = ['345345', '345345', '4534534']
        self.assertEqual(actual, expected)
        