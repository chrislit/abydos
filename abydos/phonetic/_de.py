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

"""abydos.phonetic._de.

The phonetic._de module implements the Kölner Phonetik and related
algorithms for German:

    - Kölner Phonetik
    - Phonem
    - Haase Phonetik
    - Reth-Schek Phonetik
"""

from __future__ import unicode_literals

from itertools import product
from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._util import _delete_consecutive_repeats

__all__ = [
    'haase_phonetik',
    'koelner_phonetik',
    'koelner_phonetik_alpha',
    'koelner_phonetik_num_to_alpha',
    'phonem',
    'reth_schek_phonetik',
]


def koelner_phonetik(word):
    """Return the Kölner Phonetik (numeric output) code for a word.

    Based on the algorithm defined by :cite:`Postel:1969`.

    While the output code is numeric, it is still a str because 0s can lead
    the code.

    :param str word: the word to transform
    :returns: the Kölner Phonetik value as a numeric string
    :rtype: str

    >>> koelner_phonetik('Christopher')
    '478237'
    >>> koelner_phonetik('Niall')
    '65'
    >>> koelner_phonetik('Smith')
    '862'
    >>> koelner_phonetik('Schmidt')
    '862'
    >>> koelner_phonetik('Müller')
    '657'
    >>> koelner_phonetik('Zimmermann')
    '86766'
    """

    def _after(word, pos, letters):
        """Return True if word[i] follows one of the supplied letters."""
        return pos > 0 and word[pos - 1] in letters

    def _before(word, pos, letters):
        """Return True if word[i] precedes one of the supplied letters."""
        return pos + 1 < len(word) and word[pos + 1] in letters

    _vowels = {'A', 'E', 'I', 'J', 'O', 'U', 'Y'}

    sdx = ''

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join(
        c
        for c in word
        if c
        in {
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        }
    )

    # Nothing to convert, return base case
    if not word:
        return sdx

    for i in range(len(word)):
        if word[i] in _vowels:
            sdx += '0'
        elif word[i] == 'B':
            sdx += '1'
        elif word[i] == 'P':
            if _before(word, i, {'H'}):
                sdx += '3'
            else:
                sdx += '1'
        elif word[i] in {'D', 'T'}:
            if _before(word, i, {'C', 'S', 'Z'}):
                sdx += '8'
            else:
                sdx += '2'
        elif word[i] in {'F', 'V', 'W'}:
            sdx += '3'
        elif word[i] in {'G', 'K', 'Q'}:
            sdx += '4'
        elif word[i] == 'C':
            if _after(word, i, {'S', 'Z'}):
                sdx += '8'
            elif i == 0:
                if _before(
                    word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'}
                ):
                    sdx += '4'
                else:
                    sdx += '8'
            elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                sdx += '4'
            else:
                sdx += '8'
        elif word[i] == 'X':
            if _after(word, i, {'C', 'K', 'Q'}):
                sdx += '8'
            else:
                sdx += '48'
        elif word[i] == 'L':
            sdx += '5'
        elif word[i] in {'M', 'N'}:
            sdx += '6'
        elif word[i] == 'R':
            sdx += '7'
        elif word[i] in {'S', 'Z'}:
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)

    if sdx:
        sdx = sdx[:1] + sdx[1:].replace('0', '')

    return sdx


def koelner_phonetik_num_to_alpha(num):
    """Convert a Kölner Phonetik code from numeric to alphabetic.

    :param str num: a numeric Kölner Phonetik representation (can be a str or
        an int)
    :returns: an alphabetic representation of the same word
    :rtype: str

    >>> koelner_phonetik_num_to_alpha('862')
    'SNT'
    >>> koelner_phonetik_num_to_alpha('657')
    'NLR'
    >>> koelner_phonetik_num_to_alpha('86766')
    'SNRNN'
    """
    _koelner_num_translation = dict(
        zip((ord(_) for _ in '012345678'), 'APTFKLNRS')
    )
    num = ''.join(
        c
        for c in text_type(num)
        if c in {'0', '1', '2', '3', '4', '5', '6', '7', '8'}
    )
    return num.translate(_koelner_num_translation)


