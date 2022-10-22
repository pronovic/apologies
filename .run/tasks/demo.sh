# vim: set ft=bash sw=3 ts=3:

help_demo() {
   echo "- run demo: Run a game with simulated players, displaying output on the terminal"
}

task_demo() {
   WORKING=$(mktemp -d)
   trap "rm -rf '$WORKING'" EXIT SIGINT SIGTERM
   echo 'from apologies.cli import cli; cli("demo")' > "$WORKING/demo.py"
   run_command latestcode
   poetry_run python "$WORKING/demo.py" $*
}

