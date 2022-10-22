# Build the Sphinx documentation for apologies.readthedocs.io
run_docs() {
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

   poetry run which sphinx-build > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   cd docs
   poetry run sphinx-build -N -E -a -b html -d _build/doctrees . _build/html 2>&1 | grep -v -F --file=.sphinxignore
   if [ $? != 0 ]; then
      exit 1
   fi

   if [ $open == "yes" ]; then
      $(which start || which open) _build/html/index.html 2>/dev/null  # start on Windows, open on MacOS and Debian (post-bullseye)
   fi
}
