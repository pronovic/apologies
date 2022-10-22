# Publish the current code to PyPI and push to GitHub
# Before doing this, you must retrieve and configure a local API token
# For instance: poetry config pypi-token.pypi token --local
# See: https://python-poetry.org/docs/repositories/#configuring-credentials
run_publish() {
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
}
