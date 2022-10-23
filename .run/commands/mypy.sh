# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the MyPy code checker

# We generate relative paths in the output to make integration with Pycharm work better

command_mypy() {
   echo "Running mypy checks..."
   poetry_run mypy --hide-absolute-path "$@"
   echo "done"
}

