#!/bin/bash
# Run the demo in a controlled manner if an X session is available

COMMAND="poetry run python src/scripts/demo --players=3 --mode=ADULT --delay=0.02 --exit"

if [ -z "$DISPLAY" ]; then
   echo "No display set; can't run demo"
   exit 0
fi

which xterm
if [ $? != 0 ]; then
   echo "No xterm available; can't run demo"
   exit 0
fi

set -e -x
xterm -title "apologies demo" -geometry 155x70+0+0 -j -fs 10 -e "$COMMAND"

