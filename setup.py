#!/usr/bin/env python
# Copyright 2013 Donald Stufft and individual contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

import os
import os.path
import platform
import sys

from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext


requirements = ["six"]
setup_requirements = ["setuptools",
                      "wheel"]
test_requirements = ["pytest>=3.2.1,!=3.3.0",
                     "hypothesis>=3.27.0"]
docs_requirements = ["sphinx>=1.6.5",
                     "sphinx_rtd_theme"]


if platform.python_implementation() == "PyPy":
    if sys.pypy_version_info < (2, 6):
        raise RuntimeError(
            "PyNaCl is not compatible with PyPy < 2.6. Please "
            "upgrade PyPy to use this library."
        )
else:
    requirements.append("cffi>=1.4.1")
    setup_requirements.append("cffi>=1.4.1")


def here(*paths):
    return os.path.relpath(os.path.join(*paths))


def abshere(*paths):
    return os.path.abspath(here(*paths))


sys.path.insert(0, abshere("src"))


import nacl  # noqa


class build_ext(_build_ext):

    def run(self):
        # libsodium is no longer bundled; it is always built separately and
        # linked from the system default paths or from SODIUM_HOME.
        if "SODIUM_HOME" in os.environ:
            sodium_home = os.environ["SODIUM_HOME"]
            self.include_dirs.append(
                os.path.join(sodium_home, "include"),
            )
            self.library_dirs.insert(
                0, os.path.join(sodium_home, "lib"),
            )
            self.library_dirs.insert(
                0, os.path.join(sodium_home, "lib64"),
            )

        return _build_ext.run(self)


README = open("README.rst").read()
INSTALL = open("INSTALL.rst").read()
CHANGELOG = open("CHANGELOG.rst").read()


setup(
    name=nacl.__title__,
    version=nacl.__version__,

    description=nacl.__summary__,
    long_description='\n'.join((README, INSTALL, CHANGELOG)),
    url=nacl.__uri__,
    license=nacl.__license__,

    author=nacl.__author__,
    author_email=nacl.__email__,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    setup_requires=setup_requirements,
    install_requires=requirements,
    extras_require={
        "tests": test_requirements,
        "docs": docs_requirements,
    },
    tests_require=test_requirements,

    package_dir={"": "src"},
    packages=[
        "nacl",
        "nacl.pwhash",
        "nacl.bindings",
    ],

    ext_package="nacl",
    cffi_modules=[
        "src/bindings/build.py:ffi",
    ],

    cmdclass={
        "build_ext": build_ext,
    },
    zip_safe=False,

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
