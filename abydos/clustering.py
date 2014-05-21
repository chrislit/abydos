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
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join(filter(lambda c: (c.isalnum() or c.isspace()), phrase))
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase

def qgram_fingerprint(phrase, q=2, start_stop=''):
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join(filter(lambda c: c.isalnum(), phrase))
    phrase = qgrams(phrase, q, start_stop)
    phrase = ''.join(sorted(list(set(phrase))))
    return phrase

def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    phrase = phonetic_algorithm(phrase, *args)
    if not isinstance(phrase, _unicode):
        phrase = phrase[0]
    return fingerprint(phrase)
