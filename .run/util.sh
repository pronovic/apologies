# vim: set ft=bash sw=3 ts=3 expandtab:
# General utility functions for use by the run script

# This is the set of basic tasks that must always exist
BASIC_TASKS="install outdated format checks build test suite"
BASIC_TASKS_REGEX="^install$|^outdated$|^format$|^checks$|^build$|^test$|^suite$"

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

# Get a list of additional tasks that have help, excluding basic tasks
additional_tasks() {
   local TASK
   cd "$DOTRUN_DIR/tasks" 
   for TASK in $(ls *.sh | sed 's/\.sh$//' | sort | egrep -v "$BASIC_TASKS_REGEX"); do
      if task_has_help "$TASK"; then
         echo "$TASK"
      fi
   done
   cd - >/dev/null
}

# Check whether a task exists
task_exists() {
   [ -f "$DOTRUN_DIR/tasks/$1.sh" ]
}

# Check whether has a help string
task_has_help() {
   [ ! -z "$(task_help "$1")" ]
}

# Run a task
run_task() {
   local TASK

   TASK="$1"
   shift 1

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

# Return the default Git branch
default_branch() {
   # There is no canonical way to determine the default Git branch.  This version is
   # slow, but seems more reliable than most.  At least by pulling it into a function
   # (vs. a variable) only the commands or tasks that need it will take the hit.
   # See: https://stackoverflow.com/questions/28666357/how-to-get-default-git-branch
   LC_ALL=C git remote show $(git remote) | grep 'HEAD branch' | cut -d' ' -f5
}

# Return the current Git branch
current_branch() {
   git branch -a | grep '^\*' | sed 's/^\* //'
}

# Setup the runtime environment
setup_environment() {
   local EARLIEST_YEAR LATEST_YEAR

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

