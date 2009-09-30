"""\
Unit tests for FuzzPy.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

import unittest

import fuzz
print "FuzzPy imported from '%s'" % fuzz.__path__[ 0 ]


class TestFuzzyGraphShortestPaths( unittest.TestCase ):
    
    def setUp( self ):
        v = [ 1, 2, 3, 4, 5 ]
        self.D = fuzz.FuzzyGraph( viter = v, directed = True )
        self.U = fuzz.FuzzyGraph( viter = v, directed = False )
        for G in [ self.U, self.D ]:
            G.connect( 1, 2, 0.8 )
            G.connect( 2, 3, 1.0 )
            G.connect( 3, 4, 0.9 )
            G.connect( 4, 5, 0.7 )
            G.connect( 3, 5, 0.2 )
            G.connect( 5, 2, 0.5 )

    def test_dijkstra_directed( self ):
        exp = { 1 : None, 2 : 1, 3 : 2, 4 : 3, 5 : 4 }
        act = self.D.dijkstra( 1 )
        self.assertEqual( act, exp )

    def test_dijkstra_undirected( self ):
        exp = { 1 : None, 2 : 1, 3 : 2, 4 : 3, 5 : 2 }
        act = self.U.dijkstra( 1 )
        self.assertEqual( act, exp )

    def test_shortest_path_directed( self ):
        ep = [ 1, 2, 3, 4, 5 ]
        el = 0.
        for i in range( len( ep ) - 1 ):
            el += self.D.weight( ep[ i ], ep[ i + 1 ] )
        act = self.D.shortest_path( 1, 5 )
        self.assertEqual( act, ( ep, el ) )

    def test_shortest_path_undirected( self ):
        ep = [ 1, 2, 5 ]
        el = 0.
        for i in range( len( ep ) - 1 ):
            el += self.U.weight( ep[ i ], ep[ i + 1 ] )
        act = self.U.shortest_path( 1, 5 )
        self.assertEqual( act, ( ep, el ) )

    def test_floyd_warshall_directed( self ):
        exp = self.D.shortest_path( 1, 5 )[ 1 ]
        act = self.D.floyd_warshall()[ 1 ][ 5 ]
        self.assertEqual( act, exp )

    def test_floyd_warshall_undirected( self ):
        exp = self.U.shortest_path( 1, 5 )[ 1 ]
        act = self.U.floyd_warshall()[ 1 ][ 5 ]
        self.assertEqual( act, exp )


if __name__ == '__main__':
    unittest.main()
