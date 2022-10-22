run_check() {
   run_command black --check
   echo ""
   run_command isort --check-only
   echo ""
   run_command mypy
   echo ""
   run_command pylint 
}
