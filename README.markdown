# FuzzPy - Fuzzy Mathematics for Python
Aaron Mavrinac  <mavrin1@uwindsor.ca>

## OVERVIEW

FuzzPy is a library for fuzzy sets, fuzzy graphs, and general fuzzy mathematics
for Python.


## REQUIREMENTS

FuzzPy requires [Python 2.6 or later] [1].

For plotting fuzzy numbers (optional), one of the following:

* [Gnuplot.py] [2]  is required for fuzzy number visualization.
* [Epydoc] [3]      is required for generating documentation (optional).
* [PyDot] [4]       is required for crisp and fuzzy graph visualizations.


## DOCUMENTATION AND EXAMPLES

API documentation can be generated with Epydoc using the provided gendoc.sh
script. This will create a subdirectory 'doc' containing full API documentation
in HTML format.

Examples demonstrating the use of FuzzPy can be found in the 'examples'
subdirectory.


## DEVELOPMENT

FuzzPy is in a relatively early stage of development, and is changing rapidly.
Functional compatibility may be broken between releases, even revisions in some
cases. Once the project is reasonably feature-complete and best practices are
established, the 1.x release series will begin, and the project will transition
into a policy of not breaking functional compatibility across releases with the
same minor version.

If you would like to help with development, please contact primary developer
Aaron Mavrinac to get access to the GitHub repositories and Google Code project
page.


## VISUALIZATIONS

Starting with v0.4.0, FuzzPy now ships with a plugin-based visualization system
that can produce representations of most of the data-structures supported by
FuzzPy as well as a variety of output formats.

One should consult the examples/visualizations.py to examine several different
use-cases, but the typical usage scenario works as such:

        from fuzz.visualization import VisManager
        
        # Create the appropriate plugin automatically
        vis = VisManager.create_backend(data_object)
        (vis_format, vis_data) = uvis.visualize()

        # Write data onto a file
        with open("output.%s" % vis_format, "wb") as fp:
            fp.write(vis_data)


Although the API is designed to be consistent across all plugins, we recommend
consulting the docstrings and source-code for plugins you decide to use in
order to learn about the different way you can customize their behaviour, as
well as their available output formats, supported datatypes, etc...



## VISUALIZATION PLUGIN DEVELOPMENT

If none of the supplied data visualization plugins meet your specific need, you
it might be beneficial to write your own plugin, and we encourage you 
contributing your work back to the project if you do so.

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