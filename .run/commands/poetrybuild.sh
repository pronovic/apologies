# vim: set ft=bash ts=3 sw=3 expandtab:
# Build release artifacts into the dist/ directory

# Poetry v2 attaches the epoch timestamp (1970-01-01 00:00) to all of the files
# in the sdist .tar.gz file, rather than the timestamp from the filesystem they
# were sourced from, as was the behavior in Poetry v1.  To work around this,
# I'm setting the $SOURCE_DATE_EPOCH to the current UTC epoch seconds value.
# See also: https://github.com/python-poetry/poetry/issues/10083
#
# Due to limitations in Poetry's [tool.poetry] configuration block, there's no
# simple way to include docs/ in the sdist, while also excluding the generated
# files in docs/_build.  The cleanest workaround is to remove docs/_build before
# running the `poetry build` command.  That's clearly a hack, but there's
# apparently no other alternative.  Technically, this is only necessary for
# projects that build docs, but it's easiest to just always do the cleanup.

command_poetrybuild() {
   echo "Building release artifacts..."

   rm -f dist/*
   rm -rf docs/_build

   poetry version

   SOURCE_DATE_EPOCH=$(TZ=UTC date "+%s") poetry build
   if [ $? != 0 ]; then
      echo "*** Build failed"
      exit 1
   fi

   ls -l dist/

   echo "done"
}

