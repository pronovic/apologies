# vim: set ft=bash ts=3 sw=3:
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

   if [ $coverage == "yes" ]; then
      poetry_run coverage run -m pytest --testdox tests
      if [ $? != 0 ]; then
         exit 1
      fi

      poetry_run coverage report
      if [ $html == "yes" ]; then
         poetry_run coverage html -d .htmlcov
         $(which start || which open) .htmlcov/index.html 2>/dev/null  # start on Windows, open on MacOS and Debian (post-bullseye)
      fi
   else
      poetry_run pytest --testdox tests
      if [ $? != 0 ]; then
         exit 1
      fi
   fi
}

