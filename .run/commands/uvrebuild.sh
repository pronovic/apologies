# vim: set ft=bash ts=3 sw=3 expandtab:
# Rebuild all no-binary-package dependencies, or a subset of package dependencies passed-in as arguments.
# This is done by clearing the packages out of cache, forcing UV to rebuild them.

command_uvrebuild() {
   local packages 

   if [ $# -gt 0 ]; then
      packages="$@"
   else
      packages="$(grep '^no-binary-package' pyproject.toml | sed 's/^no-binary-package = //' | sed 's/[][,"]//g')"
   fi

   uv cache clean $packages
   if [ $? != 0 ]; then
      echo "Command failed: uv cache clean $packages"
      exit 1
   fi

   run_command uvsync --reinstall
}

