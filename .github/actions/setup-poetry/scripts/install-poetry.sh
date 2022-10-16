#!/bin/bash
# Install the Poetry build tool
# The caller must set both $POETRY_VERSION and $POETRY_HOME

set -e

echo "PYTHON_VERSION=$PYTHON_VERSION"
echo "POETRY_CONFIG_DIR=$POETRY_CONFIG_DIR"
echo "POETRY_HOME=$POETRY_HOME"
echo "POETRY_CACHE=$POETRY_CACHE"

curl -sSL https://install.python-poetry.org | python -

