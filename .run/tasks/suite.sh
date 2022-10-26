# vim: set ft=bash sw=3 ts=3 expandtab:
# runscript: customized=true

help_suite() {
   echo "- run suite: Run the complete test suite, as for the GitHub Actions CI build"
}

task_suite() {
   run_task install
   run_task checks
   run_task build
   run_task test
   run_task docs
   run_task demo --players=3 --mode=ADULT --delay=0.02 --exit
}

