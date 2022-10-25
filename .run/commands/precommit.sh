# vim: set ft=bash ts=3 sw=3 expandtab:
# Install pre-commit hooks

command_precommit() {
   echo -n "Installing pre-commit hooks..."
   git -C . rev-parse 2>/dev/null
   if [ $? == 0 ]; then
      poetry_run pre-commit install
   else
      echo "not a Git repository"
   fi
}

