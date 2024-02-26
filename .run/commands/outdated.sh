# vim: set ft=bash ts=3 sw=3 expandtab:
# Show top-level dependencies with outdated constraints

# See: https://github.com/python-poetry/poetry/issues/2684#issuecomment-1076560832

command_outdated() {
   echo "Updating dependencies with current constraints..."
   echo ""
   poetry update
   if [ $? != 0 ]; then
      echo "*** Failed to update dependencies"
      exit 1
   fi

   echo ""
   echo "Checking for outdated constraints..."
   echo ""
   poetry show --outdated | grep --file=<(poetry show --tree | grep '^\w' | cut -d' ' -f1 | sed 's/.*/^&\\s/')
   if [ $? != 0 ]; then
      echo "*** Failed to check for outdated constraints"
      exit 1
   fi
}

