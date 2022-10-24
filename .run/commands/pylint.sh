# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Pylint code checker

# We generate relative paths in the output to make integration with Pycharm work better

command_pylint() {
   echo "Running pylint checks..."

   local OPTIND OPTARG option tests template

   tests="tests"
   template="{path}:{line}:{column} - {C} - ({symbol}) - {msg}"

   while getopts "t" option; do
     case $option in
       t)
         tests=""  # -t means to ignore the tests
         ;;
       ?)
         echo "invalid option -$OPTARG"
         exit 1
         ;;
     esac
   done

   shift $((OPTIND -1))  # pop off the options consumed by getopts

   poetry_run pylint --msg-template="$template" -j 0 "$@" $(ls -d src/*) $tests
   echo "done"
}
