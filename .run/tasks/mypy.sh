# vim: set ft=bash sw=3 ts=3 expandtab:

help_mypy() {
   # No help - exists for PyCharm integration
   echo -n ""
}

task_mypy() {
   run_command mypy
}

