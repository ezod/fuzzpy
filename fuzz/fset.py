"""\
Discrete fuzzy set module. Contains basic fuzzy set and element class
definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from copy import copy

from .iset import IndexedMember, IndexedSet


class FuzzyElement(IndexedMember):
    """\
    Fuzzy element class.
    """
    __slots__ = ['_index', '_mu']

    def __init__(self, index, mu=1.0):
        """\
        Constructor.

        @param index: The object for this member.
        @type index: C{object}
        @param mu: The membership degree of this member.
        @type mu: C{float}
        """
        super(FuzzyElement, self).__init__(index)
        self.mu = mu

    def __repr__(self):
        """\
        Return the canonical representation of a fuzzy element.

        @return: Canonical representation.
        @rtype: C{str}
        """
        return 'FuzzyElement(%s, %f)' % (str(self.index), self.mu)

    def __str__(self):
        """\
        Return the string representation of a fuzzy element.

        @return: String representation.
        @rtype: C{str}
        """
        return '%s \ %f' % (str(self.index), self.mu)

    @property
    def mu(self):
        """\
        The mu value of this fuzzy element.

        @rtype: C{float}
        """
        return self._mu

    @mu.setter
    def mu(self, value):
        """
        Set the mu value of this fuzzy element.

        @param value: The value for mu.
        @type value: C{float}
        """
        if value < 0 or value > 1:
            raise ValueError('mu value must be in [0, 1]')
        self._mu = value


class FuzzySet(IndexedSet):
    """\
    Discrete fuzzy set class.
    """
    NORM_STANDARD = 0
    NORM_ALGEBRAIC = 1
    NORM_BOUNDED = 2
    NORM_DRASTIC = 3

    COMP_STANDARD = 0
    COMP_YAGER = 1

    _itemcls = FuzzyElement

    class FuzzySetIterator(object):
        """\
        Discrete fuzzy set iterator class.
        """
        def __init__(self, fuzzyset):
            self.setiterator = IndexedSet.__iter__(fuzzyset)

        def __iter__(self):
            return self

        def __next__(self):
            while True:
                element = next(self.setiterator)
                if element.mu > 0:
                    return element
        
        next = __next__

    def __init__(self, iterable=set()):
        """\
        Construct a fuzzy set from an optional iterable.

        @param iterable: The iterable to construct from (optional).
        @type iterable: C{object}
        """
        super(FuzzySet, self).__init__(iterable)

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

    def __contains__(self, element):
        """\
        Override the contents function.

        @return: True if in the set, false otherwise.
        @rtype: C{bool}
        """
        return set.__contains__(self, element) and self.mu(element) > 0

    def __getitem__(self, key):
        """\
        Return a set item indexed by key (including those with a membership
        degree of zero).

        @param key: The index of the item to get.
        @type key: C{object}
        @return: The matching item.
        @rtype: C{object}
        """
        for item in IndexedSet.__iter__(self):
            if item.index == key:
                return item
        raise KeyError(key)
    
    def __str__(self):
        """\
        String representation of a fuzzy set.

        @return: String representation.
        @rtype: C{str}
        """
        return ('%s([' % self.__class__.__name__) \
            + ', '.join([str(element) for element in self]) + '])'

    def keys(self):
        """\
        Return a list of keys in the set (including those with a membership
        degree of zero).

        @return: List of keys in the set.
        @rtype: C{list}
        """
        return [element.index for element in IndexedSet.__iter__(self)]

    def mu(self, key):
        """\
        Return the membership degree of the element specified by key. Returns
        zero for any non-member element.

        @return: The membership degree of the specified element.
        @rtype: C{float}
        """
        try:
            return self[key].mu
        except KeyError:
            return 0.0

    @property
    def support(self):
        """\
        Support, the crisp set of all elements with non-zero membership in the
        fuzzy set.

        @rtype: C{set}
        """
        return set([element.index for element in self])

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

        @rtype: C{float}
        """
        return max([element.mu for element in self])

    @property
    def cardinality(self):
        """\
        Scalar cardinality, the sum of membership degrees of all elements.
        
        @rtype: C{float}
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
        return self.efficient_union(other)

    def __ior__(self, other):
        """\
        In-place fuzzy union.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union (self).
        @rtype: L{FuzzySet}
        """
        self = self.efficient_union(other)
        return self

    def union(self, other, norm=0):
        """\
        Return the fuzzy union of two fuzzy sets as a new fuzzy set.

        t-Conorm Types:
        0 - Standard Union
        1 - Algebraic Sum
        2 - Bounded Sum
        3 - Drastic Union

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @param norm: The t-conorm type to use.
        @type norm: C{int}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        if not norm in range(4):
            raise ValueError('invalid t-conorm type')
        self._binary_sanity_check(other)
        result = self.__class__()
        bothkeys = set(self.keys()) | set(other.keys())
        [lambda: result.update([FuzzyElement(key, max(self.mu(key), \
            other.mu(key))) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, self.mu(key) + other.mu(key) \
            - self.mu(key) * other.mu(key)) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, min(1.0, self.mu(key) + \
            other.mu(key))) for key in bothkeys]),
         lambda: result.update([FuzzyElement(key, (self.mu(key) == 0.0 and \
            other.mu(key)) or (other.mu(key) == 0.0 and self.mu(key)) or \
            1.0) for key in bothkeys])
        ][norm]()
        return result

    def efficient_union(self, other):
        """\
        Optimized version of the standard fuzzy union for large fuzzy sets.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: The fuzzy union.
        @rtype: L{FuzzySet}
        """
        self._binary_sanity_check(other)
        result = self.copy()
        keys = result.keys()
        for element in other:
            if element.index in keys:
                result[element.index].mu = max(result[element.index].mu,
                                               element.mu)
            else:
                set.add(result, copy(element))
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

    def intersection(self, other, norm=0):
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
            raise ValueError('invalid t-norm type')
        self._binary_sanity_check(other)
        result = self.__class__()
        [lambda: result.update([FuzzyElement(key, min(self.mu(key), \
            other.mu(key))) for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, self.mu(key) * \
            other.mu(key)) for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, max(0.0, self.mu(key) + \
            other.mu(key) - 1.0)) for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, (self.mu(key) == 1.0 and \
            other.mu(key)) or (other.mu(key) == 1.0 and self.mu(key)) or 0.0) \
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
                if element == other[element.index]:
                    if abs(element.mu - other[element.index].mu) > 1e-10:
                        return False
                else:
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

    def isdisjoint(self, other):
        """\
        Report whether two fuzzy sets have a null intersection.

        @param other: The other fuzzy set.
        @type other: L{FuzzySet}
        @return: True if null intersection.
        @rtype: C{bool}
        """
        for element in self:
            if element in other:
                return False
        return True

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
                if element.mu > other[element.index].mu:
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
                if element.mu > self[element.index].mu:
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
        @rtype: C{float}
        """
        try:
            return self.intersection(other).cardinality / other.cardinality
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def _binary_sanity_check(other):
        """\
        Check that the other argument to a binary operation is also a fuzzy
        set, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{FuzzySet}
        """
        if not isinstance(other, FuzzySet):
            raise TypeError('operation only permitted between fuzzy sets')

    # Unary fuzzy set operations

    def complement(self, comp=0, **kwargs):
        """\
        Return the complement of this fuzzy set.

        @param comp: The complement type (optional).
        @type comp: C{int}
        @return: The complement of this fuzzy set.
        @rtype: L{FuzzySet}
        """
        if not comp in range(2):
            raise ValueError('invalid complement type')
        result = self.__class__()
        [lambda: result.update([FuzzyElement(key, 1 - self.mu(key)) \
            for key in self.keys()]),
         lambda: result.update([FuzzyElement(key, (1 - self.mu(key) \
            ** kwargs['w']) ** (1.0 / kwargs['w'])) for key in self.keys()])
        ][comp]()
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
        return set([element.index for element in self if element.mu >= alpha])

    def salpha(self, alpha):
        """\
        Strong alpha cut function. Returns the crisp set of members whose
        membership degrees exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The crisp set result of the strong alpha cut.
        @rtype: C{set}
        """
        return set([element.index for element in self if element.mu > alpha])

    def prune(self):
        """\
        Prune the fuzzy set of all elements with zero membership.
        """
        prune = [element.index for element in IndexedSet.__iter__(self) \
                 if element.mu == 0]
        for key in prune:
            self.remove(key)

    def normalize(self):
        """\
        Normalize the fuzzy set by scaling all membership degrees by a factor
        such that the height equals 1.
        """
        if self.height > 0:
            scale = 1.0 / self.height
            for element in self:
                element.mu *= scale

    @property
    def normal(self):
        """\
        Returns whether the fuzzy set is normal (height = 1).

        @rtype: C{bool}
        """
        return self.height == 1.0
