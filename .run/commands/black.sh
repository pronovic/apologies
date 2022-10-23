# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the black code formatter

command_black() {
   echo "Running black formatter..."
   poetry_run black "$@" .
   echo "done"
}

