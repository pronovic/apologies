# vim: set ft=bash ts=3 sw=3 expandtab:
# Update all dependencies, or a subset of package dependencies passed in as arguments.

# UV's command line interface here is awkward. When you want to upgrade multiple
# packages, each package needs its own --upgrade-package argument to the uv command.

command_uvupdate() {
   if [ $# == 0 ]; then
      uv lock --upgrade
   else
      uv lock $(for arg in "$@"; do echo -n " --upgrade-package $arg"; done)
   fi
}

