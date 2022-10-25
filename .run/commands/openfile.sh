# vim: set ft=bash ts=3 sw=3 expandtab:
# Open a file in the platform-appropriate way

# Use 'start' on Windows, and 'open' on MacOS and Debian (post-bullseye)

command_openfile() {
   if [ $# != 1 ]; then
      echo "openfile <file>"
      exit 1
   fi

   $(which start || which open) "$1" 2>/dev/null
}

