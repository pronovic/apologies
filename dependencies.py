#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab:
# Defines runtime and production dependencies for the project

# Required Python version
PYTHON_REQUIRES = ">=3.7"

# Runtime dependencies
INSTALL_REQUIRES = [ 
]

# Unit test dependencies
TESTS_REQUIRE = [ 
   "pytest>=5.4.1",
   "flexmock>=0.9.4", 
]

# Dump requirements to stdout for use by venv.sh
if __name__ == "__main__":
   if INSTALL_REQUIRES: print(*INSTALL_REQUIRES, sep = "\n")
   if TESTS_REQUIRE: print(*TESTS_REQUIRE, sep = "\n")
