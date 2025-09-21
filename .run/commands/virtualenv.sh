# vim: set ft=bash ts=3 sw=3 expandtab:
# Create and update the virtualenv, synchronizing it to versions in poetry.lock

command_virtualenv() {
   poetry sync --all-extras --all-groups
   if [ $? != 0 ]; then
      if [ is_windows ]; then
         # Poetry on Windows sometimes fails with: [WinError 5] Access is denied
         # Removing the .poetry directory seems to fix it, for reasons that aren't clear
         rm -rf .poetry
         poetry sync --all-extras --all-groups
         if [ $? != 0 ]; then
            echo "*** Failed to install the virtualenv"
            exit 1
         fi
      else
         echo "*** Failed to install the virtualenv"
         exit 1
      fi
   fi
}

