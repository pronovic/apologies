# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the MyPy code checker

command_mypy() {
   echo "Running mypy checks..."

   # On Linux, Pycharm gets confused unless the path is relative to the workspace
   PATH_DIR=$(realpath "$REPO_DIR")
   poetry_run mypy 2>&1 | sed "s|^$PATH_DIR/||"

   echo "done"
}

