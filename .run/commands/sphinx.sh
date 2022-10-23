# vim: set ft=bash ts=3 sw=3 expandtab:
# Build the Sphinx documentation for readthedocs.io

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
      # Use 'start' on Windows, and 'open' on MacOS and Debian (post-bullseye)
      $(which start || which open) _build/html/index.html 2>/dev/null  
   fi

   cd - >/dev/null
}

