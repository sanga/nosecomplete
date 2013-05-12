import sys
import re

from unittest2 import TestLoader, TestSuite

from nose2.util import test_name

def get_tests(d = '.'):
    T = TestLoader()
    t = T.discover(d)
    stack = [t]
    tests = []

    while stack:
        s = stack.pop()
        for t in s:
            if isinstance(t, TestSuite):
                stack.append(t)
            else:
                tests.append(t)

    return [test_name(v) for v in tests] # all test qualified names from this dir

def match(x, token):
    m = re.match('\A(%s[^.]*).*' % token, x)
    if m:
	j =  m.groups()[0]
    else:
	j = None
    if j is not None and j != x:
        j = j + '.'
    return j


def _complete(token):
    options = set(match(t, token) for t in get_tests())
    options.discard(None)
    return options

def complete(x):
    for option in _complete(x):
            sys.stdout.write(option + ' ')

def main():
    args = sys.argv
    complete('[^.]*' if len(args) == 1 else args[1])

if __name__ == '__main__':
    import warnings
    with warnings.catch_warnings():
        main()
