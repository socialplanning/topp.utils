from persistent.mapping import PersistentMapping as BaseDict

_marker = "__marker__"

class OrderedPersistentMapping(BaseDict):
    """A subclass of PersistentMapping that provides an ordering for
       keys() and items().  Almost entirely taken from Archetypes's
       utils.OrderedDict class."""

    def __init__(self, dict=None):
        self._keys = []
        BaseDict.__init__(self, dict)
        if dict is not None:
            self._keys = self.data.keys()

    def __setitem__(self, key, item):
        if not self.data.has_key(key):
            self._keys.append(key)
        return BaseDict.__setitem__(self, key, item)

    def __delitem__(self, key):
        BaseDict.__delitem__(self, key)
        self._keys.remove(key)

    def clear(self):
        BaseDict.clear(self)
        self._keys = []

    def keys(self):
        return self._keys

    def items(self):
        return [(k, self.get(k)) for k in self._keys]

    def reverse(self):
        items = list(self.items())
        items.reverse()
        return items

    def values(self):
        return [self.get(k) for k in self._keys]

    def update(self, dict):
        for k in dict.keys():
            if not self.data.has_key(k):
                self._keys.append(k)
        return BaseDict.update(self, dict)

    def copy(self):
        if self.__class__ is OrderedPersistentMapping:
            c = OrderedPersistentMapping()
            for k, v in self.items():
                c[k] = v
            return c
        import copy
        c = copy.copy(self)
        return c

    def setdefault(self, key, failobj=None):
        if not self.data.has_key(key):
            self._keys.append(key)
        return BaseDict.setdefault(self, key, failobj)

    def popitem(self):
        if not self.data:
            raise KeyError, 'dictionary is empty'
        k = self._keys.pop()
        v = self.data.get(k)
        del self.data[k]
        return (k, v)

    def pop(self, key, default=_marker):
        if default is not _marker:
            v = self.data.pop(key, default)
            if key in self._keys:
                self._keys.remove(key)
                self._p_changed = True
        else:
            v = self.data.pop(key) # will raise KeyError if needed
            self._keys.remove(key)
            self._p_changed = True
        return v

    def __iter__(self):
        return iter(self._keys)
