from unittest import TestCase
import time
import random

from concurrent import concurrently


class Foo(object):
    foo = 0
    def inc(self):
        s = self.foo + 1
        time.sleep(random.random())
        self.foo = s
        return s


class ConcurrencyTests(TestCase):
    def test_concurrency(self):
        num_threads = 10
        times_each = 10
        expected = num_threads * times_each

        foo = Foo()

        @concurrently(num_threads, times_each)
        def do_stuff(f):
            return f.inc()

        do_stuff(foo)
        self.assertEqual(foo.foo, expected)
