# Developer Notes

## Supported Platforms

This code should work equivalently on MacOS, Linux, and Windows.  However, the
included demo does not run on Windows, because it needs the UNIX-only curses
library for screen drawing.

## Packaging and Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage Python packaging and dependencies.  Most day-to-day tasks (such as running unit tests from the command line) are orchestrated through Poetry.

A coding standard is enforced using [Black](https://pypi.org/project/black/), [isort](https://pypi.org/project/isort/) and [Pylint](https://pypi.org/project/pylint/).  Python 3 type hinting is validated using [MyPy](https://pypi.org/project/mypy/).  To reduce boilerplate, classes are defined using [Attrs](https://www.attrs.org/) (see this [rationale](https://glyph.twistedmatrix.com/2016/08/attrs.html)).

To add dependencies use `poetry add package` (for runtime dependencies) or `poetry add --group dev package` (for development environment dependencies).

To update dependencies, use `poetry update`.  This will update all of the dependencies without taking you past any major version changes that are likely to be incompatible.  If you want to update a single package, use `poetry update package`. If you want to update past a major version change, either specify the version like `poetry add package=^2.0.3` or get the latest with `poetry add package@latest`.  [PEP 508](https://peps.python.org/pep-0508/) specifications are also supported.

## Vulnerability Scanning

Previously, I used the Safety scanner as part of my pre-commit hooks and GitHub Actions, to identify vulnerabilities in Python dependencies.  This functionality was removed in [PR #33](https://github.com/pronovic/apologies/pull/33).  Even though Safety is distributed under the liberal [MIT license](notes/safety/license.png), and the PyPI package page [documents that Safety can be used in this manner](notes/safety/usage.png), the PyUp organization behind Safety now claims that this usage is not allowed.  (See this [bizarre email thread](notes/safety/email.md) &mdash; it has some hallmarks of a phishing email, but appears to be legitimate.)  Despite my repeated attempts to clarify what I was doing wrong, PyUp's representative never offered any specifics.  Given PyUp's unfriendly behavior, I recommend that you avoid using Safety and rely instead on other tools, such as GitHub's own Dependabot service.

## Continuous Integration (CI)

I use [GitHub Actions](https://docs.github.com/en/actions/quickstart) for CI.  See [.github/workflows/test-suite.yml](.github/workflows/test-suite.yml) for the definition of the workflow, and go to the [Actions tab](https://github.com/pronovic/apologies/actions) to see what actions have been executed.  The workflow is implemented in terms of the shared `poetry-build-and-test` workflow in the [pronovic/gha-shared-actions](https://github.com/pronovic/gha-shared-workflows) repository.  The workflow was originally developed here, and eventually refactored out when I started sharing the same process across multiple repositories.

The workflow is kicked off for all PRs, and also when code is merged to master.  It uses a matrix build and runs the same test suite on a combination of platforms (Windows, MacOS, Linux) and Python versions.  The test suite in GitHub Actions is implemented by the same `run suite` command that you would use locally. Coverage data is uploaded to coveralls.io (see discussion below).

## Third-Party Integration

There is third-party integration with [readthedocs.io](https://readthedocs.io/) (to publish documentation) and [coveralls.io](https://coveralls.io/) (to publish code coverage statistics).

Both of these services make integration very straightforward.  For readthedocs, integration happens via a [GitHub webhook](https://docs.github.com/en/github/extending-github/about-webhooks).  You first create an account at readthedocs.io.  Then, you import your repository, which creates a webhook in GitHub for your repository.  Once the webhook has been created, readthedocs is notified whenever code is pushed to your repository, and a build is kicked off on their infrastructure to generate and publish your documentation.  Configuration is taken from a combination of [.readthedocs.yml](.readthedocs.yml) and preferences that you set for your repository in the readthedocs web interface.  See the readthedocs.io [documentation](https://docs.readthedocs.io/en/stable/guides/platform.html) for more information.

For coveralls.io, integration happens via a [GitHub App](https://docs.github.com/en/developers/apps/about-apps) rather than a webhook.  Like with readthedocs, you first create an account at coveralls.io.  Next, you grant the Coveralls application permissions to your GitHub organization, and select which repositories should be enabled.  Unlike with readthedocs, you need to generate coverage information locally and upload it to coverage.io.  This happens as a part of the CI workflow.  There are several steps in the [shared workflow](https://github.com/pronovic/gha-shared-workflows/blob/master/.github/workflows/poetry-build-and-test.yml), taken more-or-less verbatim from the coveralls.io [documentation](https://coveralls-python.readthedocs.io/en/latest/usage/index.html).

## Pre-Commit Hooks

I rely on pre-commit hooks to ensure that the code is properly-formatted,
clean, and type-safe when it's checked in.  The `run install` step described
below installs the project pre-commit hooks into your repository.  These hooks
are configured in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

The pre-commit hooks run on all files for every commit.  I prefer this approach
because it ensures that the pre-commit hooks are running exactly the same
checks as the GitHub Actions build, via exactly the same `run checks` command.

This behavior can sometimes be annoying, especially if you want to do
incremental commits into a PR branch on partially-complete code. In that
situation, I find that it works best to use `run checks` to run the checks
manually. Then, I do my incremental commits with `--no-verify`, to temporarily
skip the pre-commit hooks altogether. As long as I fix all of the problems in
my local branch before pushing to GitHub, I don't get a failed PR build in
GitHub Actions. I always squash-merge my PRs, so those incremental commits that
don't meet the code quality standards never end up in the master branch.

An alternative approach is for you to adjust the pre-commit hooks so that the
checks are only run on files staged for commit.  If you want to do this, you
will need to run the steps invidually rather than using `run checks`, something
like this:

```yaml
fail_fast: true
repos:
  - repo: local
    hooks:
      - id: system
        name: Black
        entry: poetry run black
        types: [python]
        language: system
```

In this case, you can use `pre-commit run --all-files` to run the hooks
against your entire project rather than just the files staged for commit.

## Line Endings

The [`.gitattributes`](.gitattributes) file controls line endings for the files
in this repository.  Instead of relying on automatic behavior, the
`.gitattributes` file forces most files to have UNIX line endings.

## Python's Init File

I've chosen to export some frequently used classes in [`__init__.py`](src/apologies/__init__.py) to
flatten the namespace and make the library more approachable.  This isn't something
I've done before, but I noticed this pattern being followed in some other libraries
and it seemed to be worthwhile.  This [article](https://towardsdatascience.com/whats-init-for-me-d70a312da583) was
helpful in understanding the options and common practices.  Unfortunately, Sphinx
does not do a good job of documenting the init file, so this doesn't really simplify
things for users as much as I had hoped.

## Prerequisites

Nearly all prerequisites are managed by Poetry.  All you need to do is make
sure that you have a working Python 3 enviroment and install Poetry itself.

### Poetry Version

The project is designed to work with Poetry >= 1.3.0.  If you already have an older
version of Poetry installed on your system, uninstall it before following the setup
process below:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --uninstall
```

See the [Announcing Poetry 1.2.0](https://python-poetry.org/blog/announcing-poetry-1.2.0/)
blog post for more information.

### MacOS

On MacOS, it's easiest to use [Homebrew](https://brew.sh/) to install Python:

```
brew install python3
```

Once that's done, make sure the `python` on your `$PATH` is Python 3 from
Homebrew (in `/usr/local`), rather than the standard Python 2 that comes with
MacOS.

Although Poetry can also be installed from Homebrew, it works better to use
to [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer):

```
curl -sSL https://install.python-poetry.org | python3 -
```

> _Note:_ The installer prints the location of the installed `poetry` script.
> Make sure to add this to your `$PATH`, otherwise you won't be able to run it.

### Debian

First, install Python 3 and related tools:

```
sudo apt-get install python3 python3-venv python3-pip
```

Next, make sure that the `python` interpreter on your `$PATH` is Python 3.

If you are using Debian _bullseye_ or later (first released in August 2021),
then Python 2 is deprecated and Python 3 is the primary Python on your system.
However, by default there is only a `python3` interpreter on your `$PATH`, not
a `python` interpreter.  To add the `python` interpreter, use:

```
sudo apt-get install python-is-python3
```

For earlier releases of Debian where both Python 2 and Python 3 are available,
the process is a little more complicated.  The approach I used before upgrading
to _bullseye_ was based on `update-alternatives`, as discussed on
[StackExchange](https://unix.stackexchange.com/a/410851).

Next, install Poetry using the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer):

```
curl -sSL https://install.python-poetry.org | python3 -
```

> _Note:_ The installer prints the location of the installed `poetry` script.
> Make sure to add this to your `$PATH`, otherwise you won't be able to run it.

### Windows

First, install Python 3 from your preferred source, either a standard
installer or a meta-installer like Chocolatey.  Make sure the `python`
on your `$PATH` is Python 3.

Next, install Poetry using the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer):

```
curl -sSL https://install.python-poetry.org | python -
```

> _Note:_ The installer prints the location of the installed `poetry` script.
> Make sure to add this to your `$PATH`, otherwise you won't be able to run it.

The development environment (the `run` script, etc.) expects a bash shell
to be available.  On Windows, it works fine with the standard Git Bash.

## Developer Tasks

The [`run`](run) script provides shortcuts for common developer tasks:

```
$ ./run --help

------------------------------------
Shortcuts for common developer tasks
------------------------------------

Basic tasks:

- run install: Setup the virtualenv via Poetry and install pre-commit hooks
- run format: Run the code formatters
- run checks: Run the code checkers
- run build: Build artifacts in the dist/ directory
- run test: Run the unit tests
- run test -c: Run the unit tests with coverage
- run test -ch: Run the unit tests with coverage and open the HTML report
- run suite: Run the complete test suite, as for the GitHub Actions CI build

Additional tasks:

- run demo: Run a game with simulated players, displaying output on the terminal
- run docs: Build the Sphinx documentation for readthedocs.io
- run docs -o: Build the Sphinx documentation and open in a browser
- run release: Tag and release the code, triggering GHA to publish artifacts
- run sim: Run a simulation to see how well different character input sources behave
```

## Running the Simulation

This runs a simulation on the standard `RewardV1InputSource`:

```
./run sim apologies.source.RewardV1InputSource
```

Output is written to `simulation.csv`.  You can specify any source in 
the [`apologies.source`](src/apologies/source.py) module.

## Running the Demo

While this is primarily a library, it includes a quick'n'dirty console demo
that plays a game with 2-4 automated players.  This demo works only on
UNIX-like platforms that support the curses library.  Here's the help output:

```
$ ./run demo
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

This runs a really fast game in adult mode with 3 players:

```
./run demo --players=3 --mode=ADULT --delay=0.1
```

The demo only works inside a UNIX-style terminal window, like an xterm or a 
MacOS terminal.  You might be able to get it to work in an SSH session, depending 
on your terminal emulator.  As of 2022, it sort of renders in PuTTY, but does 
not work at all in a Windows Terminal.  Your terminal window must be at least 
155x58 in size.  If your terminal window is too small, the demo will refuse to run.

## Integration with PyCharm

Currently, I use [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download) as 
my day-to-day IDE.  By integrating Black and Pylint, most everything important
that can be done from a shell environment can also be done right in PyCharm.

PyCharm offers a good developer experience.  However, the underlying configuration
on disk mixes together project policy (i.e. preferences about which test runner to
use) with system-specific settings (such as the name and version of the active Python 
interpreter). This makes it impossible to commit complete PyCharm configuration 
to the Git repository.  Instead, the repository contains partial configuration, and 
there are instructions below about how to manually configure the remaining items.

### Prerequisites

Before going any further, make sure sure that you have installed all of the system
prerequisites discussed above.  Then, make sure your environment is in working
order.  In particular, if you do not run the install step, there will be no
virtualenv for PyCharm to use:

```
./run install && ./run suite
```

### Open the Project

Once you have a working shell development environment, **Open** (do not
**Import**) the `apologies` directory in PyCharm, then follow the remaining
instructions below.  By using **Open**, the existing `.idea` directory will be
retained and all of the existing settings will be used.

### Interpreter

As a security precaution, PyCharm does not trust any virtual environment
installed within the repository, such as the Poetry `.venv` directory. In the
status bar on the bottom right, PyCharm will report _No interpreter_.  Click
on this error and select **Add Interpreter**.  In the resulting dialog, click
**Ok** to accept the selected environment, which should be the Poetry virtual
environment.

### Project Structure

Go to the PyCharm settings and find the `apologies` project.  Under 
**Project Structure**, mark both `src` and `tests` as source folders.  In 
the **Exclude Files** box, enter the following:

```
LICENSE;NOTICE;PyPI.md;.coverage;.coveragerc;.github;.gitignore;.gitattributes;.htmlcov;.idea;.isort.cfg;.mypy.ini;.mypy_cache;.pre-commit-config.yaml;.pylintrc;.pytest_cache;.readthedocs.yml;.tabignore;build;dist;docs/_build;out;poetry.lock;poetry.toml;run;.run;.venv
```

When you're done, click **Ok**.  Then, go to the gear icon in the project panel 
and uncheck **Show Excluded Files**.  This will hide the files and directories 
in the list above.

### Tool Preferences

In the PyCharm settings, go to **Editor > Inspections** and be sure that the
**Project Default** profile is selected.

Unit tests are written using [Pytest](https://docs.pytest.org/en/latest/),
and API documentation is written
using [Google Style Python Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).  However, 
neither of these is the default in PyCharm.  In the PyCharm settings, go to 
**Tools > Python Integrated Tools**.  Under **Testing > Default test runner**, 
select _pytest_.  Under **Docstrings > Docstring format**, select _Google_.

### Running Unit Tests

Right click on the `tests` folder in the project explorer and choose **Run
'pytest in tests'**.  Make sure that all of the tests pass.  If you see a slightly
different option (i.e. for "Unittest" instead of "pytest") then you probably 
skipped the preferences setup discussed above.  You may need to remove the
run configuration before PyCharm will find the right test suite.

### External Tools

Optionally, you might want to set up external tools for some of common
developer tasks: code reformatting and the PyLint and MyPy checks.  One nice
advantage of doing this is that you can configure an output filter, which makes
the Pylint and MyPy errors clickable.  To set up external tools, go to PyCharm
settings and find **Tools > External Tools**.  Add the tools as described
below.

#### Linux or MacOS

On Linux or MacOS, you can set up the external tools to invoke the `run` script
directly.

##### Shell Environment

For this to work, it's important that tools like `poetry` are on the system
path used by PyCharm.  On Linux, depending on how you start PyCharm, your
normal shell environment may or may not be inherited.  For instance, I had to
adjust the target of my LXDE desktop shortcut to be the script below, which
sources my profile before running the `pycharm.sh` shell script:

```sh
#!/bin/bash
source ~/.bash_profile
/opt/local/lib/pycharm/pycharm-community-2020.3.2/bin/pycharm.sh
```

##### Format Code

|Field|Value|
|-----|-----|
|Name|`Format Code`|
|Description|`Run the code formatters`|
|Group|`Developer Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`format`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Checked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Unchecked_|
|Make console active on message in stderr|_Unchecked_|
|Output filters|_Empty_|

##### Run MyPy Checks

|Field|Value|
|-----|-----|
|Name|`Run MyPy Checks`|
|Description|`Run the MyPy code checks`|
|Group|`Developer Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`mypy`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN$:.*`|

##### Run Pylint Checks

|Field|Value|
|-----|-----|
|Name|`Run Pylint Checks`|
|Description|`Run the Pylint code checks`|
|Group|`Developer Tools`|
|Program|`$ProjectFileDir$/run`|
|Arguments|`pylint`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN.*`|

#### Windows

On Windows, PyCharm has problems invoking the `run` script.  The trick is to
invoke the Bash interpreter and tell it to invoke the `run` script.  The
examples below assume that you have installed Git Bash in its standard location
under `C:\Program Files\Git`.  If it is somewhere else on your system, just
change the path for `bash.exe`.

##### Format Code

|Field|Value|
|-----|-----|
|Name|`Format Code`|
|Description|`Run the code formatters`|
|Group|`Developer Tools`|
|Program|`powershell.exe`|
|Arguments|`& 'C:\Program Files\Git\bin\bash.exe' "./run" format | Out-String`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Checked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Unchecked_|
|Make console active on message in stderr|_Unchecked_|
|Output filters|_Empty_|

##### Run MyPy Checks

|Field|Value|
|-----|-----|
|Name|`Run MyPy Checks`|
|Description|`Run the MyPy code checks`|
|Group|`Developer Tools`|
|Program|`powershell.exe`|
|Arguments|`& 'C:\Program Files\Git\bin\bash.exe' "./run" mypy | Out-String`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN$:.*`|

##### Run Pylint Checks

|Field|Value|
|-----|-----|
|Name|`Run Pylint Checks`|
|Description|`Run the Pylint code checks`|
|Group|`Developer Tools`|
|Program|`powershell.exe`|
|Arguments|`& 'C:\Program Files\Git\bin\bash.exe' "./run" pylint | Out-String`|
|Working directory|`$ProjectFileDir$`|
|Synchronize files after execution|_Unchecked_|
|Open console for tool outout|_Checked_|
|Make console active on message in stdout|_Checked_|
|Make console active on message in stderr|_Checked_|
|Output filters|`$FILE_PATH$:$LINE$:$COLUMN.*`|

## Release Process

### Documentation

Documentation at [Read the Docs](https://apologies.readthedocs.io/en/stable/)
is generated via a GitHub hook.  So, there is no formal release process for the
documentation.

### Code

Code is released to [PyPI](https://pypi.org/project/apologies/).  There is a
partially-automated process to publish a new release.

> _Note:_ In order to publish code, you must must have push permissions to the
> GitHub repo.

Ensure that you are on the `master` branch.  Releases must always be done from
`master`.

Ensure that the `Changelog` is up-to-date and reflects all of the changes that
will be published.  The top line must show your version as unreleased:

```
Version 0.1.29     unreleased
```

Run the release command:

```
./run release 0.1.29
```

This command updates `NOTICE` and `Changelog` to reflect the release version
and release date, commits those changes, tags the code, and pushes to GitHub.
The new tag triggers a GitHub Actions build that runs the test suite, generates
the artifacts, publishes to PyPI, and finally creates a release from the tag.
