# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from os.path import dirname, relpath, join

from diylisp.interpreter import interpret, interpret_file
from diylisp.types import Environment

env = Environment()
path = join(dirname(relpath(__file__)), '..', 'stdlib.diy')
interpret_file(path, env)

def test_assert():
    assert_equals("#t", interpret('(assert #t)', env))
    assert_equals("#f", interpret('(assert #f)', env))
    assert_equals("#t", interpret('(assert (eq 1 1))', env))
    assert_equals("#f", interpret('(assert (eq 1 2))', env))
    assert_equals("#f", interpret('(assert (>= 1 2))', env))
    
