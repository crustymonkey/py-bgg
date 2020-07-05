#!/usr/bin/env python3

"""
This file is part of py-sonic.

py-sonic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-sonic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-sonic.  If not, see <http://www.gnu.org/licenses/>
"""

from setuptools import setup
from libbgg import __version__

setup(name='py-bgg',
    version=__version__,
    author='Jay Deiman',
    author_email='admin@splitstreams.com',
    url='http://stuffivelearned.org',
    description='A simple Board Game Geek (boardgamegeek.com) API library',
    long_description='A simple Board Game Geek (boardgamegeek.com) API '
        'library in Python. This mainly just handles the API calls '
        'and converts the XML to representative dict/list format',
    packages=['libbgg'],
    package_dir={'libbgg': 'libbgg'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: System',
    ]
)
