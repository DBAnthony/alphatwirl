from AlphaTwirl.EventReader import EventReaderBundle, EventLoopRunner, EventLoop
import unittest


##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##____________________________________________________________________________||
class MockReaderPackage(object):
    def __init__(self):
        self.reader = None
        self.collected = False

    def make(self, name):
        self.reader = MockReader(name)
        return self.reader

    def collect(self):
        self.collected = True

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self._events = None

##____________________________________________________________________________||
class MockEventLoopRunner(object):
    def __init__(self):
        self.began = False
        self.ended = False
        self.eventLoop = None

    def begin(self):
        self.began = True

    def run(self, eventLoop):
        self.eventLoop = eventLoop

    def end(self):
        self.ended = True

##____________________________________________________________________________||
class MockEventLoop(object):
    def __init__(self):
        self.called = False

    def __call__(self):
        self.called = True

##____________________________________________________________________________||
class TestEventLoop(unittest.TestCase):

    def test_call(self):
        eventBuilder = MockEventBuilder()
        component = MockComponent()
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component._events = [event1, event2, event3]

        reader1 = MockReader('1')
        reader2 = MockReader('2')
        readers = [reader1, reader2]

        loop = EventLoop(eventBuilder, component, readers)

        self.assertEqual(readers, loop())
        self.assertEqual([101, 102, 103], reader1._eventIds)
        self.assertEqual([101, 102, 103], reader2._eventIds)

##____________________________________________________________________________||
class TestEventLoopRunner(unittest.TestCase):

    def setUp(self):
        self.runner = EventLoopRunner()

    def test_begin(self):
        self.runner.begin()

    def test_run(self):
        loop = MockEventLoop()
        self.assertFalse(loop.called)
        self.runner.run(loop)
        self.assertTrue(loop.called)

    def test_end(self):
        self.runner.end()

##____________________________________________________________________________||
class TestEventReaderEventReaderBundle(unittest.TestCase):

    def setUp(self):
        self.eventBuilder = MockEventBuilder()
        self.eventLoopRunner = MockEventLoopRunner()
        self.bundle = EventReaderBundle(self.eventBuilder, self.eventLoopRunner)

    def test_begin_read_end(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        self.assertFalse(self.eventLoopRunner.began)
        self.bundle.begin()
        self.assertTrue(self.eventLoopRunner.began)

        component1 = MockComponent()
        component1.name = "compName1"

        self.assertIsNone(self.eventLoopRunner.eventLoop)
        self.bundle.read(component1)

        self.assertIsInstance(self.eventLoopRunner.eventLoop, EventLoop)
        self.assertIs(self.eventBuilder, self.eventLoopRunner.eventLoop.eventBuilder)
        self.assertIs(component1, self.eventLoopRunner.eventLoop.component)
        self.assertIs("compName1", self.eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader], self.eventLoopRunner.eventLoop.readers)

        component2 = MockComponent()
        component2.name = "compName2"
        self.bundle.read(component2)

        self.assertIsInstance(self.eventLoopRunner.eventLoop, EventLoop)
        self.assertIs(self.eventBuilder, self.eventLoopRunner.eventLoop.eventBuilder)
        self.assertIs(component2, self.eventLoopRunner.eventLoop.component)
        self.assertIs("compName2", self.eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader], self.eventLoopRunner.eventLoop.readers)

        self.assertFalse(self.eventLoopRunner.ended)
        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()
        self.assertTrue(self.eventLoopRunner.ended)
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

##____________________________________________________________________________||