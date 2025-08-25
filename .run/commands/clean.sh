# vim: set ft=bash ts=3 sw=3 expandtab:
# Clean the source tree, removing the virtualenv and other derived data.

command_clean() {
   rm -rf .venv
   rm -rf dist
   rm -rf docs/_build
   find . -name "__pycache__" -type d | xargs rm -rf
}

