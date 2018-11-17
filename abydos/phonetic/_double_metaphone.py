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

"""abydos.phonetic._double_metaphone.

Double Metaphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._phonetic import _Phonetic

__all__ = ['DoubleMetaphone', 'double_metaphone']


class DoubleMetaphone(_Phonetic):
    """Double Metaphone.

    Based on Lawrence Philips' (Visual) C++ code from 1999
    :cite:`Philips:2000`.
    """

    def encode(self, word, max_length=-1):
        """Return the Double Metaphone code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length of the returned Double Metaphone codes (defaults
            to unlmited, but in Philips' original implementation this was 4)

        Returns
        -------
        tuple
            The Double Metaphone value(s)

        Examples
        --------
        >>> pe = DoubleMetaphone()
        >>> pe.encode('Christopher')
        ('KRSTFR', '')
        >>> pe.encode('Niall')
        ('NL', '')
        >>> pe.encode('Smith')
        ('SM0', 'XMT')
        >>> pe.encode('Schmidt')
        ('XMT', 'SMT')

        """
        # Require a max_length of at least 4
        if max_length != -1:
            max_length = max(4, max_length)

        primary = ''
        secondary = ''

        def _slavo_germanic():
            """Return True if the word appears to be Slavic or Germanic.

            Returns
            -------
            bool
                True if the word appears to be Slavic or Germanic

            """
            if 'W' in word or 'K' in word or 'CZ' in word:
                return True
            return False

        def _metaph_add(pri, sec=''):
            """Return a new metaphone tuple with the supplied elements.

            Parameters
            ----------
            pri : str
                The primary element
            sec : str
                The secondary element

            Returns
            -------
            tuple
                A new metaphone tuple with the supplied elements

            """
            newpri = primary
            newsec = secondary
            if pri:
                newpri += pri
            if sec:
                if sec != ' ':
                    newsec += sec
            else:
                newsec += pri
            return newpri, newsec

        def _is_vowel(pos):
            """Return True if the character at word[pos] is a vowel.

            Parameters
            ----------
            pos : int
                Position in the word

            Returns
            -------
            bool
                True if the character is a vowel

            """
            if pos >= 0 and word[pos] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
                return True
            return False

        def _get_at(pos):
            """Return the character at word[pos].

            Parameters
            ----------
            pos : int
                Position in the word

            Returns
            -------
            str
                Character at word[pos]

            """
            return word[pos]

        def _string_at(pos, slen, substrings):
            """Return True if word[pos:pos+slen] is in substrings.

            Parameters
            ----------
            pos : int
                Position in the word
            slen : int
                Substring length
            substrings : set
                Substrings to search

            Returns
            -------
            bool
                True if word[pos:pos+slen] is in substrings

            """
            if pos < 0:
                return False
            return word[pos : pos + slen] in substrings

        current = 0
        length = len(word)
        if length < 1:
            return '', ''
        last = length - 1

        word = word.upper()
        word = word.replace('ß', 'SS')

        # Pad the original string so that we can index beyond the edge of the
        # world
        word += '     '

        # Skip these when at start of word
        if word[0:2] in {'GN', 'KN', 'PN', 'WR', 'PS'}:
            current += 1

        # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
        if _get_at(0) == 'X':
            primary, secondary = _metaph_add('S')  # 'Z' maps to 'S'
            current += 1

        # Main loop
        while True:
            if current >= length:
                break

            if _get_at(current) in {'A', 'E', 'I', 'O', 'U', 'Y'}:
                if current == 0:
                    # All init vowels now map to 'A'
                    primary, secondary = _metaph_add('A')
                current += 1
                continue

            elif _get_at(current) == 'B':
                # "-mb", e.g", "dumb", already skipped over...
                primary, secondary = _metaph_add('P')
                if _get_at(current + 1) == 'B':
                    current += 2
                else:
                    current += 1
                continue

            elif _get_at(current) == 'Ç':
                primary, secondary = _metaph_add('S')
                current += 1
                continue

            elif _get_at(current) == 'C':
                # Various Germanic
                if (
                    current > 1
                    and not _is_vowel(current - 2)
                    and _string_at((current - 1), 3, {'ACH'})
                    and (
                        (_get_at(current + 2) != 'I')
                        and (
                            (_get_at(current + 2) != 'E')
                            or _string_at(
                                (current - 2), 6, {'BACHER', 'MACHER'}
                            )
                        )
                    )
                ):
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                # Special case 'caesar'
                elif current == 0 and _string_at(current, 6, {'CAESAR'}):
                    primary, secondary = _metaph_add('S')
                    current += 2
                    continue

                # Italian 'chianti'
                elif _string_at(current, 4, {'CHIA'}):
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                elif _string_at(current, 2, {'CH'}):
                    # Find 'Michael'
                    if current > 0 and _string_at(current, 4, {'CHAE'}):
                        primary, secondary = _metaph_add('K', 'X')
                        current += 2
                        continue

                    # Greek roots e.g. 'chemistry', 'chorus'
                    elif (
                        current == 0
                        and (
                            _string_at((current + 1), 5, {'HARAC', 'HARIS'})
                            or _string_at(
                                (current + 1), 3, {'HOR', 'HYM', 'HIA', 'HEM'}
                            )
                        )
                        and not _string_at(0, 5, {'CHORE'})
                    ):
                        primary, secondary = _metaph_add('K')
                        current += 2
                        continue

                    # Germanic, Greek, or otherwise 'ch' for 'kh' sound
                    elif (
                        (
                            _string_at(0, 4, {'VAN ', 'VON '})
                            or _string_at(0, 3, {'SCH'})
                        )
                        or
                        # 'architect but not 'arch', 'orchestra', 'orchid'
                        _string_at(
                            (current - 2), 6, {'ORCHES', 'ARCHIT', 'ORCHID'}
                        )
                        or _string_at((current + 2), 1, {'T', 'S'})
                        or (
                            (
                                _string_at(
                                    (current - 1), 1, {'A', 'O', 'U', 'E'}
                                )
                                or (current == 0)
                            )
                            and
                            # e.g., 'wachtler', 'wechsler', but not 'tichner'
                            _string_at(
                                (current + 2),
                                1,
                                {
                                    'L',
                                    'R',
                                    'N',
                                    'M',
                                    'B',
                                    'H',
                                    'F',
                                    'V',
                                    'W',
                                    ' ',
                                },
                            )
                        )
                    ):
                        primary, secondary = _metaph_add('K')

                    else:
                        if current > 0:
                            if _string_at(0, 2, {'MC'}):
                                # e.g., "McHugh"
                                primary, secondary = _metaph_add('K')
                            else:
                                primary, secondary = _metaph_add('X', 'K')
                        else:
                            primary, secondary = _metaph_add('X')

                    current += 2
                    continue

                # e.g, 'czerny'
                elif _string_at(current, 2, {'CZ'}) and not _string_at(
                    (current - 2), 4, {'WICZ'}
                ):
                    primary, secondary = _metaph_add('S', 'X')
                    current += 2
                    continue

                # e.g., 'focaccia'
                elif _string_at((current + 1), 3, {'CIA'}):
                    primary, secondary = _metaph_add('X')
                    current += 3

                # double 'C', but not if e.g. 'McClellan'
                elif _string_at(current, 2, {'CC'}) and not (
                    (current == 1) and (_get_at(0) == 'M')
                ):
                    # 'bellocchio' but not 'bacchus'
                    if _string_at(
                        (current + 2), 1, {'I', 'E', 'H'}
                    ) and not _string_at((current + 2), 2, {'HU'}):
                        # 'accident', 'accede' 'succeed'
                        if (
                            (current == 1) and _get_at(current - 1) == 'A'
                        ) or _string_at((current - 1), 5, {'UCCEE', 'UCCES'}):
                            primary, secondary = _metaph_add('KS')
                        # 'bacci', 'bertucci', other italian
                        else:
                            primary, secondary = _metaph_add('X')
                        current += 3
                        continue
                    else:  # Pierce's rule
                        primary, secondary = _metaph_add('K')
                        current += 2
                        continue

                elif _string_at(current, 2, {'CK', 'CG', 'CQ'}):
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                elif _string_at(current, 2, {'CI', 'CE', 'CY'}):
                    # Italian vs. English
                    if _string_at(current, 3, {'CIO', 'CIE', 'CIA'}):
                        primary, secondary = _metaph_add('S', 'X')
                    else:
                        primary, secondary = _metaph_add('S')
                    current += 2
                    continue

                # else
                else:
                    primary, secondary = _metaph_add('K')

                    # name sent in 'mac caffrey', 'mac gregor
                    if _string_at((current + 1), 2, {' C', ' Q', ' G'}):
                        current += 3
                    elif _string_at(
                        (current + 1), 1, {'C', 'K', 'Q'}
                    ) and not _string_at((current + 1), 2, {'CE', 'CI'}):
                        current += 2
                    else:
                        current += 1
                    continue

            elif _get_at(current) == 'D':
                if _string_at(current, 2, {'DG'}):
                    if _string_at((current + 2), 1, {'I', 'E', 'Y'}):
                        # e.g. 'edge'
                        primary, secondary = _metaph_add('J')
                        current += 3
                        continue
                    else:
                        # e.g. 'edgar'
                        primary, secondary = _metaph_add('TK')
                        current += 2
                        continue

                elif _string_at(current, 2, {'DT', 'DD'}):
                    primary, secondary = _metaph_add('T')
                    current += 2
                    continue

                # else
                else:
                    primary, secondary = _metaph_add('T')
                    current += 1
                    continue

            elif _get_at(current) == 'F':
                if _get_at(current + 1) == 'F':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('F')
                continue

            elif _get_at(current) == 'G':
                if _get_at(current + 1) == 'H':
                    if (current > 0) and not _is_vowel(current - 1):
                        primary, secondary = _metaph_add('K')
                        current += 2
                        continue

                    # 'ghislane', ghiradelli
                    elif current == 0:
                        if _get_at(current + 2) == 'I':
                            primary, secondary = _metaph_add('J')
                        else:
                            primary, secondary = _metaph_add('K')
                        current += 2
                        continue

                    # Parker's rule (with some further refinements) -
                    # e.g., 'hugh'
                    elif (
                        (
                            (current > 1)
                            and _string_at((current - 2), 1, {'B', 'H', 'D'})
                        )
                        or
                        # e.g., 'bough'
                        (
                            (current > 2)
                            and _string_at((current - 3), 1, {'B', 'H', 'D'})
                        )
                        or
                        # e.g., 'broughton'
                        (
                            (current > 3)
                            and _string_at((current - 4), 1, {'B', 'H'})
                        )
                    ):
                        current += 2
                        continue
                    else:
                        # e.g. 'laugh', 'McLaughlin', 'cough',
                        #      'gough', 'rough', 'tough'
                        if (
                            (current > 2)
                            and (_get_at(current - 1) == 'U')
                            and (
                                _string_at(
                                    (current - 3), 1, {'C', 'G', 'L', 'R', 'T'}
                                )
                            )
                        ):
                            primary, secondary = _metaph_add('F')
                        elif (current > 0) and _get_at(current - 1) != 'I':
                            primary, secondary = _metaph_add('K')
                        current += 2
                        continue

                elif _get_at(current + 1) == 'N':
                    if (
                        (current == 1)
                        and _is_vowel(0)
                        and not _slavo_germanic()
                    ):
                        primary, secondary = _metaph_add('KN', 'N')
                    # not e.g. 'cagney'
                    elif (
                        not _string_at((current + 2), 2, {'EY'})
                        and (_get_at(current + 1) != 'Y')
                        and not _slavo_germanic()
                    ):
                        primary, secondary = _metaph_add('N', 'KN')
                    else:
                        primary, secondary = _metaph_add('KN')
                    current += 2
                    continue

                # 'tagliaro'
                elif (
                    _string_at((current + 1), 2, {'LI'})
                    and not _slavo_germanic()
                ):
                    primary, secondary = _metaph_add('KL', 'L')
                    current += 2
                    continue

                # -ges-, -gep-, -gel-, -gie- at beginning
                elif (current == 0) and (
                    (_get_at(current + 1) == 'Y')
                    or _string_at(
                        (current + 1),
                        2,
                        {
                            'ES',
                            'EP',
                            'EB',
                            'EL',
                            'EY',
                            'IB',
                            'IL',
                            'IN',
                            'IE',
                            'EI',
                            'ER',
                        },
                    )
                ):
                    primary, secondary = _metaph_add('K', 'J')
                    current += 2
                    continue

                #  -ger-,  -gy-
                elif (
                    (
                        _string_at((current + 1), 2, {'ER'})
                        or (_get_at(current + 1) == 'Y')
                    )
                    and not _string_at(0, 6, {'DANGER', 'RANGER', 'MANGER'})
                    and not _string_at((current - 1), 1, {'E', 'I'})
                    and not _string_at((current - 1), 3, {'RGY', 'OGY'})
                ):
                    primary, secondary = _metaph_add('K', 'J')
                    current += 2
                    continue

                #  italian e.g, 'biaggi'
                elif _string_at(
                    (current + 1), 1, {'E', 'I', 'Y'}
                ) or _string_at((current - 1), 4, {'AGGI', 'OGGI'}):
                    # obvious germanic
                    if (
                        _string_at(0, 4, {'VAN ', 'VON '})
                        or _string_at(0, 3, {'SCH'})
                    ) or _string_at((current + 1), 2, {'ET'}):
                        primary, secondary = _metaph_add('K')
                    elif _string_at((current + 1), 4, {'IER '}):
                        primary, secondary = _metaph_add('J')
                    else:
                        primary, secondary = _metaph_add('J', 'K')
                    current += 2
                    continue

                else:
                    if _get_at(current + 1) == 'G':
                        current += 2
                    else:
                        current += 1
                    primary, secondary = _metaph_add('K')
                    continue

            elif _get_at(current) == 'H':
                # only keep if first & before vowel or btw. 2 vowels
                if ((current == 0) or _is_vowel(current - 1)) and _is_vowel(
                    current + 1
                ):
                    primary, secondary = _metaph_add('H')
                    current += 2
                else:  # also takes care of 'HH'
                    current += 1
                continue

            elif _get_at(current) == 'J':
                # obvious spanish, 'jose', 'san jacinto'
                if _string_at(current, 4, {'JOSE'}) or _string_at(
                    0, 4, {'SAN '}
                ):
                    if (
                        (current == 0) and (_get_at(current + 4) == ' ')
                    ) or _string_at(0, 4, {'SAN '}):
                        primary, secondary = _metaph_add('H')
                    else:
                        primary, secondary = _metaph_add('J', 'H')
                    current += 1
                    continue

                elif (current == 0) and not _string_at(current, 4, {'JOSE'}):
                    # Yankelovich/Jankelowicz
                    primary, secondary = _metaph_add('J', 'A')
                # Spanish pron. of e.g. 'bajador'
                elif (
                    _is_vowel(current - 1)
                    and not _slavo_germanic()
                    and (
                        (_get_at(current + 1) == 'A')
                        or (_get_at(current + 1) == 'O')
                    )
                ):
                    primary, secondary = _metaph_add('J', 'H')
                elif current == last:
                    primary, secondary = _metaph_add('J', ' ')
                elif not _string_at(
                    (current + 1), 1, {'L', 'T', 'K', 'S', 'N', 'M', 'B', 'Z'}
                ) and not _string_at((current - 1), 1, {'S', 'K', 'L'}):
                    primary, secondary = _metaph_add('J')

                if _get_at(current + 1) == 'J':  # it could happen!
                    current += 2
                else:
                    current += 1
                continue

            elif _get_at(current) == 'K':
                if _get_at(current + 1) == 'K':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('K')
                continue

            elif _get_at(current) == 'L':
                if _get_at(current + 1) == 'L':
                    # Spanish e.g. 'cabrillo', 'gallegos'
                    if (
                        (current == (length - 3))
                        and _string_at(
                            (current - 1), 4, {'ILLO', 'ILLA', 'ALLE'}
                        )
                    ) or (
                        (
                            _string_at((last - 1), 2, {'AS', 'OS'})
                            or _string_at(last, 1, {'A', 'O'})
                        )
                        and _string_at((current - 1), 4, {'ALLE'})
                    ):
                        primary, secondary = _metaph_add('L', ' ')
                        current += 2
                        continue
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('L')
                continue

            elif _get_at(current) == 'M':
                if (
                    (
                        _string_at((current - 1), 3, {'UMB'})
                        and (
                            ((current + 1) == last)
                            or _string_at((current + 2), 2, {'ER'})
                        )
                    )
                    or
                    # 'dumb', 'thumb'
                    (_get_at(current + 1) == 'M')
                ):
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('M')
                continue

            elif _get_at(current) == 'N':
                if _get_at(current + 1) == 'N':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('N')
                continue

            elif _get_at(current) == 'Ñ':
                current += 1
                primary, secondary = _metaph_add('N')
                continue

            elif _get_at(current) == 'P':
                if _get_at(current + 1) == 'H':
                    primary, secondary = _metaph_add('F')
                    current += 2
                    continue

                # also account for "campbell", "raspberry"
                elif _string_at((current + 1), 1, {'P', 'B'}):
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('P')
                continue

            elif _get_at(current) == 'Q':
                if _get_at(current + 1) == 'Q':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('K')
                continue

            elif _get_at(current) == 'R':
                # french e.g. 'rogier', but exclude 'hochmeier'
                if (
                    (current == last)
                    and not _slavo_germanic()
                    and _string_at((current - 2), 2, {'IE'})
                    and not _string_at((current - 4), 2, {'ME', 'MA'})
                ):
                    primary, secondary = _metaph_add('', 'R')
                else:
                    primary, secondary = _metaph_add('R')

                if _get_at(current + 1) == 'R':
                    current += 2
                else:
                    current += 1
                continue

            elif _get_at(current) == 'S':
                # special cases 'island', 'isle', 'carlisle', 'carlysle'
                if _string_at((current - 1), 3, {'ISL', 'YSL'}):
                    current += 1
                    continue

                # special case 'sugar-'
                elif (current == 0) and _string_at(current, 5, {'SUGAR'}):
                    primary, secondary = _metaph_add('X', 'S')
                    current += 1
                    continue

                elif _string_at(current, 2, {'SH'}):
                    # Germanic
                    if _string_at(
                        (current + 1), 4, {'HEIM', 'HOEK', 'HOLM', 'HOLZ'}
                    ):
                        primary, secondary = _metaph_add('S')
                    else:
                        primary, secondary = _metaph_add('X')
                    current += 2
                    continue

                # Italian & Armenian
                elif _string_at(current, 3, {'SIO', 'SIA'}) or _string_at(
                    current, 4, {'SIAN'}
                ):
                    if not _slavo_germanic():
                        primary, secondary = _metaph_add('S', 'X')
                    else:
                        primary, secondary = _metaph_add('S')
                    current += 3
                    continue

                # German & anglicisations, e.g. 'smith' match 'schmidt',
                #                               'snider' match 'schneider'
                # also, -sz- in Slavic language although in Hungarian it is
                #       pronounced 's'
                elif (
                    (current == 0)
                    and _string_at((current + 1), 1, {'M', 'N', 'L', 'W'})
                ) or _string_at((current + 1), 1, {'Z'}):
                    primary, secondary = _metaph_add('S', 'X')
                    if _string_at((current + 1), 1, {'Z'}):
                        current += 2
                    else:
                        current += 1
                    continue

                elif _string_at(current, 2, {'SC'}):
                    # Schlesinger's rule
                    if _get_at(current + 2) == 'H':
                        # dutch origin, e.g. 'school', 'schooner'
                        if _string_at(
                            (current + 3),
                            2,
                            {'OO', 'ER', 'EN', 'UY', 'ED', 'EM'},
                        ):
                            # 'schermerhorn', 'schenker'
                            if _string_at((current + 3), 2, {'ER', 'EN'}):
                                primary, secondary = _metaph_add('X', 'SK')
                            else:
                                primary, secondary = _metaph_add('SK')
                            current += 3
                            continue
                        else:
                            if (
                                (current == 0)
                                and not _is_vowel(3)
                                and (_get_at(3) != 'W')
                            ):
                                primary, secondary = _metaph_add('X', 'S')
                            else:
                                primary, secondary = _metaph_add('X')
                            current += 3
                            continue

                    elif _string_at((current + 2), 1, {'I', 'E', 'Y'}):
                        primary, secondary = _metaph_add('S')
                        current += 3
                        continue

                    # else
                    else:
                        primary, secondary = _metaph_add('SK')
                        current += 3
                        continue

                else:
                    # french e.g. 'resnais', 'artois'
                    if (current == last) and _string_at(
                        (current - 2), 2, {'AI', 'OI'}
                    ):
                        primary, secondary = _metaph_add('', 'S')
                    else:
                        primary, secondary = _metaph_add('S')

                    if _string_at((current + 1), 1, {'S', 'Z'}):
                        current += 2
                    else:
                        current += 1
                    continue

            elif _get_at(current) == 'T':
                if _string_at(current, 4, {'TION'}):
                    primary, secondary = _metaph_add('X')
                    current += 3
                    continue

                elif _string_at(current, 3, {'TIA', 'TCH'}):
                    primary, secondary = _metaph_add('X')
                    current += 3
                    continue

                elif _string_at(current, 2, {'TH'}) or _string_at(
                    current, 3, {'TTH'}
                ):
                    # special case 'thomas', 'thames' or germanic
                    if (
                        _string_at((current + 2), 2, {'OM', 'AM'})
                        or _string_at(0, 4, {'VAN ', 'VON '})
                        or _string_at(0, 3, {'SCH'})
                    ):
                        primary, secondary = _metaph_add('T')
                    else:
                        primary, secondary = _metaph_add('0', 'T')
                    current += 2
                    continue

                elif _string_at((current + 1), 1, {'T', 'D'}):
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('T')
                continue

            elif _get_at(current) == 'V':
                if _get_at(current + 1) == 'V':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('F')
                continue

            elif _get_at(current) == 'W':
                # can also be in middle of word
                if _string_at(current, 2, {'WR'}):
                    primary, secondary = _metaph_add('R')
                    current += 2
                    continue
                elif (current == 0) and (
                    _is_vowel(current + 1) or _string_at(current, 2, {'WH'})
                ):
                    # Wasserman should match Vasserman
                    if _is_vowel(current + 1):
                        primary, secondary = _metaph_add('A', 'F')
                    else:
                        # need Uomo to match Womo
                        primary, secondary = _metaph_add('A')

                # Arnow should match Arnoff
                if (
                    ((current == last) and _is_vowel(current - 1))
                    or _string_at(
                        (current - 1), 5, {'EWSKI', 'EWSKY', 'OWSKI', 'OWSKY'}
                    )
                    or _string_at(0, 3, {'SCH'})
                ):
                    primary, secondary = _metaph_add('', 'F')
                    current += 1
                    continue
                # Polish e.g. 'filipowicz'
                elif _string_at(current, 4, {'WICZ', 'WITZ'}):
                    primary, secondary = _metaph_add('TS', 'FX')
                    current += 4
                    continue
                # else skip it
                else:
                    current += 1
                    continue

            elif _get_at(current) == 'X':
                # French e.g. breaux
                if not (
                    (current == last)
                    and (
                        _string_at((current - 3), 3, {'IAU', 'EAU'})
                        or _string_at((current - 2), 2, {'AU', 'OU'})
                    )
                ):
                    primary, secondary = _metaph_add('KS')

                if _string_at((current + 1), 1, {'C', 'X'}):
                    current += 2
                else:
                    current += 1
                continue

            elif _get_at(current) == 'Z':
                # Chinese Pinyin e.g. 'zhao'
                if _get_at(current + 1) == 'H':
                    primary, secondary = _metaph_add('J')
                    current += 2
                    continue
                elif _string_at((current + 1), 2, {'ZO', 'ZI', 'ZA'}) or (
                    _slavo_germanic()
                    and ((current > 0) and _get_at(current - 1) != 'T')
                ):
                    primary, secondary = _metaph_add('S', 'TS')
                else:
                    primary, secondary = _metaph_add('S')

                if _get_at(current + 1) == 'Z':
                    current += 2
                else:
                    current += 1
                continue

            else:
                current += 1

        if max_length > 0:
            primary = primary[:max_length]
            secondary = secondary[:max_length]
        if primary == secondary:
            secondary = ''

        return primary, secondary


def double_metaphone(word, max_length=-1):
    """Return the Double Metaphone code for a word.

    This is a wrapper for :py:meth:`DoubleMetaphone.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length of the returned Double Metaphone codes (defaults to
        unlimited, but in Philips' original implementation this was 4)

    Returns
    -------
    tuple
        The Double Metaphone value(s)

    Examples
    --------
    >>> double_metaphone('Christopher')
    ('KRSTFR', '')
    >>> double_metaphone('Niall')
    ('NL', '')
    >>> double_metaphone('Smith')
    ('SM0', 'XMT')
    >>> double_metaphone('Schmidt')
    ('XMT', 'SMT')

    """
    return DoubleMetaphone().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
