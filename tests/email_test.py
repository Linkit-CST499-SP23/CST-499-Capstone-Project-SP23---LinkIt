import unittest

from email import calculate_email_confidence, remove_null

class TestEmailConfidence(unittest.TestCase):
    
    def test_all_emails(self):
        column = 'email'
        values = ['user1@example.com', 'user2@example.com', 'user3@example.com']
        expected_score = 100.0
        actual_score = calculate_email_confidence(column, values)
        self.assertEqual(actual_score, expected_score)

    def test_mixed_emails(self):
        column = 'email'
        column = ['user4@example.com', 'user5@example.com', 'user6@example.com', 'na', 'user7@example.com']
        expected_score = 100.0
        cleaned_column = remove_null(column)
        print(cleaned_column)  # add this line
        actual_score = calculate_email_confidence(column, cleaned_column)
        self.assertAlmostEqual(actual_score, expected_score)

    def test_no_emails(self):
        column = 'email'
        values = ['not_an_email1', 'not_an_email2', 'not_an_email3']
        expected_score = 0
        actual_score = calculate_email_confidence(column, values)
        self.assertEqual(actual_score, expected_score)

    def test_empty_column(self):
        column = 'email'
        values = []
        expected_score = 0
        actual_score = calculate_email_confidence(column, values)
        self.assertEqual(actual_score, expected_score)

if __name__ == '__main__':
    unittest.main()