# vim: set ft=bash sw=3 ts=3 expandtab:

help_pylint() {
   # No help - exists for PyCharm integration
   echo -n ""
}

task_pylint() {
   run_command pylint
}