def koelner_phonetik_alpha(word):
    """Return the Kölner Phonetik (alphabetic output) code for a word.

    :param str word: the word to transform
    :returns: the Kölner Phonetik value as an alphabetic string
    :rtype: str

    >>> koelner_phonetik_alpha('Smith')
    'SNT'
    >>> koelner_phonetik_alpha('Schmidt')
    'SNT'
    >>> koelner_phonetik_alpha('Müller')
    'NLR'
    >>> koelner_phonetik_alpha('Zimmermann')
    'SNRNN'
    """
    return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def phonem(word):
    """Return the Phonem code for a word.

    Phonem is defined in :cite:`Wilde:1988`.

    This version is based on the Perl implementation documented at
    :cite:`Wilz:2005`.
    It includes some enhancements presented in the Java port at
    :cite:`dcm4che:2011`.

    Phonem is intended chiefly for German names/words.

    :param str word: the word to transform
    :returns: the Phonem value
    :rtype: str

    >>> phonem('Christopher')
    'CRYSDOVR'
    >>> phonem('Niall')
    'NYAL'
    >>> phonem('Smith')
    'SMYD'
    >>> phonem('Schmidt')
    'CMYD'
    """
    _phonem_substitutions = (
        ('SC', 'C'),
        ('SZ', 'C'),
        ('CZ', 'C'),
        ('TZ', 'C'),
        ('TS', 'C'),
        ('KS', 'X'),
        ('PF', 'V'),
        ('QU', 'KW'),
        ('PH', 'V'),
        ('UE', 'Y'),
        ('AE', 'E'),
        ('OE', 'Ö'),
        ('EI', 'AY'),
        ('EY', 'AY'),
        ('EU', 'OY'),
        ('AU', 'A§'),
        ('OU', '§'),
    )
    _phonem_translation = dict(
        zip(
            (ord(_) for _ in 'ZKGQÇÑßFWPTÁÀÂÃÅÄÆÉÈÊËIJÌÍÎÏÜÝ§ÚÙÛÔÒÓÕØ'),
            'CCCCCNSVVBDAAAAAEEEEEEYYYYYYYYUUUUOOOOÖ',
        )
    )

    word = unicode_normalize('NFC', text_type(word.upper()))
    for i, j in _phonem_substitutions:
        word = word.replace(i, j)
    word = word.translate(_phonem_translation)

    return ''.join(
        c
        for c in _delete_consecutive_repeats(word)
        if c
        in {
            'A',
            'B',
            'C',
            'D',
            'L',
            'M',
            'N',
            'O',
            'R',
            'S',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Ö',
        }
    )


def haase_phonetik(word, primary_only=False):
    """Return the Haase Phonetik (numeric output) code for a word.

    Based on the algorithm described at :cite:`Prante:2015`.

    Based on the original :cite:`Haase:2000`.

    While the output code is numeric, it is nevertheless a str.

    :param str word: the word to transform
    :param bool primary_only: if True, only the primary code is returned
    :returns: the Haase Phonetik value as a numeric string
    :rtype: tuple

    >>> haase_phonetik('Joachim')
    ('9496',)
    >>> haase_phonetik('Christoph')
    ('4798293', '8798293')
    >>> haase_phonetik('Jörg')
    ('974',)
    >>> haase_phonetik('Smith')
    ('8692',)
    >>> haase_phonetik('Schmidt')
    ('8692', '4692')
    """

    def _after(word, i, letters):
        """Return True if word[i] follows one of the supplied letters."""
        if i > 0 and word[i - 1] in letters:
            return True
        return False

    def _before(word, i, letters):
        """Return True if word[i] precedes one of the supplied letters."""
        if i + 1 < len(word) and word[i + 1] in letters:
            return True
        return False

    _vowels = {'A', 'E', 'I', 'J', 'O', 'U', 'Y'}

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join(
        c
        for c in word
        if c
        in {
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        }
    )

    variants = []
    if primary_only:
        variants = [word]
    else:
        pos = 0
        if word[:2] == 'CH':
            variants.append(('CH', 'SCH'))
            pos += 2
        len_3_vars = {
            'OWN': 'AUN',
            'WSK': 'RSK',
            'SCH': 'CH',
            'GLI': 'LI',
            'AUX': 'O',
            'EUX': 'O',
        }
        while pos < len(word):
            if word[pos : pos + 4] == 'ILLE':
                variants.append(('ILLE', 'I'))
                pos += 4
            elif word[pos : pos + 3] in len_3_vars:
                variants.append(
                    (word[pos : pos + 3], len_3_vars[word[pos : pos + 3]])
                )
                pos += 3
            elif word[pos : pos + 2] == 'RB':
                variants.append(('RB', 'RW'))
                pos += 2
            elif len(word[pos:]) == 3 and word[pos:] == 'EAU':
                variants.append(('EAU', 'O'))
                pos += 3
            elif len(word[pos:]) == 1 and word[pos:] in {'A', 'O'}:
                if word[pos:] == 'O':
                    variants.append(('O', 'OW'))
                else:
                    variants.append(('A', 'AR'))
                pos += 1
            else:
                variants.append((word[pos],))
                pos += 1

        variants = [''.join(letters) for letters in product(*variants)]

    def _haase_code(word):
        sdx = ''
        for i in range(len(word)):
            if word[i] in _vowels:
                sdx += '9'
            elif word[i] == 'B':
                sdx += '1'
            elif word[i] == 'P':
                if _before(word, i, {'H'}):
                    sdx += '3'
                else:
                    sdx += '1'
            elif word[i] in {'D', 'T'}:
                if _before(word, i, {'C', 'S', 'Z'}):
                    sdx += '8'
                else:
                    sdx += '2'
            elif word[i] in {'F', 'V', 'W'}:
                sdx += '3'
            elif word[i] in {'G', 'K', 'Q'}:
                sdx += '4'
            elif word[i] == 'C':
                if _after(word, i, {'S', 'Z'}):
                    sdx += '8'
                elif i == 0:
                    if _before(
                        word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'}
                    ):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif word[i] == 'X':
                if _after(word, i, {'C', 'K', 'Q'}):
                    sdx += '8'
                else:
                    sdx += '48'
            elif word[i] == 'L':
                sdx += '5'
            elif word[i] in {'M', 'N'}:
                sdx += '6'
            elif word[i] == 'R':
                sdx += '7'
            elif word[i] in {'S', 'Z'}:
                sdx += '8'

        sdx = _delete_consecutive_repeats(sdx)

        return sdx

    encoded = tuple(_haase_code(word) for word in variants)
    if len(encoded) > 1:
        encoded_set = set()
        encoded_single = []
        for code in encoded:
            if code not in encoded_set:
                encoded_set.add(code)
                encoded_single.append(code)
        return tuple(encoded_single)

    return encoded


