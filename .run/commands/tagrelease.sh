# vim: set ft=bash ts=3 sw=3 expandtab:
# Update the changelog, tag a specific version of the code, and push the changes

command_tagrelease() {
   local VERSION DATE TAG FILES MESSAGE

   if [ $# != 1 ]; then
      echo "tagrelease <version>"
      exit 1
   fi

   VERSION=$(echo "$1" | sed 's/^v//') # so you can use "0.1.5 or "v0.1.5"
   DATE=$(date +'%d %b %Y')
   TAG="v$VERSION" # follow PEP 440 naming convention
   FILES="NOTICE Changelog"
   MESSAGE="Release v$VERSION"

   # Use $COPYRIGHT_START to override the earliest year found, in case git doesn't contain all history
   EARLIEST_YEAR=${COPYRIGHT_START:-$(git log --pretty="%ci" $(git rev-list --max-parents=0 HEAD) | sed 's/-.*$//g')}
   LATEST_YEAR=$(git log -1 --pretty="%ci" | sed 's/-.*$//g')

   if [ "$EARLIEST_YEAR" == "$LATEST_YEAR" ]; then
      COPYRIGHT="${EARLIEST_YEAR}"
   else
      COPYRIGHT="${EARLIEST_YEAR}-${LATEST_YEAR}"
   fi

   if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
      echo "*** You are not on $DEFAULT_BRANCH; you cannot release from this branch"
      exit 1
   fi

   git tag -l "$TAG" | grep -q "$TAG"
   if [ $? = 0 ]; then
      echo "*** Version v$VERSION already tagged"
      exit 1
   fi

   head -1 Changelog | grep -E -q "^Version $VERSION[[:blank:]][[:blank:]]*unreleased"
   if [ $? != 0 ]; then
      echo "*** Unreleased version v$VERSION is not at the head of the Changelog"
      exit 1
   fi

   run_command sedreplace "s|^Version $VERSION[[:blank:]][[:blank:]]*unreleased|Version $VERSION     $DATE|g" Changelog
   run_command sedreplace "s|(^ *Copyright \(c\) *)([0-9,-]+)( *.*$)|\1$COPYRIGHT\3|" NOTICE

   git diff $FILES

   git commit --no-verify -m "$MESSAGE" $FILES
   if [ $? != 0 ]; then
      echo "*** Commit step failed"
      exit 1
   fi

   git tag -a "$TAG" -m "$MESSAGE"
   if [ $? != 0 ]; then
      echo "*** Tag step failed"
      exit 1
   fi

   git push --follow-tags
   if [ $? != 0 ]; then
      echo "*** Push step failed"
      exit 1
   fi

   echo ""
   echo "*** Version v$VERSION has been tagged"
   echo ""
}

