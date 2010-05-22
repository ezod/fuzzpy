#!/bin/sh

echo "Generating documentation for FuzzPy..."
rm -rf doc/
epydoc -v --name FuzzPy --url http://code.google.com/p/fuzzpy -o doc ./fuzz
