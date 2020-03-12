# Apologies Python Library

This is a Python library that implements a game similar to the Sorry
board game.  It includes a rudimentary way to play the game, intended
for use by developers and not by end users.

## Developer Notes

### Virtual Environment

To set up the Python virtual environment for development purposes, run the
[`venv.sh`](venv.sh) script.  This installs a Python 3.7 virtual environment
and all of the required dependecies from [`src/setup.py`](src/setup.py).  

The virtual environment is installed at `.python`.  Activate it like this:

```shell
.python/bin/activate
```

If you change the dependencies in [`src/requirements.txt`](src/requirements.txt), 
then re-build the environment. 
