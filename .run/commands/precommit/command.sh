# vim: set ft=bash ts=3 sw=3:
# Install pre-commit hooks

command_precommit() {
   echo -n "Installing pre-commit hooks..."

   poetry_run pre-commit install >/dev/null
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}

