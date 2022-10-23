# vim: set ft=bash sw=3 ts=3:

help_docs() {
   echo "- run docs: Build the Spinx documentation for apologies.readthedocs.io"
   echo "- run docs -o: Build the Spinx documentation and open in a browser"
}

task_docs() {
   run_command sphinx "$@"
}

