# vim: set ft=bash ts=3 sw=3 expandtab:
# Convert a file from DOS line endings to UNIX line endings

# See: https://stackoverflow.com/a/53657266

command_dos2unix() {
   cat << EOF > "$WORKING_DIR/dos2unix.py"
import sys

DOS = b"\r\n"
UNIX = b"\n"

path = sys.argv[1]

with open(path, "rb") as f:
    content = f.read()

content = content.replace(DOS, UNIX)

with open(path, "wb") as f:
    f.write(content)

sys.exit(0)
EOF

   poetry_run python "$WORKING_DIR/dos2unix.py" "$1"
}

