import os
import importlib



class PluginApi(object):
    """

    A class that acts as the API between the framework and any plugins within the LinkIt/plugins folder. 
    Seeks, imports, and provides functionality for the plugins.

    Will automatically import and use any plugin in the plugins folder, and will work so long as the plugin
    contains a function get_confidence_score() which takes in a list and returns an int

    ...

    Attributes
    -----------
    plugin_dict : Dictionary
        key = name of plugin
        value = plugin
        a dictionary of all the plugins that have been discovered and imported for use

    Methods
    ----------
    initialize_plugins():
        Searches the LinkIt/plugins/ folder for plugins and imports them for use, as well as
        adding them to plugin_dict, which allows for calling of their functions dynamically later

    plugin_confidence(plugin, column):
        retrieves a confidence score from a plugin for a column of data

    analyze_column(column):
        Runs all plugins on a column and returns a dict with the confidence 
        scores and plugin's names

    outputPluginList()
        prints plugin_dict
    
    getPluginList()
        returns the keys of plugin_dict as a list. Essentially shows the names of 
        all the plugins that have been 
    """

    plugin_dict = {}

    def __init__(self):
        self.initialize_plugins()
        print("API: plugins initialized...")

    def initialize_plugins(self):
        """ 
        Searches the LinkIt/plugins/ folder for plugins and imports them for use, as well as
        adding them to plugin_dict, which allows for calling of their functions dynamically later
        """
         
        try:
            plugin_files = os.listdir('LinkIt/plugins/')
            for plugin in plugin_files:
                if not "__" in plugin:
                    plug_name = plugin[:-3]
                    try:
                        self.plugin_dict[plug_name] = importlib.import_module("." + plug_name, package="plugins")
                    except:
                        print("API: ++ ERROR LOADING " + plug_name + " ++")
        except:
            print("error locating plugins folder or listing contents")

                    

                  
    def plugin_confidence(self, plugin, column_name, column):
        """ 
        retrieves a confidence score from a plugin for a column of data
        
        Parameters
        ----------
        plugin : string
            the plugin being run on that column
        column : string[]
            the column of data being scanned
        """
        try:
            confidence_score = self.plugin_dict[plugin].get_confidence_score(column_name, column)
            return confidence_score
        except:
            print("error getting plugin_confidence score from" + str(plugin))
            return 0.0


    def analyze_column(self, column_name, column):
        """
        Runs all plugins on a column and returns a dict with the confidence 
        scores and plugins' names

        TODO/FUTURE: add the ability to choose which plugins are applied

        Parameters
        ----------
        column : string[]
            the column of data being scanned


        output: dict {string:int}
        """
        plugins = self.plugin_dict.keys()
        confidence_scores = {}
        for plugin in plugins:
            print("--> running " + plugin)
            confidence_score = self.plugin_confidence(plugin, column_name, column)
            confidence_scores.update({plugin:confidence_score})
        
        print("API: '" + column_name + "' confidence scores:") # Console output for debug
        print(confidence_scores) # Console output for debug
        print("-------------------") # Console output for debug
        
        return confidence_scores


    def output_plugin_list(self):
        """ prints the keys (plugin names) of plugin_dict """
        for plugin in self.plugin_dict.keys():
            print(plugin + "\n")


    def get_plugin_list(self):
        """ returns the keys (plugin names) of plugin_dict """
        plugin_list = []
        for key in self.plugin_dict.keys():
            plugin_list.append(key)
        return plugin_list








        

 





