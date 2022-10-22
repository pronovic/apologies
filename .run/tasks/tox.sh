# vim: set ft=bash sw=3 ts=3:

help_tox() {
   echo "- run tox: Run the Tox test suite used by the GitHub CI action"
}

task_tox() {
   run_command tox -e "checks,docs,coverage,demo"
}

