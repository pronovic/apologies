#!/bin/bash
# vim: set ft=bash:
# Initialize a new project based on the apologies project

usage() {
   echo "Usage: initializer.sh"
   echo "Initializes a new Python library based on apologies"
   echo "You must have Git, Python 3, Poetry, and GNU sed installed first."
   echo "Python 3 is assumed to be on your path as simply 'python'."
}

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
   usage
   exit 0
fi

git --version >/dev/null 2>&1
if [ $? != 0 ]; then
   echo "No 'git' command found"
   exit 1
fi

python --version 2>&1 | grep -q '^Python 3'
if [ $? != 0 ]; then
   echo "No 'python' command found or not Python 3"
   exit 1
fi

poetry --version >/dev/null 2>&1
if [ $? != 0 ]; then
   echo "No 'poetry' command found"
   echo "See: https://python-poetry.org/docs/#installation" 
   exit 1
fi

sed --version 2>&1 | grep -q 'GNU sed'
if [ $? != 0 ]; then
   echo "Requires GNU sed; BSD sed won't work"
   echo "On MacOS, you can install GNU sed with 'brew install gnu-sed'"
   exit 1
fi

if [ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" == "true" ]; then
   echo "Do not run this from within a Git repository"
   exit 1
fi

if [ $# == 0 ]; then
   read -p "Project name: " PROJECT
   read -p "Python package: " PACKAGE
   read -p "One Line Description: " DESCRIPTION
   read -p "Author (name <email>): " AUTHOR
else 
   usage
   exit 1
fi

echo "$AUTHOR" | egrep -q "^.* +<[^>]+>"
if [ $? != 0 ]; then
   echo "Author must be in format \"name <email>\""
   exit 1
fi

if [ -d $PROJECT ]; then
   echo "Error: project $PROJECT already exists"
   exit 1
fi

echo ""
echo "Configuration:"
echo "   PROJECT=$PROJECT"
echo "   PACKAGE=$PACKAGE"
echo "   DESCRIPTION=$DESCRIPTION"
echo "   AUTHOR=$AUTHOR"
echo ""

set -e

# Clone the repository
git clone https://github.com/pronovic/apologies.git $PROJECT
cd $PROJECT

# Remove this initializer script, which does not need to be carried forward into new repos
rm -f notes/initializer.sh

# Re-initialize a fresh repository
rm -rf .git
git init .

# Remove unneeded stuff 
rm -rf .htmlcov .mypy_cache .pytest_cache dist .venv
git check-ignore $(find . -type f -print | grep -v '^\.\/\.git') | xargs rm -f

# Update pyproject.toml
sed -i "s/^name = \"apologies\".*$/name = \"$PROJECT\"/" pyproject.toml
sed -i "s/^version = \".*$/version = \"0.1.0\"/" pyproject.toml
sed -i "s/^description = \".*$/description = \"$DESCRIPTION\"/" pyproject.toml
sed -i "s/^authors = \[.*$/authors = [\"$AUTHOR\"]/" pyproject.toml
sed -i "s/^homepage = \".*$/homepage = \"unset\"/" pyproject.toml
sed -i "s/^repository = \".*$/repository = \"unset\"/" pyproject.toml
sed -i "s/^packages = \[.*$/packages = [ { include = \"$PACKAGE\", from = \"src\" } ]/" pyproject.toml

# Update various configuration files
sed -i "s/apologies/$PACKAGE/" run
sed -i "s/apologies/$PACKAGE/" .coveragerc
sed -i "s/apologies/$PACKAGE/" .mypy.ini
sed -i "s/apologies/$PACKAGE/" .pre-commit-config.yaml

# Update tools.ps1, which as a Powershell file must have DOS line endings
sed -i "s/apologies/$PACKAGE/" utils/tools.ps1
python utils/unix2dos.py utils/tools.ps1

# Stub an empty README.md
echo "# $PROJECT" > README.md
echo "$DESCRIPTION" >> README.md

# Update DEVELOPER.md
sed -i "s/apologies/$REPO/" DEVELOPER.md
sed -i "s/apologies/$PACKAGE/" DEVELOPER.md

# Rename the package
mv src/apologies src/$PACKAGE
sed -i "s/apologies\./$PACKAGE./g" src/$PACKAGE/cli.py
sed -i "s/apologies\.source/$PACKAGE.source/g" src/$PACKAGE/source.py
sed -i "s/apologies\./$PACKAGE./g" src/scripts/*
sed -i "s/apologies\./$PACKAGE./g" tests/*.py

# Install and test the package
./run install
./run format
./run checks
./run test

# Add all of the files to the git repository and commit
git add .
git commit -m "Initial stub based on apologies"

# Give the user a status message
cd ..
echo ""
echo "Repository has been created in: $PROJECT"
ls -ld $PROJECT
echo ""
echo "NOTE: you now need to manually update pyproject.toml."
echo "You should also review and clean up other documentation,"
echo "run script targets, etc. that are no longer appropriate."
echo "The initializer gets you a good starting point, but the"
echo "project is still mostly just a copy of apologies."
echo ""
