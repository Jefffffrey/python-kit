from setuptools import setup, find_packages

import kit

setup(
    name='kit',
    version=kit.__version__,
    packages=find_packages(exclude=('tests', 'tests*'))
)
