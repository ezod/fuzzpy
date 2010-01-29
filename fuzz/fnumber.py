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
    def __new__( cls, arg = ( 0.0, 0.0 ) ):
        """\
        Instatiation method. Verifies the validity of the range argument
        before returning the range object.
        """
        if not len( arg ) == 2 :
            raise ValueError, ( "range must consist of two values" )
        if not isinstance( arg[ 0 ], Number ) \
        or not isinstance( arg[ 1 ], Number ):
            raise TypeError, ( "range values must be numeric" )
        if arg[ 0 ] > arg[ 1 ]:
            raise ValueError, ( "range may not have negative size" )
        return tuple.__new__( cls, arg )

    @property
    def size( self ):
        """\
        Return the size of the range.

        @rtype: C{float}
        """
        return float( self[ 1 ] - self[ 0 ] )

    def __add__( self, other ):
        """\
        Addition operation.
   
        @param other: The other operand.
        @type other: L{RealRange}
        @return: Sum of ranges.
        @rtype: L{RealRange}
        """
        return RealRange( ( self[ 0 ] + other[ 0 ], self[ 1 ] + other[ 1 ] ) )

    def __sub__( self, other ):
        """\
        Subtraction operation.
   
        @param other: The other operand.
        @type other: L{RealRange}
        @return: Difference of ranges.
        @rtype: L{RealRange}
        """
        return RealRange( ( self[ 0 ] - other[ 1 ], self[ 1 ] - other[ 0 ] ) )

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
        if self.__class__ is FuzzyNumber:
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
        if not isinstance( kernel, RealRange ) \
        or not isinstance( support, RealRange ):
            raise TypeError, ( "kernel and support must be RealRange objects" )
        if not kernel <= support:
            raise ValueError, ( "kernel range must be within support range" )
        self.kernel = kernel
        self.support = support
        FuzzyNumber.__init__( self )

    def __repr__( self ):
        """\
        Return string representation of a trapezoidal fuzzy number.

        @return: String representation.
        @rtype: C{string}
        """
        return 'Trapezoidal: kernel %s, support %s' % \
               ( self.kernel.__repr__(), self.support.__repr__() )

    __str__ = __repr__

    @property
    def triangular( self ):
        """\
        Report if this is a triangular fuzzy number (kernel has zero size).

        @rtype: C{bool}
        """
        return self.kernel.size == 0

    @staticmethod
    def _binary_sanity_check( other ):
        """\
        Check that the other argument to a binary operation is also a
        trapezoidal fuzzy number, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{TrapezoidalFuzzyNumber}
        """
        if not isinstance( other, TrapezoidalFuzzyNumber ):
            raise TypeError, \
                ( "binary operation only permitted between trapezoidal fuzzy \
                   numbers" )

    # Binary trapezoidal fuzzy number operations

    def __add__( self, other ):
        """\
        Addition operation.

        @param other: The other trapezoidal fuzzy number.
        @type other: L{TrapezoidalFuzzyNumber}
        @return: Sum of the trapezoidal fuzzy numbers.
        @rtype: L{TrapezoidalFuzzyNumber}
        """
        self._binary_sanity_check( other )
        return self.__class__( self.kernel + other.kernel,
                               self.support + other.support )

    def __sub__( self, other ):
        """\
        Subtraction operation.

        @param other: The other trapezoidal fuzzy number.
        @type other: L{TrapezoidalFuzzyNumber}
        @return: Difference of the trapezoidal fuzzy numbers.
        @rtype: L{TrapezoidalFuzzyNumber}
        """
        self._binary_sanity_check( other )
        return self.__class__( self.kernel - other.kernel,
                               self.support - other.support )

    # Unary trapezoidal fuzzy number operations

    def mu( self, value ):
        """\
        Return the membership level of a value in the universal set domain of
        the fuzzy number.

        @param value: A value in the universal set.
        @type value: C{float}
        """
        if value in self.kernel:
            return 1.
        elif value > self.support[ 0 ] and value < self.kernel[ 0 ]:
            return ( value - self.support[ 0 ] ) / \
                   ( self.kernel[ 0 ] - self.support[ 0 ] )
        elif value < self.support[ 1 ] and value > self.kernel[ 1 ]:
            return ( self.support[ 1 ] - value ) / \
                   ( self.support[ 1 ] - self.kernel[ 1 ] )
        else:
            return 0.

    def alpha( self, alpha ):
        """\
        Alpha cut function. Returns the interval within the fuzzy number whose
        membership levels meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The alpha cut interval.
        @rtype: L{RealRange}
        """
        return RealRange( ( ( self.kernel[ 0 ] - self.support[ 0 ] ) * alpha \
                          + self.support[ 0 ], self.support[ 1 ] - \
                          ( self.support[ 1 ] - self.kernel[ 1 ] ) * alpha ) )
