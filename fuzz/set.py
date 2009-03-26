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


class FuzzySet( set ):
    """\
    Basic fuzzy set class.
    """
    def __init__( self ):
        """\
        Constructor.
        """
        super( FuzzySet, self ).__init__()

    def add( self, element ):
        """\
        Add an element to the fuzzy set. Overrides the base class add()
        function to verify that the element is a FuzzyElement.

        @param element: The element to add.
        @type element: L{FuzzySet}
        """
        if isinstance( element, FuzzyElement ):
            super( FuzzySet, self ).add( element )
        else:
            raise TypeError, ( "Element must be a FuzzyElement." )

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
