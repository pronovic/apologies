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

*Note:* This is alpha-quality code that is still under active development.
Interfaces may change without warning until the design stabilizes. 

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
$ brew install python3
$ brew install poetry
$ brew install black
$ brew install pylint
```

You need to install all of these tools before you can do local development or
commit code using the standard process, due to the pre-commit hooks (see
below).

Optionally, you may also install the following:

```
$ brew install pre-commit   # to adjust pre-commit hooks
$ brew install make         # if you want to build Sphinx documentation
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
order.  In particular, if you do not run the setup step, there will be no
virtualenv for IntelliJ to use:

```
$ run setup
$ run test
$ run lint
```

Once you have a working shell development environment, **Open** (do not
**Import**) the `apologies` directory in IntelliJ and follow the remaining
instructions below.  (By using **Open**, the existing `.idea` directory will be
retained.)  

_Note:_ If you get a **Frameworks Detected** message, ignore it for now,
because IntelliJ might be trying to import some things which aren't really part
of the project.

#### Plugins

Install the following plugins:

|Plugin|Description|
|------|-----------|
|[Python](https://plugins.jetbrains.com/plugin/631-python)|Smart editing for Python code|
|[Pylint](https://plugins.jetbrains.com/plugin/11084-pylint)|Integrates IntelliJ with [Pylint](https://www.pylint.org/)|

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
.coverage;.coveragerc;.github;.htmlcov;.idea;.pre-commit-config.yaml;.pylintrc;.pytest_cache;.readthedocs.yml;.tox;.toxrc;build;dist;docs/_build;out;poetry.lock;run
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

#### External Tools

Finally, set up [Black](https://github.com/psf/black) as an external
tool.  See the [instructions](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea).
Once this is done, you can reformat an individual file or the entire project
using the same rules that will be applied by the commit hook.
