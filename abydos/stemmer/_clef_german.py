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

"""abydos.stemmer._clef_german.

CLEF German stemmer
"""

from unicodedata import normalize

from deprecation import deprecated

from ._stemmer import _Stemmer
from .. import __version__

__all__ = ['CLEFGerman', 'clef_german']


class CLEFGerman(_Stemmer):
    """CLEF German stemmer.

    The CLEF German stemmer is defined at :cite:`Savoy:2005`.

    .. versionadded:: 0.3.6
    """

    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))

    def stem(self, word):
        """Return CLEF German stem.

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
        >>> stmr = CLEFGerman()
        >>> stmr.stem('lesen')
        'lese'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabier'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())

        # remove umlauts
        word = word.translate(self._umlauts)

        # remove plurals
        wlen = len(word) - 1

        if wlen > 3:
            if wlen > 5:
                if word[-3:] == 'nen':
                    return word[:-3]
            if wlen > 4:
                if word[-2:] in {'en', 'se', 'es', 'er'}:
                    return word[:-2]
            if word[-1] in {'e', 'n', 'r', 's'}:
                return word[:-1]
        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the CLEFGerman.stem method instead.',
)
def clef_german(word):
    """Return CLEF German stem.

    This is a wrapper for :py:meth:`CLEFGerman.stem`.

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
    >>> clef_german('lesen')
    'lese'
    >>> clef_german('graues')
    'grau'
    >>> clef_german('buchstabieren')
    'buchstabier'

    .. versionadded:: 0.1.0

    """
    return CLEFGerman().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
