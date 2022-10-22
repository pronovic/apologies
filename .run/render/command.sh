# Render a board via the render script
run_render() {
   poetry run python -c "from apologies.cli import cli" >/dev/null 2>&1
   if [ $? != 0 ]; then
      run_install
   fi

   poetry run python src/scripts/render
}

