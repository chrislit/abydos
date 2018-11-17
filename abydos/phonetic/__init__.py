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

The phonetic package includes classes for phonetic algorithms,
including:

    - Robert C. Russell's Index (:py:class:`.RussellIndex`)
    - American Soundex (:py:class:`.Soundex`)
    - Refined Soundex (:py:class:`.RefinedSoundex`)
    - Daitch-Mokotoff Soundex (:py:class:`.DaitchMokotoff`)
    - NYSIIS (:py:class:`.NYSIIS`)
    - Match Rating Algorithm (:py:class:`.phonetic.MRA`)
    - Metaphone (:py:class:`.Metaphone`)
    - Double Metaphone (:py:class:`.DoubleMetaphone`)
    - Caverphone (:py:class:`.Caverphone`)
    - Alpha Search Inquiry System (:py:class:`.AlphaSIS`)
    - Fuzzy Soundex (:py:class:`.FuzzySoundex`)
    - Phonex (:py:class:`.Phonex`)
    - Phonem (:py:class:`.Phonem`)
    - Phonix (:py:class:`.Phonix`)
    - Standardized Phonetic Frequency Code (:py:class:`.SPFC`)
    - Statistics Canada (:py:class:`.StatisticsCanada`)
    - Lein (:py:class:`.Lein`)
    - Roger Root (:py:class:`.RogerRoot`)
    - Eudex phonetic hash (:py:class:`.phonetic.Eudex`)
    - Parmar-Kumbharana (:py:class:`.ParmarKumbharana`)
    - Davidson's Consonant Code (:py:class:`.Davidson`)
    - SoundD (:py:class:`.SoundD`)
    - PSHP Soundex/Viewex Coding (:py:class:`.PSHPSoundexFirst` and
      :py:class:`.PSHPSoundexLast`)
    - Dolby Code (:py:class:`.Dolby`)
    - NRL English-to-phoneme (:py:class:`.NRL`)
    - Beider-Morse Phonetic Matching (:py:class:`.BeiderMorse`)

There are also language-specific phonetic algorithms for German:

    - Kölner Phonetik (:py:class:`.Koelner`)
    - phonet (:py:class:`.Phonet`)
    - Haase Phonetik (:py:class:`.Haase`)
    - Reth-Schek Phonetik (:py:class:`.RethSchek`)

For French:

    - FONEM (:py:class:`.FONEM`)
    - an early version of Henry Code (:py:class:`.HenryEarly`)

For Spanish:

    - Phonetic Spanish (:py:class:`.PhoneticSpanish`)
    - Spanish Metaphone (:py:class:`.SpanishMetaphone`)

For Swedish:

    - SfinxBis (:py:class:`.SfinxBis`)

For Norwegian:

    - Norphone (:py:class:`.Norphone`)

For Brazilian Portuguese:

    - SoundexBR (:py:class:`.SoundexBR`)

And there are some hybrid phonetic algorithms that employ multiple underlying
phonetic algorithms:

    - Oxford Name Compression Algorithm (ONCA) (:py:class:`.ONCA`)
    - MetaSoundex (:py:class:`.MetaSoundex`)


Each class has an ``encode`` method to return the phonetically encoded string.
Classes for which ``encode`` returns a numeric value generally have an
``encode_alpha`` method that returns an alphabetic version of the phonetic
encoding, as demonstrated below:

>>> rus = RussellIndex()
>>> rus.encode('Abramson')
128637
>>> rus.encode_alpha('Abramson')
'ABRMCN'

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._alpha_sis import AlphaSIS, alpha_sis
from ._beider_morse import BeiderMorse, bmpm
from ._caverphone import Caverphone, caverphone
from ._daitch_mokotoff import DaitchMokotoff, dm_soundex
from ._davidson import Davidson, davidson
from ._dolby import Dolby, dolby
from ._double_metaphone import DoubleMetaphone, double_metaphone
from ._eudex import Eudex, eudex
from ._fonem import FONEM, fonem
from ._fuzzy_soundex import FuzzySoundex, fuzzy_soundex
from ._haase import Haase, haase_phonetik
from ._henry_early import HenryEarly, henry_early
from ._koelner import (
    Koelner,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
)
from ._lein import Lein, lein
from ._meta_soundex import MetaSoundex, metasoundex
from ._metaphone import Metaphone, metaphone
from ._mra import MRA, mra
from ._norphone import Norphone, norphone
from ._nrl import NRL, nrl
from ._nysiis import NYSIIS, nysiis
from ._onca import ONCA, onca
from ._parmar_kumbharana import ParmarKumbharana, parmar_kumbharana
from ._phonem import Phonem, phonem
from ._phonet import Phonet, phonet
from ._phonetic_spanish import PhoneticSpanish, phonetic_spanish
from ._phonex import Phonex, phonex
from ._phonix import Phonix, phonix
from ._pshp_soundex_first import PSHPSoundexFirst, pshp_soundex_first
from ._pshp_soundex_last import PSHPSoundexLast, pshp_soundex_last
from ._refined_soundex import RefinedSoundex, refined_soundex
from ._reth_schek import RethSchek, reth_schek_phonetik
from ._roger_root import RogerRoot, roger_root
from ._russell_index import (
    RussellIndex,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)
from ._sfinx_bis import SfinxBis, sfinxbis
from ._sound_d import SoundD, sound_d
from ._soundex import Soundex, soundex
from ._soundex_br import SoundexBR, soundex_br
from ._spanish_metaphone import SpanishMetaphone, spanish_metaphone
from ._spfc import SPFC, spfc
from ._statistics_canada import StatisticsCanada, statistics_canada

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
