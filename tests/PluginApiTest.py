import unittest
import sys
sys.path.append("..")

from LinkIt.PluginApi import *

#sys.path.insert(0, 'CST-499-Capstone-Project-SP23---LinkIt/pluginApi/pluginApi')



class TestPluginApi(unittest.TestCase):


    def test_plugin_retreival(self):
        """
        Tests whether the api can import plugins from plugin folder
        """
        test = PluginApi()
        actual = test.get_plugin_list()
        print("API TEST discovered plugins:") # added for ease of test debugging
        print(test.get_plugin_list()) # added for ease of test debugging
        expected = ['GenericNumberPlugin', 'GenericTextPlugin', 'PhoneNumberPlugin'] # placeholder at the moment
        self.assertListEqual(actual, expected)

    def test_plugin_function_exec(self):
        """ Tests whether the api can dynamically execute plugin functions """
        test = PluginApi()
        plugin = "PhoneNumberPlugin"
        column = ['(555)555-555', '(555) 555-555', '+1555555555', '555.555.5555', '5555555555']
        actual = test.plugin_confidence(plugin, column)
        errorZero = 0.0
        errorHundred = 100.00
        self.assertNotEqual(actual, errorZero)
        self.assertNotEqual(actual, errorHundred)

  

    




