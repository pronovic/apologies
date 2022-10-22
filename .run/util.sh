# vim: set ft=bash sw=3 ts=3:
# General utility functions for use by the run script

# Run a command
run_command() {
   COMMAND="$1"
   shift 1

   if [ -f "$DOTRUN_DIR/commands/$COMMAND/command.sh" ]; then
      source "$DOTRUN_DIR/commands/$COMMAND/command.sh"
      if [ $? != 0 ]; then
         exit 1
      fi

      command_$COMMAND $*
      if [ $? != 0 ]; then
         exit 1
      fi
   else
      echo "Unknown command: $COMMAND"
      exit 1
   fi
} 

# Wrap "poetry run", confirming that the command is installed first
poetry_run() {
   COMMAND="$1"
   shift 1

   poetry run which "$COMMAND" > /dev/null
   if [ $? != 0 ]; then
      run_command virtualenv
      if [ $? != 0 ]; then
         exit 1
      fi
   fi

   poetry run "$COMMAND" $*
   if [ $? != 0 ]; then
      exit 1
   fi
}

# Get a list of all tasks
all_tasks() {
   cd "$DOTRUN_DIR/tasks" 
   ls *.sh | sed 's/\.sh$//' | sort
}

# Check whether a task exists
task_exists() {
   [ -f "$DOTRUN_DIR/tasks/$1.sh" ]
}

# Run a task
run_task() {
   TASK="$1"
   shift 1

   run_command disablekeyring

   source "$DOTRUN_DIR/tasks/$TASK.sh"
   if [ $? != 0 ]; then
      exit 1
   fi

   task_$TASK $*
   if [ $? != 0 ]; then
      exit 1
   fi
}

# Get the help output for a task
task_help() {
   TASK="$1"

   source "$DOTRUN_DIR/tasks/$TASK.sh"
   if [ $? != 0 ]; then
      exit 1
   fi

   help_$TASK $*
   if [ $? != 0 ]; then
      exit 1
   fi
}

