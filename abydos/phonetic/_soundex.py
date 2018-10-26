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

"""abydos.phonetic._soundex.

The phonetic._soundex module implements phonetic algorithms that are generally
Soundex-like, including:

    - American Soundex
    - Refined Soundex
    - Fuzzy Soundex
    - Phonex
    - Phonix
    - Lein
    - PSHP Soundex/Viewex Coding

Being Soundex-like, for the purposes of this module means: targeted at English,
returning a code that starts with a letter and continues with (usually 3)
numerals, and mostly based on a simple translation table.
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._util import _delete_consecutive_repeats

__all__ = [
    'fuzzy_soundex',
    'lein',
    'phonex',
    'phonix',
    'pshp_soundex_first',
    'pshp_soundex_last',
    'refined_soundex',
    'soundex',
]


def soundex(word, max_length=4, var='American', reverse=False, zero_pad=True):
    """Return the Soundex code for a word.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param str var: the variant of the algorithm to employ (defaults to
        'American'):

        - 'American' follows the American Soundex algorithm, as described at
          :cite:`US:2007` and in :cite:`Knuth:1998`; this is also called
          Miracode
        - 'special' follows the rules from the 1880-1910 US Census
          retrospective re-analysis, in which h & w are not treated as blocking
          consonants but as vowels. Cf. :cite:`Repici:2013`.
        - 'Census' follows the rules laid out in GIL 55 :cite:`US:1997` by the
          US Census, including coding prefixed and unprefixed versions of some
          names

    :param bool reverse: reverse the word before computing the selected Soundex
        (defaults to False); This results in "Reverse Soundex", which is useful
        for blocking in cases where the initial elements may be in error.
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Soundex value
    :rtype: str

    >>> soundex("Christopher")
    'C623'
    >>> soundex("Niall")
    'N400'
    >>> soundex('Smith')
    'S530'
    >>> soundex('Schmidt')
    'S530'

    >>> soundex('Christopher', max_length=-1)
    'C623160000000000000000000000000000000000000000000000000000000000'
    >>> soundex('Christopher', max_length=-1, zero_pad=False)
    'C62316'

    >>> soundex('Christopher', reverse=True)
    'R132'

    >>> soundex('Ashcroft')
    'A261'
    >>> soundex('Asicroft')
    'A226'
    >>> soundex('Ashcroft', var='special')
    'A226'
    >>> soundex('Asicroft', var='special')
    'A226'
    """
    _soundex_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230129022455012623019202',
        )
    )

    # Require a max_length of at least 4 and not more than 64
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    if var == 'Census':
        # TODO: Should these prefixes be supplemented? (VANDE, DELA, VON)
        if word[:3] in {'VAN', 'CON'} and len(word) > 4:
            return (
                soundex(word, max_length, 'American', reverse, zero_pad),
                soundex(word[3:], max_length, 'American', reverse, zero_pad),
            )
        if word[:2] in {'DE', 'DI', 'LA', 'LE'} and len(word) > 3:
            return (
                soundex(word, max_length, 'American', reverse, zero_pad),
                soundex(word[2:], max_length, 'American', reverse, zero_pad),
            )
        # Otherwise, proceed as usual (var='American' mode, ostensibly)

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
        if zero_pad:
            return '0' * max_length
        return '0'

    # Reverse word if computing Reverse Soundex
    if reverse:
        word = word[::-1]

    # apply the Soundex algorithm
    sdx = word.translate(_soundex_translation)

    if var == 'special':
        sdx = sdx.replace('9', '0')  # special rule for 1880-1910 census
    else:
        sdx = sdx.replace('9', '')  # rule 1
    sdx = _delete_consecutive_repeats(sdx)  # rule 3

    if word[0] in 'HW':
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]
    sdx = sdx.replace('0', '')  # rule 1

    if zero_pad:
        sdx += '0' * max_length  # rule 4

    return sdx[:max_length]


def refined_soundex(word, max_length=-1, zero_pad=False, retain_vowels=False):
    """Return the Refined Soundex code for a word.

    This is Soundex, but with more character classes. It was defined at
    :cite:`Boyce:1998`.

    :param word: the word to transform
    :param max_length: the length of the code returned (defaults to unlimited)
    :param zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :param retain_vowels: retain vowels (as 0) in the resulting code
    :returns: the Refined Soundex value
    :rtype: str

    >>> refined_soundex('Christopher')
    'C393619'
    >>> refined_soundex('Niall')
    'N87'
    >>> refined_soundex('Smith')
    'S386'
    >>> refined_soundex('Schmidt')
    'S386'
    """
    _ref_soundex_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01360240043788015936020505',
        )
    )

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

    # apply the Soundex algorithm
    sdx = word[:1] + word.translate(_ref_soundex_translation)
    sdx = _delete_consecutive_repeats(sdx)
    if not retain_vowels:
        sdx = sdx.replace('0', '')  # Delete vowels, H, W, Y

    if max_length > 0:
        if zero_pad:
            sdx += '0' * max_length
        sdx = sdx[:max_length]

    return sdx


def fuzzy_soundex(word, max_length=5, zero_pad=True):
    """Return the Fuzzy Soundex code for a word.

    Fuzzy Soundex is an algorithm derived from Soundex, defined in
    :cite:`Holmes:2002`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Fuzzy Soundex value
    :rtype: str

    >>> fuzzy_soundex('Christopher')
    'K6931'
    >>> fuzzy_soundex('Niall')
    'N4000'
    >>> fuzzy_soundex('Smith')
    'S5300'
    >>> fuzzy_soundex('Smith')
    'S5300'
    """
    _fuzzy_soundex_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '0193017-07745501769301-7-9',
        )
    )

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    if not word:
        if zero_pad:
            return '0' * max_length
        return '0'

    if word[:2] in {'CS', 'CZ', 'TS', 'TZ'}:
        word = 'SS' + word[2:]
    elif word[:2] == 'GN':
        word = 'NN' + word[2:]
    elif word[:2] in {'HR', 'WR'}:
        word = 'RR' + word[2:]
    elif word[:2] == 'HW':
        word = 'WW' + word[2:]
    elif word[:2] in {'KN', 'NG'}:
        word = 'NN' + word[2:]

    if word[-2:] == 'CH':
        word = word[:-2] + 'KK'
    elif word[-2:] == 'NT':
        word = word[:-2] + 'TT'
    elif word[-2:] == 'RT':
        word = word[:-2] + 'RR'
    elif word[-3:] == 'RDT':
        word = word[:-3] + 'RR'

    word = word.replace('CA', 'KA')
    word = word.replace('CC', 'KK')
    word = word.replace('CK', 'KK')
    word = word.replace('CE', 'SE')
    word = word.replace('CHL', 'KL')
    word = word.replace('CL', 'KL')
    word = word.replace('CHR', 'KR')
    word = word.replace('CR', 'KR')
    word = word.replace('CI', 'SI')
    word = word.replace('CO', 'KO')
    word = word.replace('CU', 'KU')
    word = word.replace('CY', 'SY')
    word = word.replace('DG', 'GG')
    word = word.replace('GH', 'HH')
    word = word.replace('MAC', 'MK')
    word = word.replace('MC', 'MK')
    word = word.replace('NST', 'NSS')
    word = word.replace('PF', 'FF')
    word = word.replace('PH', 'FF')
    word = word.replace('SCH', 'SSS')
    word = word.replace('TIO', 'SIO')
    word = word.replace('TIA', 'SIO')
    word = word.replace('TCH', 'CHH')

    sdx = word.translate(_fuzzy_soundex_translation)
    sdx = sdx.replace('-', '')

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    if word[0] in {'H', 'W', 'Y'}:
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]

    sdx = sdx.replace('0', '')

    if zero_pad:
        sdx += '0' * max_length

    return sdx[:max_length]


def phonex(word, max_length=4, zero_pad=True):
    """Return the Phonex code for a word.

    Phonex is an algorithm derived from Soundex, defined in :cite:`Lait:1996`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Phonex value
    :rtype: str

    >>> phonex('Christopher')
    'C623'
    >>> phonex('Niall')
    'N400'
    >>> phonex('Schmidt')
    'S253'
    >>> phonex('Smith')
    'S530'
    """
    name = unicode_normalize('NFKD', text_type(word.upper()))
    name = name.replace('ß', 'SS')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    name_code = last = ''

    # Deletions effected by replacing with next letter which
    # will be ignored due to duplicate handling of Soundex code.
    # This is faster than 'moving' all subsequent letters.

    # Remove any trailing Ss
    while name[-1:] == 'S':
        name = name[:-1]

    # Phonetic equivalents of first 2 characters
    # Works since duplicate letters are ignored
    if name[:2] == 'KN':
        name = 'N' + name[2:]  # KN.. == N..
    elif name[:2] == 'PH':
        name = 'F' + name[2:]  # PH.. == F.. (H ignored anyway)
    elif name[:2] == 'WR':
        name = 'R' + name[2:]  # WR.. == R..

    if name:
        # Special case, ignore H first letter (subsequent Hs ignored anyway)
        # Works since duplicate letters are ignored
        if name[0] == 'H':
            name = name[1:]

    if name:
        # Phonetic equivalents of first character
        if name[0] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            name = 'A' + name[1:]
        elif name[0] in {'B', 'P'}:
            name = 'B' + name[1:]
        elif name[0] in {'V', 'F'}:
            name = 'F' + name[1:]
        elif name[0] in {'C', 'K', 'Q'}:
            name = 'C' + name[1:]
        elif name[0] in {'G', 'J'}:
            name = 'G' + name[1:]
        elif name[0] in {'S', 'Z'}:
            name = 'S' + name[1:]

        name_code = last = name[0]

    # Modified Soundex code
    for i in range(1, len(name)):
        code = '0'
        if name[i] in {'B', 'F', 'P', 'V'}:
            code = '1'
        elif name[i] in {'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z'}:
            code = '2'
        elif name[i] in {'D', 'T'}:
            if name[i + 1 : i + 2] != 'C':
                code = '3'
        elif name[i] == 'L':
            if name[i + 1 : i + 2] in {
                'A',
                'E',
                'I',
                'O',
                'U',
                'Y',
            } or i + 1 == len(name):
                code = '4'
        elif name[i] in {'M', 'N'}:
            if name[i + 1 : i + 2] in {'D', 'G'}:
                name = name[: i + 1] + name[i] + name[i + 2 :]
            code = '5'
        elif name[i] == 'R':
            if name[i + 1 : i + 2] in {
                'A',
                'E',
                'I',
                'O',
                'U',
                'Y',
            } or i + 1 == len(name):
                code = '6'

        if code != last and code != '0' and i != 0:
            name_code += code

        last = name_code[-1]

    if zero_pad:
        name_code += '0' * max_length
    if not name_code:
        name_code = '0'
    return name_code[:max_length]


def phonix(word, max_length=4, zero_pad=True):
    """Return the Phonix code for a word.

    Phonix is a Soundex-like algorithm defined in :cite:`Gadd:1990`.

    This implementation is based on:
    - :cite:`Pfeifer:2000`
    - :cite:`Christen:2011`
    - :cite:`Kollar:2007`

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Phonix value
    :rtype: str

    >>> phonix('Christopher')
    'K683'
    >>> phonix('Niall')
    'N400'
    >>> phonix('Smith')
    'S530'
    >>> phonix('Schmidt')
    'S530'
    """

    def _start_repl(word, src, tar, post=None):
        r"""Replace src with tar at the start of word."""
        if post:
            for i in post:
                if word.startswith(src + i):
                    return tar + word[len(src) :]
        elif word.startswith(src):
            return tar + word[len(src) :]
        return word

    def _end_repl(word, src, tar, pre=None):
        r"""Replace src with tar at the end of word."""
        if pre:
            for i in pre:
                if word.endswith(i + src):
                    return word[: -len(src)] + tar
        elif word.endswith(src):
            return word[: -len(src)] + tar
        return word

    def _mid_repl(word, src, tar, pre=None, post=None):
        r"""Replace src with tar in the middle of word."""
        if pre or post:
            if not pre:
                return word[0] + _all_repl(word[1:], src, tar, pre, post)
            elif not post:
                return _all_repl(word[:-1], src, tar, pre, post) + word[-1]
            return _all_repl(word, src, tar, pre, post)
        return word[0] + _all_repl(word[1:-1], src, tar, pre, post) + word[-1]

    def _all_repl(word, src, tar, pre=None, post=None):
        r"""Replace src with tar anywhere in word."""
        if pre or post:
            if post:
                post = post
            else:
                post = frozenset(('',))
            if pre:
                pre = pre
            else:
                pre = frozenset(('',))

            for i, j in ((i, j) for i in pre for j in post):
                word = word.replace(i + src + j, i + tar + j)
            return word
        else:
            return word.replace(src, tar)

    _vow = {'A', 'E', 'I', 'O', 'U'}
    _con = {
        'B',
        'C',
        'D',
        'F',
        'G',
        'H',
        'J',
        'K',
        'L',
        'M',
        'N',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'V',
        'W',
        'X',
        'Y',
        'Z',
    }

    _phonix_substitutions = (
        (_all_repl, 'DG', 'G'),
        (_all_repl, 'CO', 'KO'),
        (_all_repl, 'CA', 'KA'),
        (_all_repl, 'CU', 'KU'),
        (_all_repl, 'CY', 'SI'),
        (_all_repl, 'CI', 'SI'),
        (_all_repl, 'CE', 'SE'),
        (_start_repl, 'CL', 'KL', _vow),
        (_all_repl, 'CK', 'K'),
        (_end_repl, 'GC', 'K'),
        (_end_repl, 'JC', 'K'),
        (_start_repl, 'CHR', 'KR', _vow),
        (_start_repl, 'CR', 'KR', _vow),
        (_start_repl, 'WR', 'R'),
        (_all_repl, 'NC', 'NK'),
        (_all_repl, 'CT', 'KT'),
        (_all_repl, 'PH', 'F'),
        (_all_repl, 'AA', 'AR'),
        (_all_repl, 'SCH', 'SH'),
        (_all_repl, 'BTL', 'TL'),
        (_all_repl, 'GHT', 'T'),
        (_all_repl, 'AUGH', 'ARF'),
        (_mid_repl, 'LJ', 'LD', _vow, _vow),
        (_all_repl, 'LOUGH', 'LOW'),
        (_start_repl, 'Q', 'KW'),
        (_start_repl, 'KN', 'N'),
        (_end_repl, 'GN', 'N'),
        (_all_repl, 'GHN', 'N'),
        (_end_repl, 'GNE', 'N'),
        (_all_repl, 'GHNE', 'NE'),
        (_end_repl, 'GNES', 'NS'),
        (_start_repl, 'GN', 'N'),
        (_mid_repl, 'GN', 'N', None, _con),
        (_end_repl, 'GN', 'N'),
        (_start_repl, 'PS', 'S'),
        (_start_repl, 'PT', 'T'),
        (_start_repl, 'CZ', 'C'),
        (_mid_repl, 'WZ', 'Z', _vow),
        (_mid_repl, 'CZ', 'CH'),
        (_all_repl, 'LZ', 'LSH'),
        (_all_repl, 'RZ', 'RSH'),
        (_mid_repl, 'Z', 'S', None, _vow),
        (_all_repl, 'ZZ', 'TS'),
        (_mid_repl, 'Z', 'TS', _con),
        (_all_repl, 'HROUG', 'REW'),
        (_all_repl, 'OUGH', 'OF'),
        (_mid_repl, 'Q', 'KW', _vow, _vow),
        (_mid_repl, 'J', 'Y', _vow, _vow),
        (_start_repl, 'YJ', 'Y', _vow),
        (_start_repl, 'GH', 'G'),
        (_end_repl, 'GH', 'E', _vow),
        (_start_repl, 'CY', 'S'),
        (_all_repl, 'NX', 'NKS'),
        (_start_repl, 'PF', 'F'),
        (_end_repl, 'DT', 'T'),
        (_end_repl, 'TL', 'TIL'),
        (_end_repl, 'DL', 'DIL'),
        (_all_repl, 'YTH', 'ITH'),
        (_start_repl, 'TJ', 'CH', _vow),
        (_start_repl, 'TSJ', 'CH', _vow),
        (_start_repl, 'TS', 'T', _vow),
        (_all_repl, 'TCH', 'CH'),
        (_mid_repl, 'WSK', 'VSKIE', _vow),
        (_end_repl, 'WSK', 'VSKIE', _vow),
        (_start_repl, 'MN', 'N', _vow),
        (_start_repl, 'PN', 'N', _vow),
        (_mid_repl, 'STL', 'SL', _vow),
        (_end_repl, 'STL', 'SL', _vow),
        (_end_repl, 'TNT', 'ENT'),
        (_end_repl, 'EAUX', 'OH'),
        (_all_repl, 'EXCI', 'ECS'),
        (_all_repl, 'X', 'ECS'),
        (_end_repl, 'NED', 'ND'),
        (_all_repl, 'JR', 'DR'),
        (_end_repl, 'EE', 'EA'),
        (_all_repl, 'ZS', 'S'),
        (_mid_repl, 'R', 'AH', _vow, _con),
        (_end_repl, 'R', 'AH', _vow),
        (_mid_repl, 'HR', 'AH', _vow, _con),
        (_end_repl, 'HR', 'AH', _vow),
        (_end_repl, 'HR', 'AH', _vow),
        (_end_repl, 'RE', 'AR'),
        (_end_repl, 'R', 'AH', _vow),
        (_all_repl, 'LLE', 'LE'),
        (_end_repl, 'LE', 'ILE', _con),
        (_end_repl, 'LES', 'ILES', _con),
        (_end_repl, 'E', ''),
        (_end_repl, 'ES', 'S'),
        (_end_repl, 'SS', 'AS', _vow),
        (_end_repl, 'MB', 'M', _vow),
        (_all_repl, 'MPTS', 'MPS'),
        (_all_repl, 'MPS', 'MS'),
        (_all_repl, 'MPT', 'MT'),
    )

    _phonix_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230720022455012683070808',
        )
    )

    sdx = ''

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
    if word:
        for trans in _phonix_substitutions:
            word = trans[0](word, *trans[1:])
        if word[0] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            sdx = 'v' + word[1:].translate(_phonix_translation)
        else:
            sdx = word[0] + word[1:].translate(_phonix_translation)
        sdx = _delete_consecutive_repeats(sdx)
        sdx = sdx.replace('0', '')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    if zero_pad:
        sdx += '0' * max_length
    if not sdx:
        sdx = '0'
    return sdx[:max_length]


def lein(word, max_length=4, zero_pad=True):
    """Return the Lein code for a word.

    This is Lein name coding, described in :cite:`Moore:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 4) of the code to return
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Lein code
    :rtype: str

    >>> lein('Christopher')
    'C351'
    >>> lein('Niall')
    'N300'
    >>> lein('Smith')
    'S210'
    >>> lein('Schmidt')
    'S521'
    """
    _lein_translation = dict(
        zip((ord(_) for _ in 'BCDFGJKLMNPQRSTVXZ'), '451455532245351455')
    )

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

    code = word[:1]  # Rule 1
    word = word[1:].translate(
        {
            32: None,
            65: None,
            69: None,
            72: None,
            73: None,
            79: None,
            85: None,
            87: None,
            89: None,
        }
    )  # Rule 2
    word = _delete_consecutive_repeats(word)  # Rule 3
    code += word.translate(_lein_translation)  # Rule 4

    if zero_pad:
        code += '0' * max_length  # Rule 4

    return code[:max_length]


def pshp_soundex_last(lname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a last name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate function, pshp_soundex_first() is used for first names.

    :param str lname: the last name to encode
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool german: set to True if the name is German (different rules
        apply)
    :returns: the PSHP Soundex/Viewex Coding
    :rtype: str

    >>> pshp_soundex_last('Smith')
    'S530'
    >>> pshp_soundex_last('Waters')
    'W350'
    >>> pshp_soundex_last('James')
    'J500'
    >>> pshp_soundex_last('Schmidt')
    'S530'
    >>> pshp_soundex_last('Ashcroft')
    'A225'
    """
    lname = unicode_normalize('NFKD', text_type(lname.upper()))
    lname = lname.replace('ß', 'SS')
    lname = ''.join(
        c
        for c in lname
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

    # A. Prefix treatment
    if lname[:3] == 'VON' or lname[:3] == 'VAN':
        lname = lname[3:].strip()

    # The rule implemented below says "MC, MAC become 1". I believe it meant to
    # say they become M except in German data (where superscripted 1 indicates
    # "except in German data"). It doesn't make sense for them to become 1
    # (BPFV -> 1) or to apply outside German. Unfortunately, both articles have
    # this error(?).
    if not german:
        if lname[:3] == 'MAC':
            lname = 'M' + lname[3:]
        elif lname[:2] == 'MC':
            lname = 'M' + lname[2:]

    # The non-German-only rule to strip ' is unnecessary due to filtering

    if lname[:1] in {'E', 'I', 'O', 'U'}:
        lname = 'A' + lname[1:]
    elif lname[:2] in {'GE', 'GI', 'GY'}:
        lname = 'J' + lname[1:]
    elif lname[:2] in {'CE', 'CI', 'CY'}:
        lname = 'S' + lname[1:]
    elif lname[:3] == 'CHR':
        lname = 'K' + lname[1:]
    elif lname[:1] == 'C' and lname[:2] != 'CH':
        lname = 'K' + lname[1:]

    if lname[:2] == 'KN':
        lname = 'N' + lname[1:]
    elif lname[:2] == 'PH':
        lname = 'F' + lname[1:]
    elif lname[:3] in {'WIE', 'WEI'}:
        lname = 'V' + lname[1:]

    if german and lname[:1] in {'W', 'M', 'Y', 'Z'}:
        lname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[lname[0]] + lname[1:]

    code = lname[:1]

    # B. Postfix treatment
    if german:  # moved from end of postfix treatment due to blocking
        if lname[-3:] == 'TES':
            lname = lname[:-3]
        elif lname[-2:] == 'TS':
            lname = lname[:-2]
        if lname[-3:] == 'TZE':
            lname = lname[:-3]
        elif lname[-2:] == 'ZE':
            lname = lname[:-2]
        if lname[-1:] == 'Z':
            lname = lname[:-1]
        elif lname[-2:] == 'TE':
            lname = lname[:-2]

    if lname[-1:] == 'R':
        lname = lname[:-1] + 'N'
    elif lname[-2:] in {'SE', 'CE'}:
        lname = lname[:-2]
    if lname[-2:] == 'SS':
        lname = lname[:-2]
    elif lname[-1:] == 'S':
        lname = lname[:-1]

    if not german:
        l5_repl = {'STOWN': 'SAWON', 'MPSON': 'MASON'}
        l4_repl = {
            'NSEN': 'ASEN',
            'MSON': 'ASON',
            'STEN': 'SAEN',
            'STON': 'SAON',
        }
        if lname[-5:] in l5_repl:
            lname = lname[:-5] + l5_repl[lname[-5:]]
        elif lname[-4:] in l4_repl:
            lname = lname[:-4] + l4_repl[lname[-4:]]

    if lname[-2:] in {'NG', 'ND'}:
        lname = lname[:-1]
    if not german and lname[-3:] in {'GAN', 'GEN'}:
        lname = lname[:-3] + 'A' + lname[-2:]

    # C. Infix Treatment
    lname = lname.replace('CK', 'C')
    lname = lname.replace('SCH', 'S')
    lname = lname.replace('DT', 'T')
    lname = lname.replace('ND', 'N')
    lname = lname.replace('NG', 'N')
    lname = lname.replace('LM', 'M')
    lname = lname.replace('MN', 'M')
    lname = lname.replace('WIE', 'VIE')
    lname = lname.replace('WEI', 'VEI')

    # D. Soundexing
    # code for X & Y are unspecified, but presumably are 2 & 0
    _pshp_translation = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012523010202',
        )
    )

    lname = lname.translate(_pshp_translation)
    lname = _delete_consecutive_repeats(lname)

    code += lname[1:]
    code = code.replace('0', '')  # rule 1

    if max_length != -1:
        if len(code) < max_length:
            code += '0' * (max_length - len(code))
        else:
            code = code[:max_length]

    return code


def pshp_soundex_first(fname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a first name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate function, pshp_soundex_last() is used for last names.

    :param str fname: the first name to encode
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool german: set to True if the name is German (different rules
        apply)
    :returns: the PSHP Soundex/Viewex Coding
    :rtype: str

    >>> pshp_soundex_first('Smith')
    'S530'
    >>> pshp_soundex_first('Waters')
    'W352'
    >>> pshp_soundex_first('James')
    'J700'
    >>> pshp_soundex_first('Schmidt')
    'S500'
    >>> pshp_soundex_first('Ashcroft')
    'A220'
    >>> pshp_soundex_first('John')
    'J500'
    >>> pshp_soundex_first('Colin')
    'K400'
    >>> pshp_soundex_first('Niall')
    'N400'
    >>> pshp_soundex_first('Sally')
    'S400'
    >>> pshp_soundex_first('Jane')
    'J500'
    """
    fname = unicode_normalize('NFKD', text_type(fname.upper()))
    fname = fname.replace('ß', 'SS')
    fname = ''.join(
        c
        for c in fname
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

    # special rules
    if fname == 'JAMES':
        code = 'J7'
    elif fname == 'PAT':
        code = 'P7'

    else:
        # A. Prefix treatment
        if fname[:2] in {'GE', 'GI', 'GY'}:
            fname = 'J' + fname[1:]
        elif fname[:2] in {'CE', 'CI', 'CY'}:
            fname = 'S' + fname[1:]
        elif fname[:3] == 'CHR':
            fname = 'K' + fname[1:]
        elif fname[:1] == 'C' and fname[:2] != 'CH':
            fname = 'K' + fname[1:]

        if fname[:2] == 'KN':
            fname = 'N' + fname[1:]
        elif fname[:2] == 'PH':
            fname = 'F' + fname[1:]
        elif fname[:3] in {'WIE', 'WEI'}:
            fname = 'V' + fname[1:]

        if german and fname[:1] in {'W', 'M', 'Y', 'Z'}:
            fname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[fname[0]] + fname[
                1:
            ]

        code = fname[:1]

        # B. Soundex coding
        # code for Y unspecified, but presumably is 0
        _pshp_translation = dict(
            zip(
                (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                '01230120022455012523010202',
            )
        )

        fname = fname.translate(_pshp_translation)
        fname = _delete_consecutive_repeats(fname)

        code += fname[1:]
        syl_ptr = code.find('0')
        syl2_ptr = code[syl_ptr + 1 :].find('0')
        if syl_ptr != -1 and syl2_ptr != -1 and syl2_ptr - syl_ptr > -1:
            code = code[: syl_ptr + 2]

        code = code.replace('0', '')  # rule 1

    if max_length != -1:
        if len(code) < max_length:
            code += '0' * (max_length - len(code))
        else:
            code = code[:max_length]

    return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
