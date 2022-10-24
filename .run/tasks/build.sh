# vim: set ft=bash sw=3 ts=3 expandtab:

help_build() {
   echo "- run build: Build artifacts in the dist/ directory"
}

task_build() {
   run_command poetrybuild
}

