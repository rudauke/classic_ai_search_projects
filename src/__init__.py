"""Classic AI Search Algorithms package."""

from .knight_tour import KnightTour, KnightTourResult
from .sliding_puzzle import SlidingPuzzle, Algorithm, Heuristic, PuzzleResult
from .tic_tac_toe import TicTacToe, AIPlayer, Algorithm, GameResult

__all__ = [
    "KnightTour",
    "KnightTourResult",
    "SlidingPuzzle",
    "Algorithm",
    "Heuristic",
    "PuzzleResult",
    "TicTacToe",
    "AIPlayer",
    "GameResult",
]