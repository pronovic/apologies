# vim: set ft=bash sw=3 ts=3 expandtab:

help_outdated() {
   echo "- run outdated: Find top-level dependencies with outdated constraints"
}

task_outdated() {
   run_command uvoutdated
}

