# vim: set ft=bash ts=3 sw=3 expandtab:
# Bump the version in the changelog, preparing for a new development cycle

command_bumpchangelog() {
   mv Changelog Changelog.$$
   echo "Version $(poetry version patch --short)     unreleased" > Changelog
   echo "" >> Changelog
   echo $'\t* ' >> Changelog
   echo "" >> Changelog
   cat Changelog.$$ >> Changelog
   rm -f Changelog.$$
}

