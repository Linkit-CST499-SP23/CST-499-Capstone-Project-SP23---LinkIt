import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Linkit', 'plugins')))
from urlPlugin import *

class TestGetConfidenceScore(unittest.TestCase):
    
    def test_get_confidence_score(self):
        # Test input list with various types of strings
        input_name = 'links'
        input_list = [
            'https://www.test.com',
            'http://www.example.com',
            'example.com',
            'sub.domain.example.ca/path/to/page?param=value#section',
            'www.example.org',
            'blog.example.xyz/path/to/post',
            'pop.example.ac',
            'www.example.ai#section', 
            '192.168.0.100',
            'mydomain.museum',
            '.example.com'
        ]
        
        # Expected confidence score for the above input list
        expected_score = 81.0
        
        # Call the function and check the result
        self.assertEqual(get_confidence_score(input_name, input_list), expected_score)
    
    
    
    def test_get_elem_score(self):
        # Test various types of input strings
        input_string1 = 'https://www.test.com'
        expected_score1 = 100.0
        input_string2 = 'sub.domain.example.ca/path/to/page?param=value#section'
        expected_score2 = 90.0
        input_string3 = 'blog.example.xyz/path/to/post'
        expected_score3 = 80.0
        input_string4 = '192.168.0.100'
        expected_score4 = 40.0
        input_string5 = '.example.com'
        expected_score5 = 20.0
        input_string6 = 'not_a_url'
        expected_score6 = 0.0
        
        # Call the function for each input string and check the result
        self.assertEqual(get_elem_score(input_string1), expected_score1)
        self.assertEqual(get_elem_score(input_string2), expected_score2)
        self.assertEqual(get_elem_score(input_string3), expected_score3)
        self.assertEqual(get_elem_score(input_string4), expected_score4)
        self.assertEqual(get_elem_score(input_string5), expected_score5)
        self.assertEqual(get_elem_score(input_string6), expected_score6)

if __name__ == '__main__':
    unittest.main()
        
