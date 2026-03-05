import random
from .maze import DIRS, Maze


class MazeGenerator:
    """Generates mazes using DFS, Prim's algorithm, or an imperfect variant."""
    def __init__(self, width: int, height: int,
                 seed: int | None = None, algorithm: str = "dfs",
                 perfect: bool = True, entry: tuple[int, int] = (0, 0),
                 _exit: tuple[int, int] = (0, 0)) -> None:
        """Initialise the generator with maze parameters."""
        self.width = width
        self.height = height
        self.algorithm = algorithm
        self.perfect = perfect
        self.entry = entry
        self._exit = _exit
        self.rng = random.Random(seed)
        self._maze: Maze | None = None
        self._steps: list[tuple[int, int, int]] = []

    def generate(self) -> Maze:
        """Generate a maze using the configured algorithm and settings."""
        if self.perfect:
            if self.algorithm == "dfs":
                maze, steps = self.generate_dfs()
            else:
                maze, steps = self.generate_prim()
        else:
            maze, steps = self.generate_imperfect()

        self._maze = maze
        self._steps = steps
        return maze

    def generate_dfs(self) -> tuple[Maze, list[tuple[int, int, int]]]:
        """Generate a perfect maze using iterative depth-first search."""
        from mazegen.pattern import apply_42_pattern
        maze = Maze(self.width, self.height)
        steps: list[tuple[int, int, int]] = []

        apply_42_pattern(maze, self.entry, self._exit)

        # false represent that cell is not visited
        cell_visited = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(False)
            cell_visited.append(row)

        stack: list[tuple[int, int]] = []
        start_x, start_y = self.entry
        cell_visited[start_y][start_x] = True
        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            neighbors: list[tuple[int, int, int]] = []

            for d, (dy, dx) in enumerate(DIRS):
                nx = x + dx
                ny = y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and not cell_visited[ny][nx]
                        and (nx, ny) not in maze.pattern42):
                    neighbors.append((nx, ny, d))

            if not neighbors:
                stack.pop()
                continue

            nx, ny, d = self.rng.choice(neighbors)
            maze.remove_wall(x, y, d)
            steps.append((x, y, d))
            cell_visited[ny][nx] = True
            stack.append((nx, ny))

        return maze, steps

    def generate_prim(self) -> tuple[Maze, list[tuple[int, int, int]]]:
        """Generate a perfect maze using a randomised Prim's algorithm."""
        from mazegen.pattern import apply_42_pattern

        maze = Maze(self.width, self.height)
        steps: list[tuple[int, int, int]] = []

        apply_42_pattern(maze, self.entry, self._exit)

        cell_visited = [
            [False for _ in range(self.width)] for _ in range(self.height)]
        frontier: list[tuple[int, int]] = []

        def add_frontier(x: int, y: int) -> None:
            for d, (dy, dx) in enumerate(DIRS):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        not cell_visited[ny][nx]
                        and (nx, ny) not in maze.pattern42):
                    frontier.append((nx, ny))

        sx, sy = self.entry
        cell_visited[sy][sx] = True
        add_frontier(sx, sy)

        while frontier:
            fx, fy = frontier.pop(self.rng.randrange(len(frontier)))
            if cell_visited[fy][fx]:
                continue

            neighbors_in: list[tuple[int, int, int]] = []
            for d, (dy, dx) in enumerate(DIRS):
                nx, ny = fx + dx, fy + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and cell_visited[ny][nx]
                        and (nx, ny) not in maze.pattern42):
                    neighbors_in.append((nx, ny, d))

            if not neighbors_in:
                continue

            nx, ny, d = self.rng.choice(neighbors_in)

            maze.remove_wall(fx, fy, d)
            steps.append((fx, fy, d))

            cell_visited[fy][fx] = True
            add_frontier(fx, fy)

        return maze, steps

    def generate_imperfect(self) -> tuple[Maze, list[tuple[int, int, int]]]:
        """Generate an imperfect maze by removing
        extra walls after generation."""
        if self.algorithm == "dfs":
            maze, steps = self.generate_dfs()
        elif self.algorithm == "prim":
            maze, steps = self.generate_prim()

        last_steps: list[tuple[int, int, int]] = []

        last_steps.extend(steps)

        candidates: list[tuple[int, int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if x + 1 < self.width and maze.walls[y][x][1]:
                    candidates.append((x, y, 1))
                if y + 1 < self.height and maze.walls[y][x][2]:
                    candidates.append((x, y, 2))

        self.rng.shuffle(candidates)
        removed = 0
        extra_walls = 10
        for x, y, d in candidates:
            if removed >= extra_walls:
                break
            if maze.walls[y][x][d]:
                maze.remove_wall(x, y, d)
                last_steps.append((x, y, d))
                removed += 1

        return maze, last_steps

    def get_steps(self) -> list[tuple[int, int, int]]:
        """Return the wall-removal steps recorded during the last generation"""
        return self._steps
