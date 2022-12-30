# vim: set ft=bash ts=3 sw=3 expandtab:
# Create and update the virtualenv, synchronizing it to versions in poetry.lock

command_virtualenv() {
   poetry install --sync --all-extras
   if [ $? != 0 ]; then
      echo "*** Failed to install the virtualenv"
      exit 1
   fi
}

