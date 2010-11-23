#!/usr/bin/env python

"""\
Unit tests for FuzzPy. These tests are currently not exhaustive, and are
primarily used as a development tool to make sure changes in one place aren't
breaking things in another.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

import unittest

import fuzz
print('FuzzPy imported from "%s"' % fuzz.__path__[0])


class TestFuzzySet(unittest.TestCase):

    def setUp(self):
        self.A = fuzz.FuzzySet()
        self.B = fuzz.FuzzySet()
        self.A.add('a', 1.0)
        self.A.add('b', 0.5)
        self.A.add('c', 0.8)
        self.B.add('b', 0.8)
        self.B.add('c', 0.2)
        self.B.add('d', 0.6)
        self.B.add('e', 0.0)

    def test_fuzzy_element(self):
        self.assertRaises(ValueError, fuzz.FuzzyElement, 'a', mu=2)
        self.assertRaises(ValueError, fuzz.FuzzyElement, 'b', mu=-1)
        try:
            with self.assertRaises(ValueError):
                C = fuzz.FuzzyElement('c', 0.5)
                C.mu = 2
        except TypeError:
            pass

    def test_add_update_remove(self):
        self.A.add('a', 1)
        self.assertEqual(len(self.A), 3)
        self.A.update([fuzz.FuzzyElement('a', 1), fuzz.FuzzyElement('d', 1)])
        self.assertEqual(len(self.A), 4)
        self.A.remove('d')
        self.assertEqual(len(self.A), 3)

    def test_clear(self):
        self.A.clear()
        self.assertEqual(self.A, fuzz.FuzzySet())

    def test_copy(self):
        C = self.A.copy()
        C['a'].mu = 0.0
        self.assertTrue(self.A.mu('a') > 0.5)

    def test_pop(self):
        A = [fuzz.FuzzyElement('a', 1.0),
             fuzz.FuzzyElement('c', 0.8),
             fuzz.FuzzyElement('b', 0.5)]
        self.assertTrue(self.A.pop() in A)
        self.assertTrue(self.A.pop() in A)
        self.assertTrue(self.A.pop() in A)
        self.assertEqual(self.A, fuzz.FuzzySet())
    
    def test_disjoint(self):
        self.assertFalse(self.A.isdisjoint(self.B))
        self.assertFalse(self.B.isdisjoint(self.A))
        C = fuzz.FuzzySet(['e','f'])
        self.assertTrue(self.A.isdisjoint(C))
        self.assertTrue(self.B.isdisjoint(C))

    def test_getitem(self):
        self.assertEqual(self.A['b'].mu, 0.5)
        self.assertEqual(self.B['e'].mu, 0.0)

    def test_mu(self):
        self.assertEqual(self.A.mu('b'), 0.5)
        self.assertEqual(self.B.mu('e'), 0.0)
        self.assertEqual(self.A.mu('e'), 0.0)

    def test_contents(self):
        self.assertTrue('a' in self.A)
        self.assertFalse('e' in self.B)
        self.assertEqual(len(self.B), 3)

    def test_suppkern(self):
        self.assertEqual(len(self.A.kernel), 1)
        self.assertEqual(len(self.B.support), 3)

    def test_prune(self):
        self.assertEqual(len(self.B.keys()), 4)
        self.B.prune()
        self.assertEqual(len(self.B.keys()), 3)

    def test_union(self):
        C = fuzz.FuzzySet()
        C.add('a', 1.0)
        C.add('b', 0.8)
        C.add('c', 0.8)
        C.add('d', 0.6)
        self.assertEqual(self.A | self.B, C)
        D = fuzz.FuzzySet()
        D.add('a', 1.0)
        D.add('b', 0.9)
        D.add('c', 0.84)
        D.add('d', 0.6)
        self.assertEqual(self.A.union(self.B, fuzz.FuzzySet.NORM_ALGEBRAIC), D)

    def test_intersection(self):
        C = fuzz.FuzzySet()
        C.add('b', 0.5)
        C.add('c', 0.2)
        self.assertEqual(self.A & self.B, C)
        D = fuzz.FuzzySet()
        D.add('b', 0.4)
        D.add('c', 0.16)
        self.assertEqual(self.A.intersection(self.B, \
                         fuzz.FuzzySet.NORM_ALGEBRAIC), D)

    def test_normalize(self):
        self.B.normalize()
        self.assertTrue(self.B.normal)
        self.assertEqual(self.B['c'].mu, 0.25)
        self.assertEqual(self.B['d'].mu, 0.75)

    def test_overlap(self):
        self.assertEqual(self.A.overlap(self.B), 0.7 / 1.6)
        self.assertEqual(self.B.overlap(self.A), 0.7 / 2.3)

    def test_alpha(self):
        D = set(['a', 'c'])
        self.assertEqual(self.A.alpha(0.7), D)
        self.assertEqual(self.A.salpha(0.5), D)
        self.assertTrue('e' not in self.B.alpha(0.0))

    def test_complement(self):
        D = fuzz.FuzzySet()
        D.add('b', 0.2)
        D.add('c', 0.8)
        D.add('d', 0.4)
        D.add('e', 1.0)
        self.assertEqual(self.B.complement(), D)


class TestFuzzyNumber(unittest.TestCase):

    def setUp(self):
        K = fuzz.RealRange((3.0, 5.5))
        S = fuzz.RealRange((0.0, 6.5))
        self.N = fuzz.TrapezoidalFuzzyNumber(K, S)
        self.T = fuzz.TriangularFuzzyNumber(4.0, S)
        self.G = fuzz.GaussianFuzzyNumber(12.0, 1.0)
        self.X = fuzz.PolygonalFuzzyNumber( \
            [(0.0, 0.0), (3.0, 0.5), (4.0, 0.3), (6.0, 0.8), (7.0, 0.2),
             (8.0, 0.3), (9.0, 0.2), (10.0, 0.7), (11.0, 0.0)])
        self.Y = fuzz.PolygonalFuzzyNumber( \
            [(1.0, 0.0), (2.0, 1.0), (5.0, 0.3), (7.0, 0.7), (11.0, 0.0)])

    def test_mu(self):
        exp = [0., 1./3., 1., 1., 0.5, 0.]
        act = [self.N.mu( 0. ),
               self.N.mu( 1. ),
               self.N.mu( 3. ),
               self.N.mu( 5. ),
               self.N.mu( 6. ),
               self.N.mu( 7. )]
        self.assertEqual(act, exp)
        self.assertEqual(self.T.mu(2.0), 0.5)
        self.assertEqual(self.G.mu(12.0), 1.0)
        self.assertEqual(self.G.mu(self.G.support[1] + 1.0), 0.0)
        M = fuzz.TrapezoidalFuzzyNumber((1, 2), (1, 2))
        self.assertEqual(M.mu(1), 1.0)
        self.assertEqual(M.mu(2), 1.0)

    def test_height(self):
        self.assertEqual(self.N.height, 1.0)
        self.assertEqual(self.T.height, 1.0)
        self.assertEqual(self.X.height, 0.8)
        self.assertEqual(self.Y.height, 1.0)
    
    def test_alpha(self):
        exp = fuzz.RealRange((1.5, 6.0))
        act = self.N.alpha(0.5)
        self.assertEqual(act, exp)

    def test_to_polygonal(self):
        points = [(0.0, 0.0), (3.0, 1.0), (5.5, 1.0), (6.5, 0.0)]
        P = fuzz.PolygonalFuzzyNumber(points)
        Q = self.N.to_polygonal()
        self.assertEqual(P.kernel, Q.kernel)
        self.assertEqual(P.kernel[0], self.N.kernel)
        self.assertEqual(P.support, Q.support)
        self.assertEqual(P.support[0], self.N.support)
        self.assertEqual(P.mu(1.0), Q.mu(1.0))
        self.assertEqual(P.mu(1.0), self.N.mu(1.0))
        self.assertEqual(P.mu(7.0), self.N.mu(7.0))

    def test_to_fuzzy_set(self):
        F = fuzz.FuzzySet()
        F.add(1.5, 0.25)
        F.add(6.0, 0.8)
        self.assertEqual(self.X.to_fuzzy_set([1.5, 6.0]), F)

    def test_union(self):
        Z = self.X | self.Y
        for value in [0.5, 1.5, 3.5, 5.0, 6.2, 6.7, 8.3, 10.5]:
            self.assertTrue(abs(Z.mu(value) - max(self.X.mu(value),
                                self.Y.mu(value))) < 10e-1)
        points = [(0.0, 0.0), (3.0, 1.0), (5.5, 1.0), (6.0, 0.5), (6.5, 1.0),
                  (8.0, 1.0), (9.0, 0.0)]
        K = fuzz.RealRange((6.5, 8.0))
        S = fuzz.RealRange((5.5, 9.0))
        P = fuzz.PolygonalFuzzyNumber(points)
        Q = fuzz.TrapezoidalFuzzyNumber(K, S)
        self.assertEqual(self.N | Q, P)

    def test_intersection(self):
        Z = self.X & self.Y
        for value in [1.5, 3.5, 4.5, 5.5, 6.2, 6.7, 8.3, 10.5]:
            self.assertTrue(abs(Z.mu(value) - min(self.X.mu(value),
                                self.Y.mu(value))) < 10e-1)
        points = [(5.5, 0.0), (6.0, 0.5), (6.5, 0.0)]
        K = fuzz.RealRange((6.5, 8.0))
        S = fuzz.RealRange((5.5, 9.0))
        P = fuzz.PolygonalFuzzyNumber(points)
        Q = fuzz.TrapezoidalFuzzyNumber(K, S)
        self.assertEqual(self.N & Q, P)


class TestFuzzyGraph(unittest.TestCase):
    
    def setUp(self):
        v = set([1, 2, 3, 4, 5])
        self.D = fuzz.FuzzyGraph(viter = v, directed = True)
        self.U = fuzz.FuzzyGraph(viter = v, directed = False)
        for G in [self.U, self.D]:
            G.connect(1, 2, 0.8)
            G.connect(2, 3, 1.0)
            G.connect(3, 4, 0.9)
            G.connect(4, 5, 0.7)
            G.connect(3, 5, 0.2)
            G.connect(5, 2, 0.5)
            G.connect(1, 5, 0.0)

    def test_vertices(self):
        exp = set([1, 2, 3, 4, 5])
        act = self.U.vertices()
        self.assertEqual(act, exp)

    def test_mu(self):
        exp = [0.0, 0.7, 0.7, 0.0]
        act = [self.U.mu(1, 3),
               self.U.mu(4, 5),
               self.U.mu(5, 4),
               self.D.mu(5, 4)]
        self.assertEqual(act, exp)
        self.U.add_vertex(6, 0.5)
        self.assertEqual(self.U.mu(6), 0.5)

    def test_weight(self):
        exp = [0.0, 1.0, float('inf'), 1.0 / 0.9, 1.0 / 0.9, float('inf' )]
        act = [self.U.weight(1, 1),
               self.U.weight(2, 3),
               self.U.weight(1, 5),
               self.D.weight(3, 4),
               self.U.weight(4, 3),
               self.D.weight(4, 3)]
        self.assertEqual(act, exp)

    def test_adjacent(self):
        act = True
        act &= self.D.adjacent(1, 2)
        act &= not self.D.adjacent(2, 1)
        act &= self.U.adjacent(1, 2)
        act &= self.U.adjacent(2, 1)
        self.assert_(act)

    def test_connected(self):
        act = True
        act &= self.D.connected(1, 5)
        act &= not self.D.connected(5, 1)
        act &= self.U.connected(1, 5)
        act &= self.U.connected(5, 1)
        self.assert_(act)

    def test_dijkstra_directed(self):
        exp = {1: None, 2: 1, 3: 2, 4: 3, 5: 4}
        act = self.D.dijkstra(1)
        self.assertEqual(act, exp)

    def test_dijkstra_undirected(self):
        exp = {1: None, 2: 1, 3: 2, 4: 3, 5: 2}
        act = self.U.dijkstra(1)
        self.assertEqual(act, exp)

    def test_shortest_path_directed(self):
        ep = [1, 2, 3, 4, 5]
        el = 0.0
        for i in range(len(ep) - 1):
            el += self.D.weight(ep[i], ep[i + 1])
        act = self.D.shortest_path(1, 5)
        self.assertEqual(act, (ep, el))

    def test_shortest_path_undirected(self):
        ep = [1, 2, 5]
        el = 0.0
        for i in range(len(ep) - 1):
            el += self.U.weight(ep[i], ep[i + 1])
        act = self.U.shortest_path(1, 5)
        self.assertEqual(act, (ep, el))

    def test_floyd_warshall_directed(self):
        exp = self.D.shortest_path(1, 5)[1]
        act = self.D.floyd_warshall()[1][5]
        self.assertEqual(act, exp)

    def test_floyd_warshall_undirected(self):
        exp = self.U.shortest_path(1, 5)[1]
        act = self.U.floyd_warshall()[1][5]
        self.assertEqual(act, exp)


if __name__ == '__main__':
    unittest.main()
