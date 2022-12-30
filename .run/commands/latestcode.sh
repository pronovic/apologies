# vim: set ft=bash ts=3 sw=3 expandtab:
# Make sure that the latest code is installed

command_latestcode() {
   poetry install --only-root --all-extras >/dev/null
   if [ $? != 0 ]; then
      echo "*** Failed to install the latest code"
      exit 1
   fi
}

