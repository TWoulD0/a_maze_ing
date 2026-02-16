import sys
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    algorithm: str
    seed: Optional[int] = None


def parse_xy(s: str) -> tuple[int, int]:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 2:
        raise ValueError("Invalid coordinates: expected (x,y)")
    x = int(parts[0])
    y = int(parts[1])
    return (x, y)


def parse_bool(s: str) -> bool:
    v = s.strip().lower()
    if v in ("true"):
        return True
    if v in ("false"):
        return False
    raise ValueError(f"Invalid boolean: {s}")


def parse_algorithm(s: str) -> str:
    v = s.strip().lower()
    if v in ("dfs") or v in ("prim"):
        return v
    raise ValueError(f"Invalid name: {s}")


def load_config(file_name) -> Config:
    data: dict[str, str] = {}

    try:
        with open(file_name, "r") as file:
            for raw in file:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise Exception(f"Bad line (missing '='): {line}")
                k, v = line.split("=", 1)
                k = k.strip().upper()
                v = v.strip()
                data[k] = v
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    for d in ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
              "OUTPUT_FILE", "PERFECT", "ALGORITHM"]:
        if d not in data:
            print("missing data")
            sys.exit(1)

    try:
        _width = int(data["WIDTH"])
        _height = int(data["HEIGHT"])
        _entry = parse_xy(data["ENTRY"])
        _exit = parse_xy(data["EXIT"])
        _output_file = data["OUTPUT_FILE"]
        _perfect = parse_bool(data["PERFECT"])
        if "SEED" in data and data["SEED"]:
            _seed = int(data["SEED"])
        else:
            _seed = None
        _algorithm = parse_algorithm(data["ALGORITHM"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return Config(
        width=_width,
        height=_height,
        entry=_entry,
        exit=_exit,
        output_file=_output_file,
        perfect=_perfect,
        algorithm=_algorithm,
        seed=_seed,
    )
