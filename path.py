from collections import deque
from a_maze_ing import Maze
from typing import Optional

DIR_CHARS = ["N", "E", "S", "W"]
DIR_VECS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def shortest_path_cells(maze: Maze,
                        start: tuple[int, int],
                        goal: tuple[int, int]) -> list[tuple[int, int]]:
    w = maze.width
    h = maze.height

    sx, sy = start
    gx, gy = goal

    prev: list[list[Optional[tuple[int, int]]]] = [
        [None for _ in range(w)] for _ in range(h)
    ]

    q = deque()
    q.append((sx, sy))
    prev[sy][sx] = (sx, sy)

    while q:
        x, y = q.popleft()

        if (x, y) == (gx, gy):
            break

        for d, (dx, dy) in enumerate(DIR_VECS):
            if maze.walls[y][x][d]:  # if there see the other walls
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx <= w and 0 <= ny <= h and prev[ny][nx] is None:
                prev[ny][nx] = (x, y)
                q.append((nx, ny))

    if prev[gy][gx] is None:
        return []  # there is no path so return no path

    path: list[tuple[int, int]] = []
    cx, cy = gx, gy
    while True:
        path.append((cx, cy))
        if (cx, cy) == (sx, sy):
            break
        px, py = prev[cy][cx]
        cy, cx = py, px

    path.reverse()
    return path


def has_path(maze: Maze,
             start: tuple[int, int], goal: tuple[int, int]) -> bool:
    w, h = maze.width, maze.height
    sx, sy = start
    gx, gy = goal

    seen = [[False] * w for _ in range(h)]
    q = deque([(sx, sy)])
    seen[sy][sx] = True

    while q:
        x, y = q.popleft()
        if (x, y) == (gx, gy):
            return True

        for d, (dx, dy) in enumerate(DIR_VECS):
            if maze.walls[y][x][d]:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx]:
                seen[ny][nx] = True
                q.append((nx, ny))

    return False


def cells_to_directions(path: list[tuple[int, int]]) -> str:
    dirs = []

    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == -1:
            dirs.append("N")
        elif dx == 1 and dy == 0:
            dirs.append("E")
        elif dx == 0 and dy == 1:
            dirs.append("S")
        elif dx == -1 and dy == 0:
            dirs.append("W")

    return "".join(dirs)
