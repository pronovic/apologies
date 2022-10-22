# vim: set ft=bash sw=3 ts=3:

help_checks() {
   echo "- run checks: Run the code checkers"
}

task_checks() {
   echo ""
   run_command checktabs
   if [ $? != 0 ]; then
      exit 1
   fi

   echo ""
   run_command black --check
   if [ $? != 0 ]; then
      exit 1
   fi

   echo ""
   run_command isort --check-only
   if [ $? != 0 ]; then
      exit 1
   fi

   echo ""
   run_command mypy
   if [ $? != 0 ]; then
      exit 1
   fi

   echo ""
   run_command pylint
   if [ $? != 0 ]; then
      exit 1
   fi
}

