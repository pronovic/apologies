# vim: set ft=bash ts=3 sw=3 expandtab:
# Build release artifacts into the dist/ directory

# I want the sdist to be generated with a fixed version, so the package can be
# built reproducibly from source even when Git version information is not
# available.  This just worked in Poetry, but it doesn't seem to be possible
# with hatchling.  To work around that, I'm manually adjusting pyproject.toml
# prior to the the sdist build, and then putting it back afterwards.
#
# The $SOURCE_DATE_EPOCH controls the timestamp on files in the generated sdist.
# See also: https://hatch.pypa.io/1.13/config/build/#reproducible-builds

command_uvbuild() {
   local EPOCH VERSION

   EPOCH=$(TZ=UTC date "+%s")
   VERSION=$(uvx uv-dynamic-versioning)

   rm -rf dist/*

   SOURCE_DATE_EPOCH=$EPOCH uv build --wheel
   if [ $? != 0 ]; then
      echo "*** Build failed for wheel"
      exit 1
   fi

   mv pyproject.toml pyproject.toml.$$

   cat pyproject.toml.$$ \
      | sed 's/, "uv-dynamic-versioning (>=.*]$/ ]/' \
      | sed "s/^dynamic = .*$/version = \"$VERSION\"/" \
      > pyproject.toml

   SOURCE_DATE_EPOCH=$EPOCH uv build --sdist
   if [ $? != 0 ]; then
      echo "*** Build failed for sdist"
      mv pyproject.toml.$$ pyproject.toml
      exit 1
   fi

   mv pyproject.toml.$$ pyproject.toml

   ls -l dist/

   echo "done"
}

