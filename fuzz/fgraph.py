"""\
Graph module. Contains fuzzy graph class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from fset import *

class GraphEdge( object ):
    """\
    Graph edge class.
    """
    def __init__( self, tail, head ):
        """\
        Construct a graph edge directed from tail to head.

        @param tail: The tail vertex reference.
        @type tail: C{object}
        @param head: The head vertex reference.
        @type head: C{object}
        """
        if tail == head:
            raise ValueError, ( "Tail and head must differ" )
        self.tail = tail
        self.head = head

    def __repr__( self ):
        """\
        Return string representation of this graph edge.

        @return: String representation.
        @rtype: C{string}
        """
        return '(%s, %s)' % ( self.tail.__repr__(), self.head.__repr__() )

    __str__ = __repr__

    def __hash__( self ):
        """\
        Return a hash for this object.

        @return: The hash.
        @rtype: C{int}
        """
        # FIXME: returns same hash for A,B and B,A, but seems to work?
        return hash( self.tail ) ^ hash( self.head )

    def __contains__( self, vertex ):
        """\
        Report whether this edge connects to the specified vertex.

        @param vertex: The vertex to test for.
        @type vertex: C{object}
        @return: True if connected to the vertex, false otherwise.
        @rtype: C{bool}
        """
        if self.tail == vertex or self.head == vertex:
            return True
        return False
    
    def __eq__( self, other ):
        """\
        Compare two graph edges for equality.

        @param other: The other graph edge.
        @type other: L{GraphEdge}
        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance( other, GraphEdge ):
            raise TypeError, \
                ( "Comparison only permitted between graph edges" )
        if self.tail != other.tail or self.head != other.head:
            return False
        return True

    def __ne__( self, other ):
        """\
        Compare two graph edges for inequality.

        @param other: The other graph edge.
        @type other: L{GraphEdge}
        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other

    def reverse( self ):
        """\
        Returns this edge with tail and head reversed.

        @return: The reversed graph edge.
        @rtype: L{GraphEdge}
        """
        return GraphEdge( self.head, self.tail )


class Graph( object ):
    """\
    Crisp graph class (used for alpha cuts and crisp methods).
    """
    def __init__( self, viter = None, eiter = None, directed = True ):
        """\
        Construct a crisp graph from optional iterables.

        @param viter: The iterable for the vertex set (optional).
        @type viter: C{object}
        @param eiter: The iterable for the edge set (optional).
        @type eiter: C{object}
        @param directed: Defines the graph as directed or undirected.
        @type directed: C{bool}
        """
        self._directed = directed
        self._V = set()
        self._E = set()
        if viter is not None:
            for vertex in viter:
                self.add_vertex( vertex )
        if eiter is not None:
            for edge in eiter:
                self.add_edge( edge )

    def __repr__( self ):
        """\
        Return string representation of this graph.

        @return: String representation.
        @rtype: C{string}
        """
        return 'V: %s\nE: %s' % ( self._V, self._E )

    __str__ = __repr__

    @property
    def directed( self ):
        """\
        Return whether this graph is directed. This should only be set by the
        constructor and is read-only afterward.

        @return: True if the graph is directed, false otherwise.
        @rtype: C{bool}
        """
        return self._directed

    def add_vertex( self, vertex ):
        """\
        Add a vertex to the graph.

        @param vertex: The vertex to add.
        @type vertex: C{object}
        """
        self._V.add( vertex )

    def remove_vertex( self, vertex ):
        """\
        Remove a vertex and all edges connected to it from the graph.

        @param vetex: The vertex to remove.
        @type vertex: C{object}
        """
        if not vertex in self._V:
            raise KeyError, vertex
        for edge in self._E:
            if vertex in edge:
                self._E.remove( edge )
        self._V.remove( vertex )

    def add_edge( self, edge ):
        """\
        Add an edge to the graph.

        @param edge: The edge to add.
        @type edge: L{GraphEdge}
        """
        if not isinstance( edge, GraphEdge ):
            raise TypeError, ( "Edge must be a GraphEdge" )
        if not edge.tail in self.vertices or not edge.head in self.vertices:
            raise KeyError, ( "Tail and head must be in vertex set" )
        if edge in self.edges() \
        or ( not self.directed and edge.reverse() in self.edges() ):
            raise ValueError, ( "Edge already exists" )
        self._E.add( edge )

    def remove_edge( self, edge ):
        """
        Remove an edge from the graph.

        @param edge: The edge to remove.
        @type edge: L{GraphEdge}
        """
        if not self.directed and edge.reverse() in self.edges():
            self._E.remove( edge.reverse() )
        else:
            self._E.remove( edge )

    @property
    def vertices( self ):
        """\
        Return a set of vertices in the graph.

        @return: A set of vertices.
        @rtype: C{set}
        """
        return self._V

    def edges( self, tail = None, head = None ):
        """\
        Return a set of edges with tail and/or head optionally specified.

        @param tail: The tail vertex constraint (optional).
        @type tail: C{object}
        @param head: The head vertex constraint (optional).
        @type head: C{object}
        @return: The set of edges specified.
        @rtype: C{set}
        """
        result = set()
        if ( tail is not None and not tail in self._V ) \
        or ( head is not None and not head in self._V ):
            raise KeyError, ( "Specified tail/head must be in vertex set" )
        for edge in self._E:
            if ( tail is None or edge.tail == tail ) \
            and ( head is None or edge.head == head ):
                result.add( edge )
        return result

    # Convenience functions

    def connect( self, tail, head ):
        """\
        Connect a pair of vertices with a new edge. Convenience wrapper for
        add_edge().

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        """
        self.add_edge( GraphEdge( tail, head ) )

    def disconnect( self, tail, head ):
        """\
        Disconnect a pair of vertices by removing the edge between them.
        Convenience wrapper for remove_edge().

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        """
        self.remove_edge( GraphEdge( tail, head ) )

    # Binary graph operations

    def __eq__( self, other ):
        """\
        Compare two graphs for equality. Does not recognize isomorphism
        (vertex identifiers must be the same).

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if self._V != other._V or self._E != other._E:
            return False
        return True

    def __ne__( self, other ):
        """\
        Compare two graphs for inequality.

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other

    def issubgraph( self, other ):
        """\
        Report whether another graph contains this graph.

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if a subgraph, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if self._V <= other._V and self._E <= other._E:
            return True
        return False

    def issupergraph( self, other ):
        """\
        Report whether this graph contains another graph.

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if a supergraph, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if self._V >= other._V and self._E >= other._E:
            return True
        return False

    __le__ = issubgraph
    __ge__ = issupergraph

    def __lt__( self, other ):
        """\
        Report whether another graph strictly contains this graph.

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if a strict subgraph, false otherwise.
        @rtype: C{bool}
        """
        if self.issubgraph( other ) and self != other:
            return True
        return False

    def __gt__( self, other ):
        """\
        Report whether this graph strictly contains another graph.

        @param other: The other graph.
        @type other: L{Graph}
        @return: True if a strict supergraph, false otherwise.
        """
        if self.issupergraph( other ) and self != other:
            return True
        return False

    def _binary_sanity_check( self, other ):
        """\
        Check that the other argument to a binary operation is also a graph,
        raising a TypeError otherwise.
        """
        if not isinstance( other, Graph ):
            raise TypeError, \
                ( "Binary operation only permitted between graphs" )


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
                self.add_vertex( vertex )
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
