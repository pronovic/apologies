#!/bin/sh
# Create the Python virtual environment used for development

deactivate 2>/dev/null  # just in case a virtual environment is active

if [ $# -gt 0 ] && [ $1 == "clean" ]; then
   if [ -d .python ]; then
      echo "Rebuilding virtual environment from scratch..."
      rm -rf .python
   else
      echo "Creating virtual environment..."
   fi
else
   if [ -d .python ]; then
      echo "Updating virtual environment..."
   else
      echo "Creating virtual environment..."
   fi
fi

virtualenv --quiet --download .python
source .python/bin/activate

VERSION=`python version.py`
DEPENDENCIES=`python dependencies.py`

echo "Installing dependencies for $VERSION:\n$DEPENDENCIES"
pip install --quiet "$DEPENDENCIES"

