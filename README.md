# Apologies Python Library

![](https://img.shields.io/pypi/l/apologies.svg)
![](https://img.shields.io/pypi/wheel/apologies.svg)
![](https://img.shields.io/pypi/pyversions/apologies.svg)
![](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)

This is a Python library that implements a game similar to the Sorry board
game.  It includes a rudimentary way to play the game, intended for use by
developers and not by end users.

It also serves as a complete example of how to manage a modern (circa 2020)
Python project, including style checks, code formatting, integration with
IntelliJ, CI builds at GitHub, and integration with PyPI and Read the Docs.

> *Note:* This is alpha-quality code that is still under active development.
> Interfaces may change without warning until the design stabilizes. 


## Developer Notes

### Development Environment

My primary development environment is IntelliJ (or just Vim) on MacOS, but the
code and the development process should be portable. I've tested on Windows 10
and on Debian buster.

### Packaging and Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage Python
packaging and dependencies.  Most day-to-day tasks (such as running unit 
tests from the command line) are orchestrated through Poetry.  A coding
standard is enforced using [Black](https://github.com/psf/black) 
and [Pylint](https://www.pylint.org/).  Static type checking is implemented
using [MyPy](https://pypi.org/project/mypy/).

### Pre-Commit Hooks

We rely on pre-commit hooks to ensure that the code is properly-formatted,
clean, and type-safe when it's checked in.  The `run install` step described
below installs the project pre-commit hooks into your repository.  These hooks
are configured in [`.pre-commit-config.yaml`](.pre-commit-config.yaml)).

If necessary, you can temporarily [disable a hook](https://pre-commit.com/#temporarily-disabling-hooks)
or even remove the hooks with `poetry run pre-commit uninstall`.  However, keep
in mind that the CI build on GitHub enforces these checks, so the build will fail.

### Prequisites

Nearly all prerequisites are managed by Poetry.  All you need to do is make
sure that you have a working Python 3 enviroment and install Poetry itself.  

#### MacOS

On MacOS, it's easiest to use [Homebrew](https://brew.sh/):

```
$ brew install python3
$ brew install poetry
```

When you're done, make sure that the `python` on your `$PATH` is Python 3 from
Homebrew (in `/usr/local`).  By default, you'll get the standard Python 2 that
comes with MacOS.

#### Debian

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

#### Windows

First, download the [Windows installer](https://www.python.org/downloads/windows/) for 
Python 3.7 or later, and install Python on your system.  Make sure that the
`python` on your `$PATH` is Python 3.

Then, start a Powershell prompt and install Poetry in your home directory:

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

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

- run install: Setup the virtualenv via Poetry and install pre-commit hooks
- run activate: Print command needed to activate the Poetry virtualenv
- run checks: Run the Pylint and MyPy code checkers
- run format: Run the Black code formatter
- run test: Run the unit tests
- run test -c: Run the unit tests with coverage
- run test -ch: Run the unit tests with coverage and open the HTML report
- run tox: Run the broader Tox test suite used by the GitHub CI action
- run docs: Build the Sphinx documentation for apologies.readthedocs.io
- run publish: Tag the current code and publish to PyPI
```

### Integration with IntelliJ or PyCharm

For my day-to-day IDE, I use IntelliJ Ultimate with the Python plugin
installed, which is basically equivalent to PyCharm. By integrating Black and
Pylint, most everything important that can be done from a shell environment can
also be done right in IntelliJ.

Unfortunately, it is somewhat difficult to provide a working IntelliJ
configuration that other developers can simply import. There are still some
manual steps required.  I have checked in a minimal `.idea` directory, so at
least all developers can share a single inspection profile, etc.

#### Prerequisites

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

#### Plugins

Install the following plugins:

|Plugin|Description|
|------|-----------|
|[Python](https://plugins.jetbrains.com/plugin/631-python)|Smart editing for Python code|
|[Pylint](https://plugins.jetbrains.com/plugin/11084-pylint)|Integrates IntelliJ with [Pylint](https://www.pylint.org/)|
|[MyPy](https://plugins.jetbrains.com/plugin/13348-mypy-official-)|Integrates IntelliJ with [MyPy](https://pypi.org/project/mypy/)|

#### Project and Module Setup

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
.coverage;.coveragerc;.github;.htmlcov;.idea;.mypyrc;.pre-commit-config.yaml;.pylintrc;.pytest_cache;.readthedocs.yml;.tox;.toxrc;build;dist;docs/_build;out;poetry.lock;run
```

On the **Dependencies** tab, select the Python SDK you configured above as the
**Module SDK**, and click **OK**.

You should get a **Frameworks Detected** message again at this point.  If so,
click the **Configure** link and accept the defaults.

#### Preferences

Unit tests are written using [Pytest](https://docs.pytest.org/en/latest/), 
and API documentation is written 
using [Google Style Python Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).  
However, neither of these is the default in IntelliJ.

Go to IntelliJ preferences, then select **Tools > Python Integrated Tools**.
Under **Testing > Default test runner**, select _pytest_.  Under 
**Docstrings > Docstring format**, select _Google_. Click **OK**.

#### Running Unit Tests

Use **Build > Rebuild Project**, just to be sure that everything is up-to-date.
Then, right click on the `tests` folder in IntelliJ's project explorer and
choose **Run 'pytest in tests'**.  Make sure that all of the tests pass.

#### Running Pylint Inspections

Find **Pylint** in the toolbar, which is usually on the bottom of the screen
alongside things like **TODO** and **Terminal**.  Click the button with the
tooltip that says **Check Project**.  When the scan completes, the **Scan** tab
should say `Pylint found no problems`.

> _Note:_ If you get an error `Argument list too long` when executing Pylint
> for the entire project, this means that IntelliJ is passing along a huge list
> of in-scope files, even though they're not needed.  Make sure you excluded
> the correct list of directories when configuring the module above (especially
> the large `.tox` directory).

#### Running MyPy Inspections

Find **MyPy Terminal** in the toolbar, which is usually on the bottom of the
screen alongside things like **TODO** and **Terminal**.  Right-click in the
window and select **Configure Plugin**.  In the **Mypy command** box, fill in
something like this:

```
/usr/local/bin/poetry run mypy --config-file=.mypyrc src/apologies tests
```

You will have to adjust the path to `poetry` to match your system.  Click
**OK**.  Then, click the **Run** button.  The status on the bottom of the
window should say `PASSED`.

#### External Tools

Optionally, you might want to set up [Black](https://github.com/psf/black) as
an external tool.  Once this is done, you can reformat an individual file or
the entire project using the same rules that will be applied by the commit hook
or by `run format`.  

If you want to do this, first install Black on your system, for instance:

```
$ brew install black
```

Then, follow the official [instructions](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea) to 
point IntelliJ at the location of `black` on your system.
