# vim: set ft=bash sw=3 ts=3 expandtab:

help_publish() {
   echo "- run publish: Publish the current code to PyPI and push to GitHub"
}

task_publish() {
   run_command publishpypi
}

