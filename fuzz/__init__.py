"""\
FuzzPy: Fuzzy sets for Python

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

__version__ = (0, 3, 1)

__all__ = ['iset', 'fset', 'fnumber', 'graph', 'fgraph']
__name__ = 'fuzz'

from iset import *
from fset import *
from fnumber import *
from graph import *
from fgraph import *
from plot import *
