"""\
Graph module. Contains fuzzy graph class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from fset import *

class GraphEdge( object ):
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
    def __init__( self, viter = None, eiter = None ):
        """\
        Construct a fuzzy graph from optional iterables.

        @param viter: The iterable for the vertex set (optional).
        @type viter: C{object}
        @param eiter: The iterable for the edge set (optional).
        @type eiter: C{object}
        """
        self._V = FuzzySet( viter )
        if eiter is not None:
            for edge in eiter:
                if not isinstance( edge, GraphEdge ):
                    raise TypeError, ( "Edge set must consist of GraphEdges" )
                elif not edge.tail in self._V and edge.head in self._V:
                    raise KeyError, ( "Tail and head must be in vertex set" )
        self._E = FuzzySet( eiter )
