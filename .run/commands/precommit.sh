# vim: set ft=bash ts=3 sw=3 expandtab:
# Install pre-commit hooks

command_precommit() {
   echo -n "Installing pre-commit hooks..."
   poetry_run pre-commit install >/dev/null
   echo "done"
}

