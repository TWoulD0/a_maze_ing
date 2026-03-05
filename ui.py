import signal
import sys
import shutil
from types import FrameType
from typing import Optional
from parsing import parsing


# ANSI helpers
RESET = "\033[0m"
CLEAR = "\033[H\033[J"

COLOR_SETS = [
    ("\033[38;5;15m", "\033[38;5;226m", "\033[38;5;46m"),  # white, yell, green
    ("\033[38;5;196m", "\033[38;5;51m", "\033[38;5;15m"),  # red, cyan, white
    ("\033[38;5;39m", "\033[38;5;201m", "\033[38;5;226m"),  # blue, pink, yell
    ("\033[38;5;208m", "\033[38;5;15m", "\033[38;5;196m"),  # oran, white, red
]

COLOR_42_SETS = [
    "\033[38;5;7m",
    "\033[38;5;39m",
    "\033[38;5;196m",
    "\033[38;5;40m",
]

data_config = parsing()
canvas_w = 4 * data_config.width + 2
canvas_h = 2 * data_config.height + 10


def clear_screen() -> None:
    """Clear the terminal screen using ANSI escape codes."""
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def handle_resize(signum: int, frame: FrameType | None) -> None:
    """Handle SIGWINCH by re-checking the terminal size."""
    ensure_min_size_or_exit(canvas_w, canvas_h)


def ask_choice() -> int:
    signal.signal(signal.SIGWINCH, handle_resize)
    """Prompt the user for a menu choice between 1 and 4."""

    while True:
        ensure_min_size_or_exit(canvas_w, canvas_h)

        s = input("Choice? (1 - 6): ").strip()

        if s.isdigit():
            n = int(s)
            if 1 <= n <= 6:
                return n

        print("Invalid choice. Enter 1, 2, 3, 4, 5, 6")


def print_menu() -> None:
    """Print the interactive menu options to stdout."""
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Rotate 42 colors")
    print("5. Rotate symbols")
    print("6. Quit")


def print_stats(elapsed: float, solve_time: Optional[float],
                path_length: int) -> None:
    """Display the current timer, solve time, and shortest path length."""
    CYAN = "\033[38;5;51m"
    YELLOW = "\033[38;5;226m"
    GREEN = "\033[38;5;46m"

    print(f"{CYAN}Time Maze Gen : {elapsed:6.1f}s{RESET}  "
          f"{YELLOW}Path length : {path_length} steps{RESET}  "
          f"{GREEN}Solve time : "
          f"{f'{solve_time:.1f}s' if solve_time is not None else '---'}"
          f"{RESET}")


def term_size() -> tuple[int, int]:
    """Return the current terminal dimensions."""
    s = shutil.get_terminal_size(fallback=(80, 24))
    return s.columns, s.lines


def ensure_min_size_or_exit(cols: int = 82, lines: int = 48) -> None:
    """Exit with an error if the terminal is smaller than required."""
    c_size, l_size = term_size()
    if c_size < cols or l_size < lines:
        clear_screen()

        print(f"Error: terminal too small ({c_size}x{l_size}). "
              f"Need at least {cols}x{lines}.")
        sys.exit(1)
