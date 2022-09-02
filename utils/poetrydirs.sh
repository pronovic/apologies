#!/bin/bash
# Determine location of Poetry directories to be cached, for use in GitHub Actions

# Installing Poetry is a bit slow, and installing Poetry plugins is even
# slower.  Caching helps, but we need to cache both the installation directory
# and the configuration directory, and those directories vary on every
# platform.

if [ "$GITHUB_ACTIONS" == "true" ]; then
   if [ "$RUNNER_OS" == "Linux" ]; then
      echo "POETRY_INSTALL=/home/runner/.local" >> "$GITHUB_ENV"
      echo "POETRY_CONFIG=/home/runner/.config/pypoetry" >> "$GITHUB_ENV"
   elif [ "$RUNNER_OS" == "macOS" ]; then
      echo "POETRY_INSTALL=/Users/runner/.local" >> "$GITHUB_ENV"
      echo "POETRY_CONFIG=/Users/runner/Library/Preferences/pypoetry" >> "$GITHUB_ENV"
   elif [ "$RUNNER_OS" == "Windows" ]; then
      echo "POETRY_INSTALL=C:/Users/runneradmin/AppData/Roaming/Python" >> "$GITHUB_ENV"
      echo "POETRY_CONFIG=C:/Users/runneradmin/AppData/Roaming/pypoetry" >> "$GITHUB_ENV"
   fi 
fi

