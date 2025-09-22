# vim: set ft=bash ts=3 sw=3 expandtab:
# Bump the version in the changelog, preparing for a new development cycle.
# This relies on the uv-dynamic-versioning plugin.

command_bumpchangelog() {
   mv Changelog Changelog.$$
   echo "Version $(uvx --from=semver pysemver bump patch $(uvx uv-dynamic-versioning))     unreleased" > Changelog
   echo "" >> Changelog
   echo $'\t* ' >> Changelog
   echo "" >> Changelog
   cat Changelog.$$ >> Changelog
   rm -f Changelog.$$
}

