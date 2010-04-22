"""\
Common initialization code for examples.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

import sys

sys.path.insert(0, '..')

import fuzz
print "FuzzPy imported from '%s'" % fuzz.__path__[0]
