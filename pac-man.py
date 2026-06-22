from src.models.config import ConfigFileValidation
from src.utils_io import load_json_file
from pydantic import ValidationError


def main() -> None:
    try:
        config = ConfigFileValidation(**load_json_file("./config/config.json"))
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
