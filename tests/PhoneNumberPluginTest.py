import unittest

import sys
sys.path.append("..")

from plugins.PhoneNumberPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests all valid phone number formats.
    """
    def test_valid_phone_number_list(self):
        validPhoneNumList = ['(212)456-7890', '(212) 456-7890', '+212-456-7890', '+1 212.456.7890',
                                '+12124567890', '212.456.7890', '1-212-456-7890', '212-456-7890', 
                                '212 456 7890', '2124567890']
        actual = getConfidenceScore(validPhoneNumList)
        expected = 68.0 # calculation is (100+100+80+80+80+60+60+60+40+20) / 10
        self.assertEqual(actual, expected)


    """
    Tests invalid phone number formats.
    """
    def test_invalid_phone_number_list(self):
        invalidPhoneNumList = ['((212)456-7890', '5555555555555', '-212-456-7890', 'string']
        actual = getConfidenceScore(invalidPhoneNumList)
        expected = 0.0 
        self.assertEqual(actual, expected)


    """
    Test each format in each confidence score cateogory individually.
    """
    def test_100_score_phone_number_formats(self):
        actual = getElemScore('(212) 456-7890')
        excepted = 100.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('(212) 456-7890')
        excepted = 100.0
        self.assertEqual(actual, excepted)

    def test_80_score_phone_number_formats(self):
        actual = getElemScore('+212-456-7890')
        excepted = 80.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('+1 212.456.7890')
        excepted = 80.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('+12124567890')
        excepted = 80.0
        self.assertEqual(actual, excepted)

    def test_60_score_phone_number_formats(self):
        actual = getElemScore('212.456.7890')
        excepted = 60.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('1-212-456-7890')
        excepted = 60.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('212-456-7890')
        excepted = 60.0
        self.assertEqual(actual, excepted)

    def test_40_score_phone_number_formats(self):
        actual = getElemScore('212 456 7890')
        excepted = 40.0
        self.assertEqual(actual, excepted)


    def test_20_score_phone_number_formats(self):
        actual = getElemScore('2124567890')
        excepted = 20.0
        self.assertEqual(actual, excepted)

    # The 0 score is for all invalid cases.
    def test_0_score_phone_number_formats(self):
        actual = getElemScore('2124567890977')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('-212-456-7890-')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('.22.2.456.789.')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('+2222222222')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('((212)456-7890')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('string')
        excepted = 0.0
        self.assertEqual(actual, excepted)


    """
    Tests the removeOutlier() function.
    """
    def test_remove_outlier(self):
        scores = [100, 100, 100, 100, 100, 0] # 0 is not within 2 standard deviations from the mean
        actual = removeOutliers(scores)
        expected = [100, 100, 100, 100, 100] 
        self.assertEqual(actual, expected)
        

    """
    Tests the removeNull() function.
    """
    def test_remove_null(self):
        col = ['(212)456-7890', '(212) 456-7890', None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a'] 
        actual = removeNull(col)
        expected = ['(212)456-7890', '(212) 456-7890']
        self.assertEqual(actual, expected)
        