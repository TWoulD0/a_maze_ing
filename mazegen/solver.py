from collections import deque
from typing import Optional
from .maze import Maze


def shortest_path(maze: Maze, entry: tuple[int, int], _exit: tuple[int, int]
                  ) -> Optional[list[tuple[int, int]]]:
    """Find the shortest path from entry to exit using breadth-first search."""

    queue = deque([entry])
    visited = set([entry])
    parent: dict[tuple[int, int], Optional[tuple[int, int]]] = {
        entry: None
    }

    directions = [
        ("N", 0, -1, 0),
        ("E", 1, 0, 1),
        ("S", 0, 1, 2),
        ("W", -1, 0, 3)
    ]

    while queue:
        x, y = queue.popleft()

        if (x, y) == _exit:
            path = []
            current: Optional[tuple[int, int]] = _exit
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for direction, dx, dy, dir_idx in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                if (nx, ny) not in visited:
                    if not maze.walls[y][x][dir_idx]:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
    return None
