# vim: set ft=bash sw=3 ts=3:
# General utility functions for use by the run script

# Disable the Python keyring
disable_keyring() {
   # Prevent Poetry v1.2.0 from using the Python keyring, which sometimes fails or hangs on Linux
   # See: https://github.com/python-poetry/poetry/issues/2692#issuecomment-1235683370
   export PYTHON_KEYRING_BACKEND="keyring.backends.null.Keyring"
}

# Enable the Python keyring
enable_keyring() {
   # We need to unset this for cases where the keyring is required, like publishing
   unset PYTHON_KEYRING_BACKEND
}

# Run any setup tasks needed before running a task
run_setup() {
   disable_keyring
}

# Run a named tool
run_tool() {
   TOOL="$1"
   shift 1
   source "$SCRIPT_DIR/.run/tools/$TOOL/tool.sh"
   run_$TOOL $*
} 

# Run a named task
run_task() {
   TASK="$1"
   shift 1
   source "$SCRIPT_DIR/.run/tasks/$TASK/task.sh"
   run_$TASK $*
}

# Get the help output for a named task
help_task() {
   TASK="$1"
   source "$SCRIPT_DIR/.run/tasks/$TASK/help.sh"
   help_$TASK $*
}

# Generate help output for the script
generate_help() {
   echo ""
   echo "------------------------------------"
   echo "Shortcuts for common developer tasks"
   echo "------------------------------------"
   echo ""
   echo "Usage: run <task>"
   echo ""
   cd "$SCRIPT_DIR/.run/tasks" 
   for task in $(ls -d * | sort); 
      do help_task $task
   done
   echo ""
}

# Handle command line arguments
handle_arguments() {
   if [ $# -ge 1 ] && [ -d "$SCRIPT_DIR/.run/tasks/$1" ]; then
      set -e
      run_task $*
   else
      generate_help
      exit 1
   fi
}

