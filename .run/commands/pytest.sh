# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the pytest unit tests, optionally with coverage

command_pytest() {
   coverage="no"
   html="no"

   while getopts ":ch" option; do
     case $option in
       c)
         coverage="yes"
         ;;
       h)
         html="yes"
         ;;
       ?)
         echo "invalid option -$OPTARG"
         exit 1
         ;;
     esac
   done

   color=""
   if [ "$GITHUB_ACTIONS" == "true" ] && [ "$RUNNER_OS" == "Windows" ]; then
      color="--color no"  # color messes up the terminal on Windows in GHA
   fi

   if [ $coverage == "yes" ]; then
      poetry_run coverage run -m pytest --testdox --force-testdox $color tests
      poetry_run coverage report
      if [ $html == "yes" ]; then
         # Use 'start' on Windows, and 'open' on MacOS and Debian (post-bullseye)
         poetry_run coverage html -d .htmlcov
         $(which start || which open) .htmlcov/index.html 2>/dev/null
      fi
   else
      poetry_run pytest --testdox --force-testdox $color tests
   fi
}

