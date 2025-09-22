# vim: set ft=bash sw=3 ts=3 expandtab:

help_rebuild() {
   echo "- run rebuild: Rebuild all dependencies flagged as no-binary-package"
}

task_rebuild() {
   run_command uvrebuild "$@"
}

