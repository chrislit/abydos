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

from __future__ import unicode_literals

from ._basic import phonetic_fingerprint, qgram_fingerprint, str_fingerprint
from ._lightweight import (
    MOST_COMMON_LETTERS,
    MOST_COMMON_LETTERS_CG,
    MOST_COMMON_LETTERS_DE,
    MOST_COMMON_LETTERS_DE_LC,
    MOST_COMMON_LETTERS_EN_LC,
    count_fingerprint,
    occurrence_fingerprint,
    occurrence_halved_fingerprint,
    position_fingerprint,
)
from ._speedcop import omission_key, skeleton_key
from ._synoname import synoname_toolcode

__all__ = [
    'str_fingerprint',
    'qgram_fingerprint',
    'phonetic_fingerprint',
    'omission_key',
    'skeleton_key',
    'MOST_COMMON_LETTERS',
    'MOST_COMMON_LETTERS_CG',
    'MOST_COMMON_LETTERS_DE',
    'MOST_COMMON_LETTERS_DE_LC',
    'MOST_COMMON_LETTERS_EN_LC',
    'count_fingerprint',
    'occurrence_fingerprint',
    'occurrence_halved_fingerprint',
    'position_fingerprint',
    'synoname_toolcode',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
