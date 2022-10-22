# Commands

Commands are the building blocks of tasks.  Any command can be invoked from a
task using `run_command <command>`. 

Normally, commands implement functionality that is general enough to be shared.
If you need a custom task for your repository, it's usually simpler to just
implement that behavior within the task itself.

## Creating a new command

A command is defined by a naming convention.  The directory is the name of the
command.  Within the directory is a file `command.sh`.  That file must define a
bash function `command_<command>`.

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
within the repository.

