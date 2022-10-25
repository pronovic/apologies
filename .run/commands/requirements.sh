# vim: set ft=bash ts=3 sw=3 expandtab:
# Generate a requirements.txt file in the docs directory, for use by readthedocs.io

# Unfortunately, we can't just rely on Poetry here.  Poetry wants to generate a
# file that includes our project's lowest compatible version of Python, but
# readthedocs.io can only build with older versions (v3.7 as of this writing,
# even though it's years out of date).  So, we need to modify the generated
# result to make readthedocs.io happy.
#
# The "solution" is to replace whatever lowest Python version Poetry generated
# with "3.7", and hope for the best. That seems to have been working so far,
# but it's fragile and we may eventually run into problems with it.
#
# As of late October of 2022, the GitHub Actions build is having problems
# installing poetry-plugin-export on Windows.  Since Poetry v1.2.0 includes
# this plugin automatically, it's not strictly necessary to install it here.
# For now, it seems simpler to just ignore it.  We can add it back if/when it
# becomes necessary.

command_requirements() {

   local OPTIND OPTARG option check generated

   check="false"

   while getopts "c" option; do
     case $option in
       c)
         check="true"
         ;;
       ?)
         echo "invalid option -$OPTARG"
         exit 1
         ;;
     esac
   done

   if [ "$check" == "true" ]; then
      echo "Checking docs/requirements.txt..."
   else
      echo -n "Generating docs/requirements.txt..."
   fi


   generated="$WORKING_DIR/requirements.txt"

   poetry export --format=requirements.txt --without-hashes --with dev --output="$generated"
   if [ $? != 0 ]; then
      echo ""
      echo "*** Failed to export docs/requirements.txt"
      exit 1
   fi

   run_command sedreplace 's|python_version >= "3\.[0-9][0-9]*"|python_version >= "3.7"|g' "$generated"
   run_command sedreplace 's|python_full_version >= "3\.[0-9][0-9]*(\.[0-9][0-9]*)"|python_version >= "3.7"|g' "$generated"
   run_command dos2unix "$generated"

   if [ "$check" == "true" ]; then
      if diff -q "$generated" docs/requirements.txt >/dev/null 2>&1; then
         echo "✅ No differences found"
         echo "done"
      else
         echo "❌ Differences found"
         echo "Requirements file is out-of-date with poetry.lock; use 'run requirements' and commit your changes."
         exit 1
      fi
   else
      cp -f "$generated" docs/requirements.txt
      echo "done"
   fi

}

