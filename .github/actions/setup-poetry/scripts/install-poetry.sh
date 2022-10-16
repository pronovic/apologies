#!/bin/bash
# Install the Poetry build tool
# This assumes that $POETRY_VERSION and $POETRY_HOME are set by the caller
set -e
echo "PYTHON_VERSION=$PYTHON_VERSION"
echo "POETRY_VERSION=$POETRY_VERSION"
echo "POETRY_HOME=$POETRY_HOME"
curl -sSL https://install.python-poetry.org | python -
