# vim: set ft=bash sw=3 ts=3 expandtab:

help_update() {
   echo "- run update: Update all dependencies, or a subset passed as arguments"
}

task_update() {
   run_command uvupdate "$@"
}

