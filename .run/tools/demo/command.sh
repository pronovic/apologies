# Run a game with simulated players, displaying output on the terminal
run_demo() {
   poetry run python -c "from apologies.cli import cli" >/dev/null 2>&1
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run python src/scripts/demo $*
}

