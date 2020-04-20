# Developer Notes

## Development Environment

My primary development environment is IntelliJ (or just Vim) on MacOS, but the
code and the development process should be portable. I've tested on Windows 10
and on Debian buster.

## Installing this Package Elsewhere

Normally, you would install a packaged version of [PyPI](https://pypi.org/project/apologies/).
However, if you've made changes that aren't published, and you want to use them
locally, then the easiest thing to do is build the wheel package and install it
in your virtualenv:

```
$ poetry build
$ source /path/to/bin/activate
$ pip install --force /path/to/repos/apologies/dist/apologies-0.1.11-py3-none-any.whl
```

You may need to do some manual cleanup later once the package is officially published.

## Packaging and Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage Python packaging and dependencies.  Most day-to-day tasks (such as running unit tests from the command line) are orchestrated through Poetry.  

A coding standard is enforced using [Black](https://github.com/psf/black), [isort](https://pypi.org/project/isort/) and [Pylint](https://www.pylint.org/).  Python 3 type hinting is validated using [MyPy](https://pypi.org/project/mypy/).  To reduce boilerplate, classes are defined using [Attrs](https://www.attrs.org/) (see this [rationale](https://glyph.twistedmatrix.com/2016/08/attrs.html)).

## Pre-Commit Hooks

We rely on pre-commit hooks to ensure that the code is properly-formatted,
clean, and type-safe when it's checked in.  The `run install` step described
below installs the project pre-commit hooks into your repository.  These hooks
are configured in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

If necessary, you can temporarily [disable a hook](https://pre-commit.com/#temporarily-disabling-hooks) or 
even remove the hooks with `poetry run pre-commit uninstall`.  However, keep in
mind that the CI build on GitHub enforces these checks, so the build will fail.

## Prequisites

Nearly all prerequisites are managed by Poetry.  All you need to do is make
sure that you have a working Python 3 enviroment and install Poetry itself.  

### MacOS

On MacOS, it's easiest to use [Homebrew](https://brew.sh/):

```
$ brew install python3
$ brew install poetry
```

When you're done, make sure that the `python` on your `$PATH` is Python 3 from
Homebrew (in `/usr/local`).  By default, you'll get the standard Python 2 that
comes with MacOS.

### Debian

First, install Python 3 and related tools:

```
$ sudo apt-get install python3 python3-venv python3-pip
```

Once that's done, make sure Python 3 is the default on your system.  There are
a couple of ways to do this, but using `update-alternatives` as discussed 
on [StackOverflow](https://unix.stackexchange.com/a/410851) is probably 
the best.

Then, install Poetry in your home directory:

```
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Windows

First, download the [Windows installer](https://www.python.org/downloads/windows/) for 
Python 3.7 or later, and install Python on your system.  Make sure that the
`python` on your `$PATH` is Python 3.

Then, start a Powershell prompt and install Poetry in your home directory:

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Activating the Virtual Environment

Poetry manages the virtual environment used for testing.  Theoretically, the
Poetry `shell` command gives you a shell using that virutalenv.  However, it
doesn't work that well.  Instead, it's simpler to just activate the virtual
environment directly.  The [`run`](run) script has an entry that dumps out the
correct `source` command. Otherwise, see [`notes/venv.sh`](notes/venv.sh) for a way
to set up a global alias that activates any virtualenv found in the current
directory.

## Developer Tasks

The [`run`](run) script provides shortcuts for common developer tasks:

```
$ run --help

------------------------------------
Shortcuts for common developer tasks
------------------------------------

Usage: run <command>

- run install: Setup the virtualenv via Poetry and install pre-commit hooks
- run activate: Print command needed to activate the Poetry virtualenv
- run checks: Run the PyLint and MyPy code checkers
- run format: Run the Black code formatter
- run test: Run the unit tests
- run test -c: Run the unit tests with coverage
- run test -ch: Run the unit tests with coverage and open the HTML report
- run tox: Run the broader Tox test suite used by the GitHub CI action
- run docs: Build the Spinx documentation for apologies.readthedocs.io
- run docs -o: Build the Spinx documentation and open in a browser
- run publish: Tag the current code and publish to PyPI
- run demo: Run a game with simulated players, displaying output on the terminal
- run sim: Run a simulation to see how well different character input sources behave
```

## Integration with IntelliJ or PyCharm

For my day-to-day IDE, I use IntelliJ Ultimate with the Python plugin
installed, which is basically equivalent to PyCharm. By integrating Black and
Pylint, most everything important that can be done from a shell environment can
also be done right in IntelliJ.

Unfortunately, it is somewhat difficult to provide a working IntelliJ
configuration that other developers can simply import. There are still some
manual steps required.  I have checked in a minimal `.idea` directory, so at
least all developers can share a single inspection profile, etc.

### Prerequisites

Before going any further, make sure sure that you installed all of the system
prerequisites discussed above.  Then, make sure your environment is in working
order.  In particular, if you do not run the install step, there will be no
virtualenv for IntelliJ to use:

```
$ run install
$ run test
$ run checks
```

Once you have a working shell development environment, **Open** (do not
**Import**) the `apologies` directory in IntelliJ and follow the remaining
instructions below.  (By using **Open**, the existing `.idea` directory will be
retained.)  

> _Note:_ If you get a **Frameworks Detected** message, ignore it for now,
> because IntelliJ might be trying to import some things which aren't really part
> of the project.

### Plugins

Install the following plugins:

|Plugin|Description|
|------|-----------|
|[Python](https://plugins.jetbrains.com/plugin/631-python)|Smart editing for Python code|

### Project and Module Setup

Run the following to find the location of the Python virtualenv managed by
Poetry:

```
$ poetry run which python
```

Right click on the `apologies` project in IntelliJ's project explorer and
choose **Open Module Settings**.  

Click on **Project**.  In the **Project SDK**, select the Python interpreter
virtualenv from above.  Then, under **Project compiler output**, enter `out`.  Then
click **Apply**.

Click on **Modules**.  On the **Sources** tab, find the **Exclude files** box.
Enter the following, and click **Apply**:

```
.coverage;.coveragerc;.github;.htmlcov;.idea;.isort.cfg;.mypyrc;.mypy_cache;.pre-commit-config.yaml;.pylintrc;.pytest_cache;.readthedocs.yml;.tox;.toxrc;build;dist;docs/_build;out;poetry.lock;run
```

On the **Dependencies** tab, select the Python SDK you configured above as the
**Module SDK**, and click **OK**.

You should get a **Frameworks Detected** message again at this point.  If so,
click the **Configure** link and accept the defaults.

### Preferences

Unit tests are written using [Pytest](https://docs.pytest.org/en/latest/), 
and API documentation is written 
using [Google Style Python Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).  
However, neither of these is the default in IntelliJ.

Go to IntelliJ preferences, then select **Tools > Python Integrated Tools**.
Under **Testing > Default test runner**, select _pytest_.  Under 
**Docstrings > Docstring format**, select _Google_. Click **OK**.

### Running Unit Tests

Use **Build > Rebuild Project**, just to be sure that everything is up-to-date.
Then, right click on the `tests` folder in IntelliJ's project explorer and
choose **Run 'pytest in tests'**.  Make sure that all of the tests pass.

### External Tools

Optionally, you might want to set up external tools in IntelliJ for some of
common developer tasks: code reformatting and the PyLint and MyPy checks.  One
nice advantage of doing this is that you can configure an output filter, which
makes the Pylint and MyPy errors clickable in IntelliJ.  To set up external
tools, go to IntelliJ preferences and find **Tools > External Tools**.  Add the
tools as described below.

#### Format Code

|Field|Value|
|-----|-----|
|Name|`Format Code`|
|Description|`Run the Black and isort code formatters`|
|Group|`Apologies Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`format`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Checked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Unchecked_|
|Make console active on message in stderr|_Unchecked_|
|Output filters|_Empty_|

#### Run MyPy Checks

|Field|Value|
|-----|-----|
|Name|`Run MyPy Checks`|
|Description|`Run the MyPy code checks`|
|Group|`Apologies Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`mypy`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN$:.*`|

#### Run Pylint Checks

|Field|Value|
|-----|-----|
|Name|`Run Pylint Checks`|
|Description|`Run the Pylint code checks`|
|Group|`Apologies Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`pylint`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN.*`|

## Running the Demo

While this is primarily a library, it includes a quick'n'dirty console demo
that plays a game with 2-4 automated players.  Here's the help output:

```
$ poetry run demo
usage: demo [-h] [--players PLAYERS] [--mode {STANDARD,ADULT}]
            [--source SOURCE] [--delay DELAY]

Run a game with simulated players, displaying output on the terminal.

optional arguments:
  -h, --help            show this help message and exit
  --players PLAYERS     Number of simulated players in the game
  --mode {STANDARD,ADULT}
                        Choose the game mode
  --source SOURCE       Fully-qualified name of the character source
  --delay DELAY         Delay between computer-generated moves (fractional
                        seconds)

By default, the game runs in STANDARD mode with 4 players. A source is a class
that chooses a player's move.
```

It's simplest to run a demo with the default arguments:

```
$ run demo
```

This runs a really fast game in adult mode with 3 players:

```
$ run demo --players=3 --mode=ADULT --delay=0.1
```

> _Note:_ The demo only works inside a UNIX-style terminal window (like an
> xterm or a MacOS terminal).  It doesn't work in a Windows console, because it
> relies on the curses terminal library.  Some terminals (like [iTerm2](https://www.iterm2.com/)) may
> require extra configuration before the terminal can be resized properly
> (see [StackExchange](https://apple.stackexchange.com/a/47841/249172Z)).
