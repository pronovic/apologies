# vim: set ft=bash ts=3 sw=3 expandtab:
# Display information about the Python version that is in use

command_pythonversion() {
   echo "============================================================"
   echo "Execution environment: $(run_command uvrun python --version)"
   echo "============================================================"
   echo ""
}

