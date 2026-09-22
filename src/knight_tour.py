"""Knight's Tour solver with Warnsdorff heuristic and naive backtracking."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class KnightTourResult:
    """Result of a knight's tour run."""
    success: bool
    board: List[List[int]]
    steps: int
    duration: float
    method: str


class KnightTour:
    """Knight's Tour solver for N x N board."""

    MOVES = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def __init__(self, size: int = 8):
        self.size = size
        self.board: List[List[int]] = []
        self.steps = 0

    def _is_valid(self, x: int, y: int) -> bool:
        """Check if position is within board and unvisited."""
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == -1

    def _count_exits(self, x: int, y: int) -> int:
        """Count valid moves from position (Warnsdorff heuristic)."""
        count = 0
        for dx, dy in self.MOVES:
            if self._is_valid(x + dx, y + dy):
                count += 1
        return count

    def _solve_recursive(self, x: int, y: int, move_num: int, use_heuristic: bool) -> bool:
        """Recursive backtracking solver."""
        self.steps += 1

        if move_num == self.size * self.size:
            return True

        candidates = []
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if self._is_valid(nx, ny):
                candidates.append((nx, ny))

        if use_heuristic:
            candidates.sort(key=lambda c: self._count_exits(c[0], c[1]))

        for nx, ny in candidates:
            self.board[nx][ny] = move_num
            if self._solve_recursive(nx, ny, move_num + 1, use_heuristic):
                return True
            self.board[nx][ny] = -1

        return False

    def solve(self, start_x: int = 0, start_y: int = 0, use_heuristic: bool = False) -> KnightTourResult:
        """Run knight's tour solver."""
        self.steps = 0
        self.board = [[-1] * self.size for _ in range(self.size)]
        self.board[start_x][start_y] = 0

        method = "Warnsdorff" if use_heuristic else "Naive Backtracking"
        start_time = time.perf_counter()

        success = self._solve_recursive(start_x, start_y, 1, use_heuristic)

        duration = time.perf_counter() - start_time

        return KnightTourResult(
            success=success,
            board=self.board,
            steps=self.steps,
            duration=duration,
            method=method
        )

    def print_board(self) -> None:
        """Print board in readable format."""
        for row in self.board:
            print(" ".join(f"{cell:02d}" for cell in row))


def run_demo() -> None:
    """Run demonstration of both methods."""
    print("Knight's Tour Solver")
    print("=" * 40)

    for use_heuristic in [False, True]:
        solver = KnightTour(8)
        result = solver.solve(0, 0, use_heuristic)

        print(f"\n--- {result.method} ---")
        if result.success:
            solver.print_board()
            print(f"Success! Steps: {result.steps}, Time: {result.duration:.4f}s")
        else:
            print("No solution found.")
        print("-" * 40)


if __name__ == "__main__":
    run_demo()