"""\
Visualization Manager for fuzzpy
================================

This submodule allows the dispatch of any supported fuzzpy datatypes to
an arbitrary visualization plugin. All available visualization plugins are
located in the L{vis_plugins} submodule.

The manager provides helper functions to discover installed plugins as well
as to determine which plugins can be run in the current environment.

Once instanciated, the core method in this class is the L{visualize()},
which will dispatch the specified fuzzpy object to the appropriate plugin.

The type of returned value depends on the plugin, so you should carefully read
the documentation for the plugin you are using.
"""

import vis_plugins

class VisManager:
    """\
    Visualization Manager class
    
    Provides plugin management methods and a helper method to dispatch
    a fuzzpy object to a plugin.
    """
    _plugins = {}
    
    def __init__(self):
        """\
        Constructor Method
        
        Initializes the L{_plugins} dictionary from the results of the
        L{_discover_plugins} method.
        
        @rtype: VisManager
        @return: Initialized VisManager instance
        """
        self._plugins = self._discover_plugins()
    
    def _discover_plugins(self):
        """\
        Plugin Discovery Method
        
        Attempts to import all plugins in the vis_plugins submodule
        and retrieve the list of supported fuzzpy datatypes that this plugin
        can be used to visualize.
        
        The resulting dictionary will look like this:
        C{ {'Graph' => ['graph_graphviz', 'graph_networkx', ...],
            'Number' => ['num_gnuplot', 'num_matplot', ...],
            ...
            }}
        Where the keys are supported datatypes, and the values are lists of
        supported plugins for that datatype.
        
        @rtype: C{dict}
        @return: Dictionary of k=datatype => v=list of supported plugins
        """
        plugins = {}
        for plugin in vis_plugins.__all__:
            try:
                plugin_mod = __import__("vis_plugins.%s" % plugin, 
                        fromlist=plugin)
            except ImportError, ex:
                # Don't include modules that can't be imported
                continue
            try:
                plugin_obj = plugin_mod.VisPlugin()
            except AttributeError, ex:
                # Class doesn't follow our interface
                continue
            else:
                try:
                    for vis_type in plugin_obj.types:
                        if vis_type not in plugins.keys():
                            plugins[vis_type.__name__] = [plugin]
                        else:
                            plugins[vis_type.__name__].append(plugin)
                except AttributeError:
                    # Class doesn't follow our interface
                    pass
        return plugins
    
    def get_supported_plugins(self, datatype=None):
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
        
        if None == datatype:
            # Assume we want to run the discovery for all installed plugins
            # k => keys, p => plugins
            plugins = [p for k in self._plugins.values() for p in k]
        else:
            if datatype in self._plugins.keys():
                plugins = self._plugins[datatype]
            else:
                raise ValueError("Unknown datatype: %s" % datatype)
        
        for plugin in plugins:
            try:
                plugin_mod = __import__("vis_plugins.%s" % plugin,
                        fromlist=plugin)
            except ImportError, ex:
                pass
            else:
                try:
                    if plugin_mod.is_supported():
                        supported.append(plugin)
                except Exception, ex:
                    print ex
                    pass
        
    
    def visualize(self, obj, plugin, *args, **kwargs):
        plugin_mod = __import__("vis_plugins.%s" % plugin, fromlist=plugin)
        plugin_obj = plugin_mod.VisPlugin(obj=obj, args=args, kwargs=kwargs)
        plugin_obj.visualize()
