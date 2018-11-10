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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._Caumanns import Caumanns, caumanns
from ._CLEFGerman import CLEFGerman, clef_german
from ._CLEFGermanPlus import CLEFGermanPlus, clef_german_plus
from ._CLEFSwedish import CLEFSwedish, clef_swedish
from ._Lovins import Lovins, lovins
from ._PaiceHusk import PaiceHusk, paice_husk
from ._Porter import Porter, porter
from ._Porter2 import Porter2, porter2
from ._SStemmer import SStemmer, s_stemmer
from ._Schinke import Schinke, schinke
from ._SnowballDanish import SnowballDanish, sb_danish
from ._SnowballDutch import SnowballDutch, sb_dutch
from ._SnowballGerman import SnowballGerman, sb_german
from ._SnowballNorwegian import SnowballNorwegian, sb_norwegian
from ._SnowballSwedish import SnowballSwedish, sb_swedish
from ._UEALite import UEALite, uealite

__all__ = [
    'Lovins',
    'lovins',
    'PaiceHusk',
    'paice_husk',
    'UEALite',
    'uealite',
    'SStemmer',
    's_stemmer',
    'Caumanns',
    'caumanns',
    'Schinke',
    'schinke',
    'Porter',
    'porter',
    'Porter2',
    'porter2',
    'SnowballDanish',
    'sb_danish',
    'SnowballDutch',
    'sb_dutch',
    'SnowballGerman',
    'sb_german',
    'SnowballNorwegian',
    'sb_norwegian',
    'SnowballSwedish',
    'sb_swedish',
    'CLEFGerman',
    'clef_german',
    'CLEFGermanPlus',
    'clef_german_plus',
    'CLEFSwedish',
    'clef_swedish',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
