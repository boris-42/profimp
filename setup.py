#!/usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
import os

import profimp

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215


def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


config = {
        "name": "profimp",
        "version": profimp.__version__,
        "author": "Boris Pavlovic",
        "author_email": "boris@pavlovic.me",
        "url": "http://boris-42.me",
        "description": "profimp - generates tree of imports profiles",
        "long_description": read("README.rst"),

        "classifiers": [
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4"
        ],

        "packages": ["profimp"],

        "entry_points": {
            "console_scripts": ["profimp=profimp.main:main"]
        }
}


setup(**config)
