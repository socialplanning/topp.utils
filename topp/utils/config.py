from ConfigParser import ConfigParser as CP
class ConfigMap(object):

    def __init__(self, parser):
        self.parser = parser
        self.sects = parser.sections()

    def __iter__(self):
        for sname in self.sects:
            yield sname
            
    def __getitem__(self, idx):
        return dict(self.parser.items(idx))

    @classmethod
    def load(cls, fname):
        parser = CP()
        parser.read(fname)
        return cls(parser)
