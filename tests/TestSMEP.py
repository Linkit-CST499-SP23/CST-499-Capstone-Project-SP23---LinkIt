import unittest

import sys
sys.path.append("..")

from LinkIt.plugins.SocialMediaPlugin import *

class TestSMEP(unittest.TestCase):

    def test_get_elem_score(self):
        self.assertEqual(get_elem_score(True, "@twitteruser"), 100.0)
        self.assertEqual(get_elem_score(False, "@instauser"), 100.0 * 0.75)

    def test_remove_null(self):
        col_vals = ["NA", "@facebookuser", "", "none", "@linkedinuser"]
        self.assertEqual(remove_null(col_vals), ["@facebookuser", "@linkedinuser"])

    def test_remove_lead_trail_space(self):
        col_vals = [" @twitteruser ", " @facebookuser "]
        self.assertEqual(remove_lead_trail_space(col_vals), ["@twitteruser", "@facebookuser"])

    def test_remove_outliers(self):
        scores = [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2, 100, 150]
        self.assertEqual(sorted(remove_outliers(scores)), sorted([0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2]))

    def test_get_confidence_score(self):
        col_name = "social_media"
        col_vals = [
            "@twitteruser",
            "@instauser",
            "@facebookuser",
            "@linkedinuser",
            "@youtubeuser",
            ]
        self.assertAlmostEqual(get_confidence_score(col_name, col_vals), 100.0, places=1)

if __name__ == '__main__':
    unittest.main()

