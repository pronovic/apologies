# vim: set ft=bash ts=3 sw=3:
# Build the Sphinx documentation for apologies.readthedocs.io

command_sphinx() {
   open="no"

   while getopts ":o" option; do
     case $option in
       o)
         open="yes"
         ;;
       ?)
         echo "invalid option -$OPTARG"
         exit 1
         ;;
     esac
   done

   cd docs

   poetry_run sphinx-build -N -E -a -b html -d _build/doctrees . _build/html 2>&1 | grep -v -F --file=.sphinxignore
   if [ $open == "yes" ]; then
      $(which start || which open) _build/html/index.html 2>/dev/null  # start on Windows, open on MacOS and Debian (post-bullseye)
   fi
}

