#!/bin/bash
# Configure Poetry

set -e

poetry config cache-dir "$POETRY_CACHE"

poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

if [ ! -z "$MAX_WORKERS" ]; then
  poetry config installer.max-workers "$MAX_WORKERS"
fi

poetry config --list

