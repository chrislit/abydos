# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""setup.py.

setuptools configuration file for Abydos
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from codecs import open
from os import path

from abydos import __version__

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))


def readfile(fn):
    """Read fn and return the contents.

    Parameters
    ----------
    fn : str
        A filename

    Returns
    -------
    str
        The content of the file

    """
    with open(path.join(HERE, fn), 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='abydos',
        packages=find_packages(exclude=['tests*']),
        version=__version__,
        description='Abydos NLP/IR library',
        author='Christopher C. Little',
        author_email='chrisclittle+abydos@gmail.com',
        url='https://github.com/chrislit/abydos',
        download_url='https://github.com/chrislit/abydos/archive/master.zip',
        keywords=[
            'nlp',
            'ai',
            'ir',
            'language',
            'linguistics',
            'phonetic algorithms',
            'string distance',
        ],
        license='GPLv3+',
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or \
later (GPLv3+)',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing :: Indexing',
            'Topic :: Text Processing :: Linguistic',
            'Natural Language :: English',
        ],
        long_description='\n\n'.join(
            [readfile(f) for f in ('README.rst', 'HISTORY.rst', 'AUTHORS.rst')]
        ),
        install_requires=['numpy', 'six'],
        extras_require={
            ':python_version >= "2.7" and python_version < "2.8"': [
                'pyliblzma>=0.5.3,<0.6.0'
            ]
        },
        python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    )
