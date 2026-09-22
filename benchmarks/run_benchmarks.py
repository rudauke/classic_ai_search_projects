"""Benchmark runner for classic AI search algorithms."""

from __future__ import annotations

import time
from src.knight_tour import KnightTour, KnightTourResult
from src.sliding_puzzle import SlidingPuzzle, Algorithm, Heuristic
from src.tic_tac_toe import TicTacToe, AIPlayer, Algorithm as TTAlgorithm


def benchmark_knight_tour() -> None:
    """Benchmark Knight's Tour on different board sizes."""
    print("Knight's Tour Benchmark")
    print("=" * 50)

    for size in [5, 6, 7, 8]:
        for heuristic in [False, True]:
            solver = KnightTour(size)
            result: KnightTourResult = solver.solve(0, 0, heuristic)
            method = "Warnsdorff" if heuristic else "Naive"
            status = "OK" if result.success else "FAIL"
            print(f"  {size}x{size} {method:12} {status:4}  steps={result.steps:>10}  time={result.duration:.4f}s")


def benchmark_sliding_puzzle() -> None:
    """Benchmark Sliding Puzzle algorithms."""
    print("\nSliding Puzzle Benchmark (3x3)")
    print("=" * 50)

    configs = [
        (Algorithm.A_STAR, Heuristic.MANHATTAN),
        (Algorithm.A_STAR, Heuristic.HAMMING),
        (Algorithm.IDA_STAR, Heuristic.MANHATTAN),
        (Algorithm.IDA_STAR, Heuristic.HAMMING),
    ]

    for algo, heur in configs:
        times = []
        states = []
        for _ in range(5):
            puzzle = SlidingPuzzle(3, algo, heur, 20)
            result = puzzle.solve()
            if result.success:
                times.append(result.duration)
                states.append(result.states_explored)
        if times:
            avg_time = sum(times) / len(times)
            avg_states = sum(states) / len(states)
            print(f"  {algo.value:6} {heur.value:9}  avg_time={avg_time:.4f}s  avg_states={avg_states:>8.0f}")


def benchmark_tic_tac_toe() -> None:
    """Benchmark Tic-Tac-Toe algorithms."""
    print("\nTic-Tac-Toe Benchmark (empty board, first move)")
    print("=" * 50)

    for algo in [TTAlgorithm.MINIMAX, TTAlgorithm.ALPHA_BETA]:
        for depth in [3, 5, 7, 9]:
            game = TicTacToe()
            ai = AIPlayer("X")

            start = time.perf_counter()
            move = ai.get_move(game, algo, depth)
            duration = time.perf_counter() - start

            print(f"  {algo.value:12} depth={depth}  move={move}  "
                  f"states={game.states_evaluated:>6}  time={duration:.6f}s")


def main() -> None:
    """Run all benchmarks."""
    print("Classic AI Search Algorithms - Benchmarks")
    print("=" * 50)

    benchmark_knight_tour()
    benchmark_sliding_puzzle()
    benchmark_tic_tac_toe()


if __name__ == "__main__":
    main()