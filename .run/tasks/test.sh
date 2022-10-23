# vim: set ft=bash sw=3 ts=3 expandtab:

help_test() {
   echo "- run test: Run the unit tests"
   echo "- run test -c: Run the unit tests with coverage"
   echo "- run test -ch: Run the unit tests with coverage and open the HTML report"
}

task_test() {
   run_command pytest "$@"
}

