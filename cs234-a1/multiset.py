## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
##
##   CS 234 code download
##   Version date: March 2022
##   File name: multiset.py
##
## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
##
from contiguous import *

INFINITY = 100

class Multiset:
    """
    Fields: _data is a Contiguous storing data items of any type
            _first is the integer index of the next place to fill

    """

    def __init__(self):
        """
        Multiset() produces a newly constructed empty multiset.
        Effects: Creates a new empty Multiset.
        __init__: -> Multiset

        """
        self._data = Contiguous(INFINITY)
        self._first = 0

    def __repr__(self):
        """
        repr(self) produces a string of the data stored.
        __repr__: Multiset -> Str

        """
        all_values = str(self._data)
        length = len(all_values)
        delete_pos = []
        for pos in range(length):
            if all_values[pos:pos+4] == "None":
                delete_pos = delete_pos + [pos, pos+1, pos+2, pos+3]
                if pos-1 >= 0 and all_values[pos-1] == ",":
                    delete_pos.append(pos-1)
        new_string = ""
        for pos in range(length):
            if pos not in delete_pos:
                new_string = new_string + all_values[pos]
        return new_string

    def __contains__(self, value):
        """
        value in self produces True if value is an item in self.
        __contains__: Multiset Any -> Bool

        """
        for index in range(self._first):
            if self._data.access(index) == value:
                return True
        return False

    def add(self, value):
        """
        self.add(value) adds value to self.
        Effects: Mutates self by adding value to self.
        add: Multiset Any -> None

        """
        self._data.store(self._first, value)
        self._first = self._first + 1

    def delete(self, value):
        """
        self.delete(value) removes an item with value from self.
        Effects: Mutates self by removing an item with value from self.
        delete: Multiset Any -> None
        Requires: self contains an item with value value

        """
        position = -1
        current = 0
        while position == -1 and current < self._first:
            if self._data.access(current) == value:
                position = current
                to_replace = self._data.access(self._first - 1)
                self._data.store(position, to_replace)
                self._data.store(self._first - 1, None)
                self._first = self._first - 1
            else:
                current = current + 1

