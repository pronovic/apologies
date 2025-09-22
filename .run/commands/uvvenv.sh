# vim: set ft=bash ts=3 sw=3 expandtab:
# Install the Python interpreter and virtual environment.

# By default, the Python version is taken from .python-version.
# At runtime, you can override this with $UV_PYTHON.

command_uvvenv() {
   echo -n "Installing virtual environment..."

   uv python install --quiet
   if [ $? != 0 ]; then
      echo "Command failed: uv python"
      exit 1
   fi

   uv venv --quiet --allow-existing 
   if [ $? != 0 ]; then
      echo "Command failed: uv venv"
      exit 1
   fi

   run_command uvsync

   echo "done"
}

