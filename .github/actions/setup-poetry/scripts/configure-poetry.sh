#!/bin/bash
# Configure Poetry

set -e

poetry config cache-dir "$POETRY_CACHE" --local

poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local

if [ ! -z "$MAX_WORKERS" ]; then
  poetry config installer.max-workers "$MAX_WORKERS" --local
fi

poetry config --list

