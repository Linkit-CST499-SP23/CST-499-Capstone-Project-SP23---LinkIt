import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.CreditCardExpirationDatePlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests valid cases of credit card expiration date numbers.
    """
    def test_valid_credit_card_expiration_date_list(self):
        # tests 2-digit month/year format
        # with 'credit' or 'card' and 'expiration found in the column name 
        validExpirationDateList = ['12/23', '11/22', '10/25', '09/21', '08/12',
                                '05/15', '04/30', '01/44', '02/12', '03/12']
        actual = get_confidence_score("Credit-EXPIRATION", validExpirationDateList)
        expected = 100.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests the valid 3-digit month/year format for months before October
        # with 'credit' or 'card' and 'expiration' found in column name 
        validExpirationDateList = ['2/23', '3/23', '4/45', '1/12', '9/34',
                                '5/22', '6/12', '7/43']
        actual = get_confidence_score("ExpirationDateForCard", validExpirationDateList)
        expected = 70.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        
        # tests the written expiration date format 
        # with 'credit' or 'card' and 'expiration' found in column name
        validExpirationDateList = ['NOV 2023', 'Jan 1991', 'December 2013', 'March 2045', 
                                   'August 1999', 'Feb 2020', 'APRIL 2019']
        actual = get_confidence_score("credit_card_expiration_date", validExpirationDateList)
        expected = 60.0
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Tests invalid credit card expiration date formats.
    If 'credit, 'card', or 'expiration' is not found in the column name, 
    then the score is reduced by a certain percentage. 
    [SEE CREDIT CARD EXPIRATION DATE PLUGIN DOC]
    """
    def test_invalid_credit_card_expiration_date_list(self):
        # tests 2-digit month/year formats
        # without 'expiration', 'credit', or 'card' found in column name
        invalidExpirationDateList = ['12/23', '11/22', '10/25', '09/21', '08/12',
                                '05/15', '04/30', '01/44', '02/12', '03/12']
        actual = get_confidence_score("anniversay_date", invalidExpirationDateList)
        expected = 50.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests the valid 3-digit month/year format for months before October
        # without 'credit' or 'card' and 'expiration' found in column name
        invalidExpirationDateList = ['2/23', '3/23', '4/45', '1/12', '9/34',
                                '5/22', '6/12', '7/43']
        actual = get_confidence_score("schooldate", invalidExpirationDateList)
        expected = 40.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests the written expiration date format 
        # with 'credit' or 'card' and 'expiration' found in column name
        invalidExpirationDateList = ['NOV 2023', 'Jan 1991', 'December 2013', 'March 2045', 
                                   'August 1999', 'Feb 2020', 'APRIL 2019']
        actual = get_confidence_score("concertEvents", invalidExpirationDateList)
        expected = 30.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests invalid cases
        invalidExpirationDateList = ['+212-456-78902', 'string', '12/333',
                                    '19/56', '00/45']
        actual = get_confidence_score("", invalidExpirationDateList)
        expected = 0.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Test each format in each confidence score cateogory individually.
    """
    def test_100_score_credit_card_expiration_date_formats(self):
        # test with 'credit' or 'card' and 'expiration' found in column name
        actual = get_elem_score(True, True, '08/23')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' found but not 'expiration' found in column name
        actual = get_elem_score(False, True, '12/23')
        expected = 80.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' not found and 'expiration' found in column name
        actual = get_elem_score(True, False, '12/23')
        expected = 60.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit', 'card', and 'expiration' not found in column name
        actual = get_elem_score(False, False, '12/23')
        expected = 50.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_70_score_credit_card_expiration_date_formats(self):
        # test with 'credit' or 'card' and 'expiration' found in column name
        actual = get_elem_score(True, True, '8/23')
        expected = 70.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' found but not 'expiration' found in column name
        actual = get_elem_score(False, True, '1/24')
        expected = 60.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' not found and 'expiration' found in column name
        actual = get_elem_score(True, False, '2/23')
        expected = 40.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit', 'card', and 'expiration' not found in column name
        actual = get_elem_score(False, False, '9/20')
        expected = 35.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_60_score_credit_card_expiration_date_formats(self):
        # test with 'credit' or 'card' and 'expiration' found in column name
        actual = get_elem_score(True, True, 'NOV 2023')
        expected = 60.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' found but not 'expiration' found in column name
        actual = get_elem_score(False, True, 'Jan 1991')
        expected = 50.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit' or 'card' not found and 'expiration' found in column name
        actual = get_elem_score(True, False, 'December 2013')
        expected = 40.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        # test with 'credit', 'card', and 'expiration' not found in column name
        actual = get_elem_score(False, False, 'APRIL 2019')
        expected = 30.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    # The 0 score is for all invalid cases.
    def test_0_score_credit_card_expiration_date_formats(self):
        actual = get_elem_score(False, False, '+212-456-78902')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, False, 'string')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, False, '12/333')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, False, '19/56')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score(False, False, '00/45')
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
        col = ['01/19', '12/23', None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a'] 
        actual = remove_null(col)
        expected = ['01/19', '12/23']
        self.assertEqual(actual, expected)
        

    """
    Tests the remove_lead_trail_space() function.
    """
    def test_lead_trail_space(self):
        col = ['      01/19', '12/23      ', '       04/24      '] 
        actual = remove_lead_trail_space(col)
        expected = ['01/19', '12/23', '04/24']
        self.assertEqual(actual, expected)
        