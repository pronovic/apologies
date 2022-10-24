# vim: set ft=bash sw=3 ts=3 expandtab:
# General utility functions for use by the run script

# This is the set of basic tasks that must always exist
BASIC_TASKS="install format checks test suite"
BASIC_TASKS_REGEX="install|format|checks|test|suite"

# Run a command
run_command() {
   local COMMAND

   COMMAND="$1"
   shift 1

   if [ -f "$DOTRUN_DIR/commands/$COMMAND.sh" ]; then
      source "$DOTRUN_DIR/commands/$COMMAND.sh"
      if [ $? != 0 ]; then
         echo "Unable to source command: $COMMAND"
         exit 1
      fi

      command_$COMMAND "$@"
      if [ $? != 0 ]; then
         echo "Command failed: $COMMAND"
         exit 1
      fi
   else
      echo "Unknown command: $COMMAND"
      exit 1
   fi
} 

# Wrap "poetry run", confirming that the command is installed first
poetry_run() {
   local COMMAND

   COMMAND="$1"
   shift 1

   poetry run which "$COMMAND" > /dev/null
   if [ $? != 0 ]; then
      run_command virtualenv
   fi

   poetry run "$COMMAND" "$@"
   if [ $? != 0 ]; then
      echo "Command failed: poetry run $COMMAND $*"
      exit 1
   fi
}

# Get a list of basic tasks
basic_tasks() {
   echo "$BASIC_TASKS"
}

# Get a list of all tasks, excluding basic tasks
all_tasks() {
   cd "$DOTRUN_DIR/tasks" 
   ls *.sh | sed 's/\.sh$//' | sort | egrep -v "$BASIC_TASKS_REGEX"
}

# Check whether a task exists
task_exists() {
   [ -f "$DOTRUN_DIR/tasks/$1.sh" ]
}

# Run a task
run_task() {
   local TASK

   TASK="$1"
   shift 1

   run_command disablekeyring

   source "$DOTRUN_DIR/tasks/$TASK.sh"
   if [ $? != 0 ]; then
      echo "Unable to source task: $TASK"
      exit 1
   fi

   task_$TASK "$@"
   if [ $? != 0 ]; then
      echo "Task failed: $TASK"
      exit 1
   fi
}

# Get the help output for a task
task_help() {
   local TASK
   TASK="$1"
   source "$DOTRUN_DIR/tasks/$TASK.sh"
   if [ $? == 0 ]; then
      help_$TASK
   fi
}

# Setup the runtime environment
setup_environment() {
   DOTRUN_DIR="$REPO_DIR/.run"
   WORKING_DIR=$(mktemp -d)
   trap "rm -rf '$WORKING_DIR'" EXIT SIGINT SIGTERM
}

# Add addendum information to the end of the help output
add_addendum() {
   if [ -f "$REPO_DIR/.run/addendum.sh" ]; then
      bash "$REPO_DIR/.run/addendum.sh"
   fi 
}

