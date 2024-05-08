"""sudoku_engine: Contains the Sudoku class for generating a Sudoku puzzle."""

from ..config.constants import Constants
from ..logs.setup_logging import setup_logging

sudoku_logger = setup_logging()


class Sudoku:
    """
    The Sudoku class for generating a Sudoku puzzle.

    Attributes
    ----------
    grid : list
        The Sudoku grid.

    Methods
    -------
    generate()
        Generates a Sudoku puzzle.

    Examples
    --------
    >>> sudoku = Sudoku()

    Notes
    -----
    The Sudoku puzzle is generated using a backtracking algorithm.
    """

    def __init__(self) -> None:
        """
        Initialises the Sudoku object.

        Notes
        -----
        This method initialises the Sudoku object by creating
        an empty grid.
        """
        self.grid = [[0 for _ in range(Constants.GRID_SIZE)] for _ in range(Constants.GRID_SIZE)]

    def generate(self) -> list[list[int]]:
        """
        Generates a Sudoku puzzle.

        Returns
        -------
        list[list[int]]
            The generated Sudoku puzzle.

        Examples
        --------
        >>> sudoku = Sudoku()
        >>> sudoku.generate()

        Notes
        -----
        This method generates a Sudoku puzzle using a backtracking
        algorithm. The algorithm works by placing a number in an
        empty cell and then checking if the number is valid. If
        the number is valid, the algorithm moves to the next cell
        and repeats the process. If the number is not valid, the
        algorithm backtracks to the previous cell and increments
        the number by 1. The algorithm continues until a valid
        solution is found.
        """
        return self.grid  # TODO: Implement the backtracking algorithm
