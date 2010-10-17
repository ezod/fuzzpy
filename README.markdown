# FuzzPy - Fuzzy Mathematics for Python


## Overview

FuzzPy is a library for fuzzy sets, fuzzy graphs, and general fuzzy mathematics
for Python.


## Requirements

FuzzPy requires [Python] [1] 2.6 or later.

For visualization (optional), one or more of the following are required:

* [Gnuplot-py] [2] for fuzzy number visualization.
* [PyDot] [4] for graph and fuzzy graph visualizations.

[Epydoc] [3] is required for generating API documentation (optional).


## Documentation and Examples

API documentation can be generated with Epydoc using `python setup.py doc`. This
will create a subdirectory `doc` containing full API documentation in HTML
format.

Examples demonstrating the use of FuzzPy can be found in the `examples`
subdirectory.


## Core Functionality

Unlike most other fuzzy libraries, FuzzPy focuses on pure fuzzy sets as its core
functionality. The `fset` module provides a discrete fuzzy set class `FuzzySet`
which behaves for the most part (and is a subclass of) the built-in Python `set`
type.

The `fgraph` module provides the `FuzzyGraph` class, which is based on our own
`Graph` class (in the `graph` module), and uses fuzzy sets for its vertex and
edge sets. The graph modules also provide various combinatorial optimization
and other graph-related algorithms.

The `fnumber` module provides a series of `FuzzyNumber` subclasses, for fuzzy
subsets of the real numbers. The interface tries to mimic that of the discrete
fuzzy set class as much as possible. This is intended to provide a basis for
future work in fuzzy rule-based systems and the like.


## Visualizations

Starting with v0.4.0, FuzzPy ships with a plugin-based visualization system,
which can produce representations of most of the data structures supported by
FuzzPy, and supports a variety of output formats.

One should consult the examples/visualizations.py to examine several different
use cases, but the typical usage scenario works as such:

        from fuzz.visualization import VisManager
        
        # Create the appropriate plugin automatically
        vis = VisManager.create_backend(data_object)
        (vis_format, vis_data) = uvis.visualize()

        # Write data onto a file
        with open("output.%s" % vis_format, "wb") as fp:
            fp.write(vis_data)


Although the API is designed to be consistent across all plugins, we recommend
consulting the docstrings and source code for plugins you decide to use in
order to learn about the different way you can customize their behaviour, as
well as their available output formats, supported data types, etc.


## Development

FuzzPy is in a relatively early stage of development, and is changing rapidly.
Functional compatibility may be broken between releases, even revisions in some
cases. Once the project is reasonably feature-complete and best practices are
established, the 1.x release series will begin, and the project will transition
into a policy of not breaking functional compatibility across releases with the
same minor version.

If you would like to help with development, please contact Aaron Mavrinac to get
access to the GitHub repositories.

FuzzPy's main contributors are:

* Aaron Mavrinac <mavrin1@uwindsor.ca>
* Xavier Spriet <linkadmin@gmail.com>


### Visualization Plugin Development

If none of the supplied data visualization plugins meet your specific need, it
may be beneficial to write your own, and we encourage you to contribute your
work back to the project if you do so.

Developing a new visualization plugin consists of the following steps:

- Create a new submodule for your plugin inside the vis_plugins directory
- import the `AbstractPlugin` abstract class from the `abc_plugin` submodule
    - `from abc_plugin import AbstractPlugin`
- Construct your plugin class. It must match the `AbstractPlugin` abstract
    class model.
- Add the following variables at the top of the submodule:
    - `VIS_PLUGIN`: Name of your plugin's class
    - `VIS_TYPES`: List of datatype classes supported
    - `VIS_FORMATS`: List of supported output formats for the plugin

Please consult `abc_plugin.AbstractPlugin` class as well as other example 
plugins such as the graph_pydot plugin for an explanation of the required 
methods and their behaviours.



[1]: http://www.python.org
[2]: http://gnuplot-py.sourceforge.net
[3]: http://epydoc.sourceforge.net
[4]: http://code.google.com/p/pydot/
