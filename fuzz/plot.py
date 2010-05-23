"""\
Fuzzy number plotting module.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

def plot_polygonal_fuzzy_number(number, plotter = 'gnuplot'):
    """\
    Plots a polygonal fuzzy number.

    @param number: The fuzzy number to plot.
    @type number: L{PolygonalFuzzyNumber}
    @param plotter: The external plotting library to use.
    @type plotter: C{str}
    """
    if plotter == 'gnuplot':
        from Gnuplot import Gnuplot
        plot = Gnuplot()
        plot('set data style lines')
        plot.plot([[p[1], p[1]] for p in number.points])
        raw_input("Press a key to continue...")
