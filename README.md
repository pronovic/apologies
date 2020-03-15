# Apologies Python Library

![](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)

This is a Python library that implements a game similar to the Sorry
board game.  It includes a rudimentary way to play the game, intended
for use by developers and not by end users.

It also serves as a complete example of how to manage a modern (circa 2020)
Python project, including style checks, code formatting, integration with
IntelliJ, continuous integration at GitHub, etc.

## Developer Notes

### Development Environment

My primary development environment is IntelliJ (or just Vim) on MacOS.  Notes
below assume that environment, although most of this should work the same on
Windows or Linux.

### Packaging and Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage Python
packaging and dependencies.  Most day-to-day tasks (such as running unit 
tests from the command line) are orchestrated through Poetry.  A coding
standard is enforced using [Black](https://github.com/psf/black) and [PyLint](https://www.pylint.org/).

### Developer Prequisites

Before starting, install the following tools using [Homebrew](https://brew.sh/)
or the package manager for your platform:

```
brew install python3
brew install poetry
brew install black
brew install pylint
```

You need to install all of these tools before you can do local development or
commit code using the standard process, due to the pre-commit hooks (see
below).

Optionally, you may also install the following:

```
brew install pre-commit
```

That should not be necessary unless you need to adjust pre-commit hooks.

### Pre-Commit Hooks

There are local pre-commit hooks that depend on Black and Pylint, so the code
is properly-formatted and lint-clean when it's checked in.  If you don't
install Black and Pylint as described above, then you won't be able to commit
your changes.

If necessary, you can temporarily [disable a hook](https://pre-commit.com/#temporarily-disabling-hooks)
or even remove the hook with `pre-commit uninstall`.

### Common Developer Actions

#### Setup the virtual environment

Set up the virutal environment using Poetry:

```
poetry install -v
```

This sets up the virtualenv, installs all of the depenendecies, and also
installs the latest version of the code into the virtualenv.

#### Run the unit tests

Run the unit tests via Poetry:

```
poetry run pytest tests
```

Before you commit, make sure the unit tests pass.

#### Run the unit tests with coverage

Run the coverage tool via Poetry:

```
poetry run coverage run --rcfile=.coveragerc -m pytest tests && poetry run coverage report -m
```

If you want to see a detailed report, generate the HTML:

```
poetry run coverage html -d .htmlcov && open .htmlcov/index.html
```

#### Run the style checker

Run the Pylint style checker via Poetry:

```
poetry run pylint --rcfile=.pylintrc src/apologies tests
```

Before you commit, make sure the code is clean, with no reported warnings.  The
code formatter is run as a pre-commit hook, so this is enforced.

#### Run the code formatter

Run the Black code formatter:

```
black .
```

Before you commit, make sure the code is properly-formatted.  The code
formatter is run as a pre-commit hook, so this is enforced.
