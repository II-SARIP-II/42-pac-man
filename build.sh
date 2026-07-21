#!/bin/bash
set -e
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

echo "Build done : builds/nuitka_linux/pac-man.bin"
