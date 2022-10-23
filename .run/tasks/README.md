# Tasks

Tasks are high-level actions that can be executed via the `run` script.

If you need a custom task for your repository, it's usually simpler to
implement that behavior within the task itself rather than breaking it up
between a task and a command.  This helps make it more obvious that your new
task is repository-specific.

## Required Tasks

The following tasks must always be defined if you want to use the standard
`run` script:

- install
- format
- checks
- test
- suite

These tasks are needed to set up the local development environment, and the
GitHub Actions build also relies on them.  They are called out separately as
"basic tasks" in the help output for the `run` script.  All other tasks are
listed in alphabetical order in a separate section below.  You can change the
definition of these tasks, but they must exist.

Additionally, there are two "hidden" tasks that are not shown in the help
output for the `run` script:

- mypy
- pylint

These tasks exist for easy integration with Pycharm.  If you don't want to use
one of these tools, just change the task to a no-op (i.e. `echo "MyPy is not
used in this repo"`).

## Creating a new task

A task is defined by a naming convention.  There is a bash script that
identifies the name of the task.  Within the bash script, there must be two
bash functions, `help_<task>` and `task_<task>`.

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

Tasks are implemented mostly in terms of commands (using `run_command
<command>`), but you can also run installed tools (i.e. `poetry_run isort`),
run the Python interpreter (using `poetry_run python`), or even just invoke
`poetry` directly.

Commands are supposed to `exit 1` when they encounter a permanent error, so you
don't have to check their result via `$?` when using `run_command`.  Similar
error handling exists when you use `poetry_run`.  If you invoke `poetry`
directly, you must do your own error handling.

You may use `$REPO_DIR` to refer to the main repository directory,
and `$DOTRUN_DIR` to refer to the `.run` directory within the repository.
There is a temporary working directory at `$WORKING_DIR`.

If you change directories as part of your task, you _must_ change back
to the original directory if the task completes successfuly.  This makes
it possible to safely chain together multiple tasks and commands.
