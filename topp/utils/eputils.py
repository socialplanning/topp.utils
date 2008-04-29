"""Entry point utils."""
from zope.dottedname.resolve import resolve

def str2obj(epstr):
    if ':' in epstr:
        module, obj = epstr.split(':')
        module = resolve(module)
        return getattr(module, obj)
    return resolve(epstr)
