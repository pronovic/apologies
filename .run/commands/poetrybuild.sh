# vim: set ft=bash ts=3 sw=3 expandtab:
# Build release artifacts into the dist/ directory

command_poetrybuild() {
   echo "Building release artifacts..."

   rm -f dist/*

   poetry version

   poetry build
   if [ $? != 0 ]; then
      echo "*** Build failed"
      exit 1
   fi

   ls -l dist/

   echo "done"
}

