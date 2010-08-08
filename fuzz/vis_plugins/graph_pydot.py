import pydot
from .fgraph import FuzzyGraph
from .graph import Graph
import graph


class VisPlugin:
    
    # Supported visualization datatypes
    types = [FuzzyGraph, Graph, graph]
    
    # Graph instance
    _G = None
    # Edges list
    _E = None
    # Vertices list
    _V = None
    
    
    def __init__(self, obj=None, *args, **kwargs):
        self._G = obj
        self._E = self._G._E
        self._V = self._G._V
    
    def visualize(self):
        D = pydot.Dot()
        
        for vertex in self._V:
            print "Vertex:", vertex
            D.add_node(pydot.Node(str(vertex), self._V.mu(vertex)))
                    
        for edge in self._E:
            print "Edge:", edge
            D.add_edge(pydot.Edge(edge[1].head, edge[1].tail))
        
        return D.create()
        
    
    
