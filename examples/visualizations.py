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

# Now, we create and populate some graphs - C for crisp, F for fuzzy, U for
# undirected, D for directed.
CU = fuzz.Graph(viter = v, directed = False)
CD = fuzz.Graph(viter = v, directed = True)
FD = fuzz.FuzzyGraph(viter = v, directed = True)
FU = fuzz.FuzzyGraph(viter = v, directed = False)
for FG in [FU, FD]:
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
for CG in [CD, CU]:
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
FN = fuzz.PolygonalFuzzyNumber( \
    [(0.0, 0.0), (3.0, 0.5), (4.0, 0.3), (6.0, 0.8), (7.0, 0.2),
     (8.0, 0.3), (9.0, 0.2), (10.0, 0.7), (11.0, 0.0)])

# For each object, we initialize a plugin -- in this case, the default -- then
# retrieve the visualization payload in string format.
uvis = fuzz.VisManager.create_backend(FU)
(uvis_format, uvis_data) = uvis.visualize()
dvis = fuzz.VisManager.create_backend(FD)
(dvis_format, dvis_data) = dvis.visualize()
cuvis = fuzz.VisManager.create_backend(CU)
(cuvis_format, cuvis_data) = cuvis.visualize()
cdvis = fuzz.VisManager.create_backend(CD)
(cdvis_format, cdvis_data) = cdvis.visualize()
fnvis = fuzz.VisManager.create_backend(FN)
(fnvis_format, fnvis_data) = fnvis.visualize()

# Finally, we save the visualizations, in their proper format, to disk.
with open("fuzzy_graph.%s" % uvis_format, "wb") as fp:
    fp.write(uvis_data)
with open("fuzzy_digraph.%s" % dvis_format, "wb") as fp:
    fp.write(dvis_data)
with open("crisp_graph.%s" % cuvis_format, "wb") as fp:
    fp.write(cuvis_data)
with open("crisp_digraph.%s" % cdvis_format, "wb") as fp:
    fp.write(cdvis_data)
with open("fuzzy_number.%s" % fnvis_format, "wb") as fp:
    fp.write(fnvis_data)
