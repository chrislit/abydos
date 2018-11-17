# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._fingerprint import _Fingerprint
from ..tokenizer import QGrams

__all__ = ['QGram', 'qgram_fingerprint']


class QGram(_Fingerprint):
    """Q-Gram Fingerprint.

    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated. This fingerprint is described at
    :cite:`OpenRefine:2012`.
    """

    def fingerprint(self, phrase, qval=2, start_stop='', joiner=''):
        """Return Q-Gram fingerprint.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the q-gram fingerprint
        qval : int
            The length of each q-gram (by default 2)
        start_stop : str
            The start & stop symbol(s) to concatenate on either end of the
            phrase, as defined in :py:class:`tokenizer.QGrams`
        joiner : str
            The string that will be placed between each word

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

        """
        phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
        phrase = ''.join(c for c in phrase if c.isalnum())
        phrase = QGrams(phrase, qval, start_stop)
        phrase = joiner.join(sorted(phrase))
        return phrase


def qgram_fingerprint(phrase, qval=2, start_stop='', joiner=''):
    """Return Q-Gram fingerprint.

    This is a wrapper for :py:meth:`QGram.fingerprint`.

    Parameters
    ----------
    phrase : str
        The string from which to calculate the q-gram fingerprint
    qval : int
        The length of each q-gram (by default 2)
    start_stop : str
        The start & stop symbol(s) to concatenate on either end of the phrase,
        as defined in :py:class:`tokenizer.QGrams`
    joiner : str
        The string that will be placed between each word

    Returns
    -------
    str
        The q-gram fingerprint of the phrase

    Examples
    --------
    >>> qgram_fingerprint('The quick brown fox jumped over the lazy dog.')
    'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
    >>> qgram_fingerprint('Christopher')
    'cherhehrisopphristto'
    >>> qgram_fingerprint('Niall')
    'aliallni'

    """
    return QGram().fingerprint(phrase, qval, start_stop, joiner)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
