# -*- coding: utf-8 -*-
import collections
import re

LIST =      'LIST'
OBJECT =    'OBJECT'
L_LIST =    'L_LIST'
R_LIST =    'R_LIST'
INTEGER =   'INTEGER'
SEPERATOR = 'SEPERATOR'
ESCAPE =    'ESCAPE'
NAME =      'NAME'

Token = collections.namedtuple('Token', ['type', 'value'])

TOKEN_SPECIFICATION = [
    (L_LIST,  r'\['),
    (R_LIST,  r'\]'),
    (INTEGER,  r'[-]?\d+'),
    (SEPERATOR,  r'\.'),
    # for explanation of [^\W\d_]+
    # see https://stackoverflow.com/a/6314634/2398354
    (NAME, r'[^\W\d_]+(?:\\\.){0,1}[^\W\d_]+'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tok_regex, re.UNICODE).match


def get_list_token(expr, pos):
    tokens = []
    for _ in range(3):
        mo = get_token(expr, pos)
        typ = mo.lastgroup
        val = mo.group(typ)
        tokens.append((typ, val))
        pos = mo.end()
    assert [t[0] for t in tokens] == [L_LIST, INTEGER, R_LIST]
    return Token(type=LIST, value=int(tokens[1][1])), pos


def get_object_token(expr, pos):
    mo = get_token(expr, pos)
    typ = mo.lastgroup
    val = mo.group(typ)
    pos = mo.end()
    assert typ == NAME
    name = val.replace('\.', '.')
    return Token(type=OBJECT, value=name), pos


def tokenize(expr):
    """
    Parse a string expression into a set of tokens that can be used as a path
    into a Python datastructure.
    """
    pos = 0
    mo = get_token(expr, pos)
    while mo is not None:
        typ = mo.lastgroup
        if typ == L_LIST:
            token, pos = get_list_token(expr, pos)
            yield token
        elif typ == SEPERATOR:
            pos = mo.end()
        elif typ == NAME:
            token, pos = get_object_token(expr, pos)
            yield token
        else:
            raise RuntimeError('Unexpected character %r' % expr[pos])
        mo = get_token(expr, pos)
    if pos != len(expr):
        raise RuntimeError('Unexpected character %r' % expr[pos])
