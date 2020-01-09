# Copyright 2014-2020 by Christopher C. Little.
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

The fingerprint package implements string fingerprints such as:

    - Basic fingerprinters originating in `OpenRefine <http://openrefine.org>`:

        - String (:py:class:`.String`)
        - Phonetic, which applies a phonetic algorithm and returns the string
          fingerprint of the result (:py:class:`.Phonetic`)
        - QGram, which applies Q-gram tokenization and returns the string
          fingerprint of the result (:py:class:`.QGram`)

    - Fingerprints developed by Pollock & Zomora:

        - Skeleton key (:py:class:`.SkeletonKey`)
        - Omission key (:py:class:`.OmissionKey`)

    - Fingerprints developed by Cisłak & Grabowski:

        - Occurrence (:py:class:`.Occurrence`)
        - Occurrence halved (:py:class:`.OccurrenceHalved`)
        - Count (:py:class:`.Count`)
        - Position (:py:class:`.Position`)

    - The Synoname toolcode (:py:class:`.SynonameToolcode`)

    - Taft's codings:

        - Consonant coding (:py:class:`.Consonant`)
        - Extract - letter list (:py:class:`.Extract`)
        - Extract - position & frequency
          (:py:class:`.ExtractPositionFrequency`)

    - L.A. County Sheriff's System (:py:class:`.LACSS`)

    - Library of Congress Cutter table encoding (:py:class:`.LCCutter`)

    - Burrows-Wheeler transform (:py:class:`.BWTF`) and run-length encoded
      Burrows-Wheeler transform (:py:class:`.BWTRLEF`)

Each fingerprint class has a ``fingerprint`` method that takes a string and
returns the string's fingerprint:

>>> sk = SkeletonKey()
>>> sk.fingerprint('orange')
'ORNGAE'
>>> sk.fingerprint('strange')
'STRNGAE'

----

"""

from ._bwtf import BWTF
from ._bwtrlef import BWTRLEF
from ._consonant import Consonant
from ._count import Count, count_fingerprint
from ._extract import Extract
from ._extract_position_frequency import ExtractPositionFrequency
from ._fingerprint import (
    MOST_COMMON_LETTERS,
    MOST_COMMON_LETTERS_CG,
    MOST_COMMON_LETTERS_DE,
    MOST_COMMON_LETTERS_DE_LC,
    MOST_COMMON_LETTERS_EN_LC,
    _Fingerprint,
)
from ._lacss import LACSS
from ._lc_cutter import LCCutter
from ._occurrence import Occurrence, occurrence_fingerprint
from ._occurrence_halved import OccurrenceHalved, occurrence_halved_fingerprint
from ._omission_key import OmissionKey, omission_key
from ._phonetic import Phonetic, phonetic_fingerprint
from ._position import Position, position_fingerprint
from ._qgram import QGram, qgram_fingerprint
from ._skeleton_key import SkeletonKey, skeleton_key
from ._string import String, str_fingerprint
from ._synoname_toolcode import SynonameToolcode, synoname_toolcode

__all__ = [
    '_Fingerprint',
    'String',
    'str_fingerprint',
    'QGram',
    'qgram_fingerprint',
    'Phonetic',
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
    'Consonant',
    'Extract',
    'ExtractPositionFrequency',
    'LACSS',
    'LCCutter',
    'BWTF',
    'BWTRLEF',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
