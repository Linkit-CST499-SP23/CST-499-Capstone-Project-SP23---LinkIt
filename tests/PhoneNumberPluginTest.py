import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.PhoneNumberPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests all valid phone number formats.
    """
    def test_valid_phone_number_list(self):
        # tests each phone number format once
        validPhoneNumList = ['(212)456-7890', '(212) 456-7890', '+212-456-7890', '+1 212.456.7890', '+1 605-605-6060'
                                '+12124567890', '212.456.7890', '1-212-456-7890', '212-456-7890', 
                                '212 456 7890', '2124567890']
        actual = get_confidence_score("", validPhoneNumList)
        expected = 80.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests a mix of formats that range between a confidence score of 80 and 90
        # with 'phone' found in column name 
        validPhoneNumList = ['+212-456-7890', '+1 212.456.7890', '+1 605-687-9596', 
                                '+12124567890', '+1849387349' '212.456.7890', '1-212-456-7890', '212-456-7890', 
                                '1-345-345-3453', '212.456.7890']
        actual = get_confidence_score("phone_#", validPhoneNumList)
        expected = 90.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        
        # tests a mix of formats that range between a confidence score of 65 and 20
        # with 'phone' found in column name 
        validPhoneNumList = ['234 456 7890', '212 234 7890', '212 456 4324', '212 432 7890',
                                '2124564654', '2124564654', '2124564654', '2124564654', 
                                '2124532654', '2124564654']
        actual = get_confidence_score("phone_number", validPhoneNumList)
        expected = 40.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests formats with a 100 confidence score and one 20 confidence score outlier
        # the outlier should be removed before calculation of the final confidence score
        validPhoneNumList = ['(605)605-6060', '(123)234-2342', '(605)665-1231', '(867)877-8876', 
                              '(786)660-6456', '(847)234-3460', '(454)454-5334', '6060606060']
        actual = get_confidence_score("", validPhoneNumList)
        expected = 100.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests formats with a 20 confidence score and two 100 confidence score outliers
        # the outliers should be removed before calculation of the final confidence score
        validPhoneNumList = ['2124564654', '2124564654', '2124564654', '2124564654',
                                '2124564654', '2124564654', '2124564654', '2124564654', 
                                '2124564654', '2124567890', '(212)456-7890', '(212)456-7890']
        actual = get_confidence_score("", validPhoneNumList)
        expected = 20.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Tests invalid phone number formats.
    Regex matches that do not match the entire string deducts 5 points from the confidence score per 
    unmatched character. 
    """
    def test_invalid_phone_number_list(self):
        # tests strings that guarantee a 0 confidence score
        # with 'phone' found in column name
        invalidPhoneNumList = ['4353dfgjir', '234234lgofd943', '234-42322-43243222', 'string']
        actual = get_confidence_score("alt_phone", invalidPhoneNumList)
        expected = 0.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos within the 100 score category
        # with 'phone' found in column name
        invalidPhoneNumList = ['((212)456-7890', '(212)456-789465', '((212) 456-7865rg']
        actual = get_confidence_score("phone_numbers", invalidPhoneNumList)
        expected = 90.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos within the 90 score category
        invalidPhoneNumList = ['+212-456-78902', '+1 212.456.7890..', '-+12124567890-0']
        actual = get_confidence_score("", invalidPhoneNumList)
        expected = 90.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos within the 80 score category
        # with 'phone' found in column name
        invalidPhoneNumList = ['.212.456.7890', '.1-212-456-7890.', 'io212-456-7890o']
        actual = get_confidence_score("PhoneNum", invalidPhoneNumList)
        expected = 80.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos within the 65 score category
        invalidPhoneNumList = ['212 456 7890l', 'rt212 456 7890', '&212 456 7890st']
        actual = get_confidence_score("", invalidPhoneNumList)
        expected = 60.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos within the 20 score category
        # with 'phone' found in column name
        invalidPhoneNumList = ['21245678905', '212456789060', '~2124567890--']
        actual = get_confidence_score("PHONENumbers", invalidPhoneNumList)
        expected = 10.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid typos throughout all the category scores 
        invalidPhoneNumList = ['((212)456-7890', '+212-456-78902', '.212.456.7890',
                                '212 456 7890l', '21245678905']
        actual = get_confidence_score("", invalidPhoneNumList)
        expected = 60.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # test empty list
        invalidPhoneNumList = []
        actual = get_confidence_score("", invalidPhoneNumList)
        expected = 0.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Test each format in each confidence score cateogory individually.
    """
    def test_100_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '(212)456-7890')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '(212) 456-7890')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_90_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '+212-456-7890')
        expected = 90.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '+1 212.456.7890')
        expected = 90.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(True, '+1 212-456-7890')
        expected = 90.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '+12124567890')
        expected = 90.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_80_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '212.456.7890')
        expected = 80.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '1-212-456-7890')
        expected = 80.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(True, '212-456-7890')
        expected = 80.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_65_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '212 456 7890')
        expected = 65.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '212 456 7890')
        expected = 65.0
        self.assertAlmostEqual(actual, expected, delta=10.5)


    def test_20_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '2124567890')
        expected = 20.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '2124567890')
        expected = 20.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    # The 0 score is for all invalid cases.
    def test_0_score_phone_number_formats(self):
        # test with a mix of whether 'phone' was found in the column name or not.
        actual = get_elem_score(True, '2p1p-245-678-90pE97p7')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '-212-45d6-7890-')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(True, '.22.2.456.789.')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '+22222222')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(True, '234234lgofd943')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, 'string')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)


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
        col = ['(212)456-7890', '(212) 456-7890', None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a'] 
        actual = remove_null(col)
        expected = ['(212)456-7890', '(212) 456-7890']
        self.assertEqual(actual, expected)
        

    """
    Tests the remove_lead_trail_space() function.
    """
    def test_lead_trail_space(self):
        col = ['      (212)456-7890', '(212) 456-7890      ', '       (605) 605-6060      '] 
        actual = remove_lead_trail_space(col)
        expected = ['(212)456-7890', '(212) 456-7890', '(605) 605-6060']
        self.assertEqual(actual, expected)
        