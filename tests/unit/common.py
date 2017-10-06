import os
import sys
import unittest
import importlib
from functools import wraps

from mock import patch, Mock

from pinterest.client import PintClient

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))


class BaseMockedTestCase(unittest.TestCase):
    mock_get_patcher = None

    @classmethod
    def setUpClass(cls):
        cls.mock_request_patcher = patch('requests.request')
        cls.mock_request = cls.mock_request_patcher.start()

    @classmethod
    def tearDownClas(cls):
        cls.mock_request_patcher.stop()

    def setUp(self):
        self.client = PintClient('test-mock-token')


class test_case(object):

    def __init__(self, module, attr):
        self.module = module
        self.attr = attr

    def __call__(self, fn):
        mod = importlib.import_module('.'.join(['cases', self.module]))
        response = getattr(mod, self.attr)

        @wraps(fn)
        def wrapped(slf, *args, **kwargs):
            slf.mock_request.return_value = Mock(ok=True)
            slf.mock_request.return_value.json.return_value = response

            return fn(slf, *args, **kwargs)

        return wrapped

