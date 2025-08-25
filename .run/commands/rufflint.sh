# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Ruff linter with no automatic fixes

# The command line below is a bit of a hack.  The goal is to generate output
# that's compatible with the PyCharm output filter, which expects this:
#
#     $FILE_PATH$:$LINE$
#
# However, right now ruff generates some extra stuff at the front of the line,
# ("  --> "), which needs to be stripped so PyCharm will recognize the pattern.
# In theory it seems like it should be possible to do this entirely within the
# PyCharm output filter, without needing sed, but I haven't been able to make
# it work.
#
# Note that the extra .* in the regex below is needed to handle the ANSI color
# escape sequences, which aren't immediately obvious.
#
# See: https://github.com/astral-sh/ruff/issues/19983

command_rufflint() {
   echo "Running Ruff linter..."

   # normally we would just run the command, but the $() subshell messes with error handling
   OUTPUT=$(CLICOLOR_FORCE=1 poetry_run ruff check --no-fix 2>&1)
   if [ $? != 0 ]; then
      echo "$OUTPUT" | sed 's/ *.*-->.* //'
      exit 1
   fi

   echo "$OUTPUT"
   echo "done"
}

