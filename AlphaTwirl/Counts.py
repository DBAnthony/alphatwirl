# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class Counts(object):
    def __init__(self):
        self._counts = { }

    def count(self, key, w = 1, nvar = None):
        if nvar is None: nvar = w**2
        self.addKey(key)
        self._counts[key]['n'] += w
        self._counts[key]['nvar'] += nvar

    def addKey(self, key):
        if key not in self._counts: self._counts[key] = {'n': 0.0, 'nvar': 0.0 }

    def addKeys(self, keys):
        for key in keys: self.addKey(key)

    def valNames(self):
        return ('n', 'nvar')

    def results(self):
        return self._counts

##____________________________________________________________________________||
