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
from time import sleep

from ..fnumber import PolygonalFuzzyNumber
from abc_plugin import AbstractPlugin

VIS_PLUGIN = 'FuzzPyGnuplot'
VIS_TYPES = [PolygonalFuzzyNumber]
VIS_FORMATS = ['png']


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
        plot('set terminal %s' % output_format)
        plot('set data style lines')
        tmpdir = tempfile.mkdtemp()
        filename = os.path.join(tmpdir, 'gnuplot-output')
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
