# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the pytest unit tests, optionally with coverage

command_pytest() {
   local OPTIND OPTARG option coverage html color

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

   shift $((OPTIND -1))  # pop off the options consumed by getopts

   color=""
   if [ "$GITHUB_ACTIONS" == "true" ] && [ "$RUNNER_OS" == "Windows" ]; then
      color="--color no"  # color messes up the terminal on Windows in GHA
   fi

   if [ $coverage == "yes" ]; then
      poetry_run coverage run -m pytest --testdox --force-testdox $color tests
      poetry_run coverage report
      if [ $html == "yes" ]; then
         poetry_run coverage html -d .htmlcov
         run_command openfile .htmlcov/index.html
      fi
   else
      poetry_run pytest --testdox --force-testdox $color tests
   fi
}

