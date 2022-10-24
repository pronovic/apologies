# vim: set ft=bash ts=3 sw=3 expandtab:
# Install a Poetry plugin 

command_poetryplugin() {
   poetry self add --quiet "$@"
   if [ $? != 0 ]; then
      echo ""
      echo "*** Failed to install Poetry plugin: $*"
      exit 1
   fi
}

