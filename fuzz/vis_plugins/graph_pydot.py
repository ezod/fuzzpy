import pydot
from .fgraph import FuzzyGraph
from .graph import Graph
from abc_plugin import AbstractPlugin

# Class Name
VIS_PLUGIN = 'FuzzPyDot'

# Supported Visualization Datatypes
VIS_TYPES = [FuzzyGraph, Graph]

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
        Returns True if we can import our dependencies, False otherwise.
        
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
    
    def marshall_vertices(self):
        """\
        Converts vertices to PyDot nodes
        
        Adds GraphViz attributes to each vertex and converts it into a
        pydot.Node object.
        
        @rtype: list
        @return: list of pydot.Node objects
        """
        vertices = []
        for vertex in self._G.vertices:
            if isinstance(self._G, FuzzyGraph):
                node = pydot.Node(
                    name="g_%s" % str(vertex),
                    label=str(vertex),
                    weight=str(self._G.mu(vertex)),
                    penwidth="%.2f" % self._G.mu(vertex)
                )
            elif isinstance(self._G, Graph):
                node = pydot.Node(
                    name="g_%s" % str(vertex),
                    label=str(vertex),
                )
            vertices.append(node)
            
        return vertices
        
    def marshall_edges(self):
        """\
        Converts edges to PyDot edges
        
        Adds GraphViz attributes to edges and registers them all as PyDot
        edge objects.
        
        @rtype: list
        @returns: list of pydot.Edge objects
        """
        edges = []
        
        for edge in self._G.edges():
            if isinstance(self._G, FuzzyGraph):
                connector = pydot.Edge(
                    "g_%s" % edge.head, 
                    "g_%s" % edge.tail,
                    weight=str(self._G.mu(edge)),
                    penwidth=str((self._G.mu(edge.tail, edge.head)+0.05)*2.0)
                )
            elif isinstance(self._G, Graph):
                connector = pydot.Edge(
                    "g_%s" % edge.head, 
                    "g_%s" % edge.tail,
                )
            edges.append(connector)
            
        return edges
        
    
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
        
        # Pick default output format if required
        if kwargs.has_key('format') and kwargs['format'] in VIS_FORMATS:
            output_format = kwargs['format']
        else:
            output_format = 'png'
        
        if self._G.directed == True:
            gtype = 'digraph'
        else:
            gtype = 'graph'
        
        D = pydot.Dot('rt', graph_type=gtype)
        
        # Convert vertices and edges to PyDot nodes/connectors
        for vertex in self.marshall_vertices():
            D.add_node(vertex)
        
        for edge in self.marshall_edges():
            D.add_edge(edge)
        
        # Return formatted output
        return D.create(format=output_format)

AbstractPlugin.register(FuzzPyDot)
