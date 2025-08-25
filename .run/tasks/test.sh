# vim: set ft=bash sw=3 ts=3 expandtab:

help_test() {
   if [ -f "tests/__init__.py" ] || [ -f "src/tests/__init__.py" ]; then
      echo "- run test: Run the unit tests"
      echo "- run test -c: Run the unit tests with coverage"
      echo "- run test -ch: Run the unit tests with coverage and open the HTML report"
   fi
}

task_test() {
   run_command pytest "$@"
}

