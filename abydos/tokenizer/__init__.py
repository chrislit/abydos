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

"""abydos.tokenizer.

The tokenizer package collects classes whose purpose is to tokenize
text. Currently, this is limited to the :py:class:`.QGrams` class, which
tokenizes a string into q-grams. The class supports different values of
q, the addition of start and stop symbols, and skip values. It even supports
multiple values for q and skip, using lists or ranges.

>>> QGrams('interning', qval=2, start_stop='$#')
QGrams({'in': 2, '$i': 1, 'nt': 1, 'te': 1, 'er': 1, 'rn': 1, 'ni': 1, 'ng': 1,
 'g#': 1})

>>> QGrams('AACTAGAAC', start_stop='', skip=1)
QGrams({'AC': 2, 'AT': 1, 'CA': 1, 'TG': 1, 'AA': 1, 'GA': 1, 'A': 1})

>>> QGrams('AACTAGAAC', start_stop='', skip=[0, 1])
QGrams({'AC': 4, 'AA': 3, 'GA': 2, 'CT': 1, 'TA': 1, 'AG': 1, 'AT': 1, 'CA': 1,
 'TG': 1, 'A': 1})

>>> QGrams('interdisciplinarian', qval=range(3), skip=[0, 1])
QGrams({'i': 10, 'n': 7, 'r': 4, 'a': 4, 'in': 3, 't': 2, 'e': 2, 'd': 2,
 's': 2, 'c': 2, 'p': 2, 'l': 2, 'ri': 2, 'ia': 2, '$i': 1, 'nt': 1, 'te': 1,
 'er': 1, 'rd': 1, 'di': 1, 'is': 1, 'sc': 1, 'ci': 1, 'ip': 1, 'pl': 1,
 'li': 1, 'na': 1, 'ar': 1, 'an': 1, 'n#': 1, '$n': 1, 'it': 1, 'ne': 1,
 'tr': 1, 'ed': 1, 'ds': 1, 'ic': 1, 'si': 1, 'cp': 1, 'il': 1, 'pi': 1,
 'ln': 1, 'nr': 1, 'ai': 1, 'ra': 1, 'a#': 1})

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._qgrams import QGrams

__all__ = ['QGrams']


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
