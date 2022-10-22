# Run the broader Tox test suite used by the GitHub CI action
run_tox() {
   poetry run which tox > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run tox -c .toxrc -e "checks,docs,coverage,demo"
   if [ $? != 0 ]; then
      exit 1
   fi
}
