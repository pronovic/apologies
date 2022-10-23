# vim: set ft=bash ts=3 sw=3 expandtab:
# Convert a file from UNIX line endings to DOS line endings

# See: https://stackoverflow.com/a/53657266

command_unix2dos() {
   cat << EOF > "$WORKING_DIR/unix2dos.py"
import sys

DOS = b"\r\n"
UNIX = b"\n"

path = sys.argv[1]

with open(path, "rb") as f:
    content = f.read()

content = content.replace(UNIX, DOS)

with open(path, "wb") as f:
    f.write(content)

sys.exit(0)
EOF

   poetry_run python "$WORKING_DIR/unix2dos.py" "$1"
}

