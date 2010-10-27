"""\
Graph module. Contains fuzzy graph class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from .fset import FuzzyElement, FuzzySet 
from .graph import GraphEdge, Graph


class FuzzyGraph(Graph):
    """\
    Fuzzy graph class.
    """
    _setcls = FuzzySet

    def __init__(self, viter=None, eiter=None, directed=True):
        """\
        Construct a fuzzy graph from optional iterables.

        @param viter: The iterable for the vertex set (optional).
        @type viter: C{object}
        @param eiter: The iterable for the edge set (optional).
        @type eiter: C{object}
        @param directed: Defines the graph as directed or undirected.
        @type directed: C{bool}
        """
        super(FuzzyGraph, self).__init__(viter=viter, eiter=eiter,
            directed=directed)

    def add_vertex(self, vertex, mu=1.0):
        """\
        Add a fuzzy vertex to the fuzzy graph, optionally constructing the
        vertex with the given membership degree.

        @param vertex: The vertex to add.
        @type vertex: C{object}
        @param mu: The membership degree of the vertex (optional).
        @type mu: C{float}
        """
        if not isinstance(vertex, FuzzyElement):
            vertex = FuzzyElement(vertex, mu)
        Graph.add_vertex(self, vertex)

    def add_edge(self, edge, mu=1.0):
        """\
        Add an edge to the fuzzy graph.

        @param edge: The edge to add.
        @type edge: L{FuzzyElement} of L{GraphEdge}
        @param mu: The membership degree of the edge (optional).
        @type mu: C{float}
        """
        if not isinstance(edge, FuzzyElement):
            edge = FuzzyElement(edge, mu)
        try:
            if not isinstance(edge.index, GraphEdge):
                raise TypeError('edge must be a GraphEdge')
        except AttributeError:
            Graph.add_edge(self, edge)
        if not edge.index.tail in self.vertices() \
        or not edge.index.head in self.vertices():
            raise KeyError('tail and head must be in vertex set')
        if edge.index in self.edges():
            raise ValueError('edge already exists')
        self._E.add(edge)

    def vertices(self):
        """\
        Return a set of vertices in the fuzzy graph.

        @rtype: C{set}
        """
        return set(self._V.keys())

    def edges(self, tail=None, head=None):
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
        if (tail is not None and not tail in self.vertices()) \
        or (head is not None and not head in self.vertices()):
            raise KeyError('specified tail/head must be in vertex set')
        eset = set([edge.index for edge in self._E \
            if (tail is None or edge.index.tail == tail) \
            and (head is None or edge.index.head == head)])
        if not self.directed:
            eset |= set([edge.index for edge in self._E \
                if (tail is None or edge.index.head == tail) \
                and (head is None or edge.index.tail == head)])
        return eset

    def mu(self, tail, head=None):
        """\
        Return the membership degree of a vertex or edge.

        @param tail: The vertex or tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        @return: The membership degree of the vertex or edge from tail to head.
        @rtype: C{float}
        """
        if head is None:
            return self._V.mu(tail)
        elif self.directed:
            return self._E.mu(GraphEdge((tail, head)))
        else:
            return max(self._E.mu(GraphEdge((tail, head))),
                       self._E.mu(GraphEdge((head, tail))))

    def weight(self, tail, head):
        """\
        Return the weight of an edge. Returns the inverse of the membership
        degree for a fuzzy graph.

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        @return: The weight of the edge from tail to head.
        @rtype: C{float}
        """
        if tail == head:
            return 0.0
        try:
            return 1.0 / self.mu(tail, head)
        except ZeroDivisionError:
            return float('inf')
                
    def connect(self, tail, head, mu=1.0):
        """\
        Connect a pair of vertices with a new (fuzzy) edge.

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        @param mu: The membership degree of the edge (optional).
        @type mu: C{float}
        """
        self.add_edge(FuzzyElement(GraphEdge((tail, head)), mu))

    # Binary fuzzy graph operations

    @staticmethod
    def _binary_sanity_check(other):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        graph, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{FuzzyGraph}
        """
        if not isinstance(other, FuzzyGraph):
            raise TypeError('operation only permitted between fuzzy graphs')

    # Unary fuzzy graph operations

    def alpha(self, alpha):
        """\
        Alpha cut function. Returns the crisp graph for which both vertex and
        edge membership values meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp graph result of the alpha cut.
        @rtype: L{Graph}
        """
        Va = self._V.alpha(alpha)
        Ea = set()
        for edge in self._E.alpha(alpha):
            if edge.tail in Va and edge.head in Va:
                Ea.add(edge)
        return Graph(viter=Va, eiter=Ea, directed=self.directed)

    def salpha(self, alpha):
        """\
        Strong alpha cut function. Returns the crisp graph for which both
        vertex and edge membership values exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp graph result of the strong alpha cut.
        @rtype: L{Graph}
        """
        Va = self._V.salpha(alpha)
        Ea = set()
        for edge in self._E.salpha(alpha):
            if edge.tail in Va and edge.head in Va:
                Ea.add(edge)
        return Graph(viter=Va, eiter=Ea, directed=self.directed)

    def normalize(self):
        """\
        Normalize the fuzzy graph by normalizing its vertex and edge sets.
        """
        self._V.normalize()
        self._E.normalize()
