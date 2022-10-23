# vim: set ft=bash ts=3 sw=3:
# Convert a file from DOS line endings to UNIX line endings

command_dos2unix() {
   poetry_run python "$DOTRUN_DIR/commands/dos2unix/dos2unix.py" "$1"
}