def reth_schek_phonetik(word):
    """Return Reth-Schek Phonetik code for a word.

    This algorithm is proposed in :cite:`Reth:1977`.

    Since I couldn't secure a copy of that document (maybe I'll look for it
    next time I'm in Germany), this implementation is based on what I could
    glean from the implementations published by German Record Linkage
    Center (www.record-linkage.de):

    - Privacy-preserving Record Linkage (PPRL) (in R) :cite:`Rukasz:2018`
    - Merge ToolBox (in Java) :cite:`Schnell:2004`

    Rules that are unclear:

    - Should 'C' become 'G' or 'Z'? (PPRL has both, 'Z' rule blocked)
    - Should 'CC' become 'G'? (PPRL has blocked 'CK' that may be typo)
    - Should 'TUI' -> 'ZUI' rule exist? (PPRL has rule, but I can't
      think of a German word with '-tui-' in it.)
    - Should we really change 'SCH' -> 'CH' and then 'CH' -> 'SCH'?

    :param str word: the word to transform
    :returns: the Reth-Schek Phonetik code
    :rtype: str

    >>> reth_schek_phonetik('Joachim')
    'JOAGHIM'
    >>> reth_schek_phonetik('Christoph')
    'GHRISDOF'
    >>> reth_schek_phonetik('Jörg')
    'JOERG'
    >>> reth_schek_phonetik('Smith')
    'SMID'
    >>> reth_schek_phonetik('Schmidt')
    'SCHMID'
    """
    replacements = {
        3: {
            'AEH': 'E',
            'IEH': 'I',
            'OEH': 'OE',
            'UEH': 'UE',
            'SCH': 'CH',
            'ZIO': 'TIO',
            'TIU': 'TIO',
            'ZIU': 'TIO',
            'CHS': 'X',
            'CKS': 'X',
            'AEU': 'OI',
        },
        2: {
            'LL': 'L',
            'AA': 'A',
            'AH': 'A',
            'BB': 'B',
            'PP': 'B',
            'BP': 'B',
            'PB': 'B',
            'DD': 'D',
            'DT': 'D',
            'TT': 'D',
            'TH': 'D',
            'EE': 'E',
            'EH': 'E',
            'AE': 'E',
            'FF': 'F',
            'PH': 'F',
            'KK': 'K',
            'GG': 'G',
            'GK': 'G',
            'KG': 'G',
            'CK': 'G',
            'CC': 'C',
            'IE': 'I',
            'IH': 'I',
            'MM': 'M',
            'NN': 'N',
            'OO': 'O',
            'OH': 'O',
            'SZ': 'S',
            'UH': 'U',
            'GS': 'X',
            'KS': 'X',
            'TZ': 'Z',
            'AY': 'AI',
            'EI': 'AI',
            'EY': 'AI',
            'EU': 'OI',
            'RR': 'R',
            'SS': 'S',
            'KW': 'QU',
        },
        1: {
            'P': 'B',
            'T': 'D',
            'V': 'F',
            'W': 'F',
            'C': 'G',
            'K': 'G',
            'Y': 'I',
        },
    }

    # Uppercase
    word = word.upper()

    # Replace umlauts/eszett
    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = word.replace('ß', 'SS')

    # Main loop, using above replacements table
    pos = 0
    while pos < len(word):
        for num in range(3, 0, -1):
            if word[pos : pos + num] in replacements[num]:
                word = (
                    word[:pos]
                    + replacements[num][word[pos : pos + num]]
                    + word[pos + num :]
                )
                pos += 1
                break
        else:
            pos += 1  # Advance if nothing is recognized

    # Change 'CH' back(?) to 'SCH'
    word = word.replace('CH', 'SCH')

    # Replace final sequences
    if word[-2:] == 'ER':
        word = word[:-2] + 'R'
    elif word[-2:] == 'EL':
        word = word[:-2] + 'L'
    elif word[-1:] == 'H':
        word = word[:-1]

    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
