# vim: set ft=bash ts=3 sw=3:
# Run the broader Tox test suite used by the GitHub CI action

command_tox() {
   poetry_run tox -c .toxrc $*
   if [ $? != 0 ]; then
      exit 1
   fi
}

