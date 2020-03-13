# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab:  
# Python package definition

from setuptools import setup
from setuptools import find_packages

from version import NAME, VERSION
from dependencies import PYTHON_REQUIRES, INSTALL_REQUIRES, TESTS_REQUIRE

setup(
    name=NAME,
    version=VERSION,
    author="Kenneth J. Pronovici",
    author_email="pronovic@ieee.org",
    description="Python code to play a game similar to Sorry",
    long_description="""
This is a Python library that implements a game similar to the Sorry
board game.  It includes a rudimentary way to play the game, intended
for use by developers and not by end users.
""",
    url="https://github.com/pronovic/apologies",
    python_requires= PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    packages=find_packages("src"),
    package_dir={ "": "src" },
    scripts=[ ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers", 
        "Natural Language :: English",
        "Topic :: Games/Entertainment :: Board Games", 
        "Topic :: Software Development :: Libraries",
    ],
)
