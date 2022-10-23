# Commands

Commands are the building blocks of tasks.  Any command can be invoked from a
task or another command using `run_command <command>`. 

Normally, commands implement functionality that is general enough to be shared.
If you need a custom task for your repository, it's usually simpler to
implement that behavior within the task itself rather than breaking it up
between a task and a command.  This helps make it more obvious that your new
task is repository-specific, and makes it easier to keep this set of shared
commands up-to-date with the latest improvements.

## Creating a new command

A command is defined by a naming convention.  The directory is the name of the
command.  Within the directory is a bash script called `command.sh`.  That
scipt must define a bash function `command_<command>`.

So, for command called "example", you would create a 
file `.run/commands/example/command.sh` that contains a 
single bash function `command_example`, like this:

```bash
command_example() {
   # Put your implementation here
}
```

Commands are implemented in directories so you can include other scripts or
files alongside them if necessary.  You may use `$REPO_DIR` to refer to the
main repository directory, and `$DOTRUN_DIR` to refer to the `.run` directory
within the repository.  There is a temporary working directory at
`$WORKING_DIR`.

Normal behavior is for a command to `exit 1` if it encounters a permanent
error, to simplify error-handling at the task level.  If you are invoking
commands via `run_command` or tools via `poetry_run`, this happens
automatically.  If you are invoking `poetry` directly, then you must do your
own error-handling.

If you change directories as part of your command, you _must_ change back to
the original directory if the command completes successfuly.  This makes it
possible to safely chain together multiple tasks and commands.
