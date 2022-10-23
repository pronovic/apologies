# vim: set ft=bash sw=3 ts=3 expandtab:

help_sim() {
   echo "- run sim: Run a simulation to see how well different character input sources behave"
}

task_sim() {
   cat << EOF > "$WORKING_DIR/simulation.py"
from apologies.cli import cli
cli("simulation")
EOF

   run_command latestcode
   poetry_run python "$WORKING_DIR/simulation.py" "$@"
}

