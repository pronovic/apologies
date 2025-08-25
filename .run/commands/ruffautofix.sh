# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Ruff linter, applying automatic fixes only

command_ruffautofix() {
   echo "Applying Ruff automatic fixes..."
   CLICOLOR_FORCE=1 poetry_run ruff check --fix --fix-only
   echo "done"
}

