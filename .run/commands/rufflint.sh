# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Ruff linter with no automatic fixes

command_rufflint() {
   echo "Running Ruff linter..."
   poetry_run ruff check --no-fix
   echo "done"
}

