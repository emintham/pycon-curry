from threading import Lock
from unittest import TestCase
import multiprocessing
import time

from concurrent import concurrently


class Foo(object):
    foo = 0

    def __init__(self, model='thread'):
        self.model = model

    def inc(self, lock):
        with lock:
            s = self.foo + 1
            time.sleep(0.01)
            self.foo = s

        if self.model == 'process':
            print 'process'
        return s


class ConcurrencyTests(TestCase):
    def setUp(self):
        self.num_thingies = 5
        self.num_times_each = 5
        self.expected = self.num_thingies * self.num_times_each

    def test_concurrency_with_threads(self):
        foo = Foo()
        lock = Lock()

        @concurrently(self.num_thingies, self.num_times_each, 'thread')
        def do_stuff(f):
            return f.inc(lock)

        do_stuff(foo)
        self.assertEqual(foo.foo, self.expected)

    def test_concurrency_with_processes(self):
        foo = Foo('process')
        lock = multiprocessing.Lock()

        @concurrently(self.num_thingies, self.num_times_each, 'process')
        def do_stuff(f):
            return f.inc(lock)

        do_stuff(foo)
        self.assertEqual(foo.foo, self.expected)
