import os
import functools
import unittest


def setTestEnv(target=None):
    def decorator(target):
        if isinstance(target, type) and issubclass(target, unittest.TestCase):
            # It's a class - wrap all test methods
            for attr_name in dir(target):
                attr = getattr(target, attr_name)
                if callable(attr) and attr_name.startswith('test'):
                    wrapped_method = _wrap_test_method(attr)
                    setattr(target, attr_name, wrapped_method)
            return target
        else:
            # It's a function - wrap it directly
            return _wrap_test_method(target)

    def _wrap_test_method(func):
        @functools.wraps(func)
        def wrapper_setTestEnv(*args, **kwargs):
            os.environ['LIFEORGS_TESTING'] = 'true'
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                os.environ.pop('LIFEORGS_TESTING', None)

        return wrapper_setTestEnv

    if target is None:
        return decorator
    else:
        return decorator(target)