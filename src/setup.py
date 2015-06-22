#!/usr/bin/env python

from __future__ import print_function

import os
import sys
from setuptools import setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)

try:
    import distutilazy
    import distutilazy.clean
    import distutilazy.test
except ImportError as e:
    distutilazy = None

long_description = __doc__
with open(os.path.join(os.path.dirname(BASE_PATH), "README.rst")) as fh:
    long_description = fh.read()

params = dict(
    name = "Project Name",
    description = "Project Description",
    long_description = long_description,
)

if distutilazy:
    params['cmdclass'] = {
        "clean_pyc": distutilazy.clean.clean_pyc,
        "clean_all": distutilazy.clean.clean_all,
        "test": distutilazy.test.run_tests
    }
else:
    params['test_suite'] = 'tests'

if __name__ == '__main__':
    dist = setup(**params)
