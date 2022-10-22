# Run a simulation to see how well different character input sources behave
run_sim() {
   poetry run python -c "from apologies.cli import cli" >/dev/null 2>&1
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run python src/scripts/simulation $*
}
