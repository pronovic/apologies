# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Pylint code checker

# We generate relative paths in the output to make integration with Pycharm work better

command_pylint() {
   echo "Running pylint checks..."
   TEMPLATE="{path}:{line}:{column} - {C} - ({symbol}) - {msg}"
   poetry_run pylint --msg-template="$TEMPLATE" -j 0 "$@" $(ls -d src/*) tests
   echo "done"
}
