# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the MyPy code checker

command_mypy() {
   echo "Running mypy checks..."

   poetry run mypy > "$WORKING_DIR/mypy.output"
   RESULT=$?

   PATH_DIR=$(realpath "$REPO_DIR")
   cat "$WORKING_DIR/mypy.output" | sed "s|^$PATH_DIR/||"  # make paths relative

   if [ $RESULT != 0 ]; then
      exit 1
   fi

   echo "done"
}

