# vim: set ft=bash ts=3 sw=3:
# Convert a file from UNIX line endings to DOS line endings

command_unix2dos() {
   poetry_run python "$DOTRUN_DIR/commands/unix2dos/unix2dos.py" "$1"
}

