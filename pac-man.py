from sys import argv

from ursina import Ursina

from src.GameEngine import GameEngine
from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file


def main() -> None:
    app = Ursina()
    if len(argv) != 2:
        print("Usage: pac-man.py <config_file>")
        exit(1)

    config = ConfigFileValidation(**load_json_file(argv[1]))

    GameEngine(config)

    app.run()


if __name__ == "__main__":
    main()
