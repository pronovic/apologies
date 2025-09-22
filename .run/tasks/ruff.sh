# vim: set ft=bash sw=3 ts=3 expandtab:

help_ruff() {
   # No help - exists for PyCharm integration
   echo -n ""
}

task_ruff() {
   run_command rufflint
}

