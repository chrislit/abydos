# Copyright 2018-2020 by Christopher C. Little.
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

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['Davidson', 'davidson']


class Davidson(_Phonetic):
    """Davidson Consonant Code.

    This is based on the name compression system described in
    :cite:`Davidson:1962`.

    :cite:`Dolby:1970` identifies this as having been the name compression
    algorithm used by SABRE.

    .. versionadded:: 0.3.6
    """

    _trans = {65: '', 69: '', 73: '', 79: '', 85: '', 72: '', 87: '', 89: ''}

    def __init__(self, omit_fname=False):
        """Initialize Davidson instance.

        Parameters
        ----------
        omit_fname : bool
            Set to True to completely omit the first character of the first
            name


        .. versionadded:: 0.4.0

        """
        self._omit_fname = omit_fname

    def encode(self, lname, fname='.'):
        """Return Davidson's Consonant Code.

        Parameters
        ----------
        lname : str
            Last name (or word) to be encoded
        fname : str
            First name (optional), of which the first character is included in
            the code.

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


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        lname = lname.upper()
        code = self._delete_consecutive_repeats(
            lname[:1] + lname[1:].translate(self._trans)
        )
        code = code[:4] + (4 - len(code)) * ' '

        if not self._omit_fname:
            code += fname[:1].upper()

        return code


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Davidson.encode method instead.',
)
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

    .. versionadded:: 0.3.0

    """
    return Davidson(omit_fname).encode(lname, fname)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
