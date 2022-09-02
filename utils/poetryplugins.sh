#!/bin/bash
# Install Poetry plugins
# Dependency resolution for plugins is slow, so we try to avoid doing it

set -x

if [ $# -lt 1 ]; then
   echo "usage: poetryplugins.sh <plugin> [<plugin>]"
   exit 1
fi

for plugin in $@; do
   poetry self show "$plugin"
   if [ $? != 0 ]; then
      poetry self add "$plugin"
      if [ $? != 0 ]; then
         exit 1 
      fi
   fi
done

