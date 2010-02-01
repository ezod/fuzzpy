"""\
Discrete fuzzy set module. Contains basic fuzzy set and element class
definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from iset import IndexedSet


class FuzzyElement( object ):
    """\
    Fuzzy element class.
    """
    def __init__( self, obj, mu = 1.0 ):
        """\
        Constructor.

        @param obj: The object for this member.
        @type obj: C{object}
        @param mu: The membership degree of this member.
        @type mu: C{float}
        """
        self.obj = obj
        self.mu = mu

    def __repr__( self ):
        """\
        Return string representation of a fuzzy element.

        @return: String representation.
        @rtype: C{string}
        """
        return '%s \ %f' % ( self.obj.__repr__(), self.mu )

    __str__ = __repr__

    def __hash__( self ):
        """\
        Return a hash for the fuzzy element which is the hash of its object.

        @return: The hash.
        @rtype: C{int}
        """
        return hash( self.obj )


class FuzzySet( IndexedSet ):
    """\
    Discrete fuzzy set class.
    """
    def __init__( self, iterable = set() ):
        """\
        Construct a fuzzy set from an optional iterable.

        @param iterable: The iterable to construct from (optional).
        @type iterable: C{object}
        """
        IndexedSet.__init__( self, 'obj', iterable )

    def add( self, element ):
        """\
        Add an element to the fuzzy set. Overrides the base class add()
        function to verify that the element is a FuzzyElement.

        @param element: The element to add.
        @type element: L{FuzzySet}
        """
        if not isinstance( element, FuzzyElement ):
            raise TypeError, ( "element to add must be a FuzzyElement" )
        IndexedSet.add( self, element )

    def update( self, iterable ):
        """\
        Update the fuzzy set contents from an iterable. Overrides the base
        class update() function to verify that the iterable contains only
        FuzzyElement objects.
        
        @param iterable: The iterable to update from.
        @type iterable: C{object}
        """
        for element in iterable:
            if not isinstance( element, FuzzyElement ):
                raise TypeError, ( "iterable must consist of FuzzyElements" )
        IndexedSet.update( self, iterable )

    @property
    def support( self ):
        """\
        Support, the crisp set of all elements with non-zero membership in the
        fuzzy set.

        @rtype: C{set}
        """
        return self.salpha( 0.0 )

    @property
    def kernel( self ):
        """\
        Kernel, the crisp set of all elements with membership degree of exactly
        1.

        @rtype: C{set}
        """
        return self.alpha( 1.0 )

    @property
    def height( self ):
        """\
        Height function. Returns the maximum membership degree of any element
        in the fuzzy set.

        @rtype: C{float}
        """
        return max( [ element.mu for element in self ] )

    # Binary fuzzy set operations

    def __or__( self, other ):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        return self.union( other )

    def __ior__( self, other ):
        """\
        In-place fuzzy union.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union (self).
        @rtype: L{FuzzySet}
        """
        self = self.union( other )
        return self

    def union( self, other ):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        self._binary_sanity_check( other )
        result = self.__class__()
        for element in self:
            if not element.obj in other \
            or element.mu >= other[ element.obj ].mu:
                result.add( element )
        for element in other:
            if not element.obj in result:
                result.add( element )
        return result

    def __and__( self, other ):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        return self.intersection( other )

    def __iand__( self, other ):
        """\
        In-place fuzzy intersection.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection (self).
        @rtype: L{FuzzySet}
        """
        self = self.intersection( other )
        return self

    def intersection( self, other ):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        self._binary_sanity_check( other )
        result = self.__class__()
        for element in self:
            if element.obj in other:
                if element.mu <= other[ element.obj ].mu:
                    result.add( element )
                else:
                    result.add( other[ element.obj ] )
        return result

    def __eq__( self, other ):
        """\
        Compare two fuzzy sets for equality.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if len( self ) != len( other ):
            return False
        try:
            for element in self:
                if element.mu != other[ element.obj ].mu:
                    return False
        except KeyError:
            return False
        return True

    def __ne__( self, other ):
        """\
        Compare two fuzzy sets for inequality.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other

    def issubset( self, other ):
        """\
        Report whether another fuzzy set contains this fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a subset, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if len( self ) > len( other ):
            return False
        try:
            for element in self:
                if element.mu > other[ element.obj ].mu:
                    return False
        except KeyError:
            return False
        return True

    def issuperset( self, other ):
        """\
        Report whether this fuzzy set contains another fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a superset, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check( other )
        if len( self ) < len( other ):
            return False
        try:
            for element in other:
                if element.mu > self[ element.obj ].mu:
                    return False
        except KeyError:
            return False
        return True

    __le__ = issubset
    __ge__ = issuperset

    def __lt__( self, other ):
        """\
        Report whether another fuzzy set strictly contains this fuzzy set,

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a strict subset, false otherwise.
        @rtype: C{bool}
        """
        return self.issubset( other ) and self != other

    def __gt__( self, other ):
        """\
        Report whether this fuzzy set strictly contains another fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a strict superset, false otherwise.
        @rtype: C{bool}
        """
        return self.issuperset( other ) and self != other

    @staticmethod
    def _binary_sanity_check( other ):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        set, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{FuzzySet}
        """
        if not isinstance( other, FuzzySet ):
            raise TypeError, \
                ( "binary operation only permitted between fuzzy sets" )

    # Unary fuzzy set operations

    def complement( self ):
        """\
        Return the fuzzy complement of this fuzzy set.

        @return: The complement of this fuzzy set.
        @rtype: L{FuzzySet}
        """
        result = self.__class__( self )
        for element in result:
            element.mu = 1.0 - element.mu
        return result

    def alpha( self, alpha ):
        """\
        Alpha cut function. Returns the crisp set of members whose membership
        degrees meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the alpha cut.
        @rtype: C{set}
        """
        cut = set()
        for element in self:
            if element.mu >= alpha:
                cut.add( element.obj )
        return cut

    def salpha( self, alpha ):
        """\
        Strong alpha cut function. Returns the crisp set of members whose
        membership degrees exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the strong alpha cut.
        @rtype: C{set}
        """
        cut = set()
        for element in self:
            if element.mu > alpha:
                cut.add( element.obj )
        return cut

    def prune( self ):
        """\
        Prune the fuzzy set of all elements with zero membership.
        """
        for element in self:
            if element.mu == 0:
                self.remove( element.obj )

    def normalize( self ):
        """\
        Normalize the fuzzy set by scaling all membership degrees by a factor
        such that the height equals 1.
        """
        if self.height > 0:
            scale = 1.0 / self.height
            for element in self:
                element.mu *= scale

    @property
    def normal( self ):
        """\
        Returns whether the fuzzy set is normal (height = 1).

        @rtype: C{bool}
        """
        return self.height == 1.0
