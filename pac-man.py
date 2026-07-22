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

        raw_config = load_json_file(argv[1])

        if not isinstance(raw_config, dict):
            print("\nError : JSON file must contain an object/dictionary.")
            exit(1)

        for f_name, f_info in ConfigFileValidation.model_fields.items():
            if f_name not in raw_config and not f_info.is_required():
                print(
                    f"\nInformation: the field '{f_name}' "
                    "is missing from the JSON."
                    f"\nDefault value applied: {f_info.default}\n"
                )

        config = ConfigFileValidation(**raw_config)

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
            f"\nValidation error: {e.errors()[0]['loc']} "
            f"{e.errors()[0]['msg']}")
        exit(1)

    except Exception as e:
        print(f"\nError: {e}")
        exit(1)


if __name__ == "__main__":
    main()
