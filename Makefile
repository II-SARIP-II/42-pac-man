FLK 	:= flake8
MYPY 	:= mypy
FLAGS	:= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
DEP 	:= pydantic mypy flake8

install:
	uv add $(DEP)

run:
	@uv run python pac-man.py config/config.json

debug:
	@uv run python pdb pac-man.py config/config.json

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

.PHONY: install run debug clean lint lint-strict venv init
