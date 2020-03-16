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

```shell
brew install python3
brew install poetry
brew install black
brew install pylint
```

You need to install all of these tools before you can do local development or
commit code using the standard process, due to the pre-commit hooks (see
below).

Optionally, you may also install the following:

```shell
brew install pre-commit   # to adjust pre-commit hooks
brew install make         # if you want to build Sphinx documentation
```

### Pre-Commit Hooks

There are local pre-commit hooks that depend on Black and Pylint, so the code
is properly-formatted and lint-clean when it's checked in.  If you don't
install Black and Pylint as described above, then you won't be able to commit
your changes.

If necessary, you can temporarily [disable a hook](https://pre-commit.com/#temporarily-disabling-hooks)
or even remove the hook with `pre-commit uninstall`.

### Activating the Virtual Environment

Poetry manages the virtual environment used for testing.  Theoretically, the
Poetry `shell` command gives you a shell using that virutalenv.  However, it
doesn't work that well.  Instead, it's simpler to just activate the virtual
environment directly.  The [`run`](run) script has an entry that dumps out the
correct `source` command. Otherwise, see [`notes/venv.sh`](notes/venv.sh) for a way
to set up a global alias that activates any virtualenv found in the current
directory.

### Developer Tasks

The [`run`](run) script provides shortcuts for common developer tasks:

```
$ run --help

------------------------------------
Shortcuts for common developer tasks
------------------------------------

Usage: run <command>

- run install: Setup the virtualenv via Poetry
- run activate: Print command needed to activate the Poetry virtualenv
- run lint: Run the Pylint code checker
- run format: Run the Black code formatter
- run test: Run the unit tests
- run test -c: Run the unit tests with coverage
- run test -ch: Run the unit tests with coverage and open the HTML report
- run tox: Run the broader Tox test suite used by the GitHub CI action
- run docs: Build the Spinx documentation for apologies.readthedocs.io
- run publish: Tag the current code and publish to PyPI
```
