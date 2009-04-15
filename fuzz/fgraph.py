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
        self.tail = tail
        self.head = head

    def __repr__( self ):
        """\
        Return string representation of a graph edge.

        @return: String representation.
        @rtype: C{string}
        """
        return '(%s, %s)' % ( self.tail.__repr__(), self.head.__repr__() )

    __str__ = __repr__
    
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
        if self.head != other.head or self.tail != other.tail:
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
        self._V = set( viter )
        if eiter is not None:
            for edge in eiter:
                if not isinstance( edge, GraphEdge ):
                    raise TypeError, ( "Edge set must consist of GraphEdges" )
                elif not edge.tail in self.vertices \
                or not edge.head in self.vertices:
                    raise KeyError, ( "Tail and head must be in vertex set" )
        self._E = set( eiter )
        self.directed = directed

    def __repr__( self ):
        """\
        Return string representation of a fuzzy graph.

        @return: String representation.
        @rtype: C{string}
        """
        return 'V = %s\nE = %s' % ( self._V, self._E )

    __str__ = __repr__

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
        @return: The fuzzy set of edges specified.
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
        self._V = FuzzySet( viter )
        if eiter is not None:
            for edge in eiter:
                if not isinstance( edge, GraphEdge ):
                    raise TypeError, ( "Edge set must consist of GraphEdges" )
                elif not edge.tail in self.vertices \
                or not edge.head in self.vertices:
                    raise KeyError, ( "Tail and head must be in vertex set" )
        self._E = FuzzySet( eiter )
        self.directed = directed

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
