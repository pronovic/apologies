# vim: set ft=bash ts=3 sw=3 expandtab:
# Update all dependencies, or a subset of package dependencies passed in as arguments.

# If you want to rebuild all compiled packages even when upgrading a single package, pass --force-rebuild.
# Each package needs its own --upgrade-package argument to the uv command, which is a bit awkward.

command_uvupdate() {
   if [ $# == 0 ]; then
      uv lock --upgrade
      run_command uvrebuild
   else
      if [ "$1" == "--force-rebuild" ]; then
         shift
         uv lock $(for arg in "$@"; do echo -n " --upgrade-package $arg"; done)
         run_command uvrebuild
      else
         uv lock $(for arg in "$@"; do echo -n " --upgrade-package $arg"; done)
         run_command uvrebuild "$@"
      fi
   fi
}

