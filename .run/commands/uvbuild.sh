# vim: set ft=bash ts=3 sw=3 expandtab:
# Build release artifacts into the dist/ directory

# The $SOURCE_DATE_EPOCH controls the timestamp on files in the generated sdist.
# See also: https://hatch.pypa.io/1.13/config/build/#reproducible-builds

command_uvbuild() {
   rm -f dist/*

   SOURCE_DATE_EPOCH=$(TZ=UTC date "+%s") uv build --wheel --sdist
   if [ $? != 0 ]; then
      echo "*** Build failed"
      exit 1
   fi

   ls -l dist/

   echo "done"
}

