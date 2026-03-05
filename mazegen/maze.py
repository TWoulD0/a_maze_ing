
# Directions: N, E, S, W
DIRS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
OP_DIR: dict[int, int] = {0: 2, 1: 3, 2: 0, 3: 1}


class Maze:
    """Represents a 2D grid maze with wall data per cell."""
    def __init__(self, width: int, height: int) -> None:
        """Initialize a fully walled maze of the given dimensions."""
        self.width = width
        self.height = height
        self.walls = []
        self.pattern42: set[tuple[int, int]] = set()

        # true represent that there is wall
        for y in range(height):
            row = []

            for x in range(width):
                cell_walls = [True, True, True, True]  # N, E, S, W
                row.append(cell_walls)

            self.walls.append(row)

    def remove_wall(self, x: int, y: int, d: int) -> None:
        """Remove the wall between cell (x, y)
        and its neighbour in direction d."""
        ny = y + DIRS[d][0]
        nx = x + DIRS[d][1]
        if (x, y) in self.pattern42 or (nx, ny) in self.pattern42:
            return
        self.walls[y][x][d] = False
        self.walls[ny][nx][OP_DIR[d]] = False
