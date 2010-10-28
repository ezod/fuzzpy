#!/usr/bin/env python

from fuzz import __version__
VERSION = "%s.%s.%s" % __version__[0:3]

from setuptools import setup
from distutils.cmd import Command
from shutil import rmtree
from glob import glob
import os
import sys
import epydoc.cli

NAME = 'fuzzpy'
URL = 'http://github.com/ezod/fuzzpy'
PACKAGE = 'fuzz'

class GenerateDoc(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('doc', ignore_errors=True)
        os.mkdir('doc')
        # okay, this is a bit of a hack
        sys.argv = ['epydoc', '-v', '--name', NAME, '--url', URL, '-o', 'doc', PACKAGE]
        options, names = epydoc.cli.parse_arguments()
        epydoc.cli.main(options, names)

setup(
    name = NAME,
    version = VERSION,
    license = "LGPL",
    description = "Library for fuzzy sets, fuzzy graphs, and general fuzzy mathematics for Python.",
    author = "Aaron Mavrinac",
    author_email = "mavrin1@uwindsor.ca",
    url = URL,
    download_url = "http://github.com/downloads/ezod/fuzzpy/fuzzpy-%s.tar.bz2" % VERSION,
    keywords = "fuzzy set graph math",
    packages = [PACKAGE, PACKAGE + ".visplugins"],
    test_suite = "test",
    cmdclass = {'doc': GenerateDoc},
)
