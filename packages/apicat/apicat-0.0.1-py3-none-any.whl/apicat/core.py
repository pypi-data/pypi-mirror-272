import importlib
from flask import Flask
def register_plugins(plugin_names,app):
    for plugin_name in plugin_names:
        try:
            plugin_module = importlib.import_module(f"apicat_plugin_{plugin_name}")
            blueprint = getattr(plugin_module, 'blueprint', None)
            if blueprint:
                blueprint.name = plugin_name
                app.register_blueprint(blueprint)
            else:
                print(f"Plugin {plugin_name} does not have a 'blueprint' attribute.")
        except ImportError:
            print(f"Failed to import plugin {plugin_name}.")