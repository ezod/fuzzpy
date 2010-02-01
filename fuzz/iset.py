"""\
Indexed set module. Contains the indexed set class, a set that is indexed like
a dict.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class IndexedSet( set ):
    """\
    Indexed set class.
    """
    def __init__( self, index, iterable = set() ):
        """\
        Constructor.

        @param index: The attribute by which to index items.
        @type index: C{str}
        @param iterable
        """
        self.index = str( index )
        set.__init__( self, iterable )

    def __getitem__( self, key ):
        """\
        Return a set item indexed by key.

        @param key: The index of the item to get.
        @type key: C{object}
        @return: The matching item.
        @rtype: C{object}
        """
        for item in self:
            if getattr( item, self.index ) == key:
                return item
        raise KeyError, key

    def __setitem__( self, key, item ):
        """\
        Assign an item by key. Normally, new items are added via add() and
        existing items modified via object reference; this is included for
        completeness.

        @param key: The index of the item to assign.
        @type key: C{object}
        @param item: The item to assign.
        @type item: C{object}
        """
        if not getattr( item, self.index ) == key:
            raise ValueError, ( "key does not match item index attribute" )
        if key in self:
            self.remove( key )
        set.add( self, item )

    def __contains__( self, key ):
        """\
        Return whether an item is a member of the set, by key or by object.

        @param key: The index or object to test for.
        @type key: C{object}
        @return: True if member, false otherwise.
        @rtype: C{bool}
        """
        for item in self:
            if getattr( item, self.index ) == key:
                return True
        return set.__contains__( self, key )

    def add( self, item ):
        """\
        Add an item to the set, verifying that it has the required index
        attribute and that no other item in the set has the same index.

        @param item: The item to add.
        @type item: C{object}
        """
        if not getattr( item, self.index ) in self.keys():
            set.add( self, item )

    def remove( self, key ):
        """\
        Remove an item from the set by key or by object.

        @param key: The index or object to remove.
        @type key: C{object}
        """
        try:
            set.remove( self, self[ key ] )
        except KeyError:
            set.remove( self, key )

    def keys( self ):
        """\
        Return a list of keys in the set.

        @return: List of keys in the set.
        @rtype: C{list}
        """
        return [ getattr( item, self.index ) for item in self ]

    def has_key( self, key ):
        """\
        Return whether this set contains an item with a given index.

        @param key: The index to test for.
        @type key: C{object}
        @return: True if a matching key exists, false otherwise.
        @rtype: C{bool}
        """
        return key in self.keys()
