import unittest
import sys
sys.path.append("..")

from LinkIt.pluginApi import *

#sys.path.insert(0, 'CST-499-Capstone-Project-SP23---LinkIt/pluginApi/pluginApi')



class TestPluginApi(unittest.TestCase):

    """
    Tests whether the api can import plugins from plugin folder
    """
    def test_plugin_retreival(self):
        test = pluginApi()
        actual = test.getPluginList()
        print("API TEST discovered plugins:")
        print(test.getPluginList())
        expected = ['GenericNumberPlugin', 'GenericTextPlugin', 'PhoneNumberPlugin'] # placeholder at the moment
        self.assertListEqual(actual, expected)
  

    




