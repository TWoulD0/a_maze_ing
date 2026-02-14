from a_maze_ing import Maze, DIRS
import random


def generate_perfect_maze(width: int, height: int, rng: random.Random) -> Maze:
    maze = Maze(width, height)

    # make other grid maze to see if the cell is visited
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
        cell_visited[ny][nx] = True
        stack.append((nx, ny))

    return maze


def generate_imperfect_maze(width: int, height: int, rng: random.Random,
                            extra_walls: int = 10) -> Maze:
    maze = generate_perfect_maze(width, height, rng)

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
            removed += 1

    return maze
