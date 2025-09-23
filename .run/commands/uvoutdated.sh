# vim: set ft=bash ts=3 sw=3 expandtab:
# List outdated dependency constraints in pyproject.toml, which would prevent upgrading to the latest version.
# Due to the way `uv tree` works, we need to temporarily upgrade all packages before calling it.

command_uvoutdated() {
   echo -n "Checking for outdated constraints..."

   cp uv.lock .uv.lock.saved.$$
   git checkout -q -- uv.lock
   run_command uvsync --quiet
   uv lock --quiet --upgrade

   constraints=$(
      uv tree --all-groups --outdated --depth 1 --color=never 2>/dev/null \
      | grep '^├── .*(latest: .*)$' \
      | sed 's/^├── /   /' \
      | sed 's/(group: .*) //' \
      | sed 's/(latest: /-> /' \
      | sed 's/)$//'
   )

   mv .uv.lock.saved.$$ uv.lock
   run_command uvsync --quiet

   if [ -z "$constraints" ]; then
      echo "none found"
   else
      echo "$(echo "$constraints" | wc -l) found"
      echo ""
      echo "$constraints"
      echo ""
   fi
}
