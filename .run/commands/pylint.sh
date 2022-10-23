# vim: set ft=bash ts=3 sw=3:
# Run the Pylint code checker

command_pylint() {
   echo "Running pylint checks..."
   poetry_run pylint -j 0 $(ls -d src/*) tests
   echo "done"
}

