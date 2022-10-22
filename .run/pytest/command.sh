# Run the unit tests, optionally with coverage
run_pytest() {
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

   poetry run which pytest > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   if [ $coverage == "yes" ]; then
      poetry run coverage run -m pytest --testdox tests
      if [ $? != 0 ]; then
         exit 1
      fi

      poetry run coverage report
      if [ $html == "yes" ]; then
         poetry run coverage html -d .htmlcov
         $(which start || which open) .htmlcov/index.html 2>/dev/null  # start on Windows, open on MacOS and Debian (post-bullseye)
      fi
   else
      poetry run pytest --testdox tests
      if [ $? != 0 ]; then
         exit 1
      fi
   fi
}
