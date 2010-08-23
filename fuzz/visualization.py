"""\
Visualization Manager for fuzzpy
================================

This submodule allows the dispatch of any supported fuzzpy datatypes to
an arbitrary visualization plugin. All available visualization plugins are
located in the L{vis_plugins} submodule.

The manager provides a helper function to discover installed plugins as well
as a visualization backend factory.
"""

import vis_plugins
import warnings

class VisManager:
    """\
    Visualization Plugin Factory
        
    Provides plugin management methods and a helper method to dispatch
    a fuzzpy object to a plugin.
    """
    
    @staticmethod
    def get_supported_plugins(datatype=None):
        """\
        Returns a list of plugins supported by the current system.
        
        If L{datatype} is specified, try to find supported plugins that can
        be used to represent the specified datatype. Otherwise, return a list
        of all plugins that can run on that system.
        
        If any type of exception is raised during the C{is_supported()} call,
        the plugin will B{not} be included in the resulting list.
        
        @param datatype: fuzzpy datatype to look for supported plugins.
        @type datatype: C{str}
        @rtype: C{list}
        @return: list of plugins that can run in the current environment
        """
        supported = []
        
        for plugin in vis_plugins.__all__:
            # Try to import the plugin
            try:
                plugin_mod = __import__("vis_plugins.%s" % plugin,
                        fromlist=plugin)
            except ImportError, ex:
                warnings.warn(ex)
                continue
                
            # Extract plugin class name (or raise AttributeError)
            if not getattr(plugin_mod, 'VIS_PLUGIN'):
                raise AttributeError("Plugin %s is missing VIS_PLUGIN \
                    property" % plugin)
            plugin_class = getattr(plugin_mod, plugin_mod.VIS_PLUGIN)
            
            if (getattr(plugin_class, 'is_supported')() == True) and \
                (datatype in [None] + getattr(plugin_mod, 'VIS_TYPES')):
                supported.append(plugin)

        return supported
    
    @staticmethod
    def create_backend(obj, plugin=None, *args, **kwargs):
        """\
        Visualization Plugin Factory
        
        Returns a new instance of the appropriate visualization plugin.
        If no 'plugin' argument is specified as the preferred visualization
        backend, the first plugin that supports visualization for 'obj's
        class name will be used as the backend.
        
        @param obj: Object to draw
        @type obj: Object
        @param plugin: Name of the plugin to use
        @type plugin: C{str}
        @returns: The return value of the plugin's visualize() method
        @rtype: C{tuple} (format, payload)
        """
        
        # Pick a supported plugin if none is specified
        if None == plugin:
            plugin = VisManager.get_supported_plugins(obj.__class__)[0]
        
        plugin_mod = __import__("vis_plugins.%s" % plugin, fromlist=plugin)
        
        # Extract plugin class name
        plugin_name = getattr(plugin_mod, 'VIS_PLUGIN')
        
        return getattr(plugin_mod, plugin_name)\
            (obj=obj, args=args, kwargs=kwargs)
        