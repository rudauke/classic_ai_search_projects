"""Tic-Tac-Toe with Minimax and Alpha-Beta pruning."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Algorithm(Enum):
    """Search algorithm type."""
    MINIMAX = "minimax"
    ALPHA_BETA = "alpha_beta"


@dataclass
class GameResult:
    """Result of a game."""
    winner: Optional[str]
    moves: int
    ai_time: float
    states_evaluated: int


class TicTacToe:
    """Tic-Tac-Toe game state."""

    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner: Optional[str] = None
        self.states_evaluated = 0

    def print_board(self) -> None:
        """Print current board state."""
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums() -> None:
        """Print board with position numbers."""
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self) -> List[int]:
        """Return list of available moves."""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self) -> bool:
        """Check if any empty squares remain."""
        return " " in self.board

    def make_move(self, square: int, letter: str) -> bool:
        """Make a move on the board."""
        if self.board[square] == " ":
            self.board[square] = letter
            if self._check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def _check_winner(self, square: int, letter: str) -> bool:
        """Check if move creates a winning line."""
        row_idx = square // 3
        row = self.board[row_idx * 3:(row_idx + 1) * 3]
        if all(spot == letter for spot in row):
            return True

        col_idx = square % 3
        column = [self.board[col_idx + i * 3] for i in range(3)]
        if all(spot == letter for spot in column):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all(spot == letter for spot in diagonal1):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all(spot == letter for spot in diagonal2):
                return True

        return False


class AIPlayer:
    """AI player using Minimax or Alpha-Beta."""

    def __init__(self, letter: str):
        self.letter = letter

    def get_move(self, game: TicTacToe, algorithm: Algorithm, max_depth: int) -> int:
        """Get best move for current position."""
        game.states_evaluated = 0

        if len(game.available_moves()) == 9:
            return 4  # Center is optimal first move

        if algorithm == Algorithm.MINIMAX:
            result = self._minimax(game, self.letter, 0, max_depth)
        else:
            result = self._alpha_beta(game, self.letter, 0, max_depth, -math.inf, math.inf)

        return result["position"]

    def _minimax(
        self,
        state: TicTacToe,
        player: str,
        depth: int,
        max_depth: int
    ) -> dict:
        """Minimax algorithm with depth limit."""
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.current_winner == other_player:
            score = 10 * (max_depth - depth + 1) if other_player == max_player else -10 * (max_depth - depth + 1)
            return {"position": None, "score": score}
        elif not state.empty_squares() or depth == max_depth:
            return {"position": None, "score": 0}

        if player == max_player:
            best = {"position": None, "score": -math.inf}
        else:
            best = {"position": None, "score": math.inf}

        for possible_move in state.available_moves():
            state.states_evaluated += 1
            state.make_move(possible_move, player)

            sim_score = self._minimax(state, other_player, depth + 1, max_depth)

            state.board[possible_move] = " "
            state.current_winner = None

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best["score"] = sim_score["score"]
                    best["position"] = possible_move
            else:
                if sim_score["score"] < best["score"]:
                    best["score"] = sim_score["score"]
                    best["position"] = possible_move

        return best

    def _alpha_beta(
        self,
        state: TicTacToe,
        player: str,
        depth: int,
        max_depth: int,
        alpha: float,
        beta: float
    ) -> dict:
        """Minimax with Alpha-Beta pruning."""
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.current_winner == other_player:
            score = 10 * (max_depth - depth + 1) if other_player == max_player else -10 * (max_depth - depth + 1)
            return {"position": None, "score": score}
        elif not state.empty_squares() or depth == max_depth:
            return {"position": None, "score": 0}

        if player == max_player:
            best = {"position": None, "score": -math.inf}
        else:
            best = {"position": None, "score": math.inf}

        for possible_move in state.available_moves():
            state.states_evaluated += 1
            state.make_move(possible_move, player)

            sim_score = self._alpha_beta(state, other_player, depth + 1, max_depth, alpha, beta)

            state.board[possible_move] = " "
            state.current_winner = None

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best["score"] = sim_score["score"]
                    best["position"] = possible_move
                alpha = max(alpha, best["score"])
            else:
                if sim_score["score"] < best["score"]:
                    best["score"] = sim_score["score"]
                    best["position"] = possible_move
                beta = min(beta, best["score"])

            if beta <= alpha:
                break

        return best


def play_game(algorithm: Algorithm = Algorithm.ALPHA_BETA, max_depth: int = 8) -> GameResult:
    """Play a game against AI."""
    print("Available algorithms: 1. Minimax, 2. Alpha-Beta")
    print(f"Algorithm: {algorithm.value}, Max depth: {max_depth}")
    print("Board positions:")
    TicTacToe.print_board_nums()
    print()

    game = TicTacToe()
    ai = AIPlayer("X")
    human = "O"

    turn = "X"
    ai_total_time = 0.0

    while game.empty_squares():
        if turn == "X":
            print(f"\n--- AI turn ({algorithm.value}, depth {max_depth}) ---")
            start = time.perf_counter()
            move = ai.get_move(game, algorithm, max_depth)
            end = time.perf_counter()
            ai_total_time += end - start
            game.make_move(move, turn)
            print(f"AI chose position {move} in {end - start:.4f}s")
            print(f"States evaluated: {game.states_evaluated}")
        else:
            valid = False
            while not valid:
                try:
                    square = int(input("Your move (0-8): "))
                    if square in game.available_moves():
                        game.make_move(square, turn)
                        valid = True
                    else:
                        print("Invalid move.")
                except ValueError:
                    print("Enter a number 0-8.")

        game.print_board()

        if game.current_winner:
            winner = "AI" if turn == "X" else "Human"
            print(f"\n{winner} wins!")
            return GameResult(
                winner=turn,
                moves=9 - len(game.available_moves()),
                ai_time=ai_total_time,
                states_evaluated=game.states_evaluated
            )

        turn = "O" if turn == "X" else "X"

    print("\nDraw!")
    return GameResult(
        winner=None,
        moves=9,
        ai_time=ai_total_time,
        states_evaluated=game.states_evaluated
    )


def run_benchmark() -> None:
    """Run algorithm comparison benchmark."""
    print("Tic-Tac-Toe Algorithm Benchmark")
    print("=" * 40)

    for algo in [Algorithm.MINIMAX, Algorithm.ALPHA_BETA]:
        for depth in [3, 5, 7, 9]:
            game = TicTacToe()
            ai = AIPlayer("X")

            start = time.perf_counter()
            move = ai.get_move(game, algo, depth)
            duration = time.perf_counter() - start

            print(f"{algo.value:12} depth={depth}  move={move}  "
                  f"states={game.states_evaluated}  time={duration:.6f}s")


if __name__ == "__main__":
    run_benchmark()