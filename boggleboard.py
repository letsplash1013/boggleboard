from bogglecube import BoggleCube
from gambler import Shuffler, PredictableShuffler, SixSidedDie, PredictableDie

# The sixteen letter cubes provided with the standard game of Boggle.
CUBE_FACES = [("A", "A", "C", "I", "O", "T"),  # cube 0
              ("T", "Y", "A", "B", "I", "L"),  # cube 1
              ("J", "M", "O", "Qu", "A", "B"), # cube 2
              ("A", "C", "D", "E", "M", "P"),  # cube 3

              ("A", "C", "E", "L", "S", "R"),  # cube 4
              ("A", "D", "E", "N", "V", "Z"),  # cube 5
              ("A", "H", "M", "O", "R", "S"),  # cube 6
              ("B", "F", "I", "O", "R", "X"),  # cube 7

              ("D", "E", "N", "O", "S", "W"),  # cube 8
              ("D", "K", "N", "O", "T", "U"),  # cube 9
              ("E", "E", "F", "H", "I", "Y"),  # cube 10
              ("E", "G", "I", "N", "T", "V"),  # cube 11

              ("E", "G", "K", "L", "U", "Y"),  # cube 12
              ("E", "H", "I", "N", "P", "S"),  # cube 13
              ("E", "L", "P", "S", "T", "U"),  # cube 14
              ("G", "I", "L", "R", "U", "W")]  # cube 15


class BoggleBoard:
    """A BoggleBoard represents a 4x4 grid of BoggleCube objects."""

    def __init__(self, lexicon):
        """Initializes a new BoggleBoard.
        
        Parameters
        ----------
        lexicon : set[str]
            The set of valid Boggle words.
        """
        #create variables for lexicon, cubes in the board, dictionary -- cubes with locations,
        self._lexicon = lexicon
        self._cubes = [BoggleCube(index, CUBE_FACES[index], self) for index in range(len(CUBE_FACES))]
        self._locations = {self._cubes[0] : [0,0],
                                self._cubes[1] : [0,1],
                                self._cubes[2] : [0,2],
                                self._cubes[3] : [0,3],
                                self._cubes[4] : [1,0],
                                self._cubes[5] : [1,1],
                                self._cubes[6] : [1,2],
                                self._cubes[7] : [1,3],
                                self._cubes[8] : [2,0],
                                self._cubes[9] : [2,1],
                                self._cubes[10] : [2,2],
                                self._cubes[11] : [2,3],
                                self._cubes[12] : [3,0],
                                self._cubes[13] : [3,1],
                                self._cubes[14] : [3,2],
                                self._cubes[15] : [3,3],}
        #variables for reporting the selection and doing the process associated for selection
        self._word_so_far = ""
        self._completed_words = []
        self._selected_cubes = []
        
        

    def get_cube(self, row, col):
        """Returns the BoggleCube currently at the specified row and column.
        
        Parameters
        ----------
        row : int
            The desired row (should be between 0 and 3)
        col : int
            The desired column (should be between 0 and 3)
        
        Returns
        -------
        BoggleCube
            the cube currently at the specified row and column.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.get_cube(0, 0).get_letter()
        'A'
        >>> board.get_cube(3, 3).get_letter()
        'G'
        """
        #return appropriate cube from the list of cubes
        return self._cubes[(4 * row) + col]
        
    def shake_cubes(self, shuffler=Shuffler(), die=SixSidedDie()):
        """Shakes the cubes.
        
        First, the cubes should be shuffled by the provided Shuffler.
        Then, each cube should be independently rolled using the provided SixSidedDie.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).get_letter()
        'U'
        >>> board.get_cube(1, 2).get_letter()
        'T'
        """
        #just shuffle and roll
        self._cubes = shuffler.shuffle(self._cubes)
       
        for cube in self._cubes:
            cube.roll(die)
        

    def adjacent(self, cube1, cube2):
        """Determines whether two cubes are adjacent.
        
        Two cubes are adjacent if they are vertically, horizontally, or diagonally adjacent.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.adjacent(board.get_cube(1, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 1), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(0, 1))
        False
        """
        #find the distance between the locations of two cubes
        distance = ((self._locations[cube1][0] - self._locations[cube2][0])**2 + (self._locations[cube1][1] - self._locations[cube2][1])**2)**(1/2)
        #the distance must be greater than zero since a cube can't be adjacent itself
        #the distance can be either 1 or root two for adjacent cubes. It is always higher than root 2 if not adjacent
        if distance < 1.5 and distance > 0:
            return True
        
        return False


    def unselect_all(self):
        """Sets the status of all cubes to 'unselected'.
        
        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).set_status("selected")
        >>> board.get_cube(2, 3).set_status("selected")
        >>> board.unselect_all()
        >>> board.get_cube(0, 0).get_status()
        'unselected'
        >>> board.get_cube(2, 3).get_status()
        'unselected'
        """        
        #iterate and make all the cubes unselected
        for cube in self._cubes:
            cube.set_status("unselected")
        
    def report_selection(self, cube_id):
        """Reports that the cube with the specified id has been selected by the player.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        >>> board = BoggleBoard({'GET', 'PUT', 'APT'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(9)
        >>> board.get_word_so_far()
        'PUT'
        >>> board.report_selection(9)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(11)
        >>> board.get_word_so_far()
        'PU'
        >>> board.report_selection(12)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        """
        #find the current cube
        current_cube = self._cubes[0]
        for cube in self._cubes:
            if cube.get_id() == cube_id:
                current_cube = cube
        # if no cube selected before then select the first letter and make add it the letter to the word
        if self._selected_cubes == []:
            self._selected_cubes = [current_cube]
            current_cube.set_status("most recently selected")
            self._word_so_far = current_cube.get_letter()
        #if pressed twice reset
        elif (self._selected_cubes[-1] == current_cube):
            #add to completed words if the word is in lexicon but not already added
            if (self._word_so_far in self._lexicon) and (self._word_so_far not in self._completed_words):
                self._completed_words += [self._word_so_far]
            self.unselect_all()
            self._selected_cubes = []
            self._word_so_far = ''
        #if unselected and adjacent. Select the cube and add the letter. Set it to most "recently"
        elif current_cube not in self._selected_cubes and self.adjacent(current_cube, self._selected_cubes[-1]):
            self._selected_cubes[-1].set_status("selected")
            current_cube.set_status("most recently selected")
            self._word_so_far += current_cube.get_letter()
            self._selected_cubes = self._selected_cubes + [current_cube]
        

    def get_completed_words(self):
        """Returns the list of completed words.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        """
        #just return the list of words
        return self._completed_words

    def get_word_so_far(self):
        """Returns the word corresponding to the letters selected so far.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        
        """
        #just return the word being made letter by letter
        return self._word_so_far

    def __str__(self):
        """A string representation of the BoggleBoard."""
        row_strs = []
        for row in range(4):
            column = [str(self.get_cube(row, col)) for col in range(4)]
            row_strs.append(' '.join(column))
        return '\n'.join(row_strs)

if __name__ == "__main__":
    from doctest import testmod
    testmod()