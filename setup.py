
# Copyright (c) 2017-2018 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2+
# License-Filename: LICENSE
#
# Copyright 2016-2017 David Steele <steele@debian.org>
# This file is part of comitup
# Available under the terms of the GNU General Public License version 2
# or later
#

from setuptools import setup
from distutils.command.clean import clean
from setuptools.command.test import test

import os
import shutil
import sys


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class MyClean(clean):
    def run(self):
        clean.run(self)

        for root, dirs, files in os.walk('.'):
            [shutil.rmtree(os.path.join(root, x)) for x in dirs if x in
                (".pyc", ".coverage", ".cache", "__pycache__",
                 "comitup.egg-info")]

            for file in files:
                for match in (".pyc", ".cache", ".coverage"):
                    if match in file:
                        os.unlink(os.path.join(root, file))


setup(
    name='comitup',
    packages=['comitup', 'web', 'cli'],
    version='1.3',
    description="Remotely manage wifi connections on a headless computer",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved ' +
        ':: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
    entry_points={
        'console_scripts': [
            'comitup-cmd=comitup.comitup:main',
            'comitup-cli=cli.comitupcli:interpreter',
            'comitup-web=web.comitupweb:main',
        ],
    },
    options={
        'build_scripts': {
            'executable': '/usr/bin/python3',
        },
    },
    data_files=[
        ('/etc', ['conf/comitup.conf']),
        ('/etc/dbus-1/system.d', ['conf/comitup-dbus.conf']),
        ('/usr/share/comitup/web', ['web/comitupweb.conf']),
        ('/usr/share/comitup/web/templates',
            [
                'web/templates/index.html',
                'web/templates/connect.html',
                'web/templates/confirm.html',
            ]
        ),  # noqa
	('/usr/share/comitup/web/static/js',
            [
                'web/static/js/jquery-3.3.1.slim.min.js',
                'web/static/js/bootstrap.min.js.map',
                'web/static/js/bootstrap.min.js',
                'web/static/js/bootstrap.js.map',
                'web/static/js/bootstrap.js',
                'web/static/js/bootstrap.bundle.min.js.map',
                'web/static/js/bootstrap.bundle.min.js',
                'web/static/js/bootstrap.bundle.js.map',
                'web/static/js/bootstrap.bundle.js',
            ]
        ),
        ('/usr/share/comitup/web/static/images',
            [
                'web/static/images/GoofyFPV_noText_transparent.png',
            ]
        ),
        ('/usr/share/comitup/web/static/css',
            [
                'web/static/css/bootstrap.min.css.map',
                'web/static/css/bootstrap.min.css',
                'web/static/css/bootstrap.css.map',
                'web/static/css/bootstrap.css',
                'web/static/css/bootstrap-reboot.min.css.map',
                'web/static/css/bootstrap-reboot.min.css',
                'web/static/css/bootstrap-reboot.css.map',
                'web/static/css/bootstrap-reboot.css',
                'web/static/css/bootstrap-grid.min.css.map',
                'web/static/css/bootstrap-grid.min.css',
                'web/static/css/bootstrap-grid.css.map',
                'web/static/css/bootstrap-grid.css',
            ]
        ),
    ],
    install_requires=[
        'jinja2',
    ],
    tests_require=['pytest', 'mock'],
    cmdclass={
        'clean': MyClean,
        'test': PyTest,
    },
    author="David Steele",
    author_email="steele@debian.org",
    url='https://davesteele.github.io/comitup/',
    )
