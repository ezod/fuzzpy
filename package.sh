#!/bin/bash

VERSION=`python -c "from fuzz import __version__; print '%d.%d.%d' % __version__"`

cd ..
cp -a fuzzpy fuzzpy-$VERSION
rm -rf fuzzpy-$VERSION/doc fuzzpy-$VERSION/.git fuzzpy-$VERSION/.gitignore fuzzpy-$VERSION/fuzz/*.pyc
tar cjvf fuzzpy-$VERSION.tar.bz2 fuzzpy-$VERSION
cd fuzzpy-$VERSION
python setup.py register
cd ..
rm -rf fuzzpy-$VERSION
cd fuzzpy
./gendoc.sh
cd doc
zip -r ../../fuzzpy-doc-$VERSION.zip .
cd ..
echo ""
echo "Now, upload fuzzpy-$VERSION.tar.bz2 and fuzzpy-doc-$VERSION.zip to Google"
echo "Code, and update the API docs on PyPI with fuzzpy-doc-$VERSION.zip."
