"""\
Common initialization code for examples.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""
import os
import os.path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))

import fuzz
print('FuzzPy imported from "%s"\n' % fuzz.__path__[0])
