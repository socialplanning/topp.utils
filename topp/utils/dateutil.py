from DateTime import DateTime as zdt
from datetime import datetime as pydt
from timezones import *

def zdt2pydt(zdt):
    """Takes in a Zope DateTime and returns a coincident Python datetime.
    Preserves timezone, discards milliseconds."""

    offset = zdt.tzoffset()/3600 - zdt._isDST
    tzmap = {-5: Eastern, -6: Central, -7: Mountain, -8: Pacific}
    timezone = tzmap[offset] #TODO implement non-continental-US timezones

    return pydt(zdt.year(), zdt.month(), zdt.day(), zdt.hour(),
                zdt.minute(), int(zdt.second()), 0, timezone)


def pydt2zdt(pydt):
    timezone = pydt.tzinfo and pydt.tzinfo.stdname or None # XXX dst?
    args = list(pydt.timetuple()[:6]) + [0] + [timezone]
    return zdt(*args)

def zdtstr2pydt(s):
    return pydt.now() # TODO


def pydt2localtz(pydt):
    """Converts the datetime given to one in the local time zone."""
    return pydt # TODO

