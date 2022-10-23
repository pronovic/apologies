# vim: set ft=bash ts=3 sw=3 expandtab:
# Generate a requirements.txt file in the docs directory, for use by readthedocs.io

command_requirements() {
   echo -n "Generating docs/requirements.txt..."

   poetry self add --quiet poetry-plugin-export
   if [ $? != 0 ]; then
      echo ""
      echo "*** Failed to install Poetry plugin: poetry-plugin-export"
      exit 1
   fi

   poetry export --format=requirements.txt --without-hashes --with dev --output=docs/requirements.txt
   if [ $? != 0 ]; then
      echo ""
      echo "*** Failed to export docs/requirements.txt"
      exit 1
   fi

   run_command dos2unix docs/requirements.txt

   echo "done"
}

