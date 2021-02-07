#!/bin/bash
# Check for tab characters in files controlled by Git
# To exclude a file from this check, list its complete relative path in the .tabignore file

result=$(grep -l "$(printf '\t')" $(git ls-files | grep -v -x -F --file=.tabignore))
if [ $? == 0 ]; then
   echo "*** Error: Some files contain tab characters:"
   echo "${result}"
   exit 1
fi

