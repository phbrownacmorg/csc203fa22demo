import random
from typing import Generic, Optional, MutableMapping, TypeVar
from pythonds3.basic import Stack
#from typing import Generic, TypeVar

#KT = TypeVar('KT') # Key type.  Must be hashable and comparable.
#VT = TypeVar('VT') # Value type.  Can be anything.

class Skiplist(MutableMapping):
    """Class to represent a skiplist."""

    P_INV: int = 2  # 1/P

    class Node:
        """Internal class to represent a skiplist node."""
        def __init__(self):
            self._next = None
            self._down = None

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, value):
            self._next = value

        @property
        def down(self):
            return self._down

        @down.setter
        def down(self, value):
            self._down = value

        def addLevel(self, prior) -> 'Skiplist.Node':
            newnode = Skiplist.Node()
            newnode.down = self
            if prior is not None:
                newnode.next = prior.next
                prior.next = newnode
            return newnode


    class DataNode(Node):
        """Internal class to represent a skiplist data node.  Adds data storage
        (a key and value) to Node."""

        def __init__(self, key, value):
            super().__init__()
            self._key = key
            self._data = value

        @property
        def key(self):
            return self._key

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, value):
            self._data = value

        def addLevel(self, prior) -> 'Skiplist.DataNode':
            # Pre:
            assert prior is not None
            newnode = Skiplist.DataNode(self.key, self.data)
            newnode.down = self
            newnode.next = prior.next
            prior.next = newnode
            return newnode


    def __init__(self):
        """Create an empty skiplist."""
        self._head = None

    def insert(self, key, value):
        """Insert a new (key, value) pair into the skiplist."""
        # Adding to an empty list
        if self._head is None: 
            self._head = Skiplist.Node()
            top = Skiplist.DataNode(key, value)
            self._head.next = top
            # Add levels to that first node
            while random.randrange(Skiplist.P_INV) == 0:
                self._head = self._head.addLevel(None)
                top = top.addLevel(self._head)
        # Adding to a populated list.  Find the insertion point, saving the sequence
        #  of previous nodes
        else:
            tower = Stack()
            current = self._head
            while current:
                if (current.next is None) or (current.next.key > key):
                    tower.push(current)
                    current = current.down
                else:
                    current = current.next

            lowest_level = tower.pop()
            top = Skiplist.DataNode(key, value)
            top.next = lowest_level.next
            lowest_level.next = top
            while random.randrange(Skiplist.P_INV) == 0:
                if tower.is_empty(): # Add a whole new level to the skiplist
                    self._head = self._head.addLevel(None)
                    top = top.addLevel(self._head)
                else:
                    next_level = tower.pop()
                    top = top.addLevel(next_level)

    def __setitem__(self, key, value):
        """Allows insertion into the skiplist using the syntax
        self[key] = value."""
        self.insert(key, value)

    def search(self, key):
        """Searches for an item with key KEY in the list,
        and return its value.  If nothing in the list has
        key KEY, raise KeyError."""
        current = self._head # current node
        result = None # Return value
        while current:
            if (current.next is None) or (current.next.key > key):
                current = current.down # Next level down
            elif (current.next.key < key):
                current = current.next # Move along the current level
            else: # current.next.key == key
                result = current.next.data
                current = None # To exit the loop
        if result is None:
            raise KeyError('Key {0} is not in skiplist'.format(key)) 
        return result

    def __getitem__(self, key):
        """Allows searching the skiplist using the syntax
        self[key]."""
        return self.search(key)

    def delete(self, key):
        """Deletes the item with key KEY from the skiplist.
        If no such item exists, raise KeyError."""
        pass # For HW5, replace with real code

    def __delitem__(self, key):
        """Allows deletion from the skiplist using
        square-bracket notation."""
        self.delete(key)

    def __iter__(self):
        """Iterator over a Skiplist, using a generator."""
        current = self._head
        if self._head is not None:
            # Go to the bottom level, which has all the values
            while current.down is not None:
                current = current.down

            # Go along the bottom level, yielding the key each time.
            while current.next is not None:
                current = current.next
                yield current.key
                
    def __len__(self):
        """Return the length of the Skiplist."""
        return len(list(iter(self)))