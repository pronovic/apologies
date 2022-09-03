#!/bin/bash
# Run the demo in a controlled manner if an appropriate terminal is available

DEMO="poetry run python src/scripts/demo --players=3 --mode=ADULT --delay=0.02 --exit"

which xterm
if [ $? == 0 ]; then
   if [ -z "$DISPLAY" ]; then
      echo "Demo will be tested in an xterm"
      set -e -x
      xterm -title "apologies demo" -geometry 155x70+0+0 -j -fs 10 -e "$DEMO"
      exit 0
   fi
fi

if [[ "$OSTYPE" == "darwin"* ]]; then 
   echo "Demo will be tested in a MacOS terminal"
   set -e -x
   $DEMO
   exit 0
fi

echo "No terminal available; demo will not be tested"
exit 0

