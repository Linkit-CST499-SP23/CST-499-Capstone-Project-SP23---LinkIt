import os
import importlib



class PluginApi(object):
    """

    A class that acts as the API between the framework and any plugins within the LinkIt/plugins folder. 
    Seeks, imports, and provides functionality for the plugins.

    ...

    Attributes
    -----------
    plugin_list : List
        a list of all the plugins that have been discovered and imported for use

    Methods
    ----------
    outputPluginList()
        prints plugin_list
    
    getPluginList()
        returns plugin_list
    """

    plugin_list = []

    def __init__(self):
        self.initialize_plugins()

    def initialize_plugins(self):
        plugin_files = os.listdir('LinkIt/plugins/')
        for plugin in plugin_files:
            if not "__" in plugin:
                importlib.import_module("LinkIt.plugins."+plugin.split('.')[0])
                self.plugin_list.append(plugin.split('.')[0])

    def output_plugin_list(self):
        """ prints the plugin_list """
        for plugin in self.plugin_list:
            print(plugin + "\n")

    def get_plugin_list(self):
        """ returns the plugin_list """
        return self.plugin_list

        

 





