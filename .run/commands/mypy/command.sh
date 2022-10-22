# vim: set ft=bash ts=3 sw=3:
# Run the MyPy code checker

command_mypy() {
   echo "Running mypy checks..."

   poetry_run mypy
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}

