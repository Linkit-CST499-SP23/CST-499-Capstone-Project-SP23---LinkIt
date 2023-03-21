import unittest
import sys
sys.path.append("..")

from pluginApi import *

#sys.path.insert(0, 'CST-499-Capstone-Project-SP23---LinkIt/pluginApi/pluginApi')



class TestPluginApi(unittest.TestCase):

    """
    Tests whether the api can import plugins from plugin folder
    """
    def test_plugin_retreival(self):
        test = pluginApi()
        actual = test.getPluginList()
        print(test.getPluginList())
        expected = ["PhoneNumberPlugin"]
        self.assertListEqual(actual, expected)
  

    




