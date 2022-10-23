# vim: set ft=bash ts=3 sw=3 expandtab:
# Disable the Python keyring

# This prevents Poetry v1.2.0 from using the Python keyring, which sometimes fails or hangs on Linux.
# See: https://github.com/python-poetry/poetry/issues/2692#issuecomment-1235683370

command_disablekeyring() {
   export PYTHON_KEYRING_BACKEND="keyring.backends.null.Keyring"
}

