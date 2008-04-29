"""Entry point utils."""
from zope.dottedname.resolve import resolve

def str2obj(epstr):
    module, obj = epstr.split(':')
    module = resolve(module)
    return getattr(module, obj)
