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

"""abydos.phonetic._pshp_soundex_first.

PSHP Soundex/Viewex Coding for first names
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import _Phonetic

__all__ = ['PSHPSoundexFirst', 'pshp_soundex_first']


class PSHPSoundexFirst(_Phonetic):
    """PSHP Soundex/Viewex Coding of a first name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate class, :py:class:`PSHPSoundexLast` is used for last names.
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012523010202',
        )
    )

    def encode(self, fname, max_length=4, german=False):
        """Calculate the PSHP Soundex/Viewex Coding of a first name.

        Parameters
        ----------
        fname : str
            The first name to encode
        max_length : int
            The length of the code returned (defaults to 4)
        german : bool
            Set to True if the name is German (different rules apply)

        Returns
        -------
        str
            The PSHP Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexFirst()
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Waters')
        'W352'
        >>> pe.encode('James')
        'J700'
        >>> pe.encode('Schmidt')
        'S500'
        >>> pe.encode('Ashcroft')
        'A220'
        >>> pe.encode('John')
        'J500'
        >>> pe.encode('Colin')
        'K400'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Sally')
        'S400'
        >>> pe.encode('Jane')
        'J500'

        """
        fname = unicode_normalize('NFKD', text_type(fname.upper()))
        fname = fname.replace('ß', 'SS')
        fname = ''.join(c for c in fname if c in self._uc_set)

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
                fname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[
                    fname[0]
                ] + fname[1:]

            code = fname[:1]

            # B. Soundex coding
            # code for Y unspecified, but presumably is 0
            fname = fname.translate(self._trans)
            fname = self._delete_consecutive_repeats(fname)

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


def pshp_soundex_first(fname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a first name.

    This is a wrapper for :py:meth:`PSHPSoundexFirst.encode`.

    Parameters
    ----------
    fname : str
        The first name to encode
    max_length : int
        The length of the code returned (defaults to 4)
    german : bool
        Set to True if the name is German (different rules apply)

    Returns
    -------
    str
        The PSHP Soundex/Viewex Coding

    Examples
    --------
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
    return PSHPSoundexFirst().encode(fname, max_length, german)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
