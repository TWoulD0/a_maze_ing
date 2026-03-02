import sys
from typing import Dict, List, Tuple, Optional


class Config:
    def __init__(
            self,
            height: int,
            width: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            perfect: bool,
            output_file: str,
            seed: Optional[int],
            algorithm: str) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed
        self.algorithm = algorithm


def parse_args() -> str:
    args = len(sys.argv)
    if args != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    return sys.argv[1]


def read_file(config_file: str) -> List[str]:
    try:
        with open(config_file) as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print("Error: configuration file not found.")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: could not read file '{config_file}': {e}")
        sys.exit(1)


def build_config_dict(lines: List[str]) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if "=" not in line:
            print(f"Error: invalid line {i} (missing '=')")
            sys.exit(1)
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            print(f"Error: empty key at line {i}")
            sys.exit(1)
        if not value:
            print(f"Error: empty value for key '{key}' at line {i}")
            sys.exit(1)
        if key in config_dict:
            print(f"Error: duplicate key '{key}' at line {i}")
            sys.exit(1)
        config_dict[key] = value
    return config_dict


def validate_keys(config_dict: Dict[str, str]) -> None:
    required: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                          "OUTPUT_FILE", "PERFECT", "ALGORITHM"}
    found = config_dict.keys()
    missing = required - found
    if missing:
        print(f"Error: missing required keys: {missing}")
        sys.exit(1)


def parse_int(value: str, key_name: str) -> int:
    try:
        number = int(value)
    except ValueError:
        print(f"Error: '{key_name}' must be a valid integer.")
        sys.exit(1)

    if number < 1:
        print(f"Error: '{key_name}' must be positive.")
        sys.exit(1)

    return number


def pars_perfect(value: str, key_name: str) -> bool:
    value = value.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    print(f"Error: '{key_name}' must be True or False.")
    sys.exit(1)


def parse_algorithm(value: str) -> str:
    value = value.strip().lower()

    if value not in ("prim", "dfs"):
        print("Error: 'ALGORITHM' must be either 'prim' or 'dfs'.")
        sys.exit(1)

    return value


def parse_coordinates(value: str, key_name: str,
                      width: int, height: int) -> Tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        print(f"Error: '{key_name}' must be in format x,y.")
        sys.exit(1)

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        print(f"Error: '{key_name}' must contain valid integers")
        sys.exit(1)

    if not (0 <= x < width and 0 <= y < height):
        print(f"Error: '{key_name}' coordinates out of maze bounds")
        sys.exit(1)

    return (x, y)


def build_config(config_dict: Dict[str, str]) -> Config:
    height = parse_int(config_dict["HEIGHT"], "HEIGHT")
    width = parse_int(config_dict["WIDTH"], "WIDTH")
    if width * height > 40000:
        print("Erro: maze too large.")
        sys.exit(1)

    entry = parse_coordinates(
        config_dict["ENTRY"], "ENTRY", width, height
    )

    exit = parse_coordinates(
        config_dict["EXIT"], "EXIT", width, height
    )

    if entry == exit:
        print("Error: ENTRY and EXIT must be different.")
        sys.exit(1)

    perfect = pars_perfect(config_dict["PERFECT"], "PERFECT")
    output_file = config_dict["OUTPUT_FILE"]
    if not output_file.lower().endswith(".txt"):
        print("Error: 'OUTPUT_FILE' must end with .txt")
        sys.exit(1)

    seed_value = config_dict.get("SEED")
    if seed_value is not None:
        try:
            seed = int(seed_value)
        except ValueError:
            print("Error: 'SEED' must be a valid integer.")
            sys.exit(1)
    else:
        seed = 0

    algorithm = parse_algorithm(config_dict["ALGORITHM"])

    cfg = Config(height, width, entry, exit,
                 perfect, output_file, seed, algorithm)

    return cfg


def parsing() -> Config:
    config_file = parse_args()
    lines = read_file(config_file)
    config_dict = build_config_dict(lines)
    validate_keys(config_dict)
    config = build_config(config_dict)

    return config
