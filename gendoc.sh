#!/bin/sh

echo "Generating documentation for FuzzPy..."
rm -rf doc/
epydoc --name FuzzPy --url http://www.mavrinac.com/index.cgi?page=fuzzpy -o doc ./fuzz
