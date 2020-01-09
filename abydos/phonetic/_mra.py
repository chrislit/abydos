# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.phonetic._mra.

MRA personal numeric identifier (PNI).
"""

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['MRA', 'mra']


class MRA(_Phonetic):
    """Western Airlines Surname Match Rating Algorithm.

    A description of the Western Airlines Surname Match Rating Algorithm can
    be found on page 18 of :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    def encode(self, word):
        """Return the MRA personal numeric identifier (PNI) for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The MRA PNI

        Examples
        --------
        >>> pe = MRA()
        >>> pe.encode('Christopher')
        'CHRPHR'
        >>> pe.encode('Niall')
        'NL'
        >>> pe.encode('Smith')
        'SMTH'
        >>> pe.encode('Schmidt')
        'SCHMDT'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if not word:
            return word
        word = word.upper()
        word = word[0] + ''.join(
            c for c in word[1:] if c not in self._uc_v_set
        )
        word = self._delete_consecutive_repeats(word)
        if len(word) > 6:
            word = word[:3] + word[-3:]
        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the MRA.encode method instead.',
)
def mra(word):
    """Return the MRA personal numeric identifier (PNI) for a word.

    This is a wrapper for :py:meth:`MRA.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The MRA PNI

    Examples
    --------
    >>> mra('Christopher')
    'CHRPHR'
    >>> mra('Niall')
    'NL'
    >>> mra('Smith')
    'SMTH'
    >>> mra('Schmidt')
    'SCHMDT'

    .. versionadded:: 0.1.0

    """
    return MRA().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
