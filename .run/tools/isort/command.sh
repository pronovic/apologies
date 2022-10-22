# Run the isort import formatter
run_isort() {
   echo "Running isort formatter..."

   poetry run which isort > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run isort $* .
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}
