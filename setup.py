# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def _read(fn):
    """Read fn and return the contents."""
    with open(fn, 'r') as f:
        return f.read()

setup(
      name = 'abydos',
      packages = find_packages(exclude=['tests*']),
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
      long_description = (_read('README.rst') + '\n\n' +
                          _read('HISTORY.rst') + '\n\n' +
                          _read('AUTHORS.rst')),
      install_requires = ['numpy', 'scipy'],
      extras_require = {'LZMA': ['pyliblzma']},
    )
