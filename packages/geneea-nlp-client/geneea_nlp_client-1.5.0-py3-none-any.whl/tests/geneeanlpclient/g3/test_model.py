from unittest import TestCase

from geneeanlpclient.g3.model import GkbProperty


class TestModel(TestCase):

    def test_gkbproperty(self):
        with self.assertRaises(ValueError):
            prop = GkbProperty(name='test', label='test')
