#!/bin/bash
# Install the Poetry build tool
# This assumes that $POETRY_VERSION and $POETRY_HOME are set by the caller
set -e
curl -sSL https://install.python-poetry.org | python3 -
