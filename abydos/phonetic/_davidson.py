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

The phonetic._davidson module implements Davidson's Consonant Code.
"""

from __future__ import unicode_literals

from six import text_type

from ._util import _delete_consecutive_repeats

__all__ = ['davidson']


def davidson(lname, fname='.', omit_fname=False):
    """Return Davidson's Consonant Code.

    This is based on the name compression system described in
    :cite:`Davidson:1962`.

    :cite:`Dolby:1970` identifies this as having been the name compression
    algorithm used by SABRE.

    :param str lname: Last name (or word) to be encoded
    :param str fname: First name (optional), of which the first character is
        included in the code.
    :param bool omit_fname: Set to True to completely omit the first character
        of the first name
    :returns: Davidson's Consonant Code
    :rtype: str

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
    trans = {65: '', 69: '', 73: '', 79: '', 85: '', 72: '', 87: '', 89: ''}

    lname = text_type(lname.upper())
    code = _delete_consecutive_repeats(lname[:1] + lname[1:].translate(trans))
    code = code[:4] + (4 - len(code)) * ' '

    if not omit_fname:
        code += fname[:1].upper()

    return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
