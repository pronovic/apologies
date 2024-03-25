# vim: set ft=bash ts=3 sw=3 expandtab:
# Show top-level dependencies with outdated constraints

# See: https://github.com/python-poetry/poetry/issues/2684#issuecomment-1076560832

command_outdated() {
   echo "Updating dependencies with current constraints..."
   echo ""
   poetry update
   if [ $? != 0 ]; then
      echo "*** Failed to update dependencies"
      exit 1
   fi

   echo ""
   echo "Checking for outdated constraints..."
   echo ""

   PATTERNS=$(poetry show --tree | grep '^\w' | cut -d' ' -f1 | sed 's/.*/^&\\s/')
   if [ $? != 0 ]; then
      echo "*** Failed to run 'poetry show --tree'" 
      exit 1
   fi

   OUTDATED=$(poetry show --outdated)
   if [ $? != 0 ]; then
      echo "*** Failed to run 'poetry show --outdated'" 
      exit 1
   fi

   MATCHES=$(echo "$OUTDATED" | grep --file=<(echo "$PATTERNS")) 
   if [ $? == 0 ]; then
      echo "$MATCHES" | sed 's/(!)//' | awk '{ printf ( "%-25s %-15s -> %-15s\n", $1, $2, $3 ) }'
   elif [ $? == 1 ]; then
      echo "No outdated constraints found"
   else
      echo "*** Failed to grep for outdated constraints"
      exit 1
   fi
}

