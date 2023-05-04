import unittest
import sys

sys.path.append("..")
from LinkIt.plugins.CreditCardNumberPlugin import *


class TestGetConfidenceScoreCol(unittest.TestCase):
    """
    Test if regex patterns correctly match a credit card brand with a strings' length.
    """

    def test_numbers_match_expected_length(self):
        # American Express
        self.assertTrue(matches_expected_length("340000000000000"))
        self.assertTrue(matches_expected_length("370000000000000"))

        # Diner Club Carte Blanche
        self.assertTrue(matches_expected_length("30000000000000"))
        self.assertTrue(matches_expected_length("30300000000000"))
        self.assertTrue(matches_expected_length("30500000000000"))
        self.assertTrue(matches_expected_length("36000000000000"))
        self.assertTrue(matches_expected_length("38000000000000"))

        # MasterCard
        self.assertTrue(matches_expected_length("5100000000000000"))
        self.assertTrue(matches_expected_length("5300000000000000"))
        self.assertTrue(matches_expected_length("5500000000000000"))

        self.assertFalse(matches_expected_length("5000000000000000"))
        self.assertFalse(matches_expected_length("5600000000000000"))

        # Visa
        self.assertTrue(matches_expected_length("4000000000000"))
        self.assertTrue(matches_expected_length("4000000000000000"))

        self.assertFalse(matches_expected_length("40000000000000"))

        # Discover
        self.assertTrue(matches_expected_length("6011000000000000"))

        self.assertFalse(matches_expected_length("601100000000000"))
        self.assertFalse(matches_expected_length("60110000000000000"))

        # JCB
        self.assertTrue(matches_expected_length("212300000000000"))
        self.assertTrue(matches_expected_length("180000000000000"))
        self.assertTrue(matches_expected_length("3111111111111111"))

        self.assertFalse(matches_expected_length("21230000000000"))
        self.assertFalse(matches_expected_length("2123000000000000"))
        self.assertFalse(matches_expected_length("18000000000000"))
        self.assertFalse(matches_expected_length("1800000000000000"))
        self.assertFalse(matches_expected_length("300000000000000"))
        self.assertFalse(matches_expected_length("30000000000000000"))

        # Misc.
        self.assertFalse(matches_expected_length(""))
        self.assertFalse(matches_expected_length(" "))
        self.assertFalse(matches_expected_length("3"))
        self.assertFalse(matches_expected_length("30"))
        self.assertFalse(matches_expected_length("300"))
        self.assertFalse(matches_expected_length("34000000000000"))
        self.assertFalse(matches_expected_length("3400000000000000"))

    """
    Test that null and empty are handled as expected.
    """

    def test_empty_col(self):
        empty_col = []
        actual = get_confidence_score("ccn", empty_col)
        expected = 0.0
        self.assertEqual(actual, expected)

        null_list = [None, 'NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
        actual = get_confidence_score("ccn", null_list)
        expected = 0.0
        self.assertEqual(actual, expected)

    """
    Test the check_valid_card_number function.
    """

    def test_numbers_are_valid(self):
        self.assertTrue(check_valid_card_number("0123456789700"))
        self.assertTrue(check_valid_card_number("000000000000000"))
        self.assertTrue(check_valid_card_number("1111111000000"))
        self.assertTrue(check_valid_card_number("123456789110000"))
        self.assertTrue(check_valid_card_number("1234567897000000"))

        self.assertFalse(check_valid_card_number(""))
        self.assertFalse(check_valid_card_number("00"))
        self.assertFalse(check_valid_card_number("12345678970000008"))

    def test_100_score_credit_card_number_list(self):
        # CCNs were generated through www.fakenamegenerator.com. This list only
        # contains numbers that correspond to visa/mastercard credit card number.
        valid_ccn_list = ["5185 9079 1173 9953", "5502 5237 1521 6076",
                          "5192.5620.2049.0567", "5105.6621.8906.3407",
                          "4556-9183-3821-5083", "4929-7059-0783-2756",
                          "4556 1402 0445 9279", "4556 9040 8392 6843",
                          "5218 1257 9588 8660", "4916 9463 8998 4732", ]
        actual = get_confidence_score("ccn", valid_ccn_list)
        expected = 100.0
        self.assertEqual(actual, expected)

    def test_col_name_score_multiplier(self):
        ccns_100_score = ["5185 9079 1173 9953", "5502 5237 1521 6076",
                          "5192.5620.2049.0567", "5105.6621.8906.3407",
                          "4556-9183-3821-5083", "4929-7059-0783-2756",
                          "4556 1402 0445 9279", "4556 9040 8392 6843",
                          "5218 1257 9588 8660", "4916 9463 8998 4732", ]
        actual = get_confidence_score("credit card numbers", ccns_100_score)
        actual2 = get_confidence_score("", ccns_100_score)
        actual3 = get_confidence_score("ccn", ccns_100_score)
        expected = 100.0
        expected2 = 80.0
        expected3 = 100.0
        self.assertEqual(actual, expected)
        self.assertEqual(actual2, expected2)
        self.assertEqual(actual3, expected3)

        ccns_75_score = ["0416614079752", "3184388909532",
                         "49765178056512", "082323391520852"]

        actual = get_confidence_score("ccn", ccns_75_score)
        actual2 = get_confidence_score("", ccns_75_score)
        expected = 75.0
        expected2 = 60.0
        self.assertEqual(actual, expected)
        self.assertAlmostEqual(actual2, expected2, delta=.1)

    def test_75_score_credit_card_numbers(self):
        actual = get_elem_score("0416614079752")
        expected = 75.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("3184388909532")
        expected = 75.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("49765178056512")
        expected = 75.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("082323391520852")
        expected = 75.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("1199463524381786")
        expected = 75.0
        self.assertEqual(actual, expected)

    def test_25_score_credit_card_numbers(self):
        actual = get_elem_score("340000000000000")
        expected = 25.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("30000000000000")
        expected = 25.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("340000000000000")
        expected = 25.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("4000000000000")
        expected = 25.0
        self.assertEqual(actual, expected)

        actual = get_elem_score("6011000000000000")
        expected = 25.0
        self.assertEqual(actual, expected)
