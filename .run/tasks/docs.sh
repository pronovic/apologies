# vim: set ft=bash sw=3 ts=3 expandtab:

help_docs() {
   echo "- run docs: Build the Sphinx documentation for readthedocs.io"
   echo "- run docs -o: Build the Sphinx documentation and open in a browser"
}

task_docs() {
   run_command virtualenv    # work around the fact that Poetry sometimes uninstalls extras
   run_command sphinx "$@"
}

