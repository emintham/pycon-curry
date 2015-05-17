"""
Adapted from:

https://www.caktusgroup.com/blog/2009/05/26/testing-django-views-for-concurrency-issues/
"""
import threading
import multiprocessing


def concurrently(num_thingies, times_each, model):
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []
            def call_test_func(t_num):
                try:
                    for _ in range(times_each):
                        print '{} {}: {}'.format(model,
                                                 t_num,
                                                 test_func(*args, **kwargs))
                except Exception as e:
                    exceptions.append(e)
                    raise

            if model == 'thread':
                thingies = [threading.Thread(target=call_test_func, args=(i, ))
                           for i in range(num_thingies)]
            else:
                thingies = [multiprocessing.Process(target=call_test_func, args=(i, ))
                            for i in range(num_thingies)]

            for t in thingies:
                t.start()

            for t in thingies:
                t.join()

            if exceptions:
                raise Exception(('test_concurrently intercepted {} exceptions:'
                                 '{}').format(len(exceptions), exceptions))

        return wrapper
    return test_concurrently_decorator
