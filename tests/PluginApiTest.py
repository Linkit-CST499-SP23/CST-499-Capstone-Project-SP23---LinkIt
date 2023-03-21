import unittest
import sys
sys.path.append("..")

from LinkIt.pluginApi import *

#sys.path.insert(0, 'CST-499-Capstone-Project-SP23---LinkIt/pluginApi/pluginApi')



class TestPluginApi(unittest.TestCase):


    def test_plugin_retreival(self):
        """
        Tests whether the api can import plugins from plugin folder
        """
        test = pluginApi()
        actual = test.get_plugin_list()
        print("API TEST discovered plugins:")
        print(test.get_plugin_list())
        expected = ['GenericNumberPlugin', 'GenericTextPlugin', 'PhoneNumberPlugin'] # placeholder at the moment
        self.assertListEqual(actual, expected)
  

    




