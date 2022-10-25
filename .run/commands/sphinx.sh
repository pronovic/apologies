# vim: set ft=bash ts=3 sw=3 expandtab:
# Build the Sphinx documentation for readthedocs.io

command_sphinx() {
   local OPTIND OPTARG option open

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
      run_command openfile _build/html/index.html
   fi

   cd - >/dev/null
}

