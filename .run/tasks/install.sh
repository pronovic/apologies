# vim: set ft=bash sw=3 ts=3 expandtab:

help_install() {
   echo "- run install: Install the Python virtualenv and pre-commit hooks"
}

task_install() {
   run_command uvvenv
   run_command precommit
}

