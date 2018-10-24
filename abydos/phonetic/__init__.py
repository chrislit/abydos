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

from itertools import groupby

__all__ = [
    'alpha_sis',
    'bmpm',
    'caverphone',
    'davidson',
    'de',
    'dm',
    'dolby',
    'es',
    'eudex',
    'fr',
    'hybrid',
    'metaphone',
    'mra',
    'nrl',
    'nysiis',
    'parmar_kumbharana',
    'phonet',
    'pt',
    'roger_root',
    'russell',
    'sound_d',
    'soundex',
    'spfc',
    'statistics_canada',
    'sv',
]


def _delete_consecutive_repeats(word):
    """Delete consecutive repeated characters in a word.

    :param str word: the word to transform
    :returns: word with consecutive repeating characters collapsed to
        a single instance
    :rtype: str

    >>> _delete_consecutive_repeats('REDDEE')
    'REDE'
    >>> _delete_consecutive_repeats('AEIOU')
    'AEIOU'
    >>> _delete_consecutive_repeats('AAACCCTTTGGG')
    'ACTG'
    """
    return ''.join(char for char, _ in groupby(word))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
