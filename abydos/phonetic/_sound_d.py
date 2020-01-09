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

"""abydos.phonetic._sound_d.

SoundD phonetic algorithm
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['SoundD', 'sound_d']


class SoundD(_Phonetic):
    """SoundD code.

    SoundD is defined in :cite:`Varol:2012`.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012623010202',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '0123456'), 'APKTLNR'))

    def __init__(self, max_length=4):
        """Initialize SoundD instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length

    def encode_alpha(self, word):
        """Return the alphabetic SoundD code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic SoundD code

        Examples
        --------
        >>> pe = SoundD()
        >>> pe.encode_alpha('Gough')
        'K'
        >>> pe.encode_alpha('pneuma')
        'NN'
        >>> pe.encode_alpha('knight')
        'NT'
        >>> pe.encode_alpha('trice')
        'TRK'
        >>> pe.encode_alpha('judge')
        'KK'


        .. versionadded:: 0.4.0

        """
        return self.encode(word).rstrip('0').translate(self._alphabetic)

    def encode(self, word):
        """Return the SoundD code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The SoundD code

        Examples
        --------
        >>> pe = SoundD()
        >>> pe.encode('Gough')
        '2000'
        >>> pe.encode('pneuma')
        '5500'
        >>> pe.encode('knight')
        '5300'
        >>> pe.encode('trice')
        '3620'
        >>> pe.encode('judge')
        '2200'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        if word[:2] in {'KN', 'GN', 'PN', 'AC', 'WR'}:
            word = word[1:]
        elif word[:1] == 'X':
            word = 'S' + word[1:]
        elif word[:2] == 'WH':
            word = 'W' + word[2:]

        word = (
            word.replace('DGE', '20').replace('DGI', '20').replace('GH', '0')
        )

        word = word.translate(self._trans)
        word = self._delete_consecutive_repeats(word)
        word = word.replace('0', '')

        if self._max_length != -1:
            if len(word) < self._max_length:
                word += '0' * (self._max_length - len(word))
            else:
                word = word[: self._max_length]

        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the SoundD.encode method instead.',
)
def sound_d(word, max_length=4):
    """Return the SoundD code.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)

    Returns
    -------
    str
        The SoundD code

    Examples
    --------
    >>> sound_d('Gough')
    '2000'
    >>> sound_d('pneuma')
    '5500'
    >>> sound_d('knight')
    '5300'
    >>> sound_d('trice')
    '3620'
    >>> sound_d('judge')
    '2200'

    .. versionadded:: 0.3.0

    """
    return SoundD(max_length).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
