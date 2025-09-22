# vim: set ft=bash ts=3 sw=3 expandtab:
# Run a command via UV.

command_uvrun() {
   local COMMAND

   COMMAND="$1"
   shift 1

   run_command uvsync

   uv run "$COMMAND" "$@"
   if [ $? != 0 ]; then
      echo "Command failed: uv run $COMMAND $@"
      exit 1
   fi
}

