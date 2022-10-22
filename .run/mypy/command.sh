# Run the MyPy code checker
run_mypy() {
   echo "Running mypy checks..."

   poetry run which mypy > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run mypy
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}
