#!/bin/bash
# Determine location of Poetry directories to be cached, for use in GitHub Actions

# Installing Poetry is a bit slow, and installing Poetry plugins is even
# slower.  Caching helps, but we need to cache both the installation directory
# and the configuration directory, and those directories vary on every
# platform.

if [ "$GITHUB_ACTIONS" == "true" ]; then

   if [ "$RUNNER_OS" == "Linux" ]; then
      POETRY_INSTALL="/home/runner/.local"
      POETRY_CONFIG="/home/runner/.config/pypoetry"
   elif [ "$RUNNER_OS" == "macOS" ]; then
      POETRY_INSTALL="/Users/runner/.local"
      POETRY_CONFIG="/Users/runner/Library/Preferences/pypoetry"
   elif [ "$RUNNER_OS" == "Windows" ]; then
      POETRY_INSTALL="C:/Users/runneradmin/AppData/Roaming/Python/Scripts"
      POETRY_CONFIG="C:/Users/runneradmin/AppData/Roaming/pypoetry"
   fi 

   echo "POETRY_INSTALL=$POETRY_INSTALL" >> "$GITHUB_ENV"
   echo "POETRY_CONFIG=$POETRY_CONFIG" >> "$GITHUB_ENV"
   echo "$POETRY_INSTALL/bin" >> "$GITHUB_PATH"

fi

