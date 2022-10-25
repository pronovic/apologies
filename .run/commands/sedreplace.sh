# vim: set ft=bash ts=3 sw=3 expandtab:
# Call sed in a platform-portable way to replace a string in-place

# Annoyingly, GNU sed and BSD sed are not compatible on the syntax for -i.

command_sedreplace() {
   local replace_expr file

   if [ $# != 2 ]; then
      echo "sedreplace <replace-expr> <file>"
      exit 1
   fi

   replace_expr="$1"
   file="$2"

   sed --version 2>&1 | grep -iq "GNU sed"
   if [ $? == 0 ]; then
      # GNU sed accepts a bare -i and assumes no backup file
      sed -i -E "$replace_expr" "$file"
   else
      # BSD sed requires you to set an empty backup file extension
      sed -i "" -E "$replace_expr" "$file"
   fi
}

