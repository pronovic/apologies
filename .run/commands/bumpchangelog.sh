# vim: set ft=bash ts=3 sw=3 expandtab:
# Bump the version in the changelog, preparing for a new development cycle

# This relies on the poetry-dynamic-versioning plugin, which is assumed to be
# installed as a project plugin.  If it's not installed, the new version in the
# Changelog will always be "0.0.1", because all Poetry is aware of is the
# hardcoded version "0.0.0".

command_bumpchangelog() {
   mv Changelog Changelog.$$
   echo "Version $(poetry version patch --short --dry-run)     unreleased" > Changelog
   echo "" >> Changelog
   echo $'\t* ' >> Changelog
   echo "" >> Changelog
   cat Changelog.$$ >> Changelog
   rm -f Changelog.$$
}

