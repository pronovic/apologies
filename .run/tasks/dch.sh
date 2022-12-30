# vim: set ft=bash sw=3 ts=3 expandtab:

help_dch() {
   # No help - hidden utility feature, sort of equivalent to the Debian 'dch' command
   echo -n ""
}

task_dch() {
   run_command bumpchangelog
   vim "+3" "+startinsert!" Changelog
}

