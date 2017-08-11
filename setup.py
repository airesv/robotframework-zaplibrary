#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2017 Vitor Aires <airesv@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
ZAP Library - a OWASP ZAP testing library. 
"""

__docformat__ = 'restructuredtext'

import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

try:
    from setuptools import setup, find_packages
except ImportError:
    print('You must have setuptools installed to use setup.py. Exiting...')
    raise SystemExit(1)

LIBRARY_NAME = 'ZapLibrary'
CWD = abspath(dirname(__file__))


install_dependencies = (
    'requests',
    'six'
)

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version='0.0.1',
    description="A OWASP ZAP testing library for Robot framework",
    long_description="A OWASP ZAP testing library for Robot framework",
    author="ZAP development team & Vitor Aires",
    author_email='vapereira@criticalsoftware.com',
    license ='GPL 3.0',
    download_url="",
    platforms=['any'],
    package_dir={'': 'src',},
    packages=['ZapLibrary'],
    classifiers=[
        'Development Status :: 3 - Beta',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='robot framework testing automation Owasp Zap penetest security softwaretesting',
    install_requires=['future', 'robotframework >= 2.6.0']
)
