import sys
import random
import ui
from config_parsing import load_config

# Directions: N, E, S, W
DIRS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
OP_DIR: dict[int, int] = {0: 2, 1: 3, 2: 0, 3: 1}


class Maze:
    def __init__(self, width: int, height: int) -> None:
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

    # remove wall from current cell and neighbor cell
    def remove_wall(self, x: int, y: int, d: int) -> None:
        ny = y + DIRS[d][0]
        nx = x + DIRS[d][1]
        self.walls[y][x][d] = False
        self.walls[ny][nx][OP_DIR[d]] = False


def render_maze_blocks(maze: Maze, entry: tuple[int, int],
                       exit: tuple[int, int], color_id: int,
                       show_path: bool) -> str:

    from path import shortest_path_cells

    if color_id >= len(ui.COLOR_SETS):
        color_id = 0
    wall_color, mark_color, path_color = ui.COLOR_SETS[color_id]

    WIDTH = maze.width
    HEIGHT = maze.height

    canvas_w = 2 * WIDTH + 1
    canvas_h = 2 * HEIGHT + 1

    wall = wall_color + "██" + ui.RESET
    empty = "  "
    path_cell = path_color + "██" + ui.RESET

    grid = [[wall for _ in range(canvas_w)] for _ in range(canvas_h)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cy = 2 * y + 1
            cx = 2 * x + 1
            if (x, y) in getattr(maze, "pattern42"):
                num_color = "\033[38;5;7m"
                grid[cy][cx] = num_color + "██" + ui.RESET

            else:
                grid[cy][cx] = empty

            if not maze.walls[y][x][0]:
                grid[cy - 1][cx] = empty
            if not maze.walls[y][x][1]:
                grid[cy][cx + 1] = empty
            if not maze.walls[y][x][2]:
                grid[cy + 1][cx] = empty
            if not maze.walls[y][x][3]:
                grid[cy][cx - 1] = empty

    if show_path:
        path = shortest_path_cells(maze, entry, exit)
        for (x, y) in path:
            grid[2 * y + 1][2 * x + 1] = path_cell

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    grid[2 * entry_y + 1][2 * entry_x + 1] = mark_color + "⬤ " + ui.RESET
    grid[2 * exit_y + 1][2 * exit_x + 1] = mark_color + "⬤ " + ui.RESET

    lines = []
    for row in grid:
        line = ""
        for ch in row:
            line += ch
        lines.append(line)

    result = ""
    for line in lines:
        result += line + "\n"

    return result.rstrip("\n")


def cell_to_hex(maze: Maze, x: int, y: int) -> str:
    n, e, s, w = maze.walls[y][x]
    value = (int(n) << 0) | (int(e) << 1) | (int(s) << 2) | (int(w) << 3)
    return format(value, "x")


def write_maze_hex(maze: Maze, output_file: str,
                   entry: tuple[int, int], exit: tuple[int, int]) -> None:

    from path import shortest_path_cells, cells_to_directions

    path = shortest_path_cells(maze, entry, exit)
    path_str = cells_to_directions(path)

    with open(output_file, "w") as file:
        for y in range(maze.height):
            line = "".join(cell_to_hex(maze, x, y) for x in range(maze.width))
            file.write(line + "\n")

        file.write(f"\n{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")

        file.write(path_str + "\n")


def main(argv):
    from pattern import apply_42_pattern
    import maze_generator

    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    data_config = load_config(argv[1])
    rng = random.Random(data_config.seed)

    def maze_build():
        if data_config.perfect:
            return maze_generator.generate_perfect_maze(
                data_config.width, data_config.height, rng)
        else:
            return maze_generator.generate_imperfect_maze(
                data_config.width, data_config.height, rng)

    maze = maze_build()
    apply_42_pattern(maze, data_config.entry, data_config.exit)

    color_id = 0
    show_path = False

    try:
        while True:
            ui.clear_screen()

            write_maze_hex(maze, data_config.output_file,
                           data_config.entry, data_config.exit)

            print(render_maze_blocks(maze, data_config.entry, data_config.exit,
                                     color_id, show_path))
            print()
            ui.print_menu()
            choice = ui.ask_choice()

            if choice == 1:
                maze = maze_build()
            elif choice == 2:
                show_path = not show_path
            elif choice == 3:
                color_id += 1
                if color_id >= len(ui.COLOR_SETS):
                    color_id = 0
            else:
                break

    except KeyboardInterrupt:
        print("\nExiting...")
        return


if __name__ == "__main__":
    main(sys.argv)
