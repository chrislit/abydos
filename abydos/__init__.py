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

"""abydos.

Abydos NLP/IR library by Christopher C. Little


There are nine major packages that make up Abydos:

    - :py:mod:`.compression` for string compression classes
    - :py:mod:`.corpus` for document corpus classes
    - :py:mod:`.distance` for string distance measure & metric classes
    - :py:mod:`.fingerprint` for string fingerprint classes
    - :py:mod:`.phones` for functions relating to phones and phonemes
    - :py:mod:`.phonetic` for phonetic algorithm classes
    - :py:mod:`.stats` for statistical functions and a confusion table class
    - :py:mod:`.stemmer` for stemming classes
    - :py:mod:`.tokenizer` for tokenizer classes

Classes with each package have consistent method names, as discussed below.
A tenth package, :py:mod:`.util`, contains functions not intended for end-user
use.

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

__version__ = '0.3.6'

__all__ = [
    'compression',
    'corpus',
    'distance',
    'fingerprint',
    'phones',
    'phonetic',
    'stats',
    'stemmer',
    'tokenizer',
    'util',
]
