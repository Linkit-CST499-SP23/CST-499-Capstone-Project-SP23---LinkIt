import unittest
from SMEP import SMEP

class TestSMEP(unittest.TestCase):
    def setUp(self):
        self.smep = SMEP()

    def test_get_elem_score(self):
        self.assertEqual(self.smep.get_elem_score(True, "https://twitter.com/user"), 1.0)
        self.assertEqual(self.smep.get_elem_score(False, "https://instagram.com/user"), 0.9 * 0.75)

    def test_remove_null(self):
        col_vals = ["NA", "https://facebook.com/user", "", "none", "https://linkedin.com/in/user"]
        self.assertEqual(self.smep.remove_null(col_vals), ["https://facebook.com/user", "https://linkedin.com/in/user"])

    def test_remove_lead_trail_space(self):
        col_vals = [" https://twitter.com/user ", " https://instagram.com/user "]
        self.assertEqual(self.smep.remove_lead_trail_space(col_vals), ["https://twitter.com/user", "https://instagram.com/user"])

    def test_remove_outliers(self):
        scores = [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2, 100, 150]
        self.assertEqual(sorted(self.smep.remove_outliers(scores)), sorted([0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2]))

    def test_get_confidence_score(self):
        col_name = "social_media"
        col_vals = [
            "https://twitter.com/user",
            "https://instagram.com/user",
            "https://facebook.com/user",
            "https://linkedin.com/in/user",
            "https://youtube.com/user",
            ]
        self.assertAlmostEqual(self.smep.get_confidence_score(col_name, col_vals), 0.9, places=1)

if __name__ == '__main__':
    unittest.main()

