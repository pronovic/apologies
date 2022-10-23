# vim: set ft=bash sw=3 ts=3 expandtab:

help_install() {
   echo "- run install: Setup the virtualenv via Poetry and install pre-commit hooks"
}

task_install() {
   run_command virtualenv
   run_command precommit
}

