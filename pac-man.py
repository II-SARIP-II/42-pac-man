from ursina import *

from src.GameEngine import GameEngine
from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file


def main() -> None:
    app = Ursina()
    config = ConfigFileValidation(**load_json_file("./config/config.json"))
    GameEngine(
        str(config.highscore_filename),
        config.levels,
        config.lives,
        config.points_per_pacgum,
        config.points_per_ghost,
        config.seed,
        config.level_max_time,
    )
    app.run()


if __name__ == "__main__":
    main()
