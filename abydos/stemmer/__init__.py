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

    - Lovins stemmer
    - Paice-Husk Stemmer
    - UEA-Lite Stemmer
    - S-stemmer
    - Caumanns German stemmer
    - Schinke Latin stemmer
    - the Porter and Porter2 (Snowball English) stemmers
    - Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    - CLEF German, German plus, and Swedish stemmers
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._caumanns import Caumanns, caumanns
from ._clef_german import CLEFGerman, clef_german
from ._clef_german_plus import CLEFGermanPlus, clef_german_plus
from ._clef_swedish import CLEFSwedish, clef_swedish
from ._lovins import Lovins, lovins
from ._paice_husk import PaiceHusk, paice_husk
from ._porter import Porter, porter
from ._porter2 import Porter2, porter2
from ._s_stemmer import SStemmer, s_stemmer
from ._schinke import Schinke, schinke
from ._snowball_danish import SnowballDanish, sb_danish
from ._snowball_dutch import SnowballDutch, sb_dutch
from ._snowball_german import SnowballGerman, sb_german
from ._snowball_norwegian import SnowballNorwegian, sb_norwegian
from ._snowball_swedish import SnowballSwedish, sb_swedish
from ._uea_lite import UEALite, uealite

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
