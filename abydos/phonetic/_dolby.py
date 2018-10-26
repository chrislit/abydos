# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.phonetic._dolby.

The phonetic._dolby module implements the Dolby Code algorithm.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = ['dolby']


def dolby(word, max_length=-1, keep_vowels=False, vowel_char='*'):
    r"""Return the Dolby Code of a name.

    This follows "A Spelling Equivalent Abbreviation Algorithm For Personal
    Names" from :cite:`Dolby:1970` and :cite:`Cunningham:1969`.

    :param word: the word to encode
    :param max_length: maximum length of the returned Dolby code -- this also
        activates the fixed-length code mode if it is greater than 0
    :param keep_vowels: if True, retains all vowel markers
    :param vowel_char: the vowel marker character (default to \*)
    :returns: the Dolby Code
    :rtype: str

    >>> dolby('Hansen')
    'H*NSN'
    >>> dolby('Larsen')
    'L*RSN'
    >>> dolby('Aagaard')
    '*GR'
    >>> dolby('Braaten')
    'BR*DN'
    >>> dolby('Sandvik')
    'S*NVK'
    >>> dolby('Hansen', max_length=6)
    'H*NS*N'
    >>> dolby('Larsen', max_length=6)
    'L*RS*N'
    >>> dolby('Aagaard', max_length=6)
    '*G*R  '
    >>> dolby('Braaten', max_length=6)
    'BR*D*N'
    >>> dolby('Sandvik', max_length=6)
    'S*NF*K'

    >>> dolby('Smith')
    'SM*D'
    >>> dolby('Waters')
    'W*DRS'
    >>> dolby('James')
    'J*MS'
    >>> dolby('Schmidt')
    'SM*D'
    >>> dolby('Ashcroft')
    '*SKRFD'
    >>> dolby('Smith', max_length=6)
    'SM*D  '
    >>> dolby('Waters', max_length=6)
    'W*D*RS'
    >>> dolby('James', max_length=6)
    'J*M*S '
    >>> dolby('Schmidt', max_length=6)
    'SM*D  '
    >>> dolby('Ashcroft', max_length=6)
    '*SKRFD'
    """
    _vowels = {'A', 'E', 'I', 'O', 'U', 'Y'}

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
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

    # Rule 1 (FL2)
    if word[:3] in {'MCG', 'MAG', 'MAC'}:
        word = 'MK' + word[3:]
    elif word[:2] == 'MC':
        word = 'MK' + word[2:]

    # Rule 2 (FL3)
    pos = len(word) - 2
    while pos > -1:
        if word[pos : pos + 2] in {
            'DT',
            'LD',
            'ND',
            'NT',
            'RC',
            'RD',
            'RT',
            'SC',
            'SK',
            'ST',
        }:
            word = word[: pos + 1] + word[pos + 2 :]
            pos += 1
        pos -= 1

    # Rule 3 (FL4)
    # Although the rule indicates "after the first letter", the test cases make
    # it clear that these apply to the first letter also.
    word = word.replace('X', 'KS')
    word = word.replace('CE', 'SE')
    word = word.replace('CI', 'SI')
    word = word.replace('CY', 'SI')

    # not in the rule set, but they seem to have intended it
    word = word.replace('TCH', 'CH')

    pos = word.find('CH', 1)
    while pos != -1:
        if word[pos - 1 : pos] not in _vowels:
            word = word[:pos] + 'S' + word[pos + 1 :]
        pos = word.find('CH', pos + 1)

    word = word.replace('C', 'K')
    word = word.replace('Z', 'S')

    word = word.replace('WR', 'R')
    word = word.replace('DG', 'G')
    word = word.replace('QU', 'K')
    word = word.replace('T', 'D')
    word = word.replace('PH', 'F')

    # Rule 4 (FL5)
    # Although the rule indicates "after the first letter", the test cases make
    # it clear that these apply to the first letter also.
    pos = word.find('K', 0)
    while pos != -1:
        if pos > 1 and word[pos - 1 : pos] not in _vowels | {'L', 'N', 'R'}:
            word = word[: pos - 1] + word[pos:]
            pos -= 1
        pos = word.find('K', pos + 1)

    # Rule FL6
    if max_length > 0 and word[-1:] == 'E':
        word = word[:-1]

    # Rule 5 (FL7)
    word = _delete_consecutive_repeats(word)

    # Rule 6 (FL8)
    if word[:2] == 'PF':
        word = word[1:]
    if word[-2:] == 'PF':
        word = word[:-1]
    elif word[-2:] == 'GH':
        if word[-3:-2] in _vowels:
            word = word[:-2] + 'F'
        else:
            word = word[:-2] + 'G'
    word = word.replace('GH', '')

    # Rule FL9
    if max_length > 0:
        word = word.replace('V', 'F')

    # Rules 7-9 (FL10-FL12)
    first = 1 + (1 if max_length > 0 else 0)
    code = ''
    for pos, char in enumerate(word):
        if char in _vowels:
            if first or keep_vowels:
                code += vowel_char
                first -= 1
        elif pos > 0 and char in {'W', 'H'}:
            continue
        else:
            code += char

    if max_length > 0:
        # Rule FL13
        if len(code) > max_length and code[-1:] == 'S':
            code = code[:-1]
        if keep_vowels:
            code = code[:max_length]
        else:
            # Rule FL14
            code = code[: max_length + 2]
            # Rule FL15
            while len(code) > max_length:
                vowels = len(code) - max_length
                excess = vowels - 1
                word = code
                code = ''
                for char in word:
                    if char == vowel_char:
                        if vowels:
                            code += char
                            vowels -= 1
                    else:
                        code += char
                code = code[: max_length + excess]

        # Rule FL16
        code += ' ' * (max_length - len(code))

    return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
