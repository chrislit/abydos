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

"""abydos.fingerprint.

The fingerprint module implements string fingerprints such as:
    - string fingerprint
    - q-gram fingerprint
    - phonetic fingerprint
    - Pollock & Zomora's skeleton key
    - Pollock & Zomora's omission key
    - Cisłak & Grabowski's occurrence fingerprint
    - Cisłak & Grabowski's occurrence halved fingerprint
    - Cisłak & Grabowski's count fingerprint
    - Cisłak & Grabowski's position fingerprint
    - Synoname Toolcode
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._Fingerprint import (
    MOST_COMMON_LETTERS,
    MOST_COMMON_LETTERS_CG,
    MOST_COMMON_LETTERS_DE,
    MOST_COMMON_LETTERS_DE_LC,
    MOST_COMMON_LETTERS_EN_LC,
)
from ._PhoneticFingerprint import PhoneticFingerprint, phonetic_fingerprint
from ._QGramFingerprint import QGramFingerprint, qgram_fingerprint
from ._StringFingerprint import StringFingerprint, str_fingerprint
from ._Position import Position, position_fingerprint
from ._Count import Count, count_fingerprint
from ._Occurrence import Occurrence, occurrence_fingerprint
from ._OccurrenceHalved import OccurrenceHalved, occurrence_halved_fingerprint
from ._OmissionKey import OmissionKey, omission_key
from ._SkeletonKey import SkeletonKey, skeleton_key
from ._Synoname import SynonameToolcode, synoname_toolcode

__all__ = [
    'StringFingerprint',
    'str_fingerprint',
    'QGramFingerprint',
    'qgram_fingerprint',
    'PhoneticFingerprint',
    'phonetic_fingerprint',
    'OmissionKey',
    'omission_key',
    'SkeletonKey',
    'skeleton_key',
    'MOST_COMMON_LETTERS',
    'MOST_COMMON_LETTERS_CG',
    'MOST_COMMON_LETTERS_DE',
    'MOST_COMMON_LETTERS_DE_LC',
    'MOST_COMMON_LETTERS_EN_LC',
    'Occurrence',
    'occurrence_fingerprint',
    'OccurrenceHalved',
    'occurrence_halved_fingerprint',
    'Count',
    'count_fingerprint',
    'Position',
    'position_fingerprint',
    'SynonameToolcode',
    'synoname_toolcode',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
