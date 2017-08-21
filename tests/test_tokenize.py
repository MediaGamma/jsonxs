import unittest

from jsonxs.tokenize import tokenize


class TestTokenize(unittest.TestCase):

    def test_object_path(self):

        self.assertEqual(
            tokenize('an.object.path'),
            ['an', 'object', 'path']
        )

    def test_nested_arrays(self):

        self.assertEqual(
            tokenize('[0][1]'),
            [0, 1]
        )

    def test_combined_paths(self):

        self.assertEqual(
            tokenize('start[1].next[2]'),
            ['start', 1, 'next', 2]
        )
