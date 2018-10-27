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

"""abydos.stemmer.

The stemmer module defines word stemmers including:

    - the Lovins stemmer
    - the Porter and Porter2 (Snowball English) stemmers
    - Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    - CLEF German, German plus, and Swedish stemmers
    - Caumanns German stemmer
    - UEA-Lite Stemmer
    - Paice-Husk Stemmer
    - Schinke Latin stemmer
    - S stemmer
"""

from __future__ import unicode_literals

from ._caumanns import caumanns
from ._clef import clef_german, clef_german_plus, clef_swedish
from ._lovins import lovins
from ._paice_husk import paice_husk
from ._s_stemmer import s_stemmer
from ._schinke import schinke
from ._snowball import (
    porter,
    porter2,
    sb_danish,
    sb_dutch,
    sb_german,
    sb_norwegian,
    sb_swedish,
)
from ._uealite import uealite

__all__ = [
    'lovins',
    'paice_husk',
    'uealite',
    's_stemmer',
    'caumanns',
    'schinke',
    'porter',
    'porter2',
    'sb_danish',
    'sb_dutch',
    'sb_german',
    'sb_norwegian',
    'sb_swedish',
    'clef_german',
    'clef_german_plus',
    'clef_swedish',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
