import importlib
import pkgutil
import sys

import plugins #removed LinkIt before plugins

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    # Source: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-namespace-packages
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

def load_plugins():
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(plugins) #removed LinkIt before plugins
    }
    return discovered_plugins

def main():
    plugins = load_plugins()
    print("discovered plugins:", plugins)
    for plugin in plugins:
        plugins[plugin].greeting()
