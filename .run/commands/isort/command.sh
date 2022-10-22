# vim: set ft=bash ts=3 sw=3:
# Run the isort import formatter

command_isort() {
   echo "Running isort formatter..."

   poetry_run isort $* .
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}

