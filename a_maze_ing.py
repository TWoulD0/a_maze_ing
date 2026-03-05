from mazegen import Maze
from mazegen import MazeGenerator
from mazegen import shortest_path
from parsing import parsing
import sys
import ui
import time

ANIM = True
ANIM_DELAY = 0.01
SYMBOLS = ["⬤ ", "██", "▒▒"]


def render_maze_blocks(maze: Maze, entry: tuple[int, int],
                       exit: tuple[int, int], color_id: int,
                       color_id42: int, symbols_id: int,
                       show_path: bool) -> str:

    """Render the maze as a coloured block string for terminal display."""
    if color_id >= len(ui.COLOR_SETS):
        color_id = 0
    wall_color, mark_color, path_color = ui.COLOR_SETS[color_id]

    if color_id42 >= len(ui.COLOR_42_SETS):
        color_id42 = 0
    _42_color = ui.COLOR_42_SETS[color_id42]

    if symbols_id >= len(SYMBOLS):
        symbols_id = 0
    symbol = SYMBOLS[symbols_id]

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
                grid[cy][cx] = _42_color + "██" + ui.RESET

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
        path = shortest_path(maze, entry, exit) or []
        for (x, y) in path:
            grid[2 * y + 1][2 * x + 1] = path_cell

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    grid[2 * entry_y + 1][2 * entry_x + 1] = mark_color + symbol + ui.RESET
    grid[2 * exit_y + 1][2 * exit_x + 1] = mark_color + symbol + ui.RESET

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
    """Encode a single cell's walls as one hexadecimal character."""
    n, e, s, w = maze.walls[y][x]
    value = (int(n) << 0) | (int(e) << 1) | (int(s) << 2) | (int(w) << 3)
    return format(value, "x")


def write_maze_hex(maze: Maze, output_file: str,
                   entry: tuple[int, int], exit: tuple[int, int]) -> None:
    """Write the maze to a file in the required hexadecimal format."""
    path = shortest_path(maze, entry, exit)

    path_str = ""
    if path:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            if (x2, y2) == (x1 - 1, y1):
                path_str += "W"
            elif (x2, y2) == (x1 + 1, y1):
                path_str += "E"
            elif (x2, y2) == (x1, y1 - 1):
                path_str += "N"
            elif (x2, y2) == (x1, y1 + 1):
                path_str += "S"

    with open(output_file, "w") as file:
        for y in range(maze.height):
            line = "".join(cell_to_hex(maze, x, y) for x in range(maze.width))
            file.write(line + "\n")

        file.write(f"\n{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")

        file.write(path_str + "\n")


def get_path_length(maze: Maze, entry: tuple[int, int],
                    exit: tuple[int, int]) -> int:
    """Return the number of steps in the shortest path, or 0 if none."""
    path = shortest_path(maze, entry, exit)
    if path is None:
        return 0
    return len(path) - 1


def main(argv: list[str]) -> None:
    """Run the A-Maze-ing application."""
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    data_config = parsing()

    canvas_w = 4 * data_config.width + 2
    canvas_h = 2 * data_config.height + 10

    if data_config.exit[0] >= data_config.width or\
       data_config.exit[1] >= data_config.height or\
       data_config.entry[0] < 0 or data_config.entry[1] < 0:
        print("the entry or the exit is not correct")
        sys.exit(1)

    def on_step(m: Maze) -> None:
        if not ANIM:
            return

        ui.ensure_min_size_or_exit(canvas_w, canvas_h)

        ui.clear_screen()
        print(render_maze_blocks(m, data_config.entry, data_config.exit,
                                 color_id=0, color_id42=0, symbols_id=0,
                                 show_path=False))
        time.sleep(ANIM_DELAY)

    def replay_animation(steps: list[tuple[int, int, int]]) -> Maze:
        m = Maze(data_config.width, data_config.height)
        for (x, y, d) in steps:
            m.remove_wall(x, y, d)
            on_step(m)
        return m

    generator = MazeGenerator(data_config.width, data_config.height,
                              data_config.seed, data_config.algorithm,
                              data_config.perfect, data_config.entry,
                              data_config.exit)
    maze_start_time: float = time.time()
    maze = generator.generate()
    replay_animation(generator._steps)
    time_maze_gen: float = time.time() - maze_start_time

    color_id = 0
    color_id42 = 0
    symbols_id = 0
    show_path = False

    solve_time: float | None = None
    path_length: int = get_path_length(maze, data_config.entry,
                                       data_config.exit)

    try:
        while True:
            ui.ensure_min_size_or_exit(canvas_w, canvas_h)
            ui.clear_screen()

            write_maze_hex(maze, data_config.output_file,
                           data_config.entry, data_config.exit)

            print(render_maze_blocks(maze, data_config.entry, data_config.exit,
                                     color_id, color_id42, symbols_id,
                                     show_path))
            print()
            ui.print_menu()

            ui.print_stats(time_maze_gen, solve_time, path_length)

            choice = ui.ask_choice()

            if choice == 1:
                maze_start_time = time.time()
                maze = generator.generate()
                replay_animation(generator._steps)
                time_maze_gen: float = time.time() - maze_start_time
                solve_time = None
                show_path = False
                path_length = get_path_length(maze, data_config.entry,
                                              data_config.exit)
            elif choice == 2:
                show_path = not show_path
                if show_path and solve_time is None:
                    solve_time = time.time() - maze_start_time
            elif choice == 3:
                color_id += 1
                if color_id >= len(ui.COLOR_SETS):
                    color_id = 0
            elif choice == 4:
                color_id42 += 1
                if color_id42 >= len(ui.COLOR_42_SETS):
                    color_id42 = 0
            elif choice == 5:
                symbols_id += 1
                if symbols_id >= len(SYMBOLS):
                    symbols_id = 0
            else:
                break

    except KeyboardInterrupt:
        print("\nExiting...")
        return


if __name__ == "__main__":
    main(sys.argv)
