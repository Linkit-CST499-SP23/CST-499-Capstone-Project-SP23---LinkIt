import os
import importlib



class PluginApi(object):
    """

    A class that acts as the API between the framework and any plugins within the LinkIt/plugins folder. 
    Seeks, imports, and provides functionality for the plugins.

    ...

    Attributes
    -----------
    plugin_dict : Dictionary
        a list of all the plugins that have been discovered and imported for use

    Methods
    ----------
    outputPluginList()
        prints plugin_dict
    
    getPluginList()
        returns the keys of plugin_dict as a list. Essentially shows the names of 
        all the plugins that have been 
    """

    plugin_dict = {}

    def __init__(self):
        self.initialize_plugins()

    def initialize_plugins(self):
        plugin_files = os.listdir('LinkIt/plugins/')
        for plugin in plugin_files:
            if not "__" in plugin:
                plug_name = plugin[:-3]
                self.plugin_dict[plug_name] = importlib.import_module("LinkIt.plugins."+plugin[:-3])
                #self.plugin_dict.append(plugin.split('.')[0])

    def output_plugin_list(self):
        """ prints the plugin_dict """
        for plugin in self.plugin_dict.keys():
            print(plugin + "\n")

    def get_plugin_list(self):
        """ returns the keys of plugin_dict """
        plugin_list = []
        for key in self.plugin_dict.keys():
            plugin_list.append(key)
        return plugin_list



        

 





