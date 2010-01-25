"""\
Fuzzy number module. Contains basic fuzzy number class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from numbers import Number


class RealRange( tuple ):
    """\
    Real range class.
    """
    def __init__( self, arg ):
        """\
        Constructor. Initializes like a tuple, but must have exactly two
        numeric values, the first being less than or equal to the second.

        @param arg: Initialization argument.
        @type arg: C{object}
        """
        if not len( arg ) == 2 :
            raise ValueError, ( "range must consist of two values" )
        if not isinstance( arg[ 0 ], Number ) \
        or not isinstance( arg[ 1 ], Number ):
            raise TypeError, ( "range values must be numeric" )
        if arg[ 0 ] > arg[ 1 ]:
            raise ValueError, ( "range may not have negative size" )

    @property
    def size( self ):
        """\
        Return the size of the range.

        @return: The size of the range.
        @rtype: C{float}
        """
        return float( self[ 1 ] - self[ 0 ] )

    def __contains__( self, value ):
        """\
        Report whether a given value is within this range.

        @param value: The value.
        @type value: C{float}
        @return: True if within the range, false otherwise.
        @rtype: C{bool}
        """
        return value >= self[ 0 ] and value <= self[ 1 ]

    def issubset( self, other ):
        """\
        Report whether another range contains this range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a subset, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance( other, RealRange ):
            raise TypeError, ( "argument must be a RealRange" )
        if other[ 0 ] <= self[ 0 ] and other[ 1 ] >= self[ 1 ]:
            return True
        return False

    def issuperset( self, other ):
        """\
        Report whether this range contains another range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a superset, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance( other, RealRange ):
            raise TypeError, ( "argument must be a RealRange" )
        if self[ 0 ] <= other[ 0 ] and self[ 1 ] >= other[ 1 ]:
            return True
        return False

    __le__ = issubset
    __ge__ = issuperset

    def __lt__( self, other ):
        """\
        Report whether another range strictly contains this range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a strict subset, false otherwise.
        @rtype: C{bool}
        """
        return self.issubset( other ) and not self == other

    def __gt__( self, other ):
        """\
        Report whether this range strictly contains another range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a strict superset, false otherwise.
        @rtype: C{bool}
        """
        return self.issuperset( other ) and not self == other


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
        @type kernel: L{RealRange}
        @param support: The support of the fuzzy number.
        @type support: L{RealRange}
        """
        if not kernel <= support:
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
        if x in kernel:
            return 1.
        elif x > self.support[ 0 ] and x < self.kernel[ 0 ]:
            return ( x - self.support[ 0 ] ) / ( self.kernel[ 0 ] - self.support[ 0 ] )
        elif x < self.support[ 1 ] and x > self.kernel[ 1 ]:
            return ( self.support[ 1 ] - x ) / ( self.support[ 1 ] - self.kernel[ 1 ] )
        else:
            return 0.
