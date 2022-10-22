# vim: set ft=bash ts=3 sw=3:
# Check for tab characters in the source tree

command_checktabs() {
   echo "Checking for tab characters..."

   ORIG="$PWD"
   trap "cd '$ORIG'" EXIT SIGINT SIGTERM

   cd "$REPO_DIR" # we need to be in the root of the repo for 'git ls-files' to do what we need

   result=$(grep -l "$(printf '\t')" $(git ls-files | grep -v -x -F --file=".tabignore"))
   if [ $? == 0 ]; then
      echo "*** Error: Some files contain tab characters:"
      echo "${result}"
      exit 1
   fi

   echo "✅ No tabs found"
   echo "done"
}

