from UserDict import DictMixin
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from orderedpersistentmapping import OrderedPersistentMapping


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


class KeyedMap(OOBTreeBag):
    """simple btree ish mapping with it's own unique key"""
    def __init__(self, btree=None, key=None):
        self._data = btree
        if not btree: # for migration
            self._data = OOBTree()
        self.key = self.make_key(key)
        
    def make_key(self, input):
        return hash((self, input))


def bbb_keymap(wrap=True, secret=None):
    """auto-migrater"""
    def wrap_func(func): 
        def wrap(*args, **kwargs):
            keymap = func(*args, **kwargs)
            if isinstance(keymap, KeyedMap):
                return KeyedMap(btree=keymap, key=(args, secret))
            return keymap
        return wrap
    if wrap:
        return wrap_func
    else:
        return func
