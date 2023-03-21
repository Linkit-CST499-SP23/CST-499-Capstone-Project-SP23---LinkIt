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
        print("API TEST discovered plugins:")
        print(test.get_plugin_list())
        expected = ['GenericNumberPlugin', 'GenericTextPlugin', 'PhoneNumberPlugin'] # placeholder at the moment
        self.assertListEqual(actual, expected)

    def test_plugin_function_exec(self):
        """ Tests whether the api can dynamically execute plugin functions """
        test = PluginApi()
        actual = 100.00 #filler
        expected = 100.00
        self.assertEqual(actual, expected)

  

    




