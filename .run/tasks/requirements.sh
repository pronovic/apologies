# vim: set ft=bash sw=3 ts=3 expandtab:

help_requirements() {
   echo "- run requirements: Regenerate the docs/requirements.txt file"
}

task_requirements() {
   run_command requirements "$@"
}

