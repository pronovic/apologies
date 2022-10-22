# Tasks

Tasks are high-level actions that can be executed via the `run` script.  They
are implemented in terms of commands.

## Creating a new task

A task is defined by a naming convention.  There is a shell script that
identifies the name of the command.  Within the shell script, there must be two
bash fuctions, `help_<command>` and `task_<command>`.

So, for command called "example", you would create a file
file `.run/tasks/example.sh`.  That file must contain the 
following bash functions:

```bash
help_example() {
   echo "- run example: Description of the example task"
}

task_example() {
   # Put your implementation here
}
```

Tasks are implemented as scripts and not as directories, because in general
they should be fairly simple.

You may use `$REPO_DIR` to refer to the main repository directory,
and `$DOTRUN_DIR` to refer to the `.run` directory within the repository.
