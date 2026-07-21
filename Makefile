FLK 	:= flake8
MYPY 	:= mypy
FLAGS	:= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install:
	uv sync

run:
	@uv run python pac-man.py config/config.json

debug:
	@uv run python -m pdb pac-man.py config/config.json

clean:
	rm -rf __pycache__ .mypy_cache .python-version .vscode
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	$(FLK) . --extend-exclude .venv
	$(MYPY) . $(FLAGS)

lint-strict:
	$(FLK) . --extend-exclude .venv
	$(MYPY) . $(FLAGS) --strict

venv:
	uv venv

init:
	uv init

build:
	uv run python -m nuitka \
	 --onefile \
	 --standalone \
	 --enable-plugin=no-qt \
	 --include-package=direct \
	 --include-package=panda3d \
	 --include-package=ursina \
	 --include-data-dir=assets=assets \
	 --include-data-dir=config=config \
	 --output-dir=builds/nuitka_linux \
	 pac-man.py

.PHONY: install run debug clean lint lint-strict venv init
