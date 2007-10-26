import inspect

def dumb_method(func):
    """dumb rules for applying descriptors

    >>> intr.dumb_method(lambda self: 1) <function <lambda> ...>

    >>> intr.dumb_method(lambda cls: 1)
    <classmethod object at ...>

    >>> intr.dumb_method(lambda porkchop, tomato: 1)
    <staticmethod object at ...>
    """
    spec = inspect.getargspec(func)
    args = spec[0]
    if len(args):
        if args[0]=='self':
            return func
        if args[0]=='cls':
            return classmethod(func)
    return staticmethod(func)
