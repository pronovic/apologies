# vim: set ft=bash sw=3 ts=3 expandtab:

help_checks() {
   echo "- run checks: Run the code checkers"
}

task_checks() {
   echo ""
   run_command checktabs
   echo ""
   run_command ruffformat --check
   echo ""
   run_command mypy
   echo ""
   run_command pylint
}

