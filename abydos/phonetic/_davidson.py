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

"""abydos.phonetic._davidson.

Davidson's Consonant Code.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six import text_type

from ._phonetic import _Phonetic

__all__ = ['Davidson', 'davidson']


class Davidson(_Phonetic):
    """Davidson Consonant Code.

    This is based on the name compression system described in
    :cite:`Davidson:1962`.

    :cite:`Dolby:1970` identifies this as having been the name compression
    algorithm used by SABRE.
    """

    _trans = {65: '', 69: '', 73: '', 79: '', 85: '', 72: '', 87: '', 89: ''}

    def encode(self, lname, fname='.', omit_fname=False):
        """Return Davidson's Consonant Code.

        Parameters
        ----------
        lname : str
            Last name (or word) to be encoded
        fname : str
            First name (optional), of which the first character is included in
            the code.
        omit_fname : bool
            Set to True to completely omit the first character of the first
            name

        Returns
        -------
        str
            Davidson's Consonant Code

        Example
        -------
        >>> pe = Davidson()
        >>> pe.encode('Gough')
        'G   .'
        >>> pe.encode('pneuma')
        'PNM .'
        >>> pe.encode('knight')
        'KNGT.'
        >>> pe.encode('trice')
        'TRC .'
        >>> pe.encode('judge')
        'JDG .'
        >>> pe.encode('Smith', 'James')
        'SMT J'
        >>> pe.encode('Wasserman', 'Tabitha')
        'WSRMT'

        """
        lname = text_type(lname.upper())
        code = self._delete_consecutive_repeats(
            lname[:1] + lname[1:].translate(self._trans)
        )
        code = code[:4] + (4 - len(code)) * ' '

        if not omit_fname:
            code += fname[:1].upper()

        return code


def davidson(lname, fname='.', omit_fname=False):
    """Return Davidson's Consonant Code.

    This is a wrapper for :py:meth:`Davidson.encode`.

    Parameters
    ----------
    lname : str
        Last name (or word) to be encoded
    fname : str
        First name (optional), of which the first character is included in the
        code.
    omit_fname : bool
        Set to True to completely omit the first character of the first name

    Returns
    -------
    str
        Davidson's Consonant Code

    Example
    -------
    >>> davidson('Gough')
    'G   .'
    >>> davidson('pneuma')
    'PNM .'
    >>> davidson('knight')
    'KNGT.'
    >>> davidson('trice')
    'TRC .'
    >>> davidson('judge')
    'JDG .'
    >>> davidson('Smith', 'James')
    'SMT J'
    >>> davidson('Wasserman', 'Tabitha')
    'WSRMT'

    """
    return Davidson().encode(lname, fname, omit_fname)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
