# vim: set ft=bash sw=3 ts=3:

help_format() {
   echo "- run format: Run the code formatters"
}

task_format() {
   run_command black
   echo ""
   run_command isort
}

