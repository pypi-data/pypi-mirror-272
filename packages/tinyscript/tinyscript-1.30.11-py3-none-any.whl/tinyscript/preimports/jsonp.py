# -*- coding: UTF-8 -*-
"""Module for enhancing json preimport.

"""
import json


def loadc(fp, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None,
          **kw):
    """ Deserialize ``fp``  (a ``.read()``-supporting file-like object containing a JSON document with comments) to a
         Python object. """
    _b = lambda s: s.encode() if 'b' in fp.mode else s
    s = _b("\n").join(l.strip().split(_b("#"), 1)[0].strip() for l in fp.readlines())
    return json.loads(s, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
                      parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
json.loadc = loadc

