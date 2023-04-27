import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.CreditCardCVVPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests valid cases of credit card CVV numbers.
    """
    def test_valid_credit_card_cvv_list(self):
        # tests the valid 3-digit format with 
        # 'cvv' found in the column name
        validCVVList = ['234', '345', '543', '555', '134',
                        '154', '545', '144', '212', '212']
        actual = get_confidence_score("CVV", validCVVList)
        expected = 100.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests the valid 4-digit format
        # with 'credit' found in column name 
        validCVVList = ['2346', '3455', '5453', '5555', '4134',
                        '1554', '5445', '1544', '2512', '2152']
        actual = get_confidence_score("back_of_Credit", validCVVList)
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        
        # tests a mix of 3-4 digit formats 
        # with 'card' found in column name
        validCVVList = ['2346', '3455', '5453', '5555', '4134',
                        '154', '545', '144', '212', '212']
        actual = get_confidence_score("backOfCARD", validCVVList)
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Tests invalid credit card CVV formats.
    If 'credit, 'card', or 'cvv' is not found in the column name, 
    then the score is reduced by half.
    """
    def test_invalid_credit_card_cvv_list(self):
        # tests 3-digit formats
        # without 'cvv', 'credit', or 'card' found in column name
        invalidCVVList = ['234', '345', '543', '555', '134',
                        '154', '545', '144', '212', '212']
        actual = get_confidence_score("phone_extension", invalidCVVList)
        expected = 50.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests 4-digit formats
        # without 'cvv', 'credit', or 'card' found in column name
        invalidCVVList = ['2346', '3455', '5453', '5555', '4134',
                        '1554', '5445', '1544', '2512', '2152']
        actual = get_confidence_score("id", invalidCVVList)
        expected = 50.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests a mix of 3-4 digit formats
        # without 'cvv', 'credit', or 'card' found in column name
        invalidCVVList = ['2346', '3455', '5453', '5555', '4134',
                        '154', '545', '144', '212', '212']
        actual = get_confidence_score("phone_extension", invalidCVVList)
        expected = 50.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid cases
        invalidCVVList = ['+212-456-78902', 'string', '12',
                          '12345', '12.34']
        actual = get_confidence_score("", invalidCVVList)
        expected = 0.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # test empty list
        invalidCVVList = []
        actual = get_confidence_score("", invalidCVVList)
        expected = 0.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Test each format in each confidence score cateogory individually.
    """
    def test_100_score_credit_card_cvv_formats(self):
        actual = get_elem_score(True, '123')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(True, '1234')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_50_score_credit_card_cvv_formats(self):
        actual = get_elem_score(False, '123')
        expected = 50.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '1234')
        expected = 50.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    # The 0 score is for all invalid cases.
    def test_0_score_credit_card_cvv_formats(self):
        actual = get_elem_score(False, '+212-456-78902')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, 'string')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '12')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '12345')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, '12.34')
        expected = 0.0


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
        col = ['234', '444', None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a'] 
        actual = remove_null(col)
        expected = ['234', '444']
        self.assertEqual(actual, expected)
        

    """
    Tests the remove_lead_trail_space() function.
    """
    def test_lead_trail_space(self):
        col = ['      234', '444      ', '       224      '] 
        actual = remove_lead_trail_space(col)
        expected = ['234', '444', '224']
        self.assertEqual(actual, expected)
        