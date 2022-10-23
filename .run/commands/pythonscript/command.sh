# vim: set ft=bash ts=3 sw=3:
# Run an inline Python script using the Poetry Python interpreter

# This just seems to work better if I run it from a script file on disk rather
# than with 'python -c'.

command_pythonscript() {
   SCRIPT="$1"
   shift 1

   WORKING=$(mktemp -d)
   trap "rm -rf '$WORKING'" EXIT SIGINT SIGTERM
   echo "$SCRIPT" > "$WORKING/script.py"

   run_command latestcode
   poetry_run python "$WORKING/script.py" "$@"
}

