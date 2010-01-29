"""\
Discrete fuzzy set module. Contains basic fuzzy set and element class
definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class FuzzyElement( object ):
    """\
    Fuzzy element class.
    """
    def __init__( self, obj, mu = 1.0 ):
        """\
        Constructor.

        @param obj: The object for this member.
        @type obj: C{object}
        @param mu: The membership level of this member.
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


class FuzzySet( set ):
    """\
    Discrete fuzzy set class.
    """
    def __init__( self, iterable = None ):
        """\
        Construct a fuzzy set from an optional iterable.

        @param iterable: The iterable to construct from (optional).
        @type iterable: C{object}
        """
        if iterable is not None:
            self.update( iterable )

    _add = set.add
    _remove = set.remove
    _update = set.update

    def add( self, element ):
        """\
        Add an element to the fuzzy set. Overrides the base class add()
        function to verify that the element is a FuzzyElement.

        @param element: The element to add.
        @type element: L{FuzzySet}
        """
        if isinstance( element, FuzzyElement ):
            if not element.obj in self.objects:
                self._add( element )
        else:
            raise TypeError, ( "element to add must be a FuzzyElement" )

    def remove( self, key ):
        """\
        Remove an element from the fuzzy set indexed by its associated object.

        @param key: The object to remove.
        @type key: C{object}
        """
        self._remove( self[ key ] )

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
        self._update( iterable )

    def __getitem__( self, key ):
        """\
        Returns a fuzzy element indexed by its associated object.

        @param key: The object.
        @type key: C{object}
        @return: The fuzzy element associated with the object.
        @rtype: L{FuzzyElement}
        """
        for element in self:
            if element.obj == key:
                return element
        raise KeyError, key

    def __contains__( self, obj ):
        """\
        Report whether an object is a member of a set.

        @param obj: The element to test for.
        @type obj: C{object}
        @return: True if member, false otherwise.
        @rtype: C{bool}
        """
        for element in self:
            if element.obj == obj and element.mu > 0:
                return True
        return False

    @property
    def elements( self ):
        """\
        Returns a set of objects of elements with non-zero membership in the
        fuzzy set.

        @rtype: C{set}
        """
        result = set()
        for felement in self:
            if felement.mu > 0:
                result.add( felement.obj )
        return result

    @property
    def objects( self ):
        """\
        Returns a set of all objects in the fuzzy set (even those with zero
        membership).

        @rtype: C{set}
        """
        result = set()
        for felement in self:
            result.add( felement.obj )
        return result

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

    def _binary_sanity_check( self, other ):
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
        levels meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the alpha cut.
        @rtype: C{set}
        """
        c = set()
        for element in self:
            if element.mu >= alpha:
                c.add( element.obj )
        return c

    def salpha( self, alpha ):
        """\
        Strong alpha cut function. Returns the crisp set of members whose
        membership levels exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the strong alpha cut.
        @rtype: C{set}
        """
        c = set()
        for element in self:
            if element.mu > alpha:
                c.add( element.obj )
        return c

    def supp( self ):
        """\
        Support function. Returns the crisp set of all elements with non-zero
        membership in the fuzzy set.

        @return: The support of the fuzzy set.
        @rtype: C{set}
        """
        return self.salpha( 0.0 )

    def core( self ):
        """\
        Core function. Returns the crisp set of all elements with membership
        degree of exactly 1.

        @return: The core of the fuzzy set.
        @rtype: C{set}
        """
        return self.alpha( 1.0 )

    def height( self ):
        """\
        Height function. Returns the maximum membership degree of any element
        in the fuzzy set.

        @return: The height of the fuzzy set.
        @rtype: C{float}
        """
        h = 0
        for element in self:
            if element.mu > h:
                h = element.mu
        return h

    def normalize( self ):
        """\
        Normalize the fuzzy set by scaling all membership degrees by a factor
        such that the height equals 1.
        """
        if self.height() > 0:
            f = 1.0 / self.height()
            for element in self:
                element.mu *= f

    @property
    def normal( self ):
        """\
        Returns whether the fuzzy set is normal (height = 1).

        @rtype: C{bool}
        """
        return self.height() == 1.0
