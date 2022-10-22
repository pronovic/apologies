# Run the black code formatter
run_black() {
   echo "Running black formatter..."

   poetry run which black > /dev/null
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run black $* .
   if [ $? != 0 ]; then
      exit 1
   fi

   echo "done"
}
