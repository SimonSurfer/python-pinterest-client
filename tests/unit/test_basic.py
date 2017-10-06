import unittest

from pinterest.client import PintClient, PintNamespace


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.client = PintClient('test-token-there-is-no-secret-here', version='1')

    def test_versions(self):
        c = PintClient('test-token-there-is-no-secret-here', version='1.1')
        self.assertEquals(c.version, '1.1')
        self.assertEqual(c.endpoint, 'https://api.pinterest.com/v1.1')

    def test_client(self):
        self.assertEquals(self.client.version, '1')
        self.assertIsInstance(self.client.pins, PintNamespace)
        self.assertEqual(self.client.endpoint, 'https://api.pinterest.com/v1')

    def test_spec(self):
        self.assertIsInstance(self.client.spec.PINS, dict)
        self.assertIn('fields', self.client.spec.PINS)
        self.assertIn('params', self.client.spec.PINS)



