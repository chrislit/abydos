# -*- coding: utf-8 -*-

from setuptools import setup

setup(
      name = 'abydos',
      packages = ['abydos'],
      version = '0.1.0',
      description = 'Abydos NLP/IR library',
      author = 'Christopher C. Little',
      author_email = 'chrisclittle@gmail.com',
      url = 'https://github.com/chrislit/abydos',
      download_url = 'https://github.com/chrislit/abydos/archive/master.zip',
      keywords = ['nlp', 'ai', 'ir'],
      license='GPLv3+',
      classifiers = [
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 3',
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering :: Artificial Intelligence',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Text Processing :: Indexing',
                     'Topic :: Text Processing :: Linguistic',
                     'Natural Language :: English'
                     ],
      long_description = """\
Abydos NLP/IR library
------------------

Includes ...

This version requires Python 2.7 or later.
"""
    )
