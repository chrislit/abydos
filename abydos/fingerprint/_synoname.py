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

"""abydos.fingerprint._synoname.

Synoname toolcode
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fingerprint import _Fingerprint

__all__ = ['SynonameToolcode', 'synoname_toolcode']


class SynonameToolcode(_Fingerprint):
    """Synoname Toolcode.

    Cf. :cite:`Getty:1991,Gross:1991`.
    """

    _synoname_special_table = (
        # Roman, match, extra, method
        (False, 'NONE', '', 0),
        (False, 'aine', '', 3),
        (False, 'also erroneously', '', 4),
        (False, 'also identified with the', '', 2),
        (False, 'also identified with', '', 2),
        (False, 'archbishop', '', 7),
        (False, 'atelier', '', 7),
        (False, 'baron', '', 7),
        (False, 'cadet', '', 3),
        (False, 'cardinal', '', 7),
        (False, 'circle of', '', 5),
        (False, 'circle', '', 5),
        (False, 'class of', '', 5),
        (False, 'conde de', '', 7),
        (False, 'countess', '', 7),
        (False, 'count', '', 7),
        (False, "d'", " d'", 15),
        (False, 'dai', '', 15),
        (False, "dall'", " dall'", 15),
        (False, 'dalla', '', 15),
        (False, 'dalle', '', 15),
        (False, 'dal', '', 15),
        (False, 'da', '', 15),
        (False, 'degli', '', 15),
        (False, 'della', '', 15),
        (False, 'del', '', 15),
        (False, 'den', '', 15),
        (False, 'der altere', '', 3),
        (False, 'der jungere', '', 3),
        (False, 'der', '', 15),
        (False, 'de la', '', 15),
        (False, 'des', '', 15),
        (False, "de'", " de'", 15),
        (False, 'de', '', 15),
        (False, 'di ser', '', 7),
        (False, 'di', '', 15),
        (False, 'dos', '', 15),
        (False, 'du', '', 15),
        (False, 'duke of', '', 7),
        (False, 'earl of', '', 7),
        (False, 'el', '', 15),
        (False, 'fils', '', 3),
        (False, 'florentine follower of', '', 5),
        (False, 'follower of', '', 5),
        (False, 'fra', '', 7),
        (False, 'freiherr von', '', 7),
        (False, 'giovane', '', 7),
        (False, 'group', '', 5),
        (True, 'iii', '', 3),
        (True, 'ii', '', 3),
        (False, 'il giovane', '', 7),
        (False, 'il vecchio', '', 7),
        (False, 'il', '', 15),
        (False, "in't", '', 7),
        (False, 'in het', '', 7),
        (True, 'iv', '', 3),
        (True, 'ix', '', 3),
        (True, 'i', '', 3),
        (False, 'jr.', '', 3),
        (False, 'jr', '', 3),
        (False, 'juniore', '', 3),
        (False, 'junior', '', 3),
        (False, 'king of', '', 7),
        (False, "l'", " l'", 15),
        (False, "l'aine", '', 3),
        (False, 'la', '', 15),
        (False, 'le jeune', '', 3),
        (False, 'le', '', 15),
        (False, 'lo', '', 15),
        (False, 'maestro', '', 7),
        (False, 'maitre', '', 7),
        (False, 'marchioness', '', 7),
        (False, 'markgrafin von', '', 7),
        (False, 'marquess', '', 7),
        (False, 'marquis', '', 7),
        (False, 'master of the', '', 7),
        (False, 'master of', '', 7),
        (False, 'master known as the', '', 7),
        (False, 'master with the', '', 7),
        (False, 'master with', '', 7),
        (False, 'masters', '', 7),
        (False, 'master', '', 7),
        (False, 'meister', '', 7),
        (False, 'met de', '', 7),
        (False, 'met', '', 7),
        (False, 'mlle.', '', 7),
        (False, 'mlle', '', 7),
        (False, 'monogrammist', '', 7),
        (False, 'monsu', '', 7),
        (False, 'nee', '', 2),
        (False, 'of', '', 3),
        (False, 'oncle', '', 3),
        (False, 'op den', '', 15),
        (False, 'op de', '', 15),
        (False, 'or', '', 2),
        (False, 'over den', '', 15),
        (False, 'over de', '', 15),
        (False, 'over', '', 7),
        (False, 'p.re', '', 7),
        (False, 'p.r.a.', '', 1),
        (False, 'padre', '', 7),
        (False, 'painter', '', 7),
        (False, 'pere', '', 3),
        (False, 'possibly identified with', '', 6),
        (False, 'possibly', '', 6),
        (False, 'pseudo', '', 15),
        (False, 'r.a.', '', 1),
        (False, 'reichsgraf von', '', 7),
        (False, 'ritter von', '', 7),
        (False, 'sainte-', ' sainte-', 8),
        (False, 'sainte', '', 7),
        (False, 'saint-', ' saint-', 8),
        (False, 'saint', '', 7),
        (False, 'santa', '', 15),
        (False, "sant'", " sant'", 15),
        (False, 'san', '', 15),
        (False, 'ser', '', 7),
        (False, 'seniore', '', 3),
        (False, 'senior', '', 3),
        (False, 'sir', '', 5),
        (False, 'sr.', '', 3),
        (False, 'sr', '', 3),
        (False, 'ss.', ' ss.', 14),
        (False, 'ss', '', 6),
        (False, 'st-', ' st-', 8),
        (False, 'st.', ' st.', 15),
        (False, 'ste-', ' ste-', 8),
        (False, 'ste.', ' ste.', 15),
        (False, 'studio', '', 7),
        (False, 'sub-group', '', 5),
        (False, 'sultan of', '', 7),
        (False, 'ten', '', 15),
        (False, 'ter', '', 15),
        (False, 'the elder', '', 3),
        (False, 'the younger', '', 3),
        (False, 'the', '', 7),
        (False, 'tot', '', 15),
        (False, 'unidentified', '', 1),
        (False, 'van den', '', 15),
        (False, 'van der', '', 15),
        (False, 'van de', '', 15),
        (False, 'vanden', '', 15),
        (False, 'vander', '', 15),
        (False, 'van', '', 15),
        (False, 'vecchia', '', 7),
        (False, 'vecchio', '', 7),
        (True, 'viii', '', 3),
        (True, 'vii', '', 3),
        (True, 'vi', '', 3),
        (True, 'v', '', 3),
        (False, 'vom', '', 7),
        (False, 'von', '', 15),
        (False, 'workshop', '', 7),
        (True, 'xiii', '', 3),
        (True, 'xii', '', 3),
        (True, 'xiv', '', 3),
        (True, 'xix', '', 3),
        (True, 'xi', '', 3),
        (True, 'xviii', '', 3),
        (True, 'xvii', '', 3),
        (True, 'xvi', '', 3),
        (True, 'xv', '', 3),
        (True, 'xx', '', 3),
        (True, 'x', '', 3),
        (False, 'y', '', 7),
    )

    _method_dict = {
        'end': 1,
        'middle': 2,
        'beginning': 4,
        'beginning_no_space': 8,
    }

    # Fill field 0 (qualifier)
    _qual_3 = {
        'adaptation after',
        'after',
        'assistant of',
        'assistants of',
        'circle of',
        'follower of',
        'imitator of',
        'in the style of',
        'manner of',
        'pupil of',
        'school of',
        'studio of',
        'style of',
        'workshop of',
    }
    _qual_2 = {'copy after', 'copy after?', 'copy of'}
    _qual_1 = {
        'ascribed to',
        'attributed to or copy after',
        'attributed to',
        'possibly',
    }

    # Fill field 2 (generation)
    _gen_1 = (
        'the elder',
        ' sr.',
        ' sr',
        'senior',
        'der altere',
        'il vecchio',
        "l'aine",
        'p.re',
        'padre',
        'seniore',
        'vecchia',
        'vecchio',
    )
    _gen_2 = (
        ' jr.',
        ' jr',
        'der jungere',
        'il giovane',
        'giovane',
        'juniore',
        'junior',
        'le jeune',
        'the younger',
    )

    def fingerprint(self, lname, fname='', qual='', normalize=0):
        """Build the Synoname toolcode.

        Parameters
        ----------
        lname : str
            Last name
        fname : str
            First name (can be blank)
        qual : str
            Qualifier
        normalize : int
            Normalization mode (0, 1, or 2)

        Returns
        -------
        tuple
            The transformed names and the synoname toolcode

        Examples
        --------
        >>> st = SynonameToolcode()
        >>> st.fingerprint('hat')
        ('hat', '', '0000000003$$h')
        >>> st.fingerprint('niall')
        ('niall', '', '0000000005$$n')
        >>> st.fingerprint('colin')
        ('colin', '', '0000000005$$c')
        >>> st.fingerprint('atcg')
        ('atcg', '', '0000000004$$a')
        >>> st.fingerprint('entreatment')
        ('entreatment', '', '0000000011$$e')

        >>> st.fingerprint('Ste.-Marie', 'Count John II', normalize=2)
        ('ste.-marie ii', 'count john', '0200491310$015b049a127c$smcji')
        >>> st.fingerprint('Michelangelo IV', '', 'Workshop of')
        ('michelangelo iv', '', '3000550015$055b$mi')

        """
        lname = lname.lower()
        fname = fname.lower()
        qual = qual.lower()

        # Start with the basic code
        toolcode = ['0', '0', '0', '000', '00', '00', '$', '', '$', '']

        full_name = ' '.join((lname, fname))

        if qual in self._qual_3:
            toolcode[0] = '3'
        elif qual in self._qual_2:
            toolcode[0] = '2'
        elif qual in self._qual_1:
            toolcode[0] = '1'

        # Fill field 1 (punctuation)
        if '.' in full_name:
            toolcode[1] = '2'
        else:
            for punct in ',-/:;"&\'()!{|}?$%*+<=>[\\]^_`~':
                if punct in full_name:
                    toolcode[1] = '1'
                    break

        elderyounger = ''  # save elder/younger for possible movement later
        for gen in self._gen_1:
            if gen in full_name:
                toolcode[2] = '1'
                elderyounger = gen
                break
        else:
            for gen in self._gen_2:
                if gen in full_name:
                    toolcode[2] = '2'
                    elderyounger = gen
                    break

        # do comma flip
        if normalize:
            comma = lname.find(',')
            if comma != -1:
                lname_end = lname[comma + 1 :]
                while lname_end[0] in {' ', ','}:
                    lname_end = lname_end[1:]
                fname = lname_end + ' ' + fname
                lname = lname[:comma].strip()

        # do elder/younger move
        if normalize == 2 and elderyounger:
            elderyounger_loc = fname.find(elderyounger)
            if elderyounger_loc != -1:
                lname = ' '.join((lname, elderyounger.strip()))
                fname = ' '.join(
                    (
                        fname[:elderyounger_loc].strip(),
                        fname[elderyounger_loc + len(elderyounger) :],
                    )
                ).strip()

        toolcode[4] = '{:02d}'.format(len(fname))
        toolcode[5] = '{:02d}'.format(len(lname))

        # strip punctuation
        for char in ',/:;"&()!{|}?$%*+<=>[\\]^_`~':
            full_name = full_name.replace(char, '')
        for pos, char in enumerate(full_name):
            if char == '-' and full_name[pos - 1 : pos + 2] != 'b-g':
                full_name = full_name[:pos] + ' ' + full_name[pos + 1 :]

        # Fill field 9 (search range)
        for letter in [_[0] for _ in full_name.split()]:
            if letter not in toolcode[9]:
                toolcode[9] += letter
            if len(toolcode[9]) == 15:
                break

        def roman_check(numeral, fname, lname):
            """Move Roman numerals from first name to last.

            Parameters
            ----------
            numeral : str
                Roman numeral
            fname : str
                First name
            lname : str
                Last name

            Returns
            -------
            tuple
                First and last names with Roman numeral moved

            """
            loc = fname.find(numeral)
            if fname and (
                loc != -1
                and (len(fname[loc:]) == len(numeral))
                or fname[loc + len(numeral)] in {' ', ','}
            ):
                lname = ' '.join((lname, numeral))
                fname = ' '.join(
                    (
                        fname[:loc].strip(),
                        fname[loc + len(numeral) :].lstrip(' ,'),
                    )
                )
            return fname.strip(), lname.strip()

        # Fill fields 7 (specials) and 3 (roman numerals)
        for num, special in enumerate(self._synoname_special_table):
            roman, match, extra, method = special
            if method & self._method_dict['end']:
                match_context = ' ' + match
                loc = full_name.find(match_context)
                if (len(full_name) > len(match_context)) and (
                    loc == len(full_name) - len(match_context)
                ):
                    if roman:
                        if not any(
                            abbr in fname for abbr in ('i.', 'v.', 'x.')
                        ):
                            full_name = full_name[:loc]
                            toolcode[7] += '{:03d}'.format(num) + 'a'
                            if toolcode[3] == '000':
                                toolcode[3] = '{:03d}'.format(num)
                            if normalize == 2:
                                fname, lname = roman_check(match, fname, lname)
                    else:
                        full_name = full_name[:loc]
                        toolcode[7] += '{:03d}'.format(num) + 'a'
            if method & self._method_dict['middle']:
                match_context = ' ' + match + ' '
                loc = 0
                while loc != -1:
                    loc = full_name.find(match_context, loc + 1)
                    if loc > 0:
                        if roman:
                            if not any(
                                abbr in fname for abbr in ('i.', 'v.', 'x.')
                            ):
                                full_name = (
                                    full_name[:loc]
                                    + full_name[loc + len(match) + 1 :]
                                )
                                toolcode[7] += '{:03d}'.format(num) + 'b'
                                if toolcode[3] == '000':
                                    toolcode[3] = '{:03d}'.format(num)
                                if normalize == 2:
                                    fname, lname = roman_check(
                                        match, fname, lname
                                    )
                        else:
                            full_name = (
                                full_name[:loc]
                                + full_name[loc + len(match) + 1 :]
                            )
                            toolcode[7] += '{:03d}'.format(num) + 'b'
            if method & self._method_dict['beginning']:
                match_context = match + ' '
                loc = full_name.find(match_context)
                if loc == 0:
                    full_name = full_name[len(match) + 1 :]
                    toolcode[7] += '{:03d}'.format(num) + 'c'
            if method & self._method_dict['beginning_no_space']:
                loc = full_name.find(match)
                if loc == 0:
                    toolcode[7] += '{:03d}'.format(num) + 'd'
                    if full_name[: len(match)] not in toolcode[9]:
                        toolcode[9] += full_name[: len(match)]

            if extra:
                loc = full_name.find(extra)
                if loc != -1:
                    toolcode[7] += '{:03d}'.format(num) + 'X'
                    # Since extras are unique, we only look for each of them
                    # once, and they include otherwise impossible characters
                    # for this field, it's not possible for the following line
                    # to have ever been false.
                    # if full_name[loc:loc+len(extra)] not in toolcode[9]:
                    toolcode[9] += full_name[loc : loc + len(match)]

        return lname, fname, ''.join(toolcode)


def synoname_toolcode(lname, fname='', qual='', normalize=0):
    """Build the Synoname toolcode.

    This is a wrapper for :py:meth:`SynonameToolcode.fingerprint`.

    Parameters
    ----------
    lname : str
        Last name
    fname : str
        First name (can be blank)
    qual : str
        Qualifier
    normalize : int
        Normalization mode (0, 1, or 2)

    Returns
    -------
    tuple
        The transformed names and the synoname toolcode

    Examples
    --------
    >>> synoname_toolcode('hat')
    ('hat', '', '0000000003$$h')
    >>> synoname_toolcode('niall')
    ('niall', '', '0000000005$$n')
    >>> synoname_toolcode('colin')
    ('colin', '', '0000000005$$c')
    >>> synoname_toolcode('atcg')
    ('atcg', '', '0000000004$$a')
    >>> synoname_toolcode('entreatment')
    ('entreatment', '', '0000000011$$e')

    >>> synoname_toolcode('Ste.-Marie', 'Count John II', normalize=2)
    ('ste.-marie ii', 'count john', '0200491310$015b049a127c$smcji')
    >>> synoname_toolcode('Michelangelo IV', '', 'Workshop of')
    ('michelangelo iv', '', '3000550015$055b$mi')

    """
    return SynonameToolcode().fingerprint(lname, fname, qual, normalize)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
