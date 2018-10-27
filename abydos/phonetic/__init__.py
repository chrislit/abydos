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

"""abydos.phonetic.

The phonetic module implements phonetic algorithms including:

    - Robert C. Russell's Index
    - American Soundex
    - Refined Soundex
    - Daitch-Mokotoff Soundex
    - Kölner Phonetik
    - NYSIIS
    - Match Rating Algorithm
    - Metaphone
    - Double Metaphone
    - Caverphone
    - Alpha Search Inquiry System
    - Fuzzy Soundex
    - Phonex
    - Phonem
    - Phonix
    - SfinxBis
    - phonet
    - Standardized Phonetic Frequency Code
    - Statistics Canada
    - Lein
    - Roger Root
    - Oxford Name Compression Algorithm (ONCA)
    - Eudex phonetic hash
    - Haase Phonetik
    - Reth-Schek Phonetik
    - FONEM
    - Parmar-Kumbharana
    - Davidson's Consonant Code
    - SoundD
    - PSHP Soundex/Viewex Coding
    - an early version of Henry Code
    - Norphone
    - Dolby Code
    - Phonetic Spanish
    - Spanish Metaphone
    - MetaSoundex
    - SoundexBR
    - NRL English-to-phoneme
    - Beider-Morse Phonetic Matching
"""

from __future__ import unicode_literals

from ._alpha_sis import alpha_sis
from ._bmpm import bmpm
from ._caverphone import caverphone
from ._davidson import davidson
from ._de import (
    haase_phonetik,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
    phonem,
    reth_schek_phonetik,
)
from ._dm import dm_soundex
from ._dolby import dolby
from ._es import phonetic_spanish, spanish_metaphone
from ._eudex import eudex
from ._fr import fonem, henry_early
from ._hybrid import metasoundex, onca
from ._metaphone import double_metaphone, metaphone
from ._mra import mra
from ._nrl import nrl
from ._nysiis import nysiis
from ._parmar_kumbharana import parmar_kumbharana
from ._phonet import phonet
from ._pt import soundex_br
from ._roger_root import roger_root
from ._russell import (
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)
from ._sound_d import sound_d
from ._soundex import (
    fuzzy_soundex,
    lein,
    phonex,
    phonix,
    pshp_soundex_first,
    pshp_soundex_last,
    refined_soundex,
    soundex,
)
from ._spfc import spfc
from ._statistics_canada import statistics_canada
from ._sv import norphone, sfinxbis

__all__ = [
    'russell_index',
    'russell_index_num_to_alpha',
    'russell_index_alpha',
    'soundex',
    'refined_soundex',
    'dm_soundex',
    'fuzzy_soundex',
    'lein',
    'phonex',
    'phonix',
    'pshp_soundex_first',
    'pshp_soundex_last',
    'nysiis',
    'mra',
    'caverphone',
    'alpha_sis',
    'davidson',
    'dolby',
    'spfc',
    'roger_root',
    'statistics_canada',
    'sound_d',
    'parmar_kumbharana',
    'metaphone',
    'double_metaphone',
    'eudex',
    'bmpm',
    'nrl',
    'metasoundex',
    'onca',
    'fonem',
    'henry_early',
    'koelner_phonetik',
    'koelner_phonetik_num_to_alpha',
    'koelner_phonetik_alpha',
    'haase_phonetik',
    'reth_schek_phonetik',
    'phonem',
    'phonet',
    'soundex_br',
    'phonetic_spanish',
    'spanish_metaphone',
    'sfinxbis',
    'norphone',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
