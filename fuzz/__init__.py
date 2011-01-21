"""\
FuzzPy: Fuzzy sets for Python

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

__version__ = (0, 4, 2)

__all__ = ['iset', 'fset', 'fnumber', 'graph', 'fgraph', 'visualization']
__name__ = 'fuzz'

from .iset import *
from .fset import *
from .fnumber import *
from .graph import *
from .fgraph import *
from .visualization import *
