# vim: set ft=bash ts=3 sw=3 expandtab:
# Return the default Git branch

# There is no canonical way to determine the default Git branch.  This version
# is slow, but seems more reliable than most.  At least by pulling it into a
# command (vs. setting a variable via util.sh), only the commands or tasks that
# need it will take the hit.
#
# See: https://stackoverflow.com/questions/28666357/how-to-get-default-git-branch
 
command_defaultbranch() {
  LC_ALL=C git remote show $(git remote) | grep 'HEAD branch' | cut -d' ' -f5
}
