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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._AlphaSIS import AlphaSIS, alpha_sis
from ._BeiderMorse import BeiderMorse, bmpm
from ._Caverphone import Caverphone, caverphone
from ._DaitchMokotoff import DaitchMokotoff, dm_soundex
from ._Davidson import Davidson, davidson
from ._Dolby import Dolby, dolby
from ._DoubleMetaphone import DoubleMetaphone, double_metaphone
from ._Eudex import Eudex, eudex
from ._FONEM import FONEM, fonem
from ._FuzzySoundex import FuzzySoundex, fuzzy_soundex
from ._Haase import Haase, haase_phonetik
from ._HenryEarly import HenryEarly, henry_early
from ._Koelner import (
    Koelner,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
)
from ._Lein import Lein, lein
from ._MRA import MRA, mra
from ._MetaSoundex import MetaSoundex, metasoundex
from ._Metaphone import Metaphone, metaphone
from ._NRL import NRL, nrl
from ._NYSIIS import NYSIIS, nysiis
from ._Norphone import Norphone, norphone
from ._ONCA import ONCA, onca
from ._PSHPSoundexFirst import PSHPSoundexFirst, pshp_soundex_first
from ._PSHPSoundexLast import PSHPSoundexLast, pshp_soundex_last
from ._ParmarKumbharana import ParmarKumbharana, parmar_kumbharana
from ._Phonem import Phonem, phonem
from ._Phonet import Phonet, phonet
from ._PhoneticSpanish import PhoneticSpanish, phonetic_spanish
from ._Phonex import Phonex, phonex
from ._Phonix import Phonix, phonix
from ._RefinedSoundex import RefinedSoundex, refined_soundex
from ._RethSchek import RethSchek, reth_schek_phonetik
from ._RogerRoot import RogerRoot, roger_root
from ._RussellIndex import (
    RussellIndex,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)
from ._SPFC import SPFC, spfc
from ._SfinxBis import SfinxBis, sfinxbis
from ._SoundD import SoundD, sound_d
from ._Soundex import Soundex, soundex
from ._SoundexBR import SoundexBR, soundex_br
from ._SpanishMetaphone import SpanishMetaphone, spanish_metaphone
from ._StatisticsCanada import StatisticsCanada, statistics_canada

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
