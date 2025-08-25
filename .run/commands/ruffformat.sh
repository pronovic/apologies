# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Ruff code formatter

command_ruffformat() {
   echo "Running Ruff formatter..."
   CLICOLOR_FORCE=1 poetry_run ruff format "$@"
   echo "done"
}

