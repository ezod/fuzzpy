#!/usr/bin/env python

from fuzz import __version__
version = "%s.%s.%s" % __version__[0:3]

from setuptools import setup

setup(
    name = "fuzz",
    version = version,
    license = "GPL",
    description = "FuzzPy",
    long_description = "Library for fuzzy sets, fuzzy graphs, and general fuzzy mathematics for Python.",
    author = "Aaron Mavrinac",
    author_email = "mavrin1@uwindsor.ca",
    url = "http://code.google.com/p/fuzzpy",
    keywords = "fuzzy set graph math",
    packages = ['fuzz'],
    zip_safe = False,
)
