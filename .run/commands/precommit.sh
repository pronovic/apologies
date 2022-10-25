# vim: set ft=bash ts=3 sw=3 expandtab:
# Install pre-commit hooks

command_precommit() {
   echo -n "Installing pre-commit hooks..."
   if git rev-parse --git-dir > /dev/null 2>&1; then
      poetry_run pre-commit install
   else
      echo "not a Git repository"
   fi
}

