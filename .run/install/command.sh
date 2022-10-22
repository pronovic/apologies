# Setup the virtual environment via Poetry and install pre-commit hooks
run_install() {

   # Install the poetry-plugin-export plugin, used to generate requirements.txt
   poetry self add --quiet poetry-plugin-export
   if [ $? != 0 ]; then
      echo "*** Failed to install Poetry plugin: poetry-plugin-export"
      exit 1
   fi

   # Create and update the virtualenv, synchronizing it to versions in poetry.lock
   poetry install --sync
   if [ $? != 0 ]; then
      echo "*** Failed to install dependencies"
      exit 1
   fi

   # Upgrade embedded packages within the virtualenv
   # This command sometimes returns $?=1 on Windows, even though it succeeds <sigh>
   poetry run pip install --quiet --upgrade pip wheel setuptools 2>/dev/null

   # Install the pre-commit hooks
   poetry run pre-commit install
   if [ $? != 0 ]; then
      echo "*** Failed to install pre-commit hooks"
      exit 1
   fi

}
