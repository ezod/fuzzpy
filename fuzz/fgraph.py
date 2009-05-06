"""\
Graph module. Contains fuzzy graph class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

# Local imports
from fset import *
from graph import *


class FuzzyGraph( Graph ):
    """\
    Fuzzy graph class.
    """
    def __init__( self, viter = None, eiter = None, directed = True ):
        """\
        Construct a fuzzy graph from optional iterables.

        @param viter: The iterable for the vertex set (optional).
        @type viter: C{object}
        @param eiter: The iterable for the edge set (optional).
        @type eiter: C{object}
        @param directed: Defines the graph as directed or undirected.
        @type directed: C{bool}
        """
        self._directed = directed
        self._V = FuzzySet()
        self._E = FuzzySet()
        if viter is not None:
            for vertex in viter:
                if isinstance( vertex, FuzzyElement ):
                    self.add_vertex( vertex )
                else:
                    self.add_vertex( FuzzyElement( vertex, 1.0 ) )
        if eiter is not None:
            for edge in eiter:
                self.add_edge( edge )

    def remove_vertex( self, vertex ):
        """\
        Remove a vertex and all edges connected to it from the fuzzy graph.

        @param vetex: The vertex to remove.
        @type vertex: C{object}
        """
        if not vertex in self._V:
            raise KeyError, vertex
        for edge in self._E:
            if vertex in edge.obj:
                self._E.remove( edge.obj )
        self._V.remove( vertex )

    def add_edge( self, edge ):
        """\
        Add an edge to the fuzzy graph.

        @param edge: The edge to add.
        @type edge: L{FuzzyElement} of L{GraphEdge}
        """
        if not isinstance( edge.obj, GraphEdge ):
            raise TypeError, ( "Edge must be a GraphEdge" )
        if not edge.obj.tail in self.vertices \
        or not edge.obj.head in self.vertices:
            raise KeyError, ( "Tail and head must be in vertex set" )
        if edge.obj in self.edges() \
        or ( not self.directed and edge.obj.reverse() in self.edges() ):
            raise ValueError, ( "Edge already exists" )
        self._E.add( edge )

    @property
    def vertices( self ):
        """\
        Return a set of vertices in the fuzzy graph.

        @return: A set of vertices.
        @rtype: C{set}
        """
        return self._V.objects

    def edges( self, tail = None, head = None ):
        """\
        Return a fuzzy set of edges with tail and/or head optionally
        specified.

        @param tail: The tail vertex constraint (optional).
        @type tail: C{object}
        @param head: The head vertex constraint (optional).
        @type head: C{object}
        @return: The fuzzy set of edges specified.
        @rtype: L{FuzzySet}
        """
        result = FuzzySet()
        if ( tail is not None and not tail in self._V ) \
        or ( head is not None and not head in self._V ):
            raise KeyError, ( "Specified tail/head must be in vertex set" )
        for edge in self._E:
            if ( tail is None or edge.tail == tail ) \
            and ( head is None or edge.head == head ):
                result.add( edge )
        return result

    # Convenience functions

    def add_fuzzy_vertex( self, vertex, mu = 1.0 ):
        """\
        Add a fuzzy vertex to the fuzzy graph (without explicitly constructing
        a FuzzyElement for it). Convenience wrapper for add_vertex().

        @param vertex: The vertex to add.
        @type vertex: C{object}
        @param mu: The membership degree of the vertex (optional).
        @type mu: C{float}
        """
        self.add_vertex( FuzzyElement( vertex, mu ) )

    def add_fuzzy_edge( self, edge, mu = 1.0 ):
        """\
        Add a fuzzy edge to the fuzzy graph (without explicitly constructing
        a FuzzyElement for it). Convenience wrapper for add_edge().

        @param vertex: The edge to add.
        @type vertex: L{GraphEdge}
        @param mu: The membership degree of the edge (optional).
        @type mu: C{float}
        """
        self.add_edge( FuzzyElement( edge, mu ) )

    def connect( self, tail, head, mu = 1.0 ):
        """\
        Connect a pair of vertices with a new edge. Convenience wrapper for
        add_edge().

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        @param mu: The membership degree of the edge (optional).
        @type mu: C{float}
        """
        self.add_edge( FuzzyElement( GraphEdge( tail, head ), mu ) )

    # Binary fuzzy graph operations

    def _binary_sanity_check( self, other ):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        graph, raising a TypeError otherwise.
        """
        if not isinstance( other, FuzzyGraph ):
            raise TypeError, \
                ( "Binary operation only permitted between fuzzy graphs" )

    # Unary fuzzy graph operations

    def alpha( self, alpha ):
        """\
        Alpha cut function. Returns the crisp graph for which both vertex and
        edge membership values meet or exceed the alpha value.

        @param alpha: The alpha value for the cut.
        @type alpha: C{float}
        @return: The crisp graph result of the alpha cut.
        @rtype: L{Graph}
        """
        Va = self._V.alpha( alpha )
        Ea = set()
        for edge in self._E.alpha( alpha ):
            if edge.tail in Va and edge.head in Va:
                Ea.add( edge )
        return Graph( Va, Ea, self.directed )

    def alpha( self, alpha ):
        """\
        Strong alpha cut function. Returns the crisp graph for which both
        vertex and edge membership values exceed the alpha value.

        @param alpha: The alpha value for the cut.
        @type alpha: C{float}
        @return: The crisp graph result of the strong alpha cut.
        @rtype: L{Graph}
        """
        Va = self._V.salpha( alpha )
        Ea = set()
        for edge in self._E.salpha( alpha ):
            if edge.tail in Va and edge.head in Va:
                Ea.add( edge )
        return Graph( Va, Ea, self.directed )
