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

"""abydos.phonetic._nrl.

NRL English-to-phoneme algorithm
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from re import match as re_match

from ._phonetic import _Phonetic

__all__ = ['NRL', 'nrl']


class NRL(_Phonetic):
    """Naval Research Laboratory English-to-phoneme encoder.

    This is defined by :cite:`Elovitz:1976`.
    """

    _rules = {
        ' ': (
            ('', ' ', '', ' '),
            ('', '-', '', ''),
            ('.', '\'S', '', 'z'),
            ('#:.E', '\'S', '', 'z'),
            ('#', '\'S', '', 'z'),
            ('', '\'', '', ''),
            ('', ',', '', ' '),
            ('', '.', '', ' '),
            ('', '?', '', ' '),
            ('', '!', '', ' '),
        ),
        'A': (
            ('', 'A', ' ', 'AX'),
            (' ', 'ARE', ' ', 'AAr'),
            (' ', 'AR', 'O', 'AXr'),
            ('', 'AR', '#', 'EHr'),
            ('^', 'AS', '#', 'EYs'),
            ('', 'A', 'WA', 'AX'),
            ('', 'AW', '', 'AO'),
            (' :', 'ANY', '', 'EHnIY'),
            ('', 'A', '^+#', 'EY'),
            ('#:', 'ALLY', '', 'AXlIY'),
            (' ', 'AL', '#', 'AXl'),
            ('', 'AGAIN', '', 'AXgEHn'),
            ('#:', 'AG', 'E', 'IHj'),
            ('', 'A', '^+:#', 'AE'),
            (' :', 'A', '^+ ', 'EY'),
            ('', 'A', '^%', 'EY'),
            (' ', 'ARR', '', 'AXr'),
            ('', 'ARR', '', 'AEr'),
            (' :', 'AR', ' ', 'AAr'),
            ('', 'AR', ' ', 'ER'),
            ('', 'AR', '', 'AAr'),
            ('', 'AIR', '', 'EHr'),
            ('', 'AI', '', 'EY'),
            ('', 'AY', '', 'EY'),
            ('', 'AU', '', 'AO'),
            ('#:', 'AL', ' ', 'AXl'),
            ('#:', 'ALS', ' ', 'AXlz'),
            ('', 'ALK', '', 'AOk'),
            ('', 'AL', '^', 'AOl'),
            (' :', 'ABLE', '', 'EYbAXl'),
            ('', 'ABLE', '', 'AXbAXl'),
            ('', 'ANG', '+', 'EYnj'),
            ('', 'A', '', 'AE'),
        ),
        'B': (
            (' ', 'BE', '^#', 'bIH'),
            ('', 'BEING', '', 'bIYIHNG'),
            (' ', 'BOTH', ' ', 'bOWTH'),
            (' ', 'BUS', '#', 'bIHz'),
            ('', 'BUIL', '', 'bIHl'),
            ('', 'B', '', 'b'),
        ),
        'C': (
            (' ', 'CH', '^', 'k'),
            ('^E', 'CH', '', 'k'),
            ('', 'CH', '', 'CH'),
            (' S', 'CI', '#', 'sAY'),
            ('', 'CI', 'A', 'SH'),
            ('', 'CI', 'O', 'SH'),
            ('', 'CI', 'EN', 'SH'),
            ('', 'C', '+', 's'),
            ('', 'CK', '', 'k'),
            ('', 'COM', '%', 'kAHm'),
            ('', 'C', '', 'k'),
        ),
        'D': (
            ('#:', 'DED', ' ', 'dIHd'),
            ('.E', 'D', ' ', 'd'),
            ('#:^E', 'D', ' ', 't'),
            (' ', 'DE', '^#', 'dIH'),
            (' ', 'DO', ' ', 'dUW'),
            (' ', 'DOES', '', 'dAHz'),
            (' ', 'DOING', '', 'dUWIHNG'),
            (' ', 'DOW', '', 'dAW'),
            ('', 'DU', 'A', 'jUW'),
            ('', 'D', '', 'd'),
        ),
        'E': (
            ('#:', 'E', ' ', ''),
            ('\':^', 'E', ' ', ''),
            (' :', 'E', ' ', 'IY'),
            ('#', 'ED', ' ', 'd'),
            ('#:', 'E', 'D ', ''),
            ('', 'EV', 'ER', 'EHv'),
            ('', 'E', '^%', 'IY'),
            ('', 'ERI', '#', 'IYrIY'),
            ('', 'ERI', '', 'EHrIH'),
            ('#:', 'ER', '#', 'ER'),
            ('', 'ER', '#', 'EHr'),
            ('', 'ER', '', 'ER'),
            (' ', 'EVEN', '', 'IYvEHn'),
            ('#:', 'E', 'W', ''),
            ('T', 'EW', '', 'UW'),
            ('S', 'EW', '', 'UW'),
            ('R', 'EW', '', 'UW'),
            ('D', 'EW', '', 'UW'),
            ('L', 'EW', '', 'UW'),
            ('Z', 'EW', '', 'UW'),
            ('N', 'EW', '', 'UW'),
            ('J', 'EW', '', 'UW'),
            ('TH', 'EW', '', 'UW'),
            ('CH', 'EW', '', 'UW'),
            ('SH', 'EW', '', 'UW'),
            ('', 'EW', '', 'yUW'),
            ('', 'E', 'O', 'IY'),
            ('#:S', 'ES', ' ', 'IHz'),
            ('#:C', 'ES', ' ', 'IHz'),
            ('#:G', 'ES', ' ', 'IHz'),
            ('#:Z', 'ES', ' ', 'IHz'),
            ('#:X', 'ES', ' ', 'IHz'),
            ('#:J', 'ES', ' ', 'IHz'),
            ('#:CH', 'ES', ' ', 'IHz'),
            ('#:SH', 'ES', ' ', 'IHz'),
            ('#:', 'E', 'S ', ''),
            ('#:', 'ELY', ' ', 'lIY'),
            ('#:', 'EMENT', '', 'mEHnt'),
            ('', 'EFUL', '', 'fUHl'),
            ('', 'EE', '', 'IY'),
            ('', 'EARN', '', 'ERn'),
            (' ', 'EAR', '^', 'ER'),
            ('', 'EAD', '', 'EHd'),
            ('#:', 'EA', ' ', 'IYAX'),
            ('', 'EA', 'SU', 'EH'),
            ('', 'EA', '', 'IY'),
            ('', 'EIGH', '', 'EY'),
            ('', 'EI', '', 'IY'),
            (' ', 'EYE', '', 'AY'),
            ('', 'EY', '', 'IY'),
            ('', 'EU', '', 'yUW'),
            ('', 'E', '', 'EH'),
        ),
        'F': (('', 'FUL', '', 'fUHl'), ('', 'F', '', 'f')),
        'G': (
            ('', 'GIV', '', 'gIHv'),
            (' ', 'G', 'I^', 'g'),
            ('', 'GE', 'T', 'gEH'),
            ('SU', 'GGES', '', 'gjEHs'),
            ('', 'GG', '', 'g'),
            (' B#', 'G', '', 'g'),
            ('', 'G', '+', 'j'),
            ('', 'GREAT', '', 'grEYt'),
            ('#', 'GH', '', ''),
            ('', 'G', '', 'g'),
        ),
        'H': (
            (' ', 'HAV', '', 'hAEv'),
            (' ', 'HERE', '', 'hIYr'),
            (' ', 'HOUR', '', 'AWER'),
            ('', 'HOW', '', 'hAW'),
            ('', 'H', '#', 'h'),
            ('', 'H', '', ''),
        ),
        'I': (
            (' ', 'IN', '', 'IHn'),
            (' ', 'I', ' ', 'AY'),
            ('', 'IN', 'D', 'AYn'),
            ('', 'IER', '', 'IYER'),
            ('#:R', 'IED', '', 'IYd'),
            ('', 'IED', ' ', 'AYd'),
            ('', 'IEN', '', 'IYEHn'),
            ('', 'IE', 'T', 'AYEH'),
            (' :', 'I', '%', 'AY'),
            ('', 'I', '%', 'IY'),
            ('', 'IE', '', 'IY'),
            ('', 'I', '^+:#', 'IH'),
            ('', 'IR', '#', 'AYr'),
            ('', 'IZ', '%', 'AYz'),
            ('', 'IS', '%', 'AYz'),
            ('', 'I', 'D%', 'AY'),
            ('+^', 'I', '^+', 'IH'),
            ('', 'I', 'T%', 'AY'),
            ('#:^', 'I', '^+', 'IH'),
            ('', 'I', '^+', 'AY'),
            ('', 'IR', '', 'ER'),
            ('', 'IGH', '', 'AY'),
            ('', 'ILD', '', 'AYld'),
            ('', 'IGN', ' ', 'AYn'),
            ('', 'IGN', '^', 'AYn'),
            ('', 'IGN', '%', 'AYn'),
            ('', 'IQUE', '', 'IYk'),
            ('', 'I', '', 'IH'),
        ),
        'J': (('', 'J', '', 'j'),),
        'K': ((' ', 'K', 'N', ''), ('', 'K', '', 'k')),
        'L': (
            ('', 'LO', 'C#', 'lOW'),
            ('L', 'L', '', ''),
            ('#:^', 'L', '%', 'AXl'),
            ('', 'LEAD', '', 'lIYd'),
            ('', 'L', '', 'l'),
        ),
        'M': (('', 'MOV', '', 'mUWv'), ('', 'M', '', 'm')),
        'N': (
            ('E', 'NG', '+', 'nj'),
            ('', 'NG', 'R', 'NGg'),
            ('', 'NG', '#', 'NGg'),
            ('', 'NGL', '%', 'NGgAXl'),
            ('', 'NG', '', 'NG'),
            ('', 'NK', '', 'NGk'),
            (' ', 'NOW', ' ', 'nAW'),
            ('', 'N', '', 'n'),
        ),
        'O': (
            ('', 'OF', ' ', 'AXv'),
            ('', 'OROUGH', '', 'EROW'),
            ('#:', 'OR', ' ', 'ER'),
            ('#:', 'ORS', ' ', 'ERz'),
            ('', 'OR', '', 'AOr'),
            (' ', 'ONE', '', 'wAHn'),
            ('', 'OW', '', 'OW'),
            (' ', 'OVER', '', 'OWvER'),
            ('', 'OV', '', 'AHv'),
            ('', 'O', '^%', 'OW'),
            ('', 'O', '^EN', 'OW'),
            ('', 'O', '^I#', 'OW'),
            ('', 'OL', 'D', 'OWl'),
            ('', 'OUGHT', '', 'AOt'),
            ('', 'OUGH', '', 'AHf'),
            (' ', 'OU', '', 'AW'),
            ('H', 'OU', 'S#', 'AW'),
            ('', 'OUS', '', 'AXs'),
            ('', 'OUR', '', 'AOr'),
            ('', 'OULD', '', 'UHd'),
            ('^', 'OU', '^L', 'AH'),
            ('', 'OUP', '', 'UWp'),
            ('', 'OU', '', 'AW'),
            ('', 'OY', '', 'OY'),
            ('', 'OING', '', 'OWIHNG'),
            ('', 'OI', '', 'OY'),
            ('', 'OOR', '', 'AOr'),
            ('', 'OOK', '', 'UHk'),
            ('', 'OOD', '', 'UHd'),
            ('', 'OO', '', 'UW'),
            ('', 'O', 'E', 'OW'),
            ('', 'O', ' ', 'OW'),
            ('', 'OA', '', 'OW'),
            (' ', 'ONLY', '', 'OWnlIY'),
            (' ', 'ONCE', '', 'wAHns'),
            ('', 'ON\'T', '', 'OWnt'),
            ('C', 'O', 'N', 'AA'),
            ('', 'O', 'NG', 'AO'),
            (' :^', 'O', 'N', 'AH'),
            ('I', 'ON', '', 'AXn'),
            ('#:', 'ON', ' ', 'AXn'),
            ('#^', 'ON', '', 'AXn'),
            ('', 'O', 'ST ', 'OW'),
            ('', 'OF', '^', 'AOf'),
            ('', 'OTHER', '', 'AHDHER'),
            ('', 'OSS', ' ', 'AOs'),
            ('#:^', 'OM', '', 'AHm'),
            ('', 'O', '', 'AA'),
        ),
        'P': (
            ('', 'PH', '', 'f'),
            ('', 'PEOP', '', 'pIYp'),
            ('', 'POW', '', 'pAW'),
            ('', 'PUT', ' ', 'pUHt'),
            ('', 'P', '', 'p'),
        ),
        'Q': (
            ('', 'QUAR', '', 'kwAOr'),
            ('', 'QU', '', 'kw'),
            ('', 'Q', '', 'k'),
        ),
        'R': ((' ', 'RE', '^#', 'rIY'), ('', 'R', '', 'r')),
        'S': (
            ('', 'SH', '', 'SH'),
            ('#', 'SION', '', 'ZHAXn'),
            ('', 'SOME', '', 'sAHm'),
            ('#', 'SUR', '#', 'ZHER'),
            ('', 'SUR', '#', 'SHER'),
            ('#', 'SU', '#', 'ZHUW'),
            ('#', 'SSU', '#', 'SHUW'),
            ('#', 'SED', ' ', 'zd'),
            ('#', 'S', '#', 'z'),
            ('', 'SAID', '', 'sEHd'),
            ('^', 'SION', '', 'SHAXn'),
            ('', 'S', 'S', ''),
            ('.', 'S', ' ', 'z'),
            ('#:.E', 'S', ' ', 'z'),
            ('#:^##', 'S', ' ', 'z'),
            ('#:^#', 'S', ' ', 's'),
            ('U', 'S', ' ', 's'),
            (' :#', 'S', ' ', 'z'),
            (' ', 'SCH', '', 'sk'),
            ('', 'S', 'C+', ''),
            ('#', 'SM', '', 'zm'),
            ('#', 'SN', '\'', 'zAXn'),
            ('', 'S', '', 's'),
        ),
        'T': (
            (' ', 'THE', ' ', 'DHAX'),
            ('', 'TO', ' ', 'tUW'),
            ('', 'THAT', ' ', 'DHAEt'),
            (' ', 'THIS', ' ', 'DHIHs'),
            (' ', 'THEY', '', 'DHEY'),
            (' ', 'THERE', '', 'DHEHr'),
            ('', 'THER', '', 'DHER'),
            ('', 'THEIR', '', 'DHEHr'),
            (' ', 'THAN', ' ', 'DHAEn'),
            (' ', 'THEM', ' ', 'DHEHm'),
            ('', 'THESE', ' ', 'DHIYz'),
            (' ', 'THEN', '', 'DHEHn'),
            ('', 'THROUGH', '', 'THrUW'),
            ('', 'THOSE', '', 'DHOWz'),
            ('', 'THOUGH', ' ', 'DHOW'),
            (' ', 'THUS', '', 'DHAHs'),
            ('', 'TH', '', 'TH'),
            ('#:', 'TED', ' ', 'tIHd'),
            ('S', 'TI', '#N', 'CH'),
            ('', 'TI', 'O', 'SH'),
            ('', 'TI', 'A', 'SH'),
            ('', 'TIEN', '', 'SHAXn'),
            ('', 'TUR', '#', 'CHER'),
            ('', 'TU', 'A', 'CHUW'),
            (' ', 'TWO', '', 'tUW'),
            ('', 'T', '', 't'),
        ),
        'U': (
            (' ', 'UN', 'I', 'yUWn'),
            (' ', 'UN', '', 'AHn'),
            (' ', 'UPON', '', 'AXpAOn'),
            ('T', 'UR', '#', 'UHr'),
            ('S', 'UR', '#', 'UHr'),
            ('R', 'UR', '#', 'UHr'),
            ('D', 'UR', '#', 'UHr'),
            ('L', 'UR', '#', 'UHr'),
            ('Z', 'UR', '#', 'UHr'),
            ('N', 'UR', '#', 'UHr'),
            ('J', 'UR', '#', 'UHr'),
            ('TH', 'UR', '#', 'UHr'),
            ('CH', 'UR', '#', 'UHr'),
            ('SH', 'UR', '#', 'UHr'),
            ('', 'UR', '#', 'yUHr'),
            ('', 'UR', '', 'ER'),
            ('', 'U', '^ ', 'AH'),
            ('', 'U', '^^', 'AH'),
            ('', 'UY', '', 'AY'),
            (' G', 'U', '#', ''),
            ('G', 'U', '%', ''),
            ('G', 'U', '#', 'w'),
            ('#N', 'U', '', 'yUW'),
            ('T', 'U', '', 'UW'),
            ('S', 'U', '', 'UW'),
            ('R', 'U', '', 'UW'),
            ('D', 'U', '', 'UW'),
            ('L', 'U', '', 'UW'),
            ('Z', 'U', '', 'UW'),
            ('N', 'U', '', 'UW'),
            ('J', 'U', '', 'UW'),
            ('TH', 'U', '', 'UW'),
            ('CH', 'U', '', 'UW'),
            ('SH', 'U', '', 'UW'),
            ('', 'U', '', 'yUW'),
        ),
        'V': (('', 'VIEW', '', 'vyUW'), ('', 'V', '', 'v')),
        'W': (
            (' ', 'WERE', '', 'wER'),
            ('', 'WA', 'S', 'wAA'),
            ('', 'WA', 'T', 'wAA'),
            ('', 'WHERE', '', 'WHEHr'),
            ('', 'WHAT', '', 'WHAAt'),
            ('', 'WHOL', '', 'hOWl'),
            ('', 'WHO', '', 'hUW'),
            ('', 'WH', '', 'WH'),
            ('', 'WAR', '', 'wAOr'),
            ('', 'WOR', '^', 'wER'),
            ('', 'WR', '', 'r'),
            ('', 'W', '', 'w'),
        ),
        'X': (('', 'X', '', 'ks'),),
        'Y': (
            ('', 'YOUNG', '', 'yAHNG'),
            (' ', 'YOU', '', 'yUW'),
            (' ', 'YES', '', 'yEHs'),
            (' ', 'Y', '', 'y'),
            ('#:^', 'Y', ' ', 'IY'),
            ('#:^', 'Y', 'I', 'IY'),
            (' :', 'Y', ' ', 'AY'),
            (' :', 'Y', '#', 'AY'),
            (' :', 'Y', '^+:#', 'IH'),
            (' :', 'Y', '^#', 'AY'),
            ('', 'Y', '', 'IH'),
        ),
        'Z': (('', 'Z', '', 'z'),),
    }

    def encode(self, word):
        """Return the Naval Research Laboratory phonetic encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The NRL phonetic encoding

        Examples
        --------
        >>> pe = NRL()
        >>> pe.encode('the')
        'DHAX'
        >>> pe.encode('round')
        'rAWnd'
        >>> pe.encode('quick')
        'kwIHk'
        >>> pe.encode('eaten')
        'IYtEHn'
        >>> pe.encode('Smith')
        'smIHTH'
        >>> pe.encode('Larsen')
        'lAArsEHn'

        """

        def _to_regex(pattern, left_match=True):
            new_pattern = ''
            replacements = {
                '#': '[AEIOU]+',
                ':': '[BCDFGHJKLMNPQRSTVWXYZ]*',
                '^': '[BCDFGHJKLMNPQRSTVWXYZ]',
                '.': '[BDVGJLMNTWZ]',
                '%': '(ER|E|ES|ED|ING|ELY)',
                '+': '[EIY]',
                ' ': '^',
            }
            for char in pattern:
                new_pattern += (
                    replacements[char] if char in replacements else char
                )

            if left_match:
                new_pattern += '$'
                if '^' not in pattern:
                    new_pattern = '^.*' + new_pattern
            else:
                new_pattern = '^' + new_pattern.replace('^', '$')
                if '$' not in new_pattern:
                    new_pattern += '.*$'

            return new_pattern

        word = word.upper()

        pron = ''
        pos = 0
        while pos < len(word):
            left_orig = word[:pos]
            right_orig = word[pos:]
            first = word[pos] if word[pos] in self._rules else ' '
            for rule in self._rules[first]:
                left, match, right, out = rule
                if right_orig.startswith(match):
                    if left:
                        l_pattern = _to_regex(left, left_match=True)
                    if right:
                        r_pattern = _to_regex(right, left_match=False)
                    if (not left or re_match(l_pattern, left_orig)) and (
                        not right
                        or re_match(r_pattern, right_orig[len(match) :])
                    ):
                        pron += out
                        pos += len(match)
                        break
            else:
                pron += word[pos]
                pos += 1

        return pron


def nrl(word):
    """Return the Naval Research Laboratory phonetic encoding of a word.

    This is a wrapper for :py:meth:`NRL.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The NRL phonetic encoding

    Examples
    --------
    >>> nrl('the')
    'DHAX'
    >>> nrl('round')
    'rAWnd'
    >>> nrl('quick')
    'kwIHk'
    >>> nrl('eaten')
    'IYtEHn'
    >>> nrl('Smith')
    'smIHTH'
    >>> nrl('Larsen')
    'lAArsEHn'

    """
    return NRL().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
