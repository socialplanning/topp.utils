"""Entry point utils."""
from zope.dottedname.resolve import resolve

def load_object(epstr):
    """Loads the object represented in entry-point syntax by the
    specified string."""
    if ':' in epstr:
        module, attr = epstr.split(':')
        module = resolve(module)
        return getattr(module, attr)
    return resolve(epstr)
