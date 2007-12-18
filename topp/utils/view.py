from zope.interface import providedBy
from zope.app.apidoc.component import getRequiredAdapters as get_required
from zope.publisher.interfaces import IRequest
from zope.interface import Interface, implements


class IIgnorableDummy(Interface):
    """go ahead and ignore me"""


def get_view_names(obj, ignore_dummy=False):
    """Gets all view names for a particular object"""
    ifaces = providedBy(obj)
    regs = itertools.chain(*(get_required(iface, withViews=True) for iface in ifaces))
    if ignore_dummy:
        return set(reg.name for reg in regs\
                   if reg.required[-1].isOrExtends(IRequest) \
                   and not IIgnorableDummy.providedBy(reg.value))
    return set(reg.name for reg in regs\
               if reg.required[-1].isOrExtends(IRequest))


class Dummy(BaseView):
    """Creates dummy for blocking the overcreation of deliverance
    paths"""

    def __init__(self, context, request):
        super(Dummy, self).__init__(context, request)
        
    def __call__(self, *args, **kw):
        raise Redirect, self.redirect_url

    @property
    def redirect_url(self):
        return "%s/%s" %(self.area.absolute_url(), "preferences")


class IgnorableDummy(Dummy):
    """a dummy that get_view_names will ignore (for special persistent objects)"""
    implements(IIgnorableDummy)
