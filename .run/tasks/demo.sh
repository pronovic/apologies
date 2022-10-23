# vim: set ft=bash sw=3 ts=3:

help_demo() {
   echo "- run demo: Run a game with simulated players, displaying output on the terminal"
}

task_demo() {
   run_command pythonscript "from apologies.cli import cli; cli('demo')" "$@"
}

