# vim: set ft=bash sw=3 ts=3 expandtab:

help_release() {
   echo "- run release: Release a specific version and tag the code"
}

task_release() {
   run_command tagrelease "$@"
}

