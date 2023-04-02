import unittest

import sys
sys.path.append("..")

from plugins.GenericTextPlugin import *

class TestGetConfidenceScoreCol(unittest.TestCase):
    
    """
    Tests valid generic text cases.
    """
    #TODO: test cases here


    """
    Tests invalid generic text formats.
    """
    #TODO: test cases here


    """
    Tests the get_elem_score() function.
    """
    #TODO: test cases here


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
        