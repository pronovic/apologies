# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Pylint code checker

command_pylint() {
   echo "Running pylint checks..."

   # On Linux, Pycharm sometimes gets confused unless the path is relative to the workspace
   # This doesn't do anything on Windows (because pylint outputs a Windows-style path), but it doesn't really matter
   PATH_DIR=$(realpath "$REPO_DIR")
   poetry_run pylint -j 0 $(ls -d src/*) tests | sed "s|^$PATH_DIR/||"

   echo "done"
}

