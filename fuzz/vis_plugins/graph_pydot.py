"""\
Pydot visualization plugin for FuzzPy.

@author: Xavier Spriet
@contact: linkadmin@gmail.com
@license: LGPL-3
"""

from ..fgraph import FuzzyGraph
from ..graph import Graph
from abc_plugin import AbstractPlugin

VIS_PLUGIN = 'FuzzPyDot'
VIS_TYPES = [FuzzyGraph, Graph]
VIS_FORMATS = ['bmp', 'canon', 'dot', 'xdot', 'eps', 'fig', 'gd', 'gd2', 
    'gif', 'gtk', 'ico', 'imap', 'cmapx', 'jpg', 'jpeg', 'jpe', 'pdf', 
    'plain', 'plain-ext', 'png', 'ps', 'ps2', 'svg', 'svgz', 'tif', 'tiff', 
    'vml', 'vmlz', 'vrml', 'wbmp', 'xlib']


class FuzzPyDot(AbstractPlugin):
    """\
    Pydot visualization plugin for fuzzpy
    
    This plugin converts vertices and edges to pydot elements then create
    a rendering based on the 'format' attribute (default=png).
    """
    def __init__(self, obj=None, *args, **kwargs):
        """\
        Plugin constructor.
        
        Maps the specified graph object locally and marshalls method
        keywords to local arguments for the PyDot object.
        
        @param obj: The graph or fuzzy graph to visualize.
        @type obj: L{Graph} or L{FuzzyGraph}
        """
        import pydot
        self.pydot = pydot
        self._G = obj
        
        if ('name' in kwargs.keys()):
            self.name = kwargs['name']
        else:
            name = 'FuzzPy Graph'
    
    @staticmethod
    def is_supported():
        """\
        Return whether this plugin is supported.

        @return: True if the plugin can run in this environment.
        @rtype: C{bool}
        """
        try:
            import pydot
        except ImportError:
            warning.warn(("PyDot plugin will not run on this system. "
                          "You must install the PyDot Python module first."))
            return False
        return True
    
    def marshall_vertices(self):
        """\
        Converts vertices to PyDot nodes.
        
        Adds GraphViz attributes to each vertex and converts it into a
        pydot.Node object.
        
        @return: List of pydot.Node objects.
        @rtype: C{list}
        """
        vertices = []
        for vertex in self._G.vertices():
            if isinstance(self._G, FuzzyGraph):
                node = self.pydot.Node(
                    name="g_%s" % str(vertex),
                    label=str(vertex),
                    weight=str(self._G.mu(vertex)),
                    penwidth="%.2f" % self._G.mu(vertex)
                )
            elif isinstance(self._G, Graph):
                node = self.pydot.Node(
                    name="g_%s" % str(vertex),
                    label=str(vertex),
                )
            vertices.append(node)
        return vertices
        
    def marshall_edges(self):
        """\
        Converts edges to PyDot edges.
        
        Adds GraphViz attributes to edges and registers them all as PyDot
        edge objects.
        
        @returns: List of pydot.Edge objects.
        @rtype: C{list}
        """
        edges = []
        for edge in self._G.edges():
            if isinstance(self._G, FuzzyGraph):
                connector = self.pydot.Edge(
                    src="g_%s" % str(edge.head), 
                    dst="g_%s" % str(edge.tail),
                    weight=str(self._G.mu(edge.tail, edge.head)),
                    penwidth=str((self._G.mu(edge.tail, edge.head) \
                        + 0.05) * 2.0),
                    # For older versions of graphviz
                    style="setlinewidth(%f)" % ((self._G.mu(edge.tail, \
                        edge.head) + 0.05) * 2.0)
                )
            elif isinstance(self._G, Graph):
                connector = self.pydot.Edge(
                    "g_%s" % str(edge.head), 
                    "g_%s" % str(edge.tail),
                )
            edges.append(connector)
        return edges
    
    def visualize(self, *args, **kwargs):
        """\
        PyDot visualization method.
        
        Converts all vertices and edges from the graph provided to the
        plugin's constructor into a PyDot graph and converts any apppropriate
        attributes to be passed to GraphViz.
        
        @return: Output data string.
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
        
        D = self.pydot.Dot(rankdir='RT', graph_type=gtype)
        
        # Convert vertices and edges to PyDot nodes/connectors
        for vertex in self.marshall_vertices():
            D.add_node(vertex)
        
        for edge in self.marshall_edges():
            D.add_edge(edge)

        # Return formatted output
        return (output_format, D.create(format=output_format))

AbstractPlugin.register(FuzzPyDot)
