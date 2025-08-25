# vim: set ft=bash sw=3 ts=3 expandtab:

help_format() {
   echo "- run format: Run the code formatters"
}

task_format() {
   run_command ruffformat
   run_command ruffautofix
}

