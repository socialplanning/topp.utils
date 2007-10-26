"""
zopeish utils
"""
from Acquisition import aq_inner, aq_parent
from zope.component import adapter, getUtility
from zope.interface import implementer
from topp.featurelets.interfaces import IFeatureletRegistry
from topp.featurelets.interfaces import IFeatureletSupporter

def aq_iface(obj, iface):
    obj = aq_inner(obj)
    while obj is not None and not iface.providedBy(obj):
        obj = aq_parent(obj)
    return obj


