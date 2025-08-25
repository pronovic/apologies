# vim: set ft=bash ts=3 sw=3 expandtab:
# Run the Ruff linter with no automatic fixes

# The command line below is a bit of a hack.  The goal is to generate output
# that's compatible with the PyCharm output filter:
#
#     $FILE_PATH$:$LINE$:$COLUMN.*
#
# However, that requires stripping out some extra junk.  In theory it seems
# like the PyCharm output filter (which is supposed to be a regex) should be
# able to handle this, but I haven't been able to make it work.
#
# See: https://github.com/astral-sh/ruff/issues/19983

command_rufflint() {
   echo "Running Ruff linter..."
   CLICOLOR_FORCE=1 poetry_run ruff check --no-fix | sed 's/ .*-.*-.*>.* //'
   echo "done"
}

