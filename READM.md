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

# Configuration File Format
- The file must contain one KEY=VALUE per line.
- Lines staring with # are ignored


## Resources

# AI Usage Disclosure

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

