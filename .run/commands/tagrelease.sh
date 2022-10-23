# vim: set ft=bash ts=3 sw=3 expandtab:
# Update the changelog and tag a specific version of the code

command_tagrelease() {
   if [ $# != 1 ]; then
      echo "<version> required"
      exit 1
   fi

   VERSION=$(echo "$1" | sed 's/^v//') # so you can use "0.1.5 or "v0.1.5"
   EARLIEST_YEAR=$(git log --pretty="%ci" $(git rev-list --max-parents=0 HEAD) | sed 's/-.*$//g')
   LATEST_YEAR=$(git log -1 --pretty="%ci" | sed 's/-.*$//g')
   DEFAULT_BRANCH=$(git config --get init.defaultBranch)  # works on git > 2.28.0 from 2020
   CURRENT_BRANCH=$(git branch -a | grep '^\*' | sed 's/^\* //')
   COPYRIGHT="${EARLIEST_YEAR}-${LATEST_YEAR}"
   DATE=$(date +'%d %b %Y')
   TAG="v$VERSION" # follow PEP 440 naming convention
   FILES="NOTICE pyproject.toml Changelog"
   MESSAGE="Release v$VERSION to PyPI"

   if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
      echo "*** You are not on $DEFAULT_BRANCH; you cannot release from this branch"
      exit 1
   fi

   git tag -l "$TAG" | grep -q "$TAG"
   if [ $? = 0 ]; then
      echo "*** Version v$VERSION already tagged"
      exit 1
   fi

   head -1 Changelog | grep -q "^Version $VERSION\s\s*unreleased"
   if [ $? != 0 ]; then
      echo "*** Unreleased version v$VERSION is not at the head of the Changelog"
      exit 1
   fi

   poetry version $VERSION
   if [ $? != 0 ]; then
      echo "*** Failed to update version"
      exit 1
   fi

   run_command dos2unix pyproject.toml

   # annoyingly, BSD sed and GNU sed are not compatible on the syntax for -i
   # I failed miserably in all attempts to put the sed command (with empty string) into a variable
   sed --version 2>&1 | grep -iq "GNU sed"
   if [ $? = 0 ]; then
      # GNU sed accepts a bare -i and assumes no backup file
      sed -i "s/^Version $VERSION\s\s*unreleased/Version $VERSION     $DATE/g" Changelog
      sed -i -E "s/(^ *Copyright \(c\) *)([0-9,-]+)( *Kenneth.*$)/\1$COPYRIGHT\3/" NOTICE
   else
      # BSD sed requires you to set an empty backup file extension
      sed -i "" "s/^Version $VERSION\s\s*unreleased/Version $VERSION     $DATE/g" Changelog
      sed -i "" -E "s/(^ *Copyright \(c\) *)([0-9,-]+)( *Kenneth.*$)/\1$COPYRIGHT\3/" NOTICE
   fi

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

   echo ""
   echo "*** Version v$VERSION has been released and commited; you may publish now"
   echo ""
}

