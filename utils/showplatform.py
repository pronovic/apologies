#!/usr/bin/env python3
# Display information about the current platform, for use in GitHub Actions

import platform
import sys

fields = ["   %s: %s" % i for i in zip(["system", "node", "release", "version", "machine", "processor"], platform.uname()) if i[1]]
print("Python %s" % sys.version)
print("Platform\n%s" % "\n".join(fields))
