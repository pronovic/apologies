# vim: set ft=bash ts=3 sw=3 expandtab:
# Enable the Python keyring

# We need to unset this for cases where the keyring is required, like publishing

command_enablekeyring() {
   unset PYTHON_KEYRING_BACKEND
}

