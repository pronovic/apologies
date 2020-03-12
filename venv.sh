#!/bin/sh
# Create the Python virtual environment used for development

if [ $# -gt 0 ] && [ $1 == "clean" ]; then
   echo "Building virtual environment from scratch..."
   virtualenv --clear --quiet --download .python
else
   echo "Building virtual environment..."
   virtualenv --quiet --download .python
fi

source .python/bin/activate
pip install -r src/requirements.txt
