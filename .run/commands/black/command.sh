# vim: set ft=bash ts=3 sw=3:
# Run the black code formatter

command_black() {
   echo "Running black formatter..."

   poetry_run black $* .
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}

