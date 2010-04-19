"""\
Discrete fuzzy set module. Contains basic fuzzy set and element class
definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from decimal import Decimal

from iset import IndexedSet


class FuzzyElement(object):
    """\
    Fuzzy element class.
    """
    def __init__(self, obj, mu = 1.0):
        """\
        Constructor.

        @param obj: The object for this member.
        @type obj: C{object}
        @param mu: The membership degree of this member.
        @type mu: C{float}
        """
        self.obj = obj
        self.mu = Decimal(str(mu))

    def __repr__(self):
        """\
        Return string representation of a fuzzy element.

        @return: String representation.
        @rtype: C{string}
        """
        return '%s \ %f' % (str(self.obj), self.mu)

    __str__ = __repr__

    def __hash__(self):
        """\
        Return a hash for the fuzzy element which is the hash of its object.

        @return: The hash.
        @rtype: C{int}
        """
        return hash(self.obj)

    def __eq__(self, other):
        """\
        Equality operator. Note that, because this also checks for equality of
        membership values, fuzzy sets must verify the uniqueness of obj (this
        is handled by setting the index attribute of IndexedSet to 'obj').

        @param other: The other fuzzy element.
        @type other: L{FuzzyElement}
        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance(other, FuzzyElement):
            return False
        return self.obj == other.obj and self.mu == other.mu

    def __ne__(self, other):
        """\
        Inequality operator.

        @param other: The other fuzzy element.
        @type other: L{FuzzyElement}
        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other


class FuzzySet(IndexedSet):
    """\
    Discrete fuzzy set class.
    """
    NORM_STANDARD = 0
    NORM_ALGEBRAIC = 1
    NORM_BOUNDED = 2
    NORM_DRASTIC = 3

    class FuzzySetIterator(object):
        """\
        Discrete fuzzy set iterator class.
        """
        def __init__(self, fuzzyset):
            self.setiterator = set.__iter__(fuzzyset)

        def __iter__(self):
            return self

        def next(self):
            while True:
                element = self.setiterator.next()
                if element.mu > 0:
                    return element

    def __init__(self, iterable = set()):
        """\
        Construct a fuzzy set from an optional iterable.

        @param iterable: The iterable to construct from (optional).
        @type iterable: C{object}
        """
        IndexedSet.__init__(self, 'obj', iterable)

    def __iter__(self):
        """\
        Return an iterator for this fuzzy set.

        @return: Iterator.
        @rtype: L{FuzzySet.FuzzySetIterator}
        """
        return FuzzySet.FuzzySetIterator(self)

    def __len__(self):
        """\
        Override the length function.

        @return: Size of this fuzzy set.
        @rtype: C{int}
        """
        return len([element for element in self])

    def __getitem__(self, key):
        """\
        Return a set item indexed by key (including those with a membership
        degree of zero).

        @param key: The index of the item to get.
        @type key: C{object}
        @return: The matching item.
        @rtype: C{object}
        """
        for item in set.__iter__(self):
            if getattr(item, self.index) == key:
                return item
        raise KeyError, key

    def add(self, element):
        """\
        Add an element to the fuzzy set. Overrides the base class add()
        function to verify that the element is a FuzzyElement.

        @param element: The element to add.
        @type element: L{FuzzySet}
        """
        if not isinstance(element, FuzzyElement):
            raise TypeError, ("element to add must be a FuzzyElement")
        IndexedSet.add(self, element)

    def add_fuzzy(self, element, mu = 1.0):
        """\
        Add a fuzzy element to the fuzzy set (without explicitly constructing
        a FuzzyElement for it). Convenience wrapper for add().

        @param element: The object of the element to add.
        @type element: C{object}
        @param mu: The membership degree of the element.
        @type mu: C{float}
        """
        self.add(FuzzyElement(element, mu))

    def update(self, iterable):
        """\
        Update the fuzzy set contents from an iterable. Overrides the base
        class update() function to verify that the iterable contains only
        FuzzyElement objects.
        
        @param iterable: The iterable to update from.
        @type iterable: C{object}
        """
        for element in iterable:
            if not isinstance(element, FuzzyElement):
                raise TypeError, ("iterable must consist of FuzzyElements")
        IndexedSet.update(self, iterable)

    def keys(self):
        """\
        Return a list of keys in the set (including those with a membership
        degree of zero).

        @return: List of keys in the set.
        @rtype: C{list}
        """
        return [element.obj for element in set.__iter__(self)]

    def mu(self, key):
        """\
        Return the membership degree of the element specified by key. Returns
        zero for any non-member element.

        @return: The membership degree of the specified element.
        @rtype: L{Decimal}
        """
        try:
            return self[key].mu
        except KeyError:
            return Decimal('0.0')

    @property
    def support(self):
        """\
        Support, the crisp set of all elements with non-zero membership in the
        fuzzy set.

        @rtype: C{set}
        """
        return set([element.obj for element in self])

    @property
    def kernel(self):
        """\
        Kernel, the crisp set of all elements with membership degree of exactly
        1.

        @rtype: C{set}
        """
        return self.alpha(1.0)

    @property
    def height(self):
        """\
        Height function. Returns the maximum membership degree of any element
        in the fuzzy set.

        @rtype: L{Decimal}
        """
        return max([element.mu for element in self])

    @property
    def cardinality(self):
        """\
        Scalar cardinality, the sum of membership degrees of all elements.
        
        @rtype: L{Decimal}
        """
        return sum([element.mu for element in self])

    # Binary fuzzy set operations

    def __or__(self, other):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        return self.union(other)

    def __ior__(self, other):
        """\
        In-place fuzzy union.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union (self).
        @rtype: L{FuzzySet}
        """
        self = self.union(other)
        return self

    def union(self, other, norm = 0):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        t-Conorm Types:
        0 - Standard Union
        1 - Algebraic Sum
        2 - Bounded Sum
        3 - Drastic Intersection

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @param norm: The t-conorm type to use.
        @type norm: C{int}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        if not norm in range(4):
            raise ValueError("invalid t-conorm type")
        self._binary_sanity_check(other)
        result = self.__class__()
        bothkeys = set(self.keys()) | set(other.keys())
        [lambda: result.update([FuzzyElement(key, max(self.mu(key), \
            other.mu(key))) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, self.mu(key) + other.mu(key) \
            - self.mu(key) * other.mu(key)) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, min(Decimal('1.0'), \
            self.mu(key) + other.mu(key))) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, (self.mu(key) == \
            Decimal('0.0') and other.mu(key)) or (other.mu(key) == \
            Decimal('0.0') and self.mu(key)) or Decimal('1.0')) \
            for key in bothkeys])
        ][norm]()
        return result

    def __and__(self, other):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        return self.intersection(other)

    def __iand__(self, other):
        """\
        In-place fuzzy intersection.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy intersection (self).
        @rtype: L{FuzzySet}
        """
        self = self.intersection(other)
        return self

    def intersection(self, other, norm = 0):
        """\
        Return the fuzzy intersection of two fuzzy sets as a new fuzzy set.

        t-Norm Types:
        0 - Standard Intersection
        1 - Algebraic Product
        2 - Bounded Difference
        3 - Drastic Intersection

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @param norm: The t-norm type to use.
        @type norm: C{int}
        @return: The fuzzy intersection.
        @rtype: L{FuzzySet}
        """
        if not norm in range(4):
            raise ValueError("invalid t-norm type")
        self._binary_sanity_check(other)
        result = self.__class__()
        [lambda: result.update([FuzzyElement(key, min(self.mu( key ), \
            other.mu(key))) for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, self.mu(key) * \
            other.mu(key)) for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, max(Decimal('0.0'), \
            self.mu(key) + other.mu(key) - Decimal('1.0'))) \
            for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, (self.mu(key) == \
            Decimal('1.0') and other.mu(key)) or (other.mu(key) == \
            Decimal('1.0') and self.mu(key)) or Decimal('0.0')) \
            for key in self.keys()])
        ][norm]()
        return result

    def __eq__(self, other):
        """\
        Compare two fuzzy sets for equality.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check(other)
        if len(self) != len(other):
            return False
        try:
            for element in self:
                if element != other[element.obj]:
                    return False
        except KeyError:
            return False
        return True

    def __ne__(self, other):
        """\
        Compare two fuzzy sets for inequality.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other

    def issubset(self, other):
        """\
        Report whether another fuzzy set contains this fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a subset, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check(other)
        if len(self) > len(other):
            return False
        try:
            for element in self:
                if element.mu > other[element.obj].mu:
                    return False
        except KeyError:
            return False
        return True

    def issuperset(self, other):
        """\
        Report whether this fuzzy set contains another fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a superset, false otherwise.
        @rtype: C{bool}
        """
        self._binary_sanity_check(other)
        if len(self) < len(other):
            return False
        try:
            for element in other:
                if element.mu > self[element.obj].mu:
                    return False
        except KeyError:
            return False
        return True

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        """\
        Report whether another fuzzy set strictly contains this fuzzy set,

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a strict subset, false otherwise.
        @rtype: C{bool}
        """
        return self.issubset(other) and self != other

    def __gt__(self, other):
        """\
        Report whether this fuzzy set strictly contains another fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if a strict superset, false otherwise.
        @rtype: C{bool}
        """
        return self.issuperset(other) and self != other

    def overlap(self, other):
        """\
        Return the degree of overlap of this fuzzy set on another fuzzy set.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The overlap in [0, 1] of this set on the other.
        @rtype: L{Decimal}
        """
        return self.intersection(other).cardinality / other.cardinality

    @staticmethod
    def _binary_sanity_check(other):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        set, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{FuzzySet}
        """
        if not isinstance(other, FuzzySet):
            raise TypeError, \
                ("binary operation only permitted between fuzzy sets")

    # Unary fuzzy set operations

    def complement(self):
        """\
        Return the complement of this fuzzy set.

        @return: The complement of this fuzzy set.
        @rtype: L{FuzzySet}
        """
        result = self.__class__()
        result.update([FuzzyElement(key, Decimal('1.0') - \
                       self.mu(key)) for key in self.keys()])
        return result

    def complement_yager(self, w):
        """\
        Return the Yager complement of this fuzzy set.

        @param w: Yager operator exponent.
        @type w: C{float}
        @return: The Yager complement of this fuzzy set.
        @rtype: L{FuzzySet}
        """
        result = self.__class__()
        result.update([FuzzyElement(key, (Decimal('1.0') - self.mu(key) ** \
                       Decimal(str(w))) ** (Decimal('1.0') / Decimal(str(w)))) \
                       for key in self.keys()])
        return result

    def alpha(self, alpha):
        """\
        Alpha cut function. Returns the crisp set of members whose membership
        degrees meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in (0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the alpha cut.
        @rtype: C{set}
        """
        return set([element.obj for element in self \
                    if element.mu >= Decimal(str(alpha))])

    def salpha(self, alpha):
        """\
        Strong alpha cut function. Returns the crisp set of members whose
        membership degrees exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the strong alpha cut.
        @rtype: C{set}
        """
        return set([element.obj for element in self \
                    if element.mu > Decimal(str(alpha))])

    def prune(self):
        """\
        Prune the fuzzy set of all elements with zero membership.
        """
        prune = [element.obj for element in set.__iter__(self) \
                 if element.mu == 0 ]
        for key in prune:
            self.remove(key)

    def normalize(self):
        """\
        Normalize the fuzzy set by scaling all membership degrees by a factor
        such that the height equals 1.
        """
        #TODO: normalize to values other than 1?
        if self.height > 0:
            scale = Decimal('1.0') / self.height
            for element in self:
                element.mu *= scale

    @property
    def normal(self):
        """\
        Returns whether the fuzzy set is normal (height = 1).

        @rtype: C{bool}
        """
        return self.height == Decimal('1.0')
