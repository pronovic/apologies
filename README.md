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

My primary development environment is IntelliJ (or just Vim) on MacOS.

### Packaging and Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage Python
packaging and dependencies.  Most day-to-day tasks (such as running unit 
tests from the command line) are orchestrated through Poetry.  A coding
standard is enforced using [Black](https://github.com/psf/black) and [PyLint](https://www.pylint.org/).

### System Prequisites

Before starting, install the following tools using [Homebrew](https://brew.sh/):

```
brew install python3
brew install poetry
brew install black
brew install pylint
```

If you're not on MacOS, install the similar packages for your platform.

### Common Developer Actions

#### Run unit tests

Run the unit tests via Poetry:

```
poetry run pytest tests
```

Before you commit, make sure the unit tests pass.

#### Run unit tests with coverage

Run the coverage tool via Poetry:

```
poetry run coverage run --rcfile=.coveragerc -m pytest tests && poetry run coverage report -m
```

If you want to see a detailed report, generate the HTML:

```
poetry run coverage html -d .htmlcov && open .htmlcov/index.html
```

#### Run style checker

Run the Pylint style checker via Poetry:

```
poetry run pylint --rcfile=.pylintrc src/apologies tests
```

Before you commit, make sure the code is clean, with no reported warnings.

#### Run the code formatter

Run the Black code formatter:

```
black .
```

Before you commit, make sure the code is properly-formatted.  The code
formatter is run as a pre-commit hook, so this is enforced.
