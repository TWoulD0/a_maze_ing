*This project has been created as part of the 42 curriculum by aessabri, watoumi.*


## Description

**A-Maze-ing** is a Python maze generator that creates valid, fully connected mazes based on a configuration file.


The Program:
- Parses a configuration file (`config.txt`)
- Generates a random maze (perfect or non-perfect)
- Ensures structural validity and coherence
- Encodes the maze using a hexadecimal wall representation
- Computes the shortest path from entry to exit
- Writes everyting to an output file
- Provides a visual representation (terminal rendering)


The maze generation logic is implemented as a reusable module that can later be installed as a Python package.


### Projects Goals

- Implement a configurable maze generator
- Guarantee structural validity and connectivity
- Support reproducibility via seed
- Provide shortest path computation
- Include a visible "42" pattern inside the maze
- Ensure clean architecture and reusable code

---

## Instructions

# Requirements
- Python 3.10+
- pip (to build the reusable package)

# Run the Program
make run
- Executes :
python3 a_maze_ing.py config.txt

# Install Dependencies
make install

Installs development tools:

* flake8 (code style checker)
* mypy (static type checker)

# Debug Mode
make debug
* Runs the program using Python’s built-in debugger (pdb) to help trace and debug execution step by step.

# Clean Cache Files
make clean
Removes:
* __pycache__ directories
* .mypy_cache directories
* Compiled .pyc files
- Useful before submission or to reset the project state.

# Code Quality Checks
Standars Linting
make lint
Runs:
* flake8 for style checks
* mypy with strict return and typing warnings

# Strict Type Checking
make lint-strict
Runs:
* flake8
* mypy --strict for full strict typing enforcement

# Build the Package
make build
- Generates "mazegen-1.0.0.tar.gz" at the project root.

## Configuration File Format
- The file must contain one KEY=VALUE per line.
- Lines staring with # are ignored

| Key | Description | Required |
|---|---|---|
| `WIDTH`       | Maze width in cells (positive integer)        | yes |
| `HEIGHT`      | Maze height in cells (positive integer)       | yes |
| `ENTRY`       | Entry coordinates as `x,y` (0-indexed)        | yes |
| `EXIT`        | Exit coordinates as `x,y` (0-indexed)         | yes |
| `OUTPUT_FILE` | Output filename (must end with `.txt`)        | yes |
| `PERFECT`     | Whether the maze is perfect (`true`/`false`)  | yes |
| `ALGORITHM`   | Generation algorithm (`dfs` or `prim`)        | yes |
| `SEED`        | Integer seed for reproducibility              | optional |

**Rules:**
- Keys and values are case-insensitive where applicable
- Duplicate keys are not allowed
- `ENTRY` and `EXIT` must be different and within maze bounds
- `WIDTH * HEIGHT` must not exceed 40,000
- `OUTPUT_FILE` must end with `.txt`

**Example `config.txt`:**
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=false
SEED=42

# algorithm can be dfs or prim
ALGORITHM=prim
```



## Maze Generation Algorithms

### Algorithms Implemented

**DFS — Recursive Backtracker**
Starts from the entry cell and explores neighbors randomly, backtracking when stuck. Produces long winding corridors with relatively few dead ends.

**Prim's Algorithm**
Grows the maze by randomly selecting from a frontier of reachable unvisited cells. Produces mazes with many short branches distributed uniformly across the grid.

### Why We Chose These Algorithms

We implemented both algorithms to offer a meaningful bonus and to contrast their visual outputs.

**DFS** was our primary choice because it is the most classical maze generation approach and produces a strikingly different corridor style. Offering both algorithms lets users directly compare them by changing a single config key.

**Prim's** was added because it produces a more visually balanced maze — branches are distributed across the whole grid rather than clustered near the start, making the result more challenging to solve and more interesting to look at.

Both algorithms are adapted to work around the pre-placed **"42" pattern** cells, which are fully closed before generation begins and are never touched by wall removal.



## Reusable Module — `mazegen`

The maze generation logic is fully encapsulated in the `mazegen` Python package located in the `mazegen/` directory. It can be installed independently via pip and imported into any project.

### What Is Reusable

| Component | File | Description |
|---|---|---|
| `MazeGenerator` | `generator.py` | Main class — generates mazes with DFS or Prim |
| `Maze` | `maze.py` | Data structure holding walls and the 42 pattern |
| `shortest_path` | `solver.py` | BFS solver returning the shortest path as a list of cells |
| `apply_42_pattern` | `pattern.py` | Stamps the "42" pattern into the maze before generation |

### Installation
```bash
# Install from the prebuilt package at the project root
pip install mazegen-1.0.0.tar.gz

# Or rebuild from source and install
pip install build
python3 -m build
pip install dist/mazegen-1.0.0.tar.gz
```

### Basic Usage Example
```python
from mazegen import MazeGenerator, shortest_path

# Instantiate the generator
generator = MazeGenerator(
    width=20,
    height=15,
    seed=42,
    algorithm="prim",   # or "dfs"
    perfect=True,
    entry=(0, 0),
    _exit=(19, 14)
)

# Generate the maze
maze = generator.generate()

# Access the wall structure
# maze.walls[y][x] → [North, East, South, West] as booleans
# True = wall present (closed), False = passage (open)
print(maze.walls[0][0])  # e.g. [True, False, True, True]

# Replay generation step by step (for animation)
steps = generator.get_steps()  # list of (x, y, direction_index) tuples

# Find the shortest path from entry to exit
path = shortest_path(maze, entry=(0, 0), _exit=(19, 14))
# Returns a list of (x, y) tuples, or None if no path exists
if path:
    print(f"Path length: {len(path)} steps")
```


### Direction Reference

| Index | Direction | (dy, dx) offset |
|---|---|---|
| 0 | North | (-1, 0) |
| 1 | East  | (0, +1) |
| 2 | South | (+1, 0) |
| 3 | West  | (0, -1) |



## Team and Project Management

### Roles

| Member | Responsibilities |
|---|---|
| **watoumi** | Maze generation algorithms (DFS, Prim, imperfect mode), `maze.py`, `generator.py`, `pattern.py`, output file format, terminal UI (`ui.py`), animation, integration (`a_maze_ing.py`), package structure and `pyproject.toml` |
| **aessabri** | Config parsing (`parsing.py`), BFS solver (`solver.py`), `Makefile`|


### Anticipated Planning and How It Evolved

**Initial plan:**
1. Design data structures
2. config parsing
3. implement `Maze` and DFS
4. the "42" pattern
5. BFS solver
6. hex output, terminal rendering
7. add prim algo and animation
8. ui menu
9. package, README, tests


### What Worked Well

- Splitting (generation / UI / parsing / solver) made work smooth
- The simple `walls[y][x]` list-of-bools structure was easy for both teammates to reason about

### What Could Be Improved

- using curses instead of what in ui.py


### Tools Used

- **VS Code** with Python and Pylance extensions
- **mypy** and **flake8** for type checking and style
- **github** for version control and collaboration


## Resources

### AI Usage Disclosure

AI tools were used strictly for learning and understanding theoretical concepts related to:

* Breadth-First Search (BFS)
* Depth-First Search (DFS)
* Prim’s Algorithm
* General maze generation strategies

AI was used to:

* Clarify how these algorithms work step-by-step.
* Compare algorithm behavior and complexity.
* Understand implementation strategies before coding.

AI was not used to automatically generate the project’s final codebase.
All core implementation, architecture, debugging, and integration were written and structured by the team.
