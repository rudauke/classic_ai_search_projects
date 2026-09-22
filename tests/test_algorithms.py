"""Tests for classic AI search algorithms."""

from __future__ import annotations

import unittest

from src.knight_tour import KnightTour
from src.sliding_puzzle import SlidingPuzzle, Algorithm, Heuristic
from src.tic_tac_toe import TicTacToe, AIPlayer, Algorithm as TTAlgorithm


class TestKnightTour(unittest.TestCase):
    """Tests for Knight's Tour solver."""

    def test_small_board_naive(self) -> None:
        """Test 5x5 board with naive backtracking."""
        solver = KnightTour(5)
        result = solver.solve(0, 0, use_heuristic=False)
        self.assertTrue(result.success)
        self.assertEqual(result.steps, 25)

    def test_small_board_warnsdorff(self) -> None:
        """Test 5x5 board with Warnsdorff heuristic."""
        solver = KnightTour(5)
        result = solver.solve(0, 0, use_heuristic=True)
        self.assertTrue(result.success)
        self.assertEqual(result.steps, 25)

    def test_warnsdorff_faster_than_naive(self) -> None:
        """Warnsdorff should explore fewer states than naive on 6x6."""
        solver_naive = KnightTour(6)
        result_naive = solver_naive.solve(0, 0, use_heuristic=False)

        solver_warn = KnightTour(6)
        result_warn = solver_warn.solve(0, 0, use_heuristic=True)

        self.assertTrue(result_naive.success)
        self.assertTrue(result_warn.success)
        self.assertLess(result_warn.steps, result_naive.steps)


class TestSlidingPuzzle(unittest.TestCase):
    """Tests for Sliding Puzzle solver."""

    def test_a_star_manhattan(self) -> None:
        """Test A* with Manhattan heuristic."""
        puzzle = SlidingPuzzle(3, Algorithm.A_STAR, Heuristic.MANHATTAN, 10)
        result = puzzle.solve()
        self.assertTrue(result.success)
        self.assertGreater(result.moves, 0)

    def test_a_star_hamming(self) -> None:
        """Test A* with Hamming heuristic."""
        puzzle = SlidingPuzzle(3, Algorithm.A_STAR, Heuristic.HAMMING, 10)
        result = puzzle.solve()
        self.assertTrue(result.success)

    def test_ida_star_manhattan(self) -> None:
        """Test IDA* with Manhattan heuristic."""
        puzzle = SlidingPuzzle(3, Algorithm.IDA_STAR, Heuristic.MANHATTAN, 10)
        result = puzzle.solve()
        self.assertTrue(result.success)

    def test_manhattan_better_than_hamming(self) -> None:
        """Manhattan should explore fewer states than Hamming on average."""
        manhattan_states = []
        hamming_states = []

        for _ in range(3):
            p1 = SlidingPuzzle(3, Algorithm.A_STAR, Heuristic.MANHATTAN, 15)
            r1 = p1.solve()
            if r1.success:
                manhattan_states.append(r1.states_explored)

            p2 = SlidingPuzzle(3, Algorithm.A_STAR, Heuristic.HAMMING, 15)
            r2 = p2.solve()
            if r2.success:
                hamming_states.append(r2.states_explored)

        if manhattan_states and hamming_states:
            self.assertLess(sum(manhattan_states) / len(manhattan_states),
                          sum(hamming_states) / len(hamming_states))


class TestTicTacToe(unittest.TestCase):
    """Tests for Tic-Tac-Toe AI."""

    def test_ai_first_move_center(self) -> None:
        """AI should pick center on empty board."""
        game = TicTacToe()
        ai = AIPlayer("X")
        move = ai.get_move(game, TTAlgorithm.ALPHA_BETA, 8)
        self.assertEqual(move, 4)

    def test_ai_blocks_win(self) -> None:
        """AI should block opponent's winning move."""
        game = TicTacToe()
        # Human plays X at 0, AI plays O at 4
        game.make_move(0, "X")
        game.make_move(4, "O")
        # Human plays X at 1, AI must block at 2
        game.make_move(1, "X")

        ai = AIPlayer("O")
        move = ai.get_move(game, TTAlgorithm.ALPHA_BETA, 8)
        self.assertEqual(move, 2)

    def test_alpha_beta_fewer_states_than_minimax(self) -> None:
        """Alpha-Beta should evaluate fewer states than Minimax."""
        game = TicTacToe()
        ai = AIPlayer("X")

        ai.get_move(game, TTAlgorithm.MINIMAX, 9)
        minimax_states = game.states_evaluated

        game2 = TicTacToe()
        ai2 = AIPlayer("X")
        ai2.get_move(game2, TTAlgorithm.ALPHA_BETA, 9)
        ab_states = game2.states_evaluated

        self.assertLess(ab_states, minimax_states)


if __name__ == "__main__":
    unittest.main()