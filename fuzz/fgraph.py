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


class FuzzyGraph( object ):
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
        Return a list of vertices in the fuzzy graph. Returns

        @return: A list of vertices.
        @rtype: C{list}
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
