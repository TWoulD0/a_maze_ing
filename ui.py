import signal
import sys
import shutil
from types import FrameType
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

data_config = parsing()
canvas_w = 4 * data_config.width + 2
canvas_h = 2 * data_config.height + 10


def clear_screen() -> None:
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def handle_resize(signum: int, frame: FrameType | None) -> None:
    ensure_min_size_or_exit(canvas_w, canvas_h)


def ask_choice() -> int:
    signal.signal(signal.SIGWINCH, handle_resize)

    while True:
        ensure_min_size_or_exit(canvas_w, canvas_h)

        s = input("Choice? (1 - 4): ").strip()

        if s.isdigit():
            n = int(s)
            if 1 <= n <= 4:
                return n

        print("Invalid choice. Enter 1, 2, 3, 4")


def print_menu() -> None:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")


def term_size() -> tuple[int, int]:
    s = shutil.get_terminal_size(fallback=(80, 24))
    return s.columns, s.lines


def ensure_min_size_or_exit(cols: int = 82, lines: int = 48) -> None:
    c_size, l_size = term_size()
    if c_size < cols or l_size < lines:
        clear_screen()

        print(f"Error: terminal too small ({c_size}x{l_size}). "
              f"Need at least {cols}x{lines}.")
        sys.exit(1)
