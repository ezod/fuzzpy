"""\
Indexed set module. Contains the indexed set class, a set that is indexed like
a dict.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from copy import copy


class IndexedMember(object):
    """\
    Indexed member class. This is a special type of object which has mutable
    properties but a special immutable property (called the index) which is
    used for hashing and equality, allowing it to be stored in a set or to be
    used as a dict key.
    """
    def __init__(self, index):
        """\
        Constructor.

        @param index: The index object (immutable).
        @type index: C{object}
        """
        if not hasattr(type(index), '__hash__') \
        or not hasattr(type(index), '__eq__'):
            raise TypeError('index object must be immutable')
        self._index = index

    @property
    def index(self):
        """\
        Return the index object.

        @rtype: C{object}
        """
        return self._index

    def __repr__(self):
        """\
        Return the canonical string representation of the index.

        @return: Canonical string representation.
        @rtype: C{str}
        """
        return repr(self.index)

    def __str__(self):
        """\
        Return the string representation of the index.

        @return: String representation.
        @rtype: C{str}
        """
        return str(self.index)

    def __hash__(self):
        """\
        Return a hash of the index object.

        @return: The index hash.
        @rtype: C{int}
        """
        return hash(self.index)

    def __eq__(self, other):
        """\
        Return whether the index objects match.

        @return: True if equal, false otherwise.
        @rtype: C{bool}
        """
        return self.index == other.index if isinstance(other, IndexedMember) \
            else self.index == other

    def __ne__(self, other):
        """\
        Return whether the index objects do not match.

        @return: True if not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other


class IndexedSet(set):
    """\
    Indexed set class. This is a special type of set whose members are mutable
    objects with an immutable attribute. These overall-mutable members can then
    be accessed in dict style, using the index as key.
    """
    _itemcls = IndexedMember

    def __init__(self, iterable=set()):
        """\
        Constructor.

        @param iterable: The iterable to intialize the set with.
        @type iterable: C{iterable}
        """
        super(IndexedSet, self).__init__()
        for item in iterable:
            self.add(item)

    def __getitem__(self, key):
        """\
        Return a set item indexed by key.

        @param key: The index of the item to get.
        @type key: C{object}
        @return: The matching item.
        @rtype: C{object}
        """
        for item in self:
            if item.index == key:
                return item
        raise KeyError(key)

    def __setitem__(self, key, item):
        """\
        Assign an item by key. Normally, new items are added via add() and
        existing items modified via object reference; this is included for
        completeness.

        @param key: The index of the item to assign.
        @type key: C{object}
        @param item: The item to assign.
        @type item: C{object}
        """
        if not item.index == key:
            raise ValueError('key does not match item index attribute')
        if key in self:
            self.remove(key)
        set.add(self, item)

    def add(self, item, *args, **kwargs):
        """\
        Add an item to the set. Uses a copy since IndexedMembers have mutable
        properties.

        @param item: The item to add.
        @type item: L{IndexedMember}
        """
        if not isinstance(item, self._itemcls):
            item = self._itemcls(item, *args, **kwargs)
        set.add(self, copy(item))

    def update(self, *args):
        """\
        Update the set with the union of itself and other iterables.
        """
        for arg in args:
            for item in arg:
                self.add(item)

    def intersection_update(self, *args):
        """\
        Update the set with the intersection of itself and other iterables.
        """
        common = set()
        common.update(args)
        for item in self.keys():
            if item not in common:
                self.remove(item)

    def difference(self, *args):
        """\
        Return the difference of the set with other iterables.
        """
        result = self.copy()
        result.difference_update(*args)
        return result

    def difference_update(self, *args):
        """\
        Update the set with the difference of itself and other iterables.
        """
        common = set()
        common.update(args)
        for item in common:
            self.discard(item)

    def symmetric_difference(self, *args):
        """\
        Return the symmetric difference of the set with other iterables.
        """
        result = self.copy()
        result.symmetric_difference_update(*args)
        return result

    def symmetric_difference_update(self, *args):
        """\
        Update the set with the symmetric difference of itself and other
        iterables.
        """
        common = set()
        common.update(args)
        for item in common:
            try:
                self.remove(item)
            except KeyError:
                self.add(item)

    def copy(self):
        """\
        Return a copy of the set with shallow copies of all members.
        """
        return self.__class__(self)

    def keys(self):
        """\
        Return a list of keys in the set.

        @return: List of keys in the set.
        @rtype: C{list}
        """
        return [item.index for item in self]

    def has_key(self, key):
        """\
        Return whether this set contains an item with a given index.

        @param key: The index to test for.
        @type key: C{object}
        @return: True if a matching key exists, false otherwise.
        @rtype: C{bool}
        """
        return key in self.keys()
