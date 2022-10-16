#!/bin/bash
# Install the Poetry build tool, working around platform differences

set -e

echo "PYTHON_VERSION=$PYTHON_VERSION"
echo "POETRY_CONFIG_DIR=$POETRY_CONFIG_DIR"
echo "POETRY_HOME=$POETRY_HOME"
echo "POETRY_CACHE=$POETRY_CACHE"

curl -sSL https://install.python-poetry.org | python -

# On Windows, something gets screwed up with this soft link when restoring from cache.
# Recreating it seems to resolve the problem, although it's not clear why.
cd "$POETRY_HOME/bin"
if [ -f poetry.exe ]; then
  rm -f poetry.exe
  ln -s ../venv/Scripts/poetry.exe
fi

