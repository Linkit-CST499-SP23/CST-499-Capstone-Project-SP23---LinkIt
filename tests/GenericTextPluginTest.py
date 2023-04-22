import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.GenericTextPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests valid generic text cases.
    """
    def test_valid_phone_number_list(self):
        # tests generic text
        validTextList1 = ['piano', 'guitar', 'ukulele', 'violin', 'cello'
                        'flute', 'clarinet']
        actual = get_confidence_score("", validTextList1)
        expected = 100.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests generic text with date month indicators
        # score should be lower because of the date indicators
        validTextList2 = ['This month is January.', 'Next month is FEB.', 'This morning is March 4th, 2021.', 
                        'Christmas is in December.', 'She starts work in AUG.']
        actual = get_confidence_score("", validTextList2)
        expected = 98.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests generic text with date day indicators
        # score should be lower because of the date indicators
        validTextList3 = ['Spirit day is on Wednesday.', 'Come to the potluck on TUES.', 'Sunday is for church.', 
                        'Change your time on MON', 'Party on Fri.']
        actual = get_confidence_score("", validTextList3)
        expected = 98.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        
        # tests generic text with time indicators
        # score should be lower because of the time indicators
        validTextList4 = ['The time is 9:78PM', 'Make sure to change time from EST to EDT.', 
                          'Announcements are at 8:00AM.', 'Universal time is UTC.', 'West Coast is PST time.']
        actual = get_confidence_score("", validTextList4)
        expected = 97.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # tests generic text with one number outlier
        # the outlier should be removed before calculation of the final confidence score
        validTextList5 = ['yellow', 'blue', 'green', 'purple',
                        'orange', 'red', 'indigo', '2124564654']
        actual = get_confidence_score("", validTextList5)
        expected = 100.0 
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Tests invalid generic text formats.
    """
    def test_invalid_number_list(self):
        # test generic numbers
        invalidTextList1 = ['12345', '45678.56789000', '.456789', '67,564', '89,890,890.89089898',
                        '98%', '98.56%', '.53%', '34/434']
        actual = get_confidence_score("", invalidTextList1)
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

        # test pure date/time text
        # Generic Date/Time Plugin should give 100 for the below items thus 
        # this plugin needs give just needs to be below 100
        invalidTextList2 = ['12:00AM', '9:00PM PST', '21:43 EDT', 'March 31st, 2021', 
                            'May 1st', 'JAN 2ND', 'Monday', 'TUES 6TH']
        actual = get_confidence_score("", invalidTextList2)
        expected = 98.0
        self.assertAlmostEqual(actual, expected, delta=10.5)


    """
    Tests the get_elem_score() function.
    More specifically, tests each confidence score category.
    """
    def test_100_score_text(self):
        actual = get_elem_score('Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
                                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')
        expected = 100.0
        self.assertAlmostEqual(actual, expected, delta=10.5)

    def test_0_score_text(self):
        actual = get_elem_score('789')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score('.789')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score('98.98')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score('123,456.09')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score('67.87%')
        expected = 0.0
        self.assertAlmostEqual(actual, expected, delta=10.5)
        actual = get_elem_score('45/45')
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
        col = ['Generic text.', 'Generic text.', None, 'Generic text.', None, None] 
        actual = remove_null(col)
        expected = ['Generic text.', 'Generic text.', 'Generic text.']
        self.assertEqual(actual, expected)
        