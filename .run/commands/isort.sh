# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the isort import formatter

command_isort() {
   echo "Running isort formatter..."
   poetry_run isort --color "$@" .
   echo "done"
}

