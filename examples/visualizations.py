"""\
Visualizations - this example demonstrates the generation of visualizations for
various data types.

@author: Xavier Spriet
@contact: linkadmin@gmail.com
@license: GPL-3
"""

from common import fuzz

# First, let's create a set of vertices.
v = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

sets = {}

# Now, we create and populate some graphs - C for crisp, F for fuzzy, U for
# undirected, D for directed.
sets['crisp_undirected_graph'] = fuzz.Graph(viter = v, directed = False)
sets['crisp_directed_graph'] = fuzz.Graph(viter = v, directed = True)
sets['fuzzy_directed_graph'] = fuzz.FuzzyGraph(viter = v, directed = True)
sets['fuzzy_undirected_graph'] = fuzz.FuzzyGraph(viter = v, directed = False)

# Populate the graphs
for FG in [sets['fuzzy_undirected_graph'], sets['fuzzy_directed_graph']]:
    FG.connect(1, 2, 0.08)
    FG.connect(2, 3, 1.0)
    FG.connect(3, 4, 0.9)
    FG.connect(4, 5, 0.7)
    FG.connect(3, 5, 0.2)
    FG.connect(5, 2, 0.5)
    FG.connect(1, 5, 0.0)
    FG.connect(6, 3, 0.4)
    FG.connect(7, 2, 1.0)
    FG.connect(8, 6, 0.1)
    FG.connect(9, 7, 0.7)
    FG.connect(10, 6, 0.5)
    FG.connect(2, 10, 0.2)
for CG in [sets['crisp_directed_graph'], sets['crisp_undirected_graph']]:
    CG.connect(1, 2)
    CG.connect(2, 3)
    CG.connect(3, 4)
    CG.connect(4, 5)
    CG.connect(3, 5)
    CG.connect(5, 2)
    CG.connect(1, 5)
    CG.connect(6, 3)
    CG.connect(7, 2)
    CG.connect(8, 6)
    CG.connect(9, 7)
    CG.connect(10, 6)
    CG.connect(2, 10)

# We'll also create a polygonal fuzzy number.
sets['polygonal'] = fuzz.PolygonalFuzzyNumber( \
    [(0.0, 0.0), (3.0, 0.5), (4.0, 0.3), (6.0, 0.8), (7.0, 0.2),
     (8.0, 0.3), (9.0, 0.2), (10.0, 0.7), (11.0, 0.0)])

sets['trapezoidal'] = fuzz.TrapezoidalFuzzyNumber((1.0, 2.0), (0.0, 3.0))

sets['triangular'] = fuzz.TriangularFuzzyNumber(1.0, (0.0, 3.0))

sets['gaussian'] = fuzz.GaussianFuzzyNumber(1.0, 0.2)

for (name, obj) in sets.items():
    vis = fuzz.VisManager.create_backend(obj)
    (vis_format, data) = vis.visualize()
    
    with open("%s.%s" % (name, vis_format), "wb") as fp:
        fp.write(data)
