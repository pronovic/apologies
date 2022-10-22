# Run the Pylint code checker
run_pylint() {
   echo "Running pylint checks..."

   poetry run which pylint > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run pylint -j 0 src/apologies tests
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}
