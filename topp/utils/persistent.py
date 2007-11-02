from UserDict import DictMixin
from persistent import Persistent
from BTree.OOBTree import OOBTree


class OOBTreeBag(DictMixin, Persistent):
    def __init__(self):
        self._data = OOBTree()
    def __getitem__(self, item):
        return self._data[item]
    def __setitem__(self, item, value):
        self._data[item] = value
    def __delitem__(self, item):
        del self._data[item]
    def keys(self):
        return [x for x in self._data.keys()]
    def lazy_keys(self):
        return self._data.keys()
