from sys import argv, exit

from pydantic import ValidationError
from ursina import Ursina

from src.GameEngine import GameEngine
from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file


def main() -> None:
    """Load config from argv, launch the app, and run the game loop.

    Returns:
        None.
    """

    try:
        app = Ursina()

        if len(argv) != 2:
            print("\nUsage: pac-man.py <config_file>")
            exit(1)

        config = ConfigFileValidation(**load_json_file(argv[1]))

        GameEngine(
            str(config.highscore_filename),
            config.levels,
            config.lives,
            config.points_per_pacgum,
            config.points_per_super_pacgum,
            config.points_per_ghost,
            config.seed,
            config.level_max_time,
        )

        app.run()

    except ValidationError as e:
        print(
            f"Validation error: {e.errors()[0]['loc']} {e.errors()[0]['msg']}")
        exit(1)

    except Exception as e:
        print(f"\nError: {e}")
        exit(1)


if __name__ == "__main__":
    main()
