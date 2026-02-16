from a_maze_ing import Maze, DIRS
import random


def generate_perfect_maze_dfs(
        width: int, height: int, rng: random.Random
        ) -> tuple[Maze, list[tuple[int, int, int]]]:
    maze = Maze(width, height)
    steps: list[tuple[int, int, int]] = []

    # false represent that cell is not visited
    cell_visited = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(False)
        cell_visited.append(row)

    stack: list[tuple[int, int]] = []
    start_x, start_y = 0, 0
    cell_visited[start_y][start_x] = True
    stack.append((start_x, start_y))

    while stack:
        x, y = stack[-1]
        neighbors: list[tuple[int, int, int]] = []

        for d, (dy, dx) in enumerate(DIRS):
            nx = x + dx
            ny = y + dy
            if 0 <= nx < width and 0 <= ny < height \
               and not cell_visited[ny][nx]:
                neighbors.append((nx, ny, d))

        if not neighbors:
            stack.pop()
            continue

        nx, ny, d = rng.choice(neighbors)
        maze.remove_wall(x, y, d)
        steps.append((x, y, d))
        cell_visited[ny][nx] = True
        stack.append((nx, ny))

    return maze, steps


def generate_perfect_maze_prim(
        width: int, height: int, rng: random.Random
        ) -> tuple[Maze, list[tuple[int, int, int]]]:
    maze = Maze(width, height)
    steps: list[tuple[int, int, int]] = []

    in_maze = [[False for _ in range(width)] for _ in range(height)]
    frontier: list[tuple[int, int]] = []

    def add_frontier(x: int, y: int) -> None:
        for d, (dy, dx) in enumerate(DIRS):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not in_maze[ny][nx]:
                frontier.append((nx, ny))

    # pick a random starting cell
    sx, sy = rng.randrange(width), rng.randrange(height)
    in_maze[sy][sx] = True
    add_frontier(sx, sy)

    while frontier:
        # pick a random frontier cell
        fx, fy = frontier.pop(rng.randrange(len(frontier)))
        if in_maze[fy][fx]:
            continue

        neighbors_in: list[tuple[int, int, int]] = []
        for d, (dy, dx) in enumerate(DIRS):
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < width and 0 <= ny < height and in_maze[ny][nx]:
                neighbors_in.append((nx, ny, d))

        if not neighbors_in:
            continue

        nx, ny, d = rng.choice(neighbors_in)

        maze.remove_wall(fx, fy, d)
        steps.append((fx, fy, d))

        in_maze[fy][fx] = True
        add_frontier(fx, fy)

    return maze, steps


def generate_imperfect_maze(width: int, height: int, rng: random.Random,
                            algorithm: str, extra_walls: int = 10) -> Maze:
    if algorithm == "dfs":
        maze, steps = generate_perfect_maze_dfs(width, height, rng)
    elif algorithm == "prim":
        maze, steps = generate_perfect_maze_prim(width, height, rng)

    last_steps: list[tuple[int, int, int]] = []

    last_steps.extend(steps)

    candidates: list[tuple[int, int, int]] = []
    for y in range(height):
        for x in range(width):
            if x + 1 < width and maze.walls[y][x][1]:
                candidates.append((x, y, 1))
            if y + 1 < height and maze.walls[y][x][2]:
                candidates.append((x, y, 2))

    rng.shuffle(candidates)
    removed = 0
    for x, y, d in candidates:
        if removed >= extra_walls:
            break
        if maze.walls[y][x][d]:
            maze.remove_wall(x, y, d)
            last_steps.append((x, y, d))
            removed += 1

    return maze, last_steps
