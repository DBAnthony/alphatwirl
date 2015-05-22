# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class Counter(object):
    def __init__(self, keyNames, keyComposer, countMethod,
                 nextKeyComposer = None, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethod = countMethod
        self._weightCalculator = weightCalculator
        self._nextKeyComposer = nextKeyComposer

    def begin(self, event):
        self._keyComposer.begin(event)

    def event(self, event):
        keys = self._keyComposer(event)
        weight = self._weightCalculator(event)
        for key in keys:
            if self._nextKeyComposer is not None:
                nextKeys = self._nextKeyComposer(key)
                for nextKey in nextKeys: self._countMethod.addKey(nextKey)
            self._countMethod.count(key, weight)

    def end(self):
        pass

    def keynames(self):
        return self._keynames

    def valNames(self):
        return self._countMethod.valNames()

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
