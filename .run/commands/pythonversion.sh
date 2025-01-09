# vim: set ft=bash ts=3 sw=3 expandtab:
# Display information about the Python version that is in use

command_pythonversion() {
   if [ "$1" == "--short" ]; then
      echo "============================================================"
      echo "Execution environment: $(poetry run python3 --version)"
      echo "============================================================"
      echo ""
   else
      echo "============================================================"
      echo "Execution environment: $(poetry run python3 --version)"
      echo "============================================================"
      poetry env info
      echo ""
      echo "============================================================"
      echo ""
   fi
}

