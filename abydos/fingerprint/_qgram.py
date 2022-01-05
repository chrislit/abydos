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

"""abydos.fingerprint._q_gram_fingerprint.

q-gram fingerprint
"""

from unicodedata import normalize as unicode_normalize

from ._fingerprint import _Fingerprint
from ..tokenizer import QGrams

__all__ = ['QGram']


class QGram(_Fingerprint):
    """Q-Gram Fingerprint.

    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated. This fingerprint is described at
    :cite:`OpenRefine:2012`.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        qval: int = 2,
        start_stop: str = '',
        joiner: str = '',
        skip: int = 0,
    ) -> None:
        """Initialize Q-Gram fingerprinter.

        qval : int
            The length of each q-gram (by default 2)
        start_stop : str
            The start & stop symbol(s) to concatenate on either end of the
            phrase, as defined in :py:class:`tokenizer.QGrams`
        joiner : str
            The string that will be placed between each word
        skip : int or Iterable
            The number of characters to skip, can be an integer, range object,
            or list


        .. versionadded:: 0.4.0

        """
        super().__init__()
        self._tokenizer = QGrams(qval, start_stop, skip)
        self._joiner = joiner

    def fingerprint(self, phrase: str) -> str:
        """Return Q-Gram fingerprint.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the q-gram fingerprint

        Returns
        -------
        str
            The q-gram fingerprint of the phrase

        Examples
        --------
        >>> qf = QGram()
        >>> qf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
        >>> qf.fingerprint('Christopher')
        'cherhehrisopphristto'
        >>> qf.fingerprint('Niall')
        'aliallni'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        phrase = unicode_normalize('NFKD', phrase.strip().lower())
        phrase = ''.join(c for c in phrase if c.isalnum())
        phrase = self._joiner.join(
            sorted(self._tokenizer.tokenize(phrase).get_set())
        )
        return phrase


if __name__ == '__main__':
    import doctest

    doctest.testmod()
