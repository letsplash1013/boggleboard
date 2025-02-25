from colorama import Fore
from gambler import SixSidedDie, PredictableDie


class BoggleCube:
    """A BoggleCube represents a single 6-sided letter cube."""

    def __init__(self, cube_id, faces, board=None):
        """Initializes a BoggleCube with the specified id, faces, and board.
        
        Parameters
        ----------
        cube_id : int
            The cube's id (an integer between 0 and 15)
        faces : tuple[str]
            A tuple of six strings, corresponding to the letters on each face
        board : BoggleBoard
            The BoggleBoard to which this cube belongs.        
        """
        #define variables needed for code in protected variables
        self._cube_id = cube_id
        self._faces = faces
        self._board = board
        self._status = "unselected"
        self._top_face = faces[0]

    def get_id(self):
        """Returns this cube's id (an integer between 0 and 15).
        
        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_id()
        8
        """
        #just return Id
        return self._cube_id
    
    def get_faces(self):
        """Returns the letters on the six faces of the cube (as a tuple of strings).
        
        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_faces()
        ('D', 'E', 'N', 'O', 'S', 'W')
        """
        #jurst return the faces
        return self._faces

    def get_letter(self):
        """Returns the letter on the top face of the cube. Upon
        initializiation of a cube, its top face is the 0th index of faces.
                
        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_letter()
        'D'
        >>> cube = BoggleCube(8, ("E", "D", "S", "N", "W", "O"))
        >>> cube.get_letter()
        'E'
        """
        #just return the letter on top
        return self._top_face

    def get_status(self):
        """Returns the current status of the cube.
        
        The status can be one of the following three strings: 
        "unselected", "selected", "most recently selected".
        Upon initialization, all cubes start out as "unselected".

        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_status()
        'unselected'
        """
        #just return current status
        return self._status

    def set_status(self, status):
        """Modifies the current status of the cube.
        
        The status should be one of the following three strings: 
        "unselected", "selected", "most recently selected"
        
        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_status()
        'unselected'
        >>> cube.set_status("most recently selected")
        >>> cube.get_status()
        'most recently selected'
        >>> cube.set_status("selected")
        >>> cube.get_status()
        'selected'
        """
        #set the status to given status
        self._status = status

    def roll(self, die=SixSidedDie()):
        """Rolls the cube.
        
        >>> cube = BoggleCube(8, ("D", "E", "N", "O", "S", "W"))
        >>> cube.get_letter()
        'D'
        >>> cube.roll(die=PredictableDie(4))
        'S'
        >>> cube.get_letter()
        'S'
        """
        #roll the die then return the top face after the die is rolled
        self._top_face = self._faces[die.roll()]
        return self._top_face
    
    def select(self):
        """Informs the cube that it has been selected by the player.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        It should immediately report this information to its BoggleBoard
        using the `report_selection` method of the BoggleBoard class.
        """
        #just report the selection to the board class(according to lab handout)
        self._board.report_selection(self._cube_id)

    def __str__(cube):
        """A string representation of the BoggleCube."""
        colors = {'most recently selected': Fore.GREEN,
                  'selected': Fore.BLUE,
                  'unselected': Fore.WHITE}
        return colors[cube.get_status()] + cube.get_letter()



if __name__ == "__main__":
    from doctest import testmod
    testmod()