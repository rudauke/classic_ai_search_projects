# Classic AI Search

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/OWNER/REPO/blob/main/classic-ai-search/examples/demo.py)

Clean implementations of fundamental AI search algorithms: Knight's Tour (Warnsdorff's heuristic), Sliding Puzzle (A*, IDA*), and Tic-Tac-Toe (Minimax, Alpha-Beta pruning). No external dependencies — pure Python.

## The Problem

Educational implementations of classic search algorithms with:
- Readable, well-documented code
- Benchmarks comparing heuristics and algorithms
- Unified CLI for all three problems
- Zero dependencies (stdlib only)

## Quick Start

```bash
cd classic-ai-search
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m examples.demo --help
```

## Usage

```bash
# Knight's Tour on 8x8 with Warnsdorff heuristic
python -m examples.demo knight --size 8 --heuristic

# Sliding puzzle with A* and Manhattan heuristic
python -m examples.demo puzzle --algorithm A* --heuristic Manhattan

# Tic-Tac-Toe vs Alpha-Beta AI
python -m examples.demo tictactoe --algorithm alpha_beta --depth 8

# Run all benchmarks
python -m benchmarks.run_benchmarks
```

## Algorithms

| Problem | Algorithm | Heuristic | Complexity |
|---------|-----------|-----------|------------|
| Knight's Tour | Warnsdorff's Rule | Degree heuristic | O(N²) |
| Sliding Puzzle | A* | Manhattan / Misplaced tiles | O(b^d) |
| Sliding Puzzle | IDA* | Manhattan | O(b^d) memory: O(d) |
| Tic-Tac-Toe | Minimax | None (exact) | O(b^d) |
| Tic-Tac-Toe | Alpha-Beta | None (exact) | O(b^(d/2)) |

## Benchmarks

Run `python -m benchmarks.run_benchmarks` for full results. Typical output:

```
=== Knight's Tour (8x8) ===
Warnsdorff:        0.002s  (100% success)
Backtracking:      45.2s   (timeout)

=== Sliding Puzzle (3x3) ===
A* Manhattan:      0.001s  (optimal)
A* Misplaced:      0.003s  (optimal)
IDA* Manhattan:    0.005s  (optimal)

=== Tic-Tac-Toe ===
Minimax:           0.0001s (perfect play)
Alpha-Beta:        0.00005s (perfect play, 2x faster)
```

## Project Structure

```
classic-ai-search/
├── src/
│   ├── knight_tour.py      # Warnsdorff + backtracking
│   ├── sliding_puzzle.py   # A*, IDA*, heuristics
│   └── tic_tac_toe.py      # Minimax, Alpha-Beta
├── examples/
│   └── demo.py             # Unified CLI
├── benchmarks/
│   └── run_benchmarks.py   # Performance comparisons
├── tests/
│   └── test_algorithms.py  # Unit tests
├── pyproject.toml
└── README.md
```

## Design Decisions

- **No numpy, no torch, no deps** — runs anywhere Python runs
- **Generators for move iteration** — memory efficient
- **Dataclasses for state** — clean, typed, immutable
- **Heuristics as callables** — swap Manhattan ↔ Misplaced easily
- **Iterative deepening for IDA*** — avoids recursion limits

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

## License

MIT