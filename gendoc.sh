#!/bin/sh

echo "Generating documentation for FuzzPy..."
rm -rf doc/
epydoc -v --name FuzzPy --url http://www.mavrinac.com/index.cgi?page=fuzzpy -o doc ./fuzz
