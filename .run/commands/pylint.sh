# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Pylint code checker

command_pylint() {
   echo "Running pylint checks..."

   # On Linux, Pycharm gets confused unless the path is relative to the workspace
   PATH_DIR=$(realpath "$REPO_DIR")
   poetry_run pylint -j 0 $(ls -d src/*) tests | sed "s|^$PATH_DIR/||"

   echo "done"
}

