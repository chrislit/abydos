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

"""abydos.stemmer._clef_swedish.

CLEF Swedish stemmer
"""

from ._stemmer import _Stemmer

__all__ = ['CLEFSwedish']


class CLEFSwedish(_Stemmer):
    """CLEF Swedish stemmer.

    The CLEF Swedish stemmer is defined at :cite:`Savoy:2005`.

    .. versionadded:: 0.3.6
    """

    def stem(self, word):
        """Return CLEF Swedish stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = CLEFSwedish()
        >>> stmr.stem('undervisa')
        'undervis'
        >>> stmr.stem('suspension')
        'suspensio'
        >>> stmr.stem('visshet')
        'viss'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        wlen = len(word) - 2

        if wlen > 2 and word[-1] == 's':
            word = word[:-1]
            wlen -= 1

        _endings = {
            5: {'elser', 'heten'},
            4: {'arne', 'erna', 'ande', 'else', 'aste', 'orna', 'aren'},
            3: {'are', 'ast', 'het'},
            2: {'ar', 'er', 'or', 'en', 'at', 'te', 'et'},
            1: {'a', 'e', 'n', 't'},
        }

        for end_len in range(5, 0, -1):
            if wlen > end_len and word[-end_len:] in _endings[end_len]:
                return word[:-end_len]
        return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
