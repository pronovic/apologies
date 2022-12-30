# vim: set ft=bash sw=3 ts=3 expandtab:

help_release() {
   echo "- run release: Tag and release the code, triggering GHA to publish artifacts"
}

task_release() {
   run_command tagrelease "$@"
}

