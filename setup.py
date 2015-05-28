# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def readfile(fn):
    """Read fn and return the contents."""
    with open(path.join(here, fn), 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='abydos',
    packages=find_packages(exclude=['tests*']),
    version='0.2.0',
    description='Abydos NLP/IR library',
    author='Chris Little',
    author_email='chrisclittle+abydos@gmail.com',
    url='https://github.com/chrislit/abydos',
    download_url='https://github.com/chrislit/abydos/archive/master.zip',
    keywords=['nlp', 'ai', 'ir', 'language', 'linguistics',
              'phonetic algorithms', 'string distance'],
    license='GPLv3+',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later \
(GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: English'
    ],
    long_description='\n\n'.join([readfile(f) for f in ('README.rst',
                                                        'HISTORY.rst',
                                                        'AUTHORS.rst')]),
    install_requires=['numpy'],
    # extras_require = {'LZMA': ['pyliblzma']},
)
