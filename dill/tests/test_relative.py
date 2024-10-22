#!/usr/bin/env python

import dill
import os
import sys

sys.path = [os.path.dirname(dill.__file__)] + sys.path

def test_saves_relative_paths():
    f = dill.copy(lambda x: x, relative=True)
    co_filename = f.__code__.co_filename
    assert co_filename == 'tests/test_relative.py'
    assert not os.path.isabs(co_filename)

def test_relative_paths_fully_match_the_directory():
    # The path for /aaa/bbb/c.py is relative to /aaa/bbb and not /aaa/bb.
    sys.path = [os.path.dirname(dill.__file__) + '/te'] + sys.path
    f = dill.copy(lambda x: x, relative=True)
    co_filename = f.__code__.co_filename
    assert co_filename == 'tests/test_relative.py'
    sys.path = sys.path[1:]

def test_saves_absolute_path_by_default():
    f = dill.copy(lambda x: x)
    co_filename = f.__code__.co_filename
    assert co_filename == os.path.join(os.path.dirname(dill.__file__),
                                       'tests', 'test_relative.py')
    assert os.path.isabs(co_filename)

def test_update_global_default():
    dill.settings['relative'] = True
    f = dill.copy(lambda x: x)
    co_filename = f.__code__.co_filename
    assert co_filename == 'tests/test_relative.py'

if __name__ == '__main__':
    test_saves_relative_paths()
    test_saves_absolute_path_by_default()
    test_update_global_default()
