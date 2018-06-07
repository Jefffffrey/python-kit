from setuptools import setup, find_packages

import utils

setup(
    name='kit',
    version=utils.__version__,
    packages=find_packages(exclude=('tests', 'tests*'))
)
