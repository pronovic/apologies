# vim: set ft=bash ts=3 sw=3 expandtab:
# Build release artifacts into the dist/ directory

# Poetry v2 attaches the epoch timestamp (1970-01-01 00:00) to all of the files
# in the sdist .tar.gz file, rather than the timestamp from the filesystem they
# were sourced from, as was the behavior in Poetry v1.  To work around this, I'm
# setting the $SOURCE_DATE_EPOCH to the current UTC epoch seconds value.
# 
# See also: https://github.com/python-poetry/poetry/issues/10083

command_poetrybuild() {
   echo "Building release artifacts..."

   rm -f dist/*

   poetry version

   SOURCE_DATE_EPOCH=$(TZ=UTC date "+%s") poetry build
   if [ $? != 0 ]; then
      echo "*** Build failed"
      exit 1
   fi

   ls -l dist/

   echo "done"
}

