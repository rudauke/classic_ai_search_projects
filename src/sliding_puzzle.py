"""Sliding puzzle solver with A* and IDA* algorithms."""

from __future__ import annotations

import heapq
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union


class Algorithm(Enum):
    """Search algorithm type."""
    A_STAR = "A*"
    IDA_STAR = "IDA*"


class Heuristic(Enum):
    """Heuristic function type."""
    MANHATTAN = "Manhattan"
    HAMMING = "Hamming"


@dataclass
class PuzzleResult:
    """Result of a puzzle solve attempt."""
    success: bool
    solution: Optional[List[str]]
    states_explored: int
    duration: float
    algorithm: Algorithm
    heuristic: Heuristic
    moves: int


class SlidingPuzzle:
    """N x N sliding puzzle solver."""

    def __init__(
        self,
        size: int = 3,
        algorithm: Algorithm = Algorithm.A_STAR,
        heuristic: Heuristic = Heuristic.MANHATTAN,
        shuffle_moves: int = 20
    ):
        self.size = size
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.shuffle_moves = shuffle_moves
        self.goal = tuple(range(1, size * size)) + (0,)
        self.states_explored = 0

    def _get_neighbors(self, state: Tuple[int, ...]) -> List[Tuple[Tuple[int, ...], str]]:
        """Generate all valid neighbor states."""
        neighbors = []
        zero_pos = state.index(0)
        row, col = divmod(zero_pos, self.size)

        moves = [
            (-1, 0, "DOWN"),
            (1, 0, "UP"),
            (0, -1, "RIGHT"),
            (0, 1, "LEFT")
        ]

        for dr, dc, direction in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                new_pos = nr * self.size + nc
                state_list = list(state)
                state_list[zero_pos], state_list[new_pos] = state_list[new_pos], state_list[zero_pos]
                tile = state_list[zero_pos]
                neighbors.append((tuple(state_list), f"Tile {tile} moves {direction}"))
        return neighbors

    def _calculate_heuristic(self, state: Tuple[int, ...]) -> int:
        """Calculate heuristic value for state."""
        cost = 0
        for i, value in enumerate(state):
            if value == 0:
                continue
            if self.heuristic == Heuristic.HAMMING:
                if value != self.goal[i]:
                    cost += 1
            else:  # MANHATTAN
                goal_pos = value - 1
                curr_row, curr_col = divmod(i, self.size)
                goal_row, goal_col = divmod(goal_pos, self.size)
                cost += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return cost

    def _generate_random_state(self) -> Tuple[int, ...]:
        """Generate solvable random state by reverse shuffling from goal."""
        state = self.goal
        previous = None
        for _ in range(self.shuffle_moves):
            neighbors = [n for n, _ in self._get_neighbors(state) if n != previous]
            if neighbors:
                previous = state
                state = random.choice(neighbors)
        return state

    def _solve_a_star(self, start: Tuple[int, ...]) -> Optional[List[str]]:
        """A* search algorithm."""
        visited = {}
        queue = [(self._calculate_heuristic(start), 0, start, [])]

        while queue:
            f, g, current, path = heapq.heappop(queue)

            if current in visited and visited[current] <= g:
                continue

            visited[current] = g
            self.states_explored += 1

            if current == self.goal:
                return path

            for neighbor, move in self._get_neighbors(current):
                if neighbor not in visited or g + 1 < visited[neighbor]:
                    f_new = g + 1 + self._calculate_heuristic(neighbor)
                    heapq.heappush(queue, (f_new, g + 1, neighbor, path + [move]))
        return None

    def _solve_ida_star(self, start: Tuple[int, ...]) -> Optional[List[str]]:
        """IDA* search algorithm."""

        def search(path: List[Tuple[int, ...]], g: int, threshold: float, moves: List[str]) -> Union[float, str]:
            self.states_explored += 1
            current = path[-1]
            f = g + self._calculate_heuristic(current)

            if f > threshold:
                return f
            if current == self.goal:
                return "FOUND"

            min_threshold = float("inf")
            for neighbor, move in self._get_neighbors(current):
                if neighbor not in path:
                    path.append(neighbor)
                    moves.append(move)

                    result = search(path, g + 1, threshold, moves)

                    if result == "FOUND":
                        return "FOUND"
                    if isinstance(result, int) and result < min_threshold:
                        min_threshold = result

                    moves.pop()
                    path.pop()
            return min_threshold

        threshold = self._calculate_heuristic(start)
        path = [start]
        moves = []

        while True:
            result = search(path, 0, threshold, moves)
            if result == "FOUND":
                return moves
            if result == float("inf"):
                return None
            threshold = float(result)

    def solve(self) -> PuzzleResult:
        """Run the selected solver on a random puzzle."""
        self.states_explored = 0
        start_state = self._generate_random_state()

        print(f"--- Algorithm: {self.algorithm.value} | Heuristic: {self.heuristic.value} ---")
        print("Initial state:")
        self._print_state(start_state)
        print("-" * 30)

        start_time = time.perf_counter()

        if self.algorithm == Algorithm.A_STAR:
            solution = self._solve_a_star(start_state)
        else:
            solution = self._solve_ida_star(start_state)

        duration = time.perf_counter() - start_time

        if solution is not None:
            print("Success!")
            print(f"States explored: {self.states_explored}")
            print(f"Solution length: {len(solution)} moves")
            print(f"Time: {duration:.4f}s")
            print("\nMoves:")
            for i, move in enumerate(solution, 1):
                print(f"  {i}. {move}")
        else:
            print("No solution found.")

        print("-" * 30)

        return PuzzleResult(
            success=solution is not None,
            solution=solution,
            states_explored=self.states_explored,
            duration=duration,
            algorithm=self.algorithm,
            heuristic=self.heuristic,
            moves=len(solution) if solution else 0
        )

    def _print_state(self, state: Tuple[int, ...]) -> None:
        """Print puzzle state as grid."""
        for row in range(self.size):
            values = state[row * self.size:(row + 1) * self.size]
            print("  ".join(f"{v:02d}" for v in values))


def run_demo() -> None:
    """Run demonstration of different algorithm/heuristic combinations."""
    print("Sliding Puzzle Solver")
    print("=" * 40)

    configs = [
        (Algorithm.A_STAR, Heuristic.MANHATTAN, 15),
        (Algorithm.A_STAR, Heuristic.HAMMING, 15),
        (Algorithm.IDA_STAR, Heuristic.MANHATTAN, 15),
        (Algorithm.IDA_STAR, Heuristic.HAMMING, 15),
    ]

    for algo, heur, shuffle in configs:
        puzzle = SlidingPuzzle(3, algo, heur, shuffle)
        puzzle.solve()


if __name__ == "__main__":
    run_demo()