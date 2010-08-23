import graph
import pydot
from .fgraph import FuzzyGraph
from .graph import Graph
from abc_plugin import AbstractPlugin

# Class Name
VIS_PLUGIN = 'FuzzPyDot'

# Supported Visualization Datatypes
VIS_TYPES = [FuzzyGraph, Graph, graph]

# Supported Output Formats
VIS_FORMATS = ['bmp', 'canon', 'dot', 'xdot', 'eps', 'fig', 'gd', 'gd2', 
    'gif', 'gtk', 'ico', 'imap', 'cmapx', 'jpg', 'jpeg', 'jpe', 'pdf', 
    'plain', 'plain-ext', 'png', 'ps', 'ps2', 'svg', 'svgz', 'tif', 'tiff', 
    'vml', 'vmlz', 'vrml', 'wbmp', 'xlib']


class FuzzPyDot(AbstractPlugin):
    """\
    Pydot visualization plugin for fuzzpy
    
    This plugin converts vertices and edges to pydot elements then create
    a rendering based on the 'format' attribute (default=ps).
    """
    
    # Graph instance
    _G = None
    # Graph name
    name = 'Fuzzpy Graph'
    
    def __init__(self, obj=None, *args, **kwargs):
        """\
        Plugin Constructor
        
        Maps the specified graph object locally and marshalls method
        keywords to local arguments for the PyDot object.
        
        @param obj: Graph, FuzzyGraph or graph instance
        @type obj: L{Graph} or L{FuzzyGraph} or C{graph}
        @return: Initialized plugin instance
        @rtype: VisPlugin
        """
        self._G = obj
        
        if ('name' in kwargs.keys()):
            self.name = kwargs['name']
    
    @staticmethod
    def is_supported():
        """\
        Placeholder
        
        @rtype: Boolean
        @return: True if the plugin can run in this environment.
        """
        try:
            import pydot
        except ImportError, ex:
            warning.warn("PyDot plugin will not run on this system. \
            You must install the PyDot python module first.")
            return False
        return True
    
    def visualize(self, *args, **kwargs):
        """\
        PyDot visualization method
        
        Converts all vertices and edges from the graph provided to the
        plugin's constructor into a PyDot graph and converts any apppropriate
        attributes to be passed to GraphViz.
        
        This method will return a postscript string that can be written into
        a file, or passwd through stdin to a postscript viewer such as gv.
        
        @return: Postscript visualization string
        @rtype: C{str}
        """
        if self._G.directed == True:
            gtype = 'digraph'
        else:
            gtype = 'graph'
        
        # Pick default output format if required
        if kwargs.has_key('format') and kwargs['format'] in VIS_FORMATS:
            output_format = kwargs['format']
        else:
            output_format = 'png'
        
        D = pydot.Dot('rt', graph_type=gtype)
        
        # Convert vertices
        for vertex in self._G.vertices:
            D.add_node(
                    pydot.Node(
                            name="g_%s" % str(vertex),
                            label=str(vertex),
                            weight=str(self._G.mu(vertex)),
                            penwidth="%.2f" % self._G.mu(vertex)
                        )
                    )
        
        # Convert edges
        for edge in self._G.edges():
            D.add_edge(
                pydot.Edge(
                    "g_%s" % edge.head, 
                    "g_%s" % edge.tail,
                    weight=str(self._G.mu(edge)),
                    penwidth=str((self._G.mu(edge.tail, edge.head)+0.05)*2.0)
                )
            )
        
        return D.create(format=output_format)

AbstractPlugin.register(FuzzPyDot)
