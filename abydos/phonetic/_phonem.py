# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.phonetic._phonem.

Phonem
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['Phonem']


class Phonem(_Phonetic):
    """Phonem.

    Phonem is defined in :cite:`Wilde:1988`.

    This version is based on the Perl implementation documented at
    :cite:`Wilz:2005`.
    It includes some enhancements presented in the Java port at
    :cite:`dcm4che:2011`.

    Phonem is intended chiefly for German names/words.

    .. versionadded:: 0.3.6
    """

    _substitutions = (
        ('SC', 'C'),
        ('SZ', 'C'),
        ('CZ', 'C'),
        ('TZ', 'C'),
        ('TS', 'C'),
        ('KS', 'X'),
        ('PF', 'V'),
        ('QU', 'KW'),
        ('PH', 'V'),
        ('UE', 'Y'),
        ('AE', 'E'),
        ('OE', 'Ö'),
        ('EI', 'AY'),
        ('EY', 'AY'),
        ('EU', 'OY'),
        ('AU', 'A§'),
        ('OU', '§'),
    )

    _trans = dict(
        zip(
            (ord(_) for _ in 'ZKGQÇÑßFWPTÁÀÂÃÅÄÆÉÈÊËIJÌÍÎÏÜÝ§ÚÙÛÔÒÓÕØ'),
            'CCCCCNSVVBDAAAAAEEEEEEYYYYYYYYUUUUOOOOÖ',
        )
    )

    _uc_set = set('ABCDLMNORSUVWXYÖ')

    def encode(self, word: str) -> str:
        """Return the Phonem code for a word.

        Parameters
        ----------
        word : str
        The word to transform

        Returns
        -------
        str
            The Phonem value

        Examples
        --------
        >>> pe = Phonem()
        >>> pe.encode('Christopher')
        'CRYSDOVR'
        >>> pe.encode('Niall')
        'NYAL'
        >>> pe.encode('Smith')
        'SMYD'
        >>> pe.encode('Schmidt')
        'CMYD'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = unicode_normalize('NFC', word.upper())
        for i, j in self._substitutions:
            word = word.replace(i, j)
        word = word.translate(self._trans)

        return ''.join(
            c
            for c in self._delete_consecutive_repeats(word)
            if c in self._uc_set
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
