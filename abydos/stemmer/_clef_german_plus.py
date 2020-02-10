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

"""abydos.stemmer._clef_german_plus.

CLEF German plus stemmer
"""

from unicodedata import normalize

from ._stemmer import _Stemmer

__all__ = ['CLEFGermanPlus']


class CLEFGermanPlus(_Stemmer):
    """CLEF German stemmer plus.

    The CLEF German stemmer plus is defined at :cite:`Savoy:2005`.

    .. versionadded:: 0.3.6
    """

    _st_ending = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 't'}

    _accents = dict(
        zip((ord(_) for _ in 'äàáâöòóôïìíîüùúû'), 'aaaaooooiiiiuuuu')
    )

    def stem(self, word: str) -> str:
        """Return 'CLEF German stemmer plus' stem.

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
        >>> stmr = CLEFGermanPlus()
        >>> stmr.stem('lesen')
        'les'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabi'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())

        # remove umlauts
        word = word.translate(self._accents)

        # Step 1
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'ern':
            word = word[:-3]
        elif wlen > 3 and word[-2:] in {'em', 'en', 'er', 'es'}:
            word = word[:-2]
        elif wlen > 2 and (
            word[-1] == 'e'
            or (word[-1] == 's' and word[-2] in self._st_ending)
        ):
            word = word[:-1]

        # Step 2
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'est':
            word = word[:-3]
        elif wlen > 3 and (
            word[-2:] in {'er', 'en'}
            or (word[-2:] == 'st' and word[-3] in self._st_ending)
        ):
            word = word[:-2]

        return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
