# vim: set ft=bash sw=3 ts=3:

# This is a little complicated, because the demo is senstive to terminal size
# and terminal definition.  On MacOS, I run it directly in the terminal where
# 'run demo' was invoked.  On Linux, it's safer to pop an xterm, if one is
# available.  We never run this in GitHub Actions, because there's never any
# real cursor-addressable terminal available there.

help_demo() {
   echo "- run demo: Run a game with simulated players, displaying output on the terminal"
}

task_demo() {
   cat << EOF > "$WORKING_DIR/demo.py"
from apologies.cli import cli
cli("demo")
EOF

   DEMO="poetry run python $WORKING_DIR/demo.py $*"

   which xterm >/dev/null 2>&1
   if [ $? == 0 ]; then
      if [ ! -z "$DISPLAY" ] && [ -z "$GITHUB_ACTIONS" ]; then
         echo ""
         echo "Demo will be run in a standalone xterm"

         run_command latestcode

         xterm -title "apologies demo" -geometry 155x60+0+0 -j -fs 10 -e "$DEMO"
         if [ $? != 0 ]; then
            exit 1
         fi

         return
      fi
   fi

   if [[ "$OSTYPE" == "darwin"* ]] && [ -z "$GITHUB_ACTIONS" ]; then
      echo ""
      echo "Demo will be run in a MacOS terminal"

      run_command latestcode

      $DEMO
      if [ $? != 0 ]; then
         exit 1
      fi

      return
   fi

   echo ""
   echo "No usable terminal available; demo cannot be run"
}

