run_requirements() {
   poetry export --format=requirements.txt --without-hashes --with dev --output=docs/requirements.txt
   if [ $? != 0 ]; then
      echo "*** Failed to export requirements.txt"
      exit 1
   fi

   poetry run python utils/dos2unix.py docs/requirements.txt
   if [ $? != 0 ]; then
      echo "*** Failed to convert requirements.txt to UNIX line endings"
      exit 1
   fi
}
