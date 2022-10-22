# vim: set ft=bash sw=3 ts=3:

help_sim() {
   echo "- run sim: Run a simulation to see how well different character input sources behave"
}

task_sim() {
   WORKING=$(mktemp -d -p . tmp.XXXXXXXXX)
   trap "rm -rf '$WORKING'" EXIT SIGINT SIGTERM
   echo 'from apologies.cli import cli; cli("simulation")' > $WORKING/simulation.py
   run_command latestcode
   poetry_run python "$WORKING/simulation.py" $*
}

