# vim: set ft=bash ts=3 sw=3 expandtab:
# Clean the source tree, removiong the virtualenv and derived data

command_clean() {
   rm -rf .venv
   rm -rf dist
   rm -rf docs/_build
   find . -name "__pycache__" | xargs rm -rf 
}

