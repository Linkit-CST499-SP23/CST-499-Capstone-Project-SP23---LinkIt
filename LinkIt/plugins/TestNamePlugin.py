import unittest
from NamePlugin import NamesPlugin

class TestNamesPlugin(unittest.TestCase):

    def setUp(self):
        self.names_plugin = NamesPlugin()

    def test_get_name_score(self):
        self.assertEqual(self.names_plugin.get_name_score("John Smith"), 100.0)
        self.assertEqual(self.names_plugin.get_name_score("John S Smith"), 80.0)
        self.assertEqual(self.names_plugin.get_name_score("John"), 0.0)
        self.assertEqual(self.names_plugin.get_name_score("John$%Smith"), 0.0)

    def test_remove_null(self):
        names = ["NA", "John Smith", None, "", "n/a"]
        self.assertEqual(self.names_plugin.remove_null(names), ["John Smith"])

    def test_remove_lead_trail_space(self):
        names = ["  John Smith  ", "  John S Smith "]
        self.assertEqual(self.names_plugin.remove_lead_trail_space(names), ["John Smith", "John S Smith"])

    def test_remove_outliers(self):
        scores = [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2, 100, 150]
        self.assertEqual(sorted(self.names_plugin.remove_outliers(scores)), [0.75, 0.8, 0.85, 1.0, 1.0, 1.0, 1.2])

    def test_get_confidence_score(self):
        names = ["John Smith", "Jane Doe", "Robert Johnson", "Lisa Baker"]
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 100.0)

        names = ["John Smith", "Jane Doe", "Robert Johnson", "John S Smith", "Lisa Baker", "Joe Johnson"]
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 88.0)

        names = ["john smith", "Jane Doe", "Robert Johnson", "LISA BAKER", "john S smith"]
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 92.0)

        names = ["John Smith", "Jane Doe", "John", "Robert Johnson", "Lisa Baker", "john Smith", "N/A"]
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 76.0)

        names = []
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 0.0)

        names = ["Robert Johnson", "john smith", "Amanda Cook", "Lisa Baker", "N/a", "Jane Doe"]
        self.assertAlmostEqual(self.names_plugin.get_confidence_score(names), 83.0)


if __name__ == '__main__':
    unittest.main()
