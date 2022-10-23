# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Pylint code checker

command_pylint() {
   echo "Running pylint checks..."

   poetry run pylint -j 0 $(ls -d src/*) tests > "$WORKING_DIR/pylint.output"
   RESULT=$?

   PATH_DIR=$(realpath "$REPO_DIR")
   cat "$WORKING_DIR/pylint.output" | sed "s|^$PATH_DIR/||"  # make paths relative

   if [ $RESULT != 0 ]; then
      exit 1
   fi

   echo "done"
}
