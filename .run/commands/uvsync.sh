# vim: set ft=bash ts=3 sw=3 expandtab:
# Run UV's synchronize operation.

command_uvsync() {
   uv sync --quiet --all-extras --all-groups --frozen --compile-bytecode "$@"
   if [ $? != 0 ]; then
      echo "Command failed: uv sync"
      exit 1
   fi
}

