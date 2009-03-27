"""\
Set module. Contains basic fuzzy set and element class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class FuzzyElement( object ):
    """\
    Fuzzy element class.
    """
    def __init__( self, obj, mu = 0.0 ):
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
        """
        return '%s\%f' % ( self.obj.__repr__(), self.mu )

    __str__ = __repr__


class FuzzySet( set ):
    """\
    Basic fuzzy set class.
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

    def add( self, element ):
        """\
        Add an element to the fuzzy set. Overrides the base class add()
        function to verify that the element is a FuzzyElement.

        @param element: The element to add.
        @type element: L{FuzzySet}
        """
        if isinstance( element, FuzzyElement ):
            self._add( element )
        else:
            raise TypeError, ( "Element to add must be a FuzzyElement" )

    def __contains__( self, element ):
        """\
        Report whether an element is a member of a set.

        @param element: The element to test for.
        @type element: C{object}
        """
        for felement in self:
            if felement.obj == element and felement.mu > 0:
                return True
        return False

    def __or__( self, other ):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        return self.union( other )

    def union( self, other ):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        return NotImplemented

    def __and__( self, other ):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        return self.intersection( other )

    def intersection( self, other ):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        return NotImplemented

    def _binary_sanity_check( self, other ):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        set, raising a TypeError otherwise.
        """
        if not isinstance( other, FuzzySet ):
            raise TypeError, "Binary operation only permitted between fuzzy sets"

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

        @param alpha: The alpha value for the cut.
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

        @param alpha: The alpha value for the cut.
        @type alpha: C{float}
        @return: The crisp set result of the strong alpha cut.
        @rtype: C{set}
        """
        c = set()
        for element in self:
            if element.mu > alpha:
                c.add( element.obj )
        return c
