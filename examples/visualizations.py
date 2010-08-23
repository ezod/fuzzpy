"""\
Generates Crisp and Fuzzy Graph Visualizations.

@author: Xavier Spriet
@contact: linkadmin@gmail.com
@license: GPL-3
"""

from common import fuzz
from fuzz.visualization import VisManager
from fuzz.fgraph import Graph, FuzzyGraph
from fuzz import vis_plugins

v = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Fuzzy - Undirected
FD = FuzzyGraph(viter = v, directed = True)
# Fuzzy - directed
FU = FuzzyGraph(viter = v, directed = False)
# Crisp - Undirected
CU = Graph(viter = v, directed = False)
# Crisp - Directed
CD = Graph(viter = v, directed = True)

# Populate the fuzzy graphs
for FG in [FU, FD]:
    FG.connect_fuzzy(1, 2, 0.08)
    FG.connect_fuzzy(2, 3, 1.0)
    FG.connect_fuzzy(3, 4, 0.9)
    FG.connect_fuzzy(4, 5, 0.7)
    FG.connect_fuzzy(3, 5, 0.2)
    FG.connect_fuzzy(5, 2, 0.5)
    FG.connect_fuzzy(1, 5, 0.0)
    FG.connect_fuzzy(6, 3, 0.4)
    FG.connect_fuzzy(7, 2, 1.0)
    FG.connect_fuzzy(8, 6, 0.1)
    FG.connect_fuzzy(9, 7, 0.7)
    FG.connect_fuzzy(10, 6, 0.5)
    FG.connect_fuzzy(2, 10, 0.2)

# Populate crisp graphs
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

# Initialize the default plugin and retrieve visualization payload
uvis = VisManager.create_backend(FU)
uvis_data = uvis.visualize()

dvis = VisManager.create_backend(FD)
dvis_data = dvis.visualize()

cuvis = VisManager.create_backend(CU)
cuvis_data = cuvis.visualize()

cdvis = VisManager.create_backend(CD)
cdvis_data = cdvis.visualize()

# Save the payload on the filesystem
with open("fuzzy_graph.png", "wb") as fp:
    fp.write(uvis_data)

with open("fuzzy_digraph.png", "wb") as fp:
    fp.write(dvis_data)

with open("crisp_graph.png", "wb") as fp:
    fp.write(cuvis_data)

with open("crisp_digraph.png", "wb") as fp:
    fp.write(cdvis_data)

