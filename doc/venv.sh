#!/bin/bash
# Identify the Python virtual environment to use
# Use with: alias activate="source \$($HOME/util/venv.sh)/bin/activate 2>/dev/null"

# If poetry thinks there is a virtualenv, then use it
VENV=$(dirname $(dirname $(poetry run which python) 2>/dev/null) 2>/dev/null)
if [ $? = 0 ]; then
   echo "$VENV"
else
   # If there's a manually-built virtualenv in the current directory,then use it
   VENV=$(dirname $(find . -name pyvenv.cfg -maxdepth 2 2>/dev/null | tail -1) 2>/dev/null)
   if [ $? = 0 ]; then
      echo "$VENV"
   fi
fi

# Otherwise, just blow up
exit 1
