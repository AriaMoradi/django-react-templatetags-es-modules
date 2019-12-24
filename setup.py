#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import re
from setuptools import setup, find_packages

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

with open('README.md') as f:
    readme = f.read()

# Convert markdown to rst
with open("README.md", "r") as fh:
    long_description = fh.read()

version = ''
with io.open('django_react_templatetags_es_modules/__init__.py', 'r', encoding='utf8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name="django_react_templatetags_es_modules",
    version=version,
    description=("This django library allows you to add React components into your django templates."),  # NOQA
    long_description=long_description,
    author="Aria Moradi",
    author_email="aria.moradi007@gmail.com",
    url="https://github.com/AriaMoradi/django-react-templatetags-es-modlues",
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
    ],
    extras_require={
        'ssr': ['requests'],
    },
    tests_require=[
        'Django>=1.11',
        'requests',
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Topic :: Utilities',
        'Programming Language :: JavaScript',
    ],
)
