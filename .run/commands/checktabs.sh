# vim: set ft=bash ts=3 sw=3 expandtab:
# Check for tab characters in the source tree

command_checktabs() {
   echo "Checking for tab characters..."

   local result

   cd "$REPO_DIR" # we need to be in the root of the repo for 'git ls-files' to do what we need

   if git rev-parse --git-dir > /dev/null 2>&1; then
      files="$(git ls-files | grep -v '^-$' | grep -v -x -F --file=".tabignore")"
      if [ ! -z "$files" ]; then
         result=$(grep -l "$(printf '\t')" $files)
         if [ $? == 0 ]; then
            echo "❌ Some files contain tab characters:"
            echo ""
            echo "$result"
            echo ""
            exit 1
         fi
      fi
      echo "✅ No tab characters found"
   else
      echo "⛔ Not a Git repository, no checks run"
   fi

   echo "done"
   cd - >/dev/null
}

