"""\
Gnuplot-py visualization plugin for FuzzPy.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import os
import tempfile
import warnings
import inspect
from time import sleep

from ..fnumber import PolygonalFuzzyNumber, TriangularFuzzyNumber, \
        TrapezoidalFuzzyNumber, GaussianFuzzyNumber
from abc_plugin import AbstractPlugin

VIS_PLUGIN = 'FuzzPyGnuplot'
VIS_TYPES = [PolygonalFuzzyNumber, TriangularFuzzyNumber, 
            TrapezoidalFuzzyNumber, GaussianFuzzyNumber]
VIS_FORMATS = {'png': 'png', 'jpg': 'jpeg', 'gif': 'gif', 'pbm': 'pbm',
               'eps': 'postscript eps enhanced'}


class FuzzPyGnuplot(AbstractPlugin):
    """\
    Gnuplot-py visualization plugin for FuzzPy.
    """
    def __init__(self, obj=None, *args, **kwargs):
        """\
        Plugin constructor.

        @param obj: The fuzzy number to visualize.
        @type obj: L{PolygonalFuzzyNumber}
        """
        from Gnuplot import Gnuplot
        self.Gnuplot = Gnuplot
        self._N = obj
        
        if hasattr(self._N, 'to_polygonal'):
            if 'np' in inspect.getargspec(self._N.to_polygonal).args:
                self._N = self._N.to_polygonal(np=50)
            else:
                self._N = self._N.to_polygonal()

    @staticmethod
    def is_supported():
        """\
        Return whether this plugin is supported.

        @return: True if the plugin can run in this environment.
        @rtype: C{bool}
        """
        try:
            import Gnuplot
        except ImportError:
            warnings.warn(("Gnuplot plugin will not run on this system. "
                          "You must install Gnuplot-py first."))
            return False
        return True

    def visualize(self, *args, **kwargs):
        """\
        Gnuplot-py visualization mehod.

        @return: Postscript visualization string.
        @rtype: C{str}
        """
        if kwargs.has_key('format') and kwargs['format'] in VIS_FORMATS:
            output_format = kwargs['format']
        else:
            output_format = 'png'
        plot = self.Gnuplot()
        if output_format in ['eps']:
            # scalable formats do not need size argument
            plot('set terminal %s' % VIS_FORMATS[output_format])
        else:
            # parse size for raster formats
            if kwargs.has_key('size') and len(kwargs['size']) == 2:
                w, h = kwargs['size']
            else:
                w, h = (640, 480)
            plot('set terminal %s size %d,%d' % (VIS_FORMATS[output_format], w, h))
        plot('set style data lines')
        tmpdir = tempfile.mkdtemp()
        filename = os.path.join(tmpdir, 'gnuplot-output' + output_format)
        plot('set output \"%s\"' % filename)
        plot.plot([[p[0], p[1]] for p in self._N.points])
        # FIXME: is there a better way to know when Gnuplot output is ready?
        sleep(0.5)
        tmpfile = open(filename, 'r')
        output_data = tmpfile.read()
        tmpfile.close()
        os.remove(filename)
        os.rmdir(tmpdir)
        return (output_format, output_data)

AbstractPlugin.register(FuzzPyGnuplot)
