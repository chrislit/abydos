# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.fingerprint._lacss.

L.A. County Sheriff's System fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from itertools import groupby

from ._fingerprint import _Fingerprint

__all__ = ['LACSS']


class LACSS(_Fingerprint):
    """L.A. County Sheriff's System fingerprint.

    Based on the description from :cite:`Taft:1970`.

    .. versionadded:: 0.4.1
    """

    def __init__(self):
        """Initialize LACSS instance.


        .. versionadded:: 0.4.1

        """
        super(_Fingerprint, self).__init__()

        self._vowels = set('AEIOUYWH')

        self._t1 = {_[0]: _[1] for _ in zip('RNLTSCMDKAGBPFVZXJQ', range(1, 20))}
        self._t1.update({_: 0 for _ in self._vowels})

        self._t2 = {_[0]:_[1] for _ in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(1, 27))}

    def fingerprint(self, word):
        """Return the LACSS coding.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The L.A. County Sheriff's System fingerprint

        Examples
        --------
        >>> cf = LACSS()
        >>> bin(cf.fingerprint('hat'))
        '0b110000100000000'
        >>> bin(cf.fingerprint('niall'))
        '0b10110000100000'
        >>> bin(cf.fingerprint('colin'))
        '0b1110000110000'
        >>> bin(cf.fingerprint('atcg'))
        '0b110000000010000'
        >>> bin(cf.fingerprint('entreatment'))
        '0b1110010010000100'


        .. versionadded:: 0.4.1

        """
        # uppercase
        word = word.upper()

        # remove vowels
        word = word[:1] + ''.join(_ for _ in word[1:] if _ not in 'AEIOUWHY')
        word += (12-len(word))*'A'

        # step 1
        code = self._t2[word[:1]]*10

        for letter in word[1:12]:
            code *= 10
            code += self._t1[letter]

        code *= 3
        code = str(int(code**0.5))

        return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
