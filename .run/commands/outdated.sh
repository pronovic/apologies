# vim: set ft=bash ts=3 sw=3 expandtab:
# Show top-level dependencies with outdated constraints

# See: https://github.com/python-poetry/poetry/issues/2684#issuecomment-1076560832

command_outdated() {
   poetry show --outdated | grep --file=<(poetry show --tree | grep '^\w' | cut -d' ' -f1 | sed 's/.*/^&\\s/')
   if [ $? != 0 ]; then
      echo "*** Failed to check for outdated constraints"
      exit 1
   fi
}

