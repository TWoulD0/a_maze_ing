from .maze import Maze, DIRS, OP_DIR
import sys


def apply_42_pattern(maze: Maze,
                     entry: tuple[int, int],
                     exit: tuple[int, int]) -> None:
    """Stamp the '42' pattern into the maze by fully walling chosen cells."""
    bitmap = [
        "1010111",
        "1010001",
        "1110111",
        "0010100",
        "0010111",
    ]

    p_height = len(bitmap)
    p_width = len(bitmap[0])

    if maze.width < p_width + 2 or maze.height < p_height + 2:
        print("Error: maze too small to draw the '42' pattern.")
        sys.exit(1)

    x0 = (maze.width - p_width) // 2
    y0 = (maze.height - p_height) // 2

    def close_cell(x: int, y: int) -> None:
        maze.walls[y][x] = [True, True, True, True]
        maze.pattern42.add((x, y))

        for d, (dy, dx) in enumerate(DIRS):
            nx = x + dx
            ny = y + dy
            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                maze.walls[ny][nx][OP_DIR[d]] = True

    for j, row in enumerate(bitmap):
        for i, ch in enumerate(row):
            if ch == "0":
                continue
            x, y = x0 + i, y0 + j
            if (x, y) == entry or (x, y) == exit:
                print("Error: the entry or exit is on 42 pattern")
                sys.exit(1)
            close_cell(x, y)
