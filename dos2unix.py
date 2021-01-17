#!/usr/bin/env python3
# vim: set ft=python ts=4 sw=4:
# Convert a file from DOS line endings to UNIX line endings
# See: https://stackoverflow.com/a/53657266

import sys

DOS = b"\r\n"
UNIX = b"\n"

if len(sys.argv) != 2:
    print("poetry run dos2unix.py <file>")
    sys.exit(1)

path = sys.argv[1]

with open(path, "rb") as f:
    content = f.read()

content = content.replace(DOS, UNIX)

with open(path, "wb") as f:
    f.write(content)

sys.exit(0)
