#!/usr/bin/env python

"""
jsonxs uses a path expression string to get and set values in JSON and Python
datastructures.

For example:

    >>> d = {
    ...   'feed': {
    ...     'id': 'my_feed',
    ...     'url': 'http://example.com/feed.rss',
    ...     'tags': ['devel', 'example', 'python'],
    ...     'short.desc': 'A feed',
    ...     'list': [
    ...       {
    ...         'uuid': 'e9b48a2'
    ...       }
    ...     ]
    ...   }
    ... }

    # Get the value for a path expression
    >>> jsonxs(d, 'feed.tags[-1]')
    'python'

    # Access paths with special chars in them
    >>> jsonxs(d, 'feed.short\.desc')
    'A feed'

    # Return default value if path not found
    >>> jsonxs(d, 'feed.long\.desc', default='N/A')
    'N/A'

    # Set the value for a path expression
    >>> jsonxs(d, 'feed.id', ACTION_SET, 'your_feed')
    >>> d['feed']['id']
    'your_feed'

    # Replace a value in a list
    >>> jsonxs(d, 'feed.tags[-1]', ACTION_SET, 'javascript')
    >>> d['feed']['tags']
    ['devel', 'example', 'javascript']

    # Create a new key in a dict
    >>> jsonxs(d, 'feed.author', ACTION_SET, 'Ferry Boender')
    >>> d['feed']['author']
    'Ferry Boender'

    # Delete a value from a list
    >>> jsonxs(d, 'feed.tags[0]', ACTION_DEL)
    >>> d['feed']['tags']
    ['example', 'javascript']

    # Delete a key/value pair from a dictionary
    >>> jsonxs(d, 'feed.url', ACTION_DEL)
    >>> 'url' in d['feed']
    False

    # Append a value to a list
    >>> jsonxs(d, 'feed.tags', ACTION_APPEND, 'programming')
    >>> d['feed']['tags']
    ['example', 'javascript', 'programming']

    # Insert a value to a list
    >>> jsonxs(d, 'feed.tags[1]', ACTION_INSERT, 'tech')
    >>> d['feed']['tags']
    ['example', 'tech', 'javascript', 'programming']

    # Create a dict value
    >>> jsonxs(d, 'feed.details', ACTION_MKDICT)
    >>> d['feed']['details'] == {}
    True

    # Add a key / value to newly created dict
    >>> jsonxs(d, 'feed.list[0].uuid', ACTION_SET, 'aeaeae')

    # Create a list value
    >>> jsonxs(d, 'feed.details.users', ACTION_MKLIST)
    >>> d['feed']['details']['users'] == []
    True

    # Fill the newly created list
    >>> jsonxs(d, 'feed.details.users', ACTION_APPEND, 'fboender')
    >>> jsonxs(d, 'feed.details.users', ACTION_APPEND, 'ppeterson')
    >>> d['feed']['details']['users']
    ['fboender', 'ppeterson']
"""

from __future__ import absolute_import
from jsonxs.tokenizer import LIST, OBJECT, tokenize

ACTION_GET = 'get'
ACTION_SET = 'set'
ACTION_DEL = 'del'
ACTION_APPEND = 'append'
ACTION_INSERT = 'insert'
ACTION_MKDICT = 'mkdict'
ACTION_MKLIST = 'mklist'


def jsonxs(data, expr, action=ACTION_GET, value=None, default=None):
    """
    Get, set, delete values in a JSON structure. `expr` is a JSONpath-like
    expression pointing to the desired value. `action` determines the action to
    perform. See the module-level `ACTION_*` constants. `value` should be given
    if action is `ACTION_SET`. If `default` is set and `expr` isn't found,
    return `default` instead. This will override all exceptions.
    """
    tokens = tokenize(expr)

    # Walk through the list of tokens to reach the correct path in the data
    # structure.
    prev_path = None
    cur_path = data
    for token in tokens:
        prev_path = cur_path
        if (token.type == LIST and isinstance(cur_path, list)) \
        or (token.type == OBJECT and token.value in cur_path):
            cur_path = cur_path[token.value]
        elif token.type == OBJECT:
            if action == ACTION_GET:
                return default
            elif action == ACTION_SET:
                cur_path[token.value] = {}
                cur_path = cur_path[token.value]
            elif action == ACTION_MKDICT:
                cur_path[token.value] = {}
            elif action == ACTION_MKLIST:
                cur_path[token.value] = []
                cur_path = cur_path[token.value]

    # Perform action the user requested.
    if action == ACTION_GET:
        return cur_path
    elif action == ACTION_DEL:
        del prev_path[token.value]
    elif action == ACTION_SET:
        prev_path[token.value] = value
    elif action == ACTION_APPEND:
        prev_path[token.value].append(value)
    elif action == ACTION_INSERT:
        prev_path.insert(token.value, value)
    elif action == ACTION_MKDICT:
        prev_path[token] = {}
    elif action == ACTION_MKLIST:
        prev_path[token.value] = []
    else:
        raise ValueError("Invalid action: {}".format(action))