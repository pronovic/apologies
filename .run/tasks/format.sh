# vim: set ft=bash sw=3 ts=3 expandtab:

help_format() {
   echo "- run format: Run the code formatters"
}

task_format() {
   echo ""
   run_command black
   echo ""
   run_command isort
}

