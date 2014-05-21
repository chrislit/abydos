# -*- coding: utf-8 -*-
"""abydos.clustering

The clustering module implements clustering algorithms such as string
fingerprinting, k-nearest neighbors, and ...


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from __future__ import division
from ._compat import _unicode
from .phonetic import double_metaphone
import unicodedata
from .util import qgrams

def fingerprint(phrase):
    """Return the fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the fingerprint of

    Description:
    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening spaces
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase

def qgram_fingerprint(phrase, q=2, start_stop=''):
    """Return the q-gram fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the q-gram fingerprint of
    q -- the length of each q-gram (by default 2)
    start_stop -- the start & stop symbol(s) to concatenate on either end of
        the phrase, as defined in abydos.util.qgram()

    Description:
    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated.
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum()])
    phrase = qgrams(phrase, q, start_stop)
    phrase = ''.join(sorted(list(set(phrase))))
    return phrase

def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    """Return the phonetic fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the phonetic fingerprint of
    phonetic_algorithm -- a phonetic algorithm that takes a string and returns
        a string (presumably a phonetic representation of the original string)
        By default, this function uses double_metaphone() from abydos.phonetic.
    *args -- additional arguments to pass to the phonetic algorithm, along with
        the phrase itself

    Description:
    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm.
    """
    phrase = phonetic_algorithm(phrase, *args)
    if not isinstance(phrase, _unicode):
        phrase = phrase[0]
    return fingerprint(phrase)
