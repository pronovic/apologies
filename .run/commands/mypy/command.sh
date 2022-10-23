# vim: set ft=bash ts=3 sw=3:
# Run the MyPy code checker

command_mypy() {
   echo "Running mypy checks..."
   poetry_run mypy
   echo "done"
}

