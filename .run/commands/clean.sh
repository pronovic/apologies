# vim: set ft=bash ts=3 sw=3 expandtab:
# Clean the source tree, removing the virtualenv and other derived data.

command_clean() {
   rm -rf .venv
   rm -rf __pycache__
   rm -rf .pytest_cache
   rm -rf .htmlcov
   rm -rf .coverage*
   rm -rf .tox
   rm -rf .mypy_cache
   rm -rf docs/_build
   rm -rf dist
   rm -rf .poetry
   find . -name "__pycache__" -type d | xargs rm -rf
}

