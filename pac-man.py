from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file
from src.GameState import GameState


def main() -> None:
    config = ConfigFileValidation(**load_json_file("./config/config.json"))
    GameState(config.highscore_filename,
              config.levels,
              config.lives,
              config.points_per_pacgum,
              config.points_per_ghost,
              config.seed,
              config.level_max_time
              )

if __name__ == "__main__":
    main()
