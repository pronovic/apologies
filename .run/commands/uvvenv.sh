# vim: set ft=bash ts=3 sw=3 expandtab:
# Install the Python interpreter and virtual environment.

# By default, the Python version is taken from .python-version. At
# runtime, you can override by exporting $UV_PYTHON in your shell.
#
# Switching back and forth between versions can sometimes leave
# leftover junk, like two different python3.x links pointing at the
# same interpreter (one of which is wrong). If I detect this, I
# re-build the virtualenv to fix it.

command_uvvenv() {
   if [ ! -z "$UV_PYTHON" ]; then
      echo -n "Installing virtual environment with UV_PYTHON=$UV_PYTHON..."
   else
      echo -n "Installing virtual environment..."
   fi

   uv python install --quiet
   if [ $? != 0 ]; then
      echo "Command failed: uv python"
      exit 1
   fi

   if [ ! -z "$UV_PYTHON" ]; then
      uv venv --quiet --clear
      if [ $? != 0 ]; then
         echo "Command failed: uv venv"
         exit 1
      fi
   else
      uv venv --quiet --allow-existing
      if [ $? != 0 ]; then
         echo "Command failed: uv venv"
         exit 1
      fi
   fi

   if [ $(/bin/ls .venv/bin/python3.?? 2>/dev/null | wc -l) -gt 1 ]; then
      uv venv --quiet --clear  # clean up leftover junk from switching versions
      if [ $? != 0 ]; then
         echo "Command failed: uv venv"
         exit 1
      fi
   fi

   run_command uvsync
   run_command uvrun python --version
}

