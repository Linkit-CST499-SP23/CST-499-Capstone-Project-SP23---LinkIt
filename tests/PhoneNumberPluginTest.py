import unittest

import sys
sys.path.append("..")

from plugins.PhoneNumberPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests all valid phone number formats.
    """
    def test_valid_phone_number_list(self):
        # tests each phone number format once
        validPhoneNumList1 = ['(212)456-7890', '(212) 456-7890', '+212-456-7890', '+1 212.456.7890', '+1 555-555-5555'
                                '+12124567890', '212.456.7890', '1-212-456-7890', '212-456-7890', 
                                '212 456 7890', '2124567890']
        actual = getConfidenceScore(validPhoneNumList1)
        expected = 62.0 
        self.assertEqual(actual, expected)

        # tests formats with a 100 confidence score and one 20 confidence score outlier
        # the outlier should be removed before calculation of the final confidence score
        validPhoneNumList2 = ['(555)555-5555', '(123)234-2342', '(555)665-1231', '(867)877-8876', 
                              '(786)655-6456', '(847)234-3455', '(454)454-5334', '5555555555']
        actual = getConfidenceScore(validPhoneNumList2)
        expected = 100.0 
        self.assertEqual(actual, expected)

        # tests a mix of formats that range between a confidence score of 60 and 80
        validPhoneNumList3 = ['+212-456-7890', '+1 212.456.7890', '+1 555-687-9596', 
                                '+12124567890', '+1849387349' '212.456.7890', '1-212-456-7890', '212-456-7890', 
                                '1-345-345-3453', '212.456.7890']
        actual = getConfidenceScore(validPhoneNumList3)
        expected = 70.0
        self.assertEqual(actual, expected)
        
        # tests a mix of formats that range between a confidence score of 40 and 20
        validPhoneNumList4 = ['234 456 7890', '212 234 7890', '212 456 4324', '212 432 7890',
                                '2124564654', '2124564654', '2124564654', '2124564654', 
                                '2124532654', '2124564654']
        actual = getConfidenceScore(validPhoneNumList4)
        expected = 28.0
        self.assertEqual(actual, expected)

        # tests formats with a 20 confidence score and two 100 confidence score outliers
        # the outliers should be removed before calculation of the final confidence score
        validPhoneNumList5 = ['2124564654', '2124564654', '2124564654', '2124564654',
                                '2124564654', '2124564654', '2124564654', '2124564654', 
                                '2124564654', '2124567890', '(212)456-7890', '(212)456-7890']
        actual = getConfidenceScore(validPhoneNumList5)
        expected = 20.0 
        self.assertEqual(actual, expected)


    """
    Tests invalid phone number formats.
    Regex matches that do not match the entire string deducts 5 points from the confidence score per 
    unmatched character. 
    """
    def test_invalid_phone_number_list(self):
        # tests strings that guarantee a 0 confidence score
        invalidPhoneNumList1 = ['4353dfgjir', '234234lgofd943', '234-42322-43243222', 'string']
        actual = getConfidenceScore(invalidPhoneNumList1)
        expected = 0.0 
        self.assertEqual(actual, expected)

        # tests invalid typos within the 100 score category
        invalidPhoneNumList2 = ['((212)456-7890', '(212)456-789440', '((212) 456-7840rg']
        actual = getConfidenceScore(invalidPhoneNumList2)
        expected = 90.0 
        self.assertEqual(actual, expected)

        # tests invalid typos within the 80 score category
        invalidPhoneNumList3 = ['+212-456-78902', '+1 212.456.7890..', '-+12124567890-0']
        actual = getConfidenceScore(invalidPhoneNumList3)
        expected = 70.0 
        self.assertEqual(actual, expected)

        # tests invalid typos within the 60 score category
        invalidPhoneNumList4 = ['.212.456.7890', '.1-212-456-7890.', 'io212-456-7890o']
        actual = getConfidenceScore(invalidPhoneNumList4)
        expected = 50.0 
        self.assertEqual(actual, expected)

        # tests invalid typos within the 40 score category
        invalidPhoneNumList5 = ['212 456 7890l', 'rt212 456 7890', '&212 456 7890st']
        actual = getConfidenceScore(invalidPhoneNumList5)
        expected = 30.0 
        self.assertEqual(actual, expected)

        # tests invalid typos within the 20 score category
        invalidPhoneNumList6 = ['21245678905', '212456789055', '~2124567890--']
        actual = getConfidenceScore(invalidPhoneNumList6)
        expected = 10.0 
        self.assertEqual(actual, expected)

        # tests invalid typos throughout all the category scores 
        invalidPhoneNumList7 = ['((212)456-7890', '+212-456-78902', '.212.456.7890',
                                '212 456 7890l', '21245678905']
        actual = getConfidenceScore(invalidPhoneNumList7)
        expected = 55.0
        self.assertEqual(actual, expected)


    """
    Test each format in each confidence score cateogory individually.
    """
    def test_100_score_phone_number_formats(self):
        actual = getElemScore('(212)456-7890')
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
        actual = getElemScore('+1 212-456-7890')
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
        actual = getElemScore('2p1p-245-678-90pE97p7')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('-212-45d6-7890-')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('.22.2.456.789.')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('+22222222')
        excepted = 0.0
        self.assertEqual(actual, excepted)
        actual = getElemScore('234234lgofd943')
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
        

    """
    Tests the removeLeadTrailSpace() function.
    """
    def test_lead_trail_space(self):
        col = ['      (212)456-7890', '(212) 456-7890      ', '       (555) 555-5555      '] 
        actual = removeLeadTrailSpace(col)
        expected = ['(212)456-7890', '(212) 456-7890', '(555) 555-5555']
        self.assertEqual(actual, expected)
        