"""\
FuzzPy visualization plugins abstract base class.

Enforce an interface that visualization plugins must follow, namely:
    - types: most provide a list of supported object types
    - is_supported: must return True if the plugin can run in the current \
    environment.
    - visualize: must return a tuple (format, payload) that contains the \
    visualization format and a string containing the visualization payload.

@author: Xavier Spriet
@contact: linkadmin@gmail.com
@license: LGPL-3
"""

from abc import ABCMeta, abstractmethod


class AbstractPlugin:
    """\
    Abstract plugins class.
    """
    __metaclass__ = ABCMeta
    
    types = []
    """Supported datatypes for visualization."""
    
    @abstractmethod
    def is_supported(self):
        """\
        Return whether the plugin is supported.

        @rtype: C{bool}
        @return: True if the plugin can run in the current environment, False\ 
        otherwise.
        """
        return False
    
    @abstractmethod
    def visualize(self, *args, **kwargs):
        """\
        Main visualization callback.
        
        Draws the visualization in-memory and saves the visualization data
        in a payload string to be returned.
        
        Arbitrary keyword arguments can be passed that will be send to the
        backend object constructor. Future versions will attempt to provide
        a consistent framework for marshalling those keywords.
        
        @rtype: C{tuple}
        @return: (format, payload) tuple. 
        """
        return ('', '')
