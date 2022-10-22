run_format() {
   run_command black
   echo ""
   run_command isort
}
