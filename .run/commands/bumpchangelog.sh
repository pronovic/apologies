# vim: set ft=bash ts=3 sw=3 expandtab:
# Bump the version in the changelog, preparing for a new development cycle

# If pyproject.toml is configured to use the poetry-dynamic-versioning plugin,
# then you need to have it installed locally, or you will get unexpected results
# from this command.  The new version in the Changelog will always be "0.0.1",
# because all Poetry is aware of is the hardcoded version "0.0.0".

command_bumpchangelog() {
   mv Changelog Changelog.$$
   echo "Version $(poetry version patch --short --dry-run)     unreleased" > Changelog
   echo "" >> Changelog
   echo $'\t* ' >> Changelog
   echo "" >> Changelog
   cat Changelog.$$ >> Changelog
   rm -f Changelog.$$
}

