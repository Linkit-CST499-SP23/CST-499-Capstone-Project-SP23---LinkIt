import os
import importlib

"""

The goal of the pluginApi object is to gather and initialize plugins that 
adhere to a basic naming convention / standardization, and to provide 
useability to the framework to manipulate them.


"""

class pluginApi(object):

    pluginList = []

    def __init__(self):
        pluginFiles = os.listdir('plugins')
        for plugin in pluginFiles:
            if not "__" in plugin:
                importlib.import_module("plugins."+plugin.split('.')[0])
                self.pluginList.append(plugin.split('.')[0])

    def outputPluginList(self):
        for plugin in self.pluginList:
            print(plugin + "\n")

    def getPluginList(self):
        return self.pluginList

        

 





