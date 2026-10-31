from pathlib import Path
from sys import argv

from state import record_overlay


if __name__ == "__main__":
    record_overlay(Path(argv[1]))
