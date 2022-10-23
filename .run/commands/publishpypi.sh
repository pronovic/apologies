# vim: set ft=bash ts=3 sw=3 expandtab:
# Publish the current tagged code to PyPI and push to GitHub

# Before doing this, you must retrieve and configure a local API token
# For instance: poetry config pypi-token.pypi token --local
# See: https://python-poetry.org/docs/repositories/#configuring-credentials

command_publishpypi() {
   run_command enablekeyring  # or we can't get the token from the keyring

   poetry build
   if [ $? != 0 ]; then
      echo "*** Build step failed."
      exit 1
   fi

   poetry publish
   if [ $? != 0 ]; then
      echo "*** Publish step failed."
      exit 1
   fi

   git push --follow-tags
   if [ $? != 0 ]; then
      exit 1
   fi
}

