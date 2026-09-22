"""Demo CLI for classic AI search algorithms."""

from __future__ import annotations

import argparse
import sys

from src.knight_tour import KnightTour
from src.sliding_puzzle import SlidingPuzzle, Algorithm, Heuristic
from src.tic_tac_toe import play_game, Algorithm as TTAlgorithm


def demo_knight_tour(args: argparse.Namespace) -> None:
    """Run Knight's Tour demo."""
    solver = KnightTour(args.size)
    result = solver.solve(args.start_x, args.start_y, args.heuristic)
    print(f"Method: {result.method}")
    print(f"Success: {result.success}")
    print(f"Steps: {result.steps}")
    print(f"Time: {result.duration:.4f}s")
    if result.success:
        solver.print_board()


def demo_sliding_puzzle(args: argparse.Namespace) -> None:
    """Run Sliding Puzzle demo."""
    algo = Algorithm(args.algorithm)
    heur = Heuristic(args.heuristic)
    puzzle = SlidingPuzzle(args.size, algo, heur, args.shuffle)
    puzzle.solve()


def demo_tic_tac_toe(args: argparse.Namespace) -> None:
    """Run Tic-Tac-Toe demo."""
    algo = TTAlgorithm(args.algorithm)
    play_game(algo, args.depth)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Classic AI Search Algorithms Demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Knight's Tour
    kt_parser = subparsers.add_parser("knight", help="Knight's Tour solver")
    kt_parser.add_argument("--size", type=int, default=8, help="Board size")
    kt_parser.add_argument("--start-x", type=int, default=0, help="Start X position")
    kt_parser.add_argument("--start-y", type=int, default=0, help="Start Y position")
    kt_parser.add_argument("--heuristic", action="store_true", help="Use Warnsdorff heuristic")
    kt_parser.set_defaults(func=demo_knight_tour)

    # Sliding Puzzle
    sp_parser = subparsers.add_parser("puzzle", help="Sliding puzzle solver")
    sp_parser.add_argument("--size", type=int, default=3, help="Puzzle size")
    sp_parser.add_argument("--algorithm", choices=["A*", "IDA*"], default="A*", help="Algorithm")
    sp_parser.add_argument("--heuristic", choices=["Manhattan", "Hamming"], default="Manhattan", help="Heuristic")
    sp_parser.add_argument("--shuffle", type=int, default=20, help="Shuffle moves")
    sp_parser.set_defaults(func=demo_sliding_puzzle)

    # Tic-Tac-Toe
    ttt_parser = subparsers.add_parser("tictactoe", help="Play Tic-Tac-Toe vs AI")
    ttt_parser.add_argument("--algorithm", choices=["minimax", "alpha_beta"], default="alpha_beta", help="Algorithm")
    ttt_parser.add_argument("--depth", type=int, default=8, help="Max search depth")
    ttt_parser.set_defaults(func=demo_tic_tac_toe)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()