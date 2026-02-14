import sys

# ANSI helpers
RESET = "\033[0m"
CLEAR = "\033[H\033[J"

COLOR_SETS = [
    ("\033[38;5;15m", "\033[38;5;226m", "\033[38;5;46m"),  # white, yell, green
    ("\033[38;5;196m", "\033[38;5;51m", "\033[38;5;15m"),  # red, cyan, white
    ("\033[38;5;39m", "\033[38;5;201m", "\033[38;5;226m"),  # blue, pink, yell
    ("\033[38;5;208m", "\033[38;5;15m", "\033[38;5;196m"),  # oran, white, red
]


def clear_screen() -> None:
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def ask_choice() -> int:
    while True:
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
