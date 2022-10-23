# vim: set ft=bash sw=3 ts=3:

# This is a little complicated, because the demo is senstive to terminal size
# and terminal definition.  On MacOS, I run it directly in the terminal where
# 'run demo' was invoked.  On Linux, it's safer to pop an xterm, if one is
# available.  The check for $DISPLAY ensures that we don't try to run this in
# GitHub Actions, where no display is available.

help_demo() {
   echo "- run demo: Run a game with simulated players, displaying output on the terminal"
}

task_demo() {
   WORKING=$(mktemp -d)

   SCRIPT="from apologies.cli import cli; cli('demo')"
   echo "$SCRIPT" > "$WORKING/script.py"

   DEMO="poetry run python $WORKING/script.py $*"

   which xterm
   if [ $? == 0 ]; then
      if [ ! -z "$DISPLAY" ]; then
         echo "Demo will be tested in an xterm"

         xterm -title "apologies demo" -geometry 155x70+0+0 -j -fs 10 -e "$DEMO; rm -rf '$WORKING'"
         if [ $? != 0 ]; then
            exit 1
         fi

         return
      fi
   fi

   if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "Demo will be tested in a MacOS terminal"

      $DEMO
      if [ $? != 0 ]; then
         rm -rf "$WORKING"
         exit 1
      fi

      rm -rf "$WORKING"
      return
   fi

   echo "No terminal available; demo will not be tested"
}

