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

"""abydos.phonetic._russell_index.

Robert C. Russell's Index
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import _Phonetic

__all__ = [
    'RussellIndex',
    'russell_index',
    'russell_index_alpha',
    'russell_index_num_to_alpha',
]


class RussellIndex(_Phonetic):
    """Russell Index.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.
    """

    _uc_set = set('ABCDEFGIKLMNOPQRSTUVXYZ')

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGIKLMNOPQRSTUVXYZ'),
            '12341231356712383412313',
        )
    )
    _num_trans = dict(zip((ord(_) for _ in '12345678'), 'ABCDLMNR'))

    _num_set = set('12345678')

    def encode(self, word):
        """Return the Russell Index (integer output) of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        int
            The Russell Index value

        Examples
        --------
        >>> pe = RussellIndex()
        >>> pe.encode('Christopher')
        3813428
        >>> pe.encode('Niall')
        715
        >>> pe.encode('Smith')
        3614
        >>> pe.encode('Schmidt')
        3614

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = word.replace('GH', '')  # discard gh (rule 3)
        word = word.rstrip('SZ')  # discard /[sz]$/ (rule 3)

        # translate according to Russell's mapping
        word = ''.join(c for c in word if c in self._uc_set)
        sdx = word.translate(self._trans)

        # remove any 1s after the first occurrence
        one = sdx.find('1') + 1
        if one:
            sdx = sdx[:one] + ''.join(c for c in sdx[one:] if c != '1')

        # remove repeating characters
        sdx = self._delete_consecutive_repeats(sdx)

        # return as an int
        return int(sdx) if sdx else float('NaN')

    def _to_alpha(self, num):
        """Convert the Russell Index integer to an alphabetic string.

        This follows Robert C. Russell's Index algorithm, as described in
        :cite:`Russell:1917`.

        Parameters
        ----------
        num : int
            A Russell Index integer value

        Returns
        -------
        str
            The Russell Index as an alphabetic string

        Examples
        --------
        >>> pe = RussellIndex()
        >>> pe._to_alpha(3813428)
        'CRACDBR'
        >>> pe._to_alpha(715)
        'NAL'
        >>> pe._to_alpha(3614)
        'CMAD'

        """
        num = ''.join(c for c in text_type(num) if c in self._num_set)
        if num:
            return num.translate(self._num_trans)
        return ''

    def encode_alpha(self, word):
        """Return the Russell Index (alphabetic output) for the word.

        This follows Robert C. Russell's Index algorithm, as described in
        :cite:`Russell:1917`.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Russell Index value as an alphabetic string

        Examples
        --------
        >>> pe = RussellIndex()
        >>> pe.encode_alpha('Christopher')
        'CRACDBR'
        >>> pe.encode_alpha('Niall')
        'NAL'
        >>> pe.encode_alpha('Smith')
        'CMAD'
        >>> pe.encode_alpha('Schmidt')
        'CMAD'

        """
        if word:
            return self._to_alpha(self.encode(word))
        return ''


def russell_index(word):
    """Return the Russell Index (integer output) of a word.

    This is a wrapper for :py:meth:`RussellIndex.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    int
        The Russell Index value

    Examples
    --------
    >>> russell_index('Christopher')
    3813428
    >>> russell_index('Niall')
    715
    >>> russell_index('Smith')
    3614
    >>> russell_index('Schmidt')
    3614

    """
    return RussellIndex().encode(word)


def russell_index_num_to_alpha(num):
    """Convert the Russell Index integer to an alphabetic string.

    This is a wrapper for :py:meth:`RussellIndex._to_alpha`.

    Parameters
    ----------
    num : int
        A Russell Index integer value

    Returns
    -------
    str
        The Russell Index as an alphabetic string

    Examples
    --------
    >>> russell_index_num_to_alpha(3813428)
    'CRACDBR'
    >>> russell_index_num_to_alpha(715)
    'NAL'
    >>> russell_index_num_to_alpha(3614)
    'CMAD'

    """
    return RussellIndex()._to_alpha(num)


def russell_index_alpha(word):
    """Return the Russell Index (alphabetic output) for the word.

    This is a wrapper for :py:meth:`RussellIndex.encode_alpha`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The Russell Index value as an alphabetic string

    Examples
    --------
    >>> russell_index_alpha('Christopher')
    'CRACDBR'
    >>> russell_index_alpha('Niall')
    'NAL'
    >>> russell_index_alpha('Smith')
    'CMAD'
    >>> russell_index_alpha('Schmidt')
    'CMAD'

    """
    return RussellIndex().encode_alpha(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
