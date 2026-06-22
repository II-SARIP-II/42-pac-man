from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file


def main() -> None:
    config = ConfigFileValidation(**load_json_file("./config/config.json"))
    gameStat(config)

if __name__ == "__main__":
    main()
