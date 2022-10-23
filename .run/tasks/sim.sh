# vim: set ft=bash sw=3 ts=3:

help_sim() {
   echo "- run sim: Run a simulation to see how well different character input sources behave"
}

task_sim() {
   run_command pythonscript 'from apologies.cli import cli; cli("simulation")' "$@"
}

