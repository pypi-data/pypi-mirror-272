# -*- coding: UTF-8 -*-
"""Preimports string assets' tests.

"""
from tinyscript.preimports import json

from utils import *


FNAME = ".test.json"
TEST_JSON = """
# test comment 1
{
    "test": ["a", "b", "c"],
    "other": 1 # test comment 2
}
"""


class TestPreimportsJson(TestCase):
    @classmethod
    def tearDownClass(cls):
        remove(FNAME)
    
    def test_commented_json_loading(self):
        with open(FNAME, 'wt') as f:
            f.write(TEST_JSON)
        with open(FNAME) as f:
            self.assertIsNotNone(json.loadc(f))
        with open(FNAME, 'wb') as f:
            f.write(TEST_JSON.encode())
        with open(FNAME, 'rb') as f:
            self.assertIsNotNone(json.loadc(f))

