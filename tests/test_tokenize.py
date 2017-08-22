# -*- coding: utf-8 -*-
import unittest

from jsonxs.tokenizer import tokenize, Token


class TestTokenize(unittest.TestCase):

    def test_object_path(self):

        self.assertEqual(
            list(tokenize(u'an.object.path')),
            [Token(type='OBJECT', value='an'),
             Token(type='OBJECT', value='object'),
             Token(type='OBJECT', value='path'),]
        )

    def test_unicode_object_path(self):

        self.assertEqual(
            list(tokenize(u'an.objéct.path')),
            [Token(type='OBJECT', value=u'an'),
             Token(type='OBJECT', value=u'objéct'),
             Token(type='OBJECT', value=u'path'),]
        )

    def test_path_with_escaped_chars(self):

        self.assertEqual(
            list(tokenize('an.object\.path')),
            [Token(type='OBJECT', value='an'),
             Token(type='OBJECT', value='object.path'),]
        )

    def test_nested_arrays(self):

        self.assertEqual(
            list(tokenize('[0][1]')),
            [Token(type='LIST', value=0),
             Token(type='LIST', value=1),]
        )

    def test_negative_arrays(self):

        self.assertEqual(
            list(tokenize('[-1]')),
            [Token(type='LIST', value=-1),]
        )

    def test_combined_paths(self):

        self.assertEqual(
            list(tokenize('start[1].next[2]')),
            [Token(type='OBJECT', value='start'),
             Token(type='LIST', value=1),
             Token(type='OBJECT', value='next'),
             Token(type='LIST', value=2),]
        )

    # def test_array_wildcard(self):

    #     self.assertEqual(
    #         tokenize('object.*]'),
    #         ['object', '*']
    #     )

    # def test_array_wildcard(self):

    #     self.assertEqual(
    #         tokenize('[*]'),
    #         ['*']
    #     )
