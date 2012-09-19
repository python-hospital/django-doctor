#!/usr/bin/env python
import os
import sys

from doctor import __version__
from setuptools import setup

# Publish to Pypi
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(name='django-doctor',
    version=__version__,
    description='Django health check and test-that-it-works application.',
    long_description=open('README.md').read(),
    author='Funkbit AS',
    author_email='post@funkbit.no',
    url='https://github.com/funkbit/django-doctor',
    include_package_data=True,
    packages=['doctor', 'doctor.management', 'doctor.management.commands'],
    tests_require=['django>=1.1,<1.4'],
    license='BSD',
    classifiers = (
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    )
)
