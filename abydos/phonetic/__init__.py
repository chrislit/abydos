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

from ._alpha_sis import AlphaSIS, alpha_sis
from ._bmpm import BeiderMorse, bmpm
from ._caverphone import Caverphone, caverphone
from ._davidson import Davidson, davidson
from ._de import (
    Haase,
    Koelner,
    Phonem,
    RethSchek,
    haase_phonetik,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
    phonem,
    reth_schek_phonetik,
)
from ._dm import DaitchMokotoff, dm_soundex
from ._dolby import Dolby, dolby
from ._es import (
    PhoneticSpanish,
    SpanishMetaphone,
    phonetic_spanish,
    spanish_metaphone,
)
from ._eudex import Eudex, eudex
from ._fr import FONEM, HenryEarly, fonem, henry_early
from ._hybrid import MetaSoundex, ONCA, metasoundex, onca
from ._metaphone import DoubleMetaphone, Metaphone, double_metaphone, metaphone
from ._mra import MRA, mra
from ._nrl import NRL, nrl
from ._nysiis import NYSIIS, nysiis
from ._parmar_kumbharana import ParmarKumbharana, parmar_kumbharana
from ._phonet import Phonet, phonet
from ._pt import SoundexBR, soundex_br
from ._roger_root import RogerRoot, roger_root
from ._russell import (
    RussellIndex,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)
from ._sound_d import SoundD, sound_d
from ._soundex import (
    FuzzySoundex,
    Lein,
    PSHPSoundexFirst,
    PSHPSoundexLast,
    Phonex,
    Phonix,
    RefinedSoundex,
    Soundex,
    fuzzy_soundex,
    lein,
    phonex,
    phonix,
    pshp_soundex_first,
    pshp_soundex_last,
    refined_soundex,
    soundex,
)
from ._spfc import SPFC, spfc
from ._statistics_canada import StatisticsCanada, statistics_canada
from ._sv import Norphone, SfinxBis, norphone, sfinxbis

__all__ = [
    'RussellIndex',
    'russell_index',
    'russell_index_num_to_alpha',
    'russell_index_alpha',
    'Soundex',
    'soundex',
    'RefinedSoundex',
    'refined_soundex',
    'DaitchMokotoff',
    'dm_soundex',
    'FuzzySoundex',
    'fuzzy_soundex',
    'Lein',
    'lein',
    'Phonex',
    'phonex',
    'Phonix',
    'phonix',
    'PSHPSoundexFirst',
    'pshp_soundex_first',
    'PSHPSoundexLast',
    'pshp_soundex_last',
    'NYSIIS',
    'nysiis',
    'MRA',
    'mra',
    'Caverphone',
    'caverphone',
    'AlphaSIS',
    'alpha_sis',
    'Davidson',
    'davidson',
    'Dolby',
    'dolby',
    'SPFC',
    'spfc',
    'RogerRoot',
    'roger_root',
    'StatisticsCanada',
    'statistics_canada',
    'SoundD',
    'sound_d',
    'ParmarKumbharana',
    'parmar_kumbharana',
    'Metaphone',
    'metaphone',
    'DoubleMetaphone',
    'double_metaphone',
    'Eudex',
    'eudex',
    'BeiderMorse',
    'bmpm',
    'NRL',
    'nrl',
    'MetaSoundex',
    'metasoundex',
    'ONCA',
    'onca',
    'FONEM',
    'fonem',
    'HenryEarly',
    'henry_early',
    'Koelner',
    'koelner_phonetik',
    'koelner_phonetik_num_to_alpha',
    'koelner_phonetik_alpha',
    'Haase',
    'haase_phonetik',
    'RethSchek',
    'reth_schek_phonetik',
    'Phonem',
    'phonem',
    'Phonet',
    'phonet',
    'SoundexBR',
    'soundex_br',
    'PhoneticSpanish',
    'phonetic_spanish',
    'SpanishMetaphone',
    'spanish_metaphone',
    'SfinxBis',
    'sfinxbis',
    'Norphone',
    'norphone',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
