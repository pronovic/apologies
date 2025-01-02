# vim: set ft=bash ts=3 sw=3 expandtab:
# Return the current Git branch
 
command_currentbranch() {
   git branch -a | grep '^\*' | sed 's/^\* //'
}

