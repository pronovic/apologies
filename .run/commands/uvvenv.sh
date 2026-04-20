# vim: set ft=bash ts=3 sw=3 expandtab:
# Install the Python interpreter and virtual environment.

# By default, the Python version is taken from .python-version. At runtime, you
# can override by exporting $UV_PYTHON in your shell.
#
# Originally, I always naively used `uv venv --allow-existing`, under the
# assumption that UV would do the right thing when dealing with an existing
# venv. Unfortunately, while this works ok on Linux and MacOS, it isn't safe on
# Windows.  On that platform, VS Code seems to lock the interpreter, and this
# prevents `uv venv` from overwriting it.  So, the logic below needs to be
# smart about about only replacing the venv when necessary, to avoid that sort
# of conflict.
#
# Switching back and forth between versions with $UV_PYTHON can sometimes leave
# leftover junk, like two different python3.x links pointing at the same
# interpreter (one of which is wrong). If I detect this, I re-build the
# virtualenv to fix it.

command_uvvenv() {
   local desired interpreter installed

   if [ ! -z "$UV_PYTHON" ]; then
      desired="$UV_PYTHON"
   else
      desired=$(cat .python-version)
   fi

   echo -n "Installing .venv for Python $desired..."

   uv python install --quiet
   if [ $? != 0 ]; then
      echo "Command failed: uv python"
      exit 1
   fi

   if [ ! -d .venv ]; then
      uv venv --quiet --clear
      if [ $? != 0 ]; then
         echo "Command failed: uv venv"
         exit 1
      fi
      echo "installed fresh"
   else
      if [ -x .venv/Scripts/python.exe ]; then
         # this is Windows
         interpreter=".venv/Scripts/python.exe"
      else
         # this is Linux, MacOS, or some other UNIX-like operating system
         interpreter=".venv/bin/python"
      fi

      installed=$($interpreter -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
      if [ "$desired" != "$installed" ]; then
         uv venv --quiet --clear
         if [ $? != 0 ]; then
            echo "Command failed: uv venv"
            echo "One possible cause is that an IDE like VS Code has the interpreter locked" # on Windows, anyway
            exit 1
         fi
         echo "version mismatch, reinstalled"
      elif [ $(/bin/ls .venv/bin/python3.?? 2>/dev/null | wc -l) -gt 1 ]; then
         uv venv --quiet --clear
         if [ $? != 0 ]; then
            echo "Command failed: uv venv"
            exit 1
         fi
         echo "appeared corrupt, reinstalled"
      else
         echo "no changes necessary"  # at least, none that we were able to detect
      fi
   fi

   run_command uvsync
   echo "Interpreter is $(run_command uvrun python -VV)"
}

