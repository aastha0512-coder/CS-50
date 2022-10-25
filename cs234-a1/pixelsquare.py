WHITE = "."

class PixelSquare:
    """
    Fields: colours (listof (listof Str)), dimension (Int)
    Requires: 0 < dimension
              Each string in colours is of length 1

    """

    def __init__(self, dim):
        """
        PixelSquare(dim) produces a PixelSquare object with
            dimension dim and colour white in all entries.
        Effects: Creates a new PixelSquare object.
         __init__: Int -> PixelSquare
        Requires: 0 < dim

        """
        self._colours = []
        self._dimension = dim
        for row in range(dim):
            newrow = [WHITE] * dim
            self._colours.append(newrow)

    def __repr__(self):
        """
        repr(self) produces a string with all colours.
        __repr__: PixelSquare -> Str

        """
        output = ""
        for row in range(self._dimension):
            for col in range(self._dimension):
                output = output + self._colours[row][col]
            output = output + "\n"
        return output


    def size(self):
        """
        self.size() returns the dimension of self.
        size: PixelSquare -> Int

        """
        return self._dimension

    def get_colour(self, i, j):
        """
        self.get_colour(i, j) returns the colour in
            row i and column j.
        get_colour: PixelSquare Int Int -> Str
        Requires: 0 <= i < self._dimension
                  0 <= j < self._dimension

        """
        return self._colours[i][j]

    def set_colour(self, i, j, colour):
        """
        self.set_colour(i, j, item) enters colour in
            row i and column j.
        Effects: Mutates self.
        set_colour: PixelSquare Int Int Str -> None
        Requires: 0 <= i < self._dimension
                  0 <= j < self._dimension
                  colour is of length 1

        """
        self._colours[i][j] = colour

    def rectangle(self, top, left, height, width, colour):
        """
        self.rectangle(top, left, height, width, colour)
            changes the colour to colour for row i and
            column j, for all i and j such that:
            top <= i < top + height, and
            left <= j < left + width.
        Effects: Changes the colour in a rectangle.
        rectangle: Int Int Int Int Str -> None
        Requires: 0 <= top <= top + height < self._dimension
                  0 <= left <= left + width < self._diemsion
                  colour is of length 1

        """
        for row in range(top, top + height):
            for col in range(left, left + width):
                self._colours[row][col] = colour


    def __eq__(self, other):
        """
        self == other produces True if self and other
            have the same colours.
        __eq__: PixelSquare PixelSquare -> Bool

        """
        if self._dimension != other.size():
            return False
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_colour(row, col) != other.get_colour(row, col):
                    return False
        return True



