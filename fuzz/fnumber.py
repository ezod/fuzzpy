"""\
Fuzzy number module. Contains basic fuzzy number class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class FuzzyNumber( object ):
    """\
    Fuzzy number class.
    """
    def __init__( self ):
        raise NotImplementedError, ( "please use one of the subclasses" )


class TrapezoidalFuzzyNumber( FuzzyNumber ):
    """\
    Trapezoidal fuzzy number class.
    """
    def __init__( self, kernel, support ):
        """\
        Constructor.

        @param kernel: The kernel of the fuzzy number.
        @type kernel: C{tuple} of C{float}
        @param support: The support of the fuzzy number.
        @type support: C{tuple} of C{float}
        """
        if support[ 0 ] > kernel[ 0 ] or support[ 1 ] < kernel[ 1 ]:
            raise ValueError, ( "kernel range must be within support range" )
        self.kernel = kernel
        self.support = support

    def mu( self, x ):
        """\
        Return the membership degree of a point in the universal set domain of
        the fuzzy number.

        @param x: A point in the universal set.
        @type x: C{float}
        """
        if x >= self.kernel[ 0 ] and x <= self.kernel[ 1 ]:
            return 1.
        elif x > self.support[ 0 ] and x < self.kernel[ 0 ]:
            return ( x - self.support[ 0 ] ) / ( self.kernel[ 0 ] - self.support[ 0 ] )
        elif x < self.support[ 1 ] and x > self.kernel[ 1 ]:
            return ( self.support[ 1 ] - x ) / ( self.support[ 1 ] - self.kernel[ 1 ] )
        else:
            return 0.
