from topp.utils.introspection import dumb_method
import types

def layer_factory(layer_name, setup=None, teardown=None, bases=()):
    """
    Lets us create zope.testing layers on the fly

    >>> class Layer1:
    ...     @classmethod
    ...     def setUp(cls):
    ...         pass
    
    >>> testing.layer_factory('Layer2', setup=lambda cls:0, teardown=lambda *args: 1)
    <class 'topp.utils.testing.Layer2'>

    >>> layer2 = testing.layer_factory('Layer2', setup=lambda cls:0, teardown=lambda *args: 1, bases=(Layer1,))
    >>> type(layer2)
    <type 'classobj'>
    >>> layer2
    <class topp.utils.testing.Layer2 at ...>
    >>> layer2.__bases__
    (<class __main__.Layer1 at ...>,)

    Now, and example with no bases::

    >>> layer3 = testing.layer_factory('Layer3', setup=lambda cls:0, teardown=lambda *args: 1)
    >>> type(layer3)
    <type 'classobj'>
    >>> layer3.__bases__
    ()
    
    """
    attrs = dict()
    if setup:
        attrs['setUp']=dumb_method(setup)
    if teardown:
        attrs['tearDown']=dumb_method(setup)
    return types.ClassType(layer_name, bases, attrs)
