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

"""abydos.fingerprint._lc_cutter.

Library of Congress Cutter table encoding
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fingerprint import _Fingerprint

__all__ = ['LCCutter']


class LCCutter(_Fingerprint):
    """LCCutter table encoding.



    .. versionadded:: 0.4.1
    """

    _vowels = set('AEIOU')
    _after_initial_vowel = ['C', 'K', 'M', 'O', 'Q', 'R', 'T', 'Z']
    _after_initial_s = ['C', 'D', 'G', 'L', 'S', 'U', 'Z']

    _after_initial_qu = ['D', 'H', 'N', 'Q', 'S', 'X', 'Z']
    _after_initial_cons = ['D', 'H', 'N', 'Q', 'T', 'X', 'Z']

    _expansions = ['D', 'H', 'L', 'O', 'S', 'V', 'Z']

    def __init__(self, variant=1):
        """Initialize LCCutter instance.

        Parameters
        ----------
        variant : int


        .. versionadded:: 0.4.1

        """
        super(_Fingerprint, self).__init__()
        self._variant = variant

    def fingerprint(self, word):
        """Return the consonant coding.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        str
            The Library of Congress Cutter table encoding

        Examples
        --------
        >>> cf = LCCutter()
        >>> cf.fingerprint('hat')
        'HT'
        >>> cf.fingerprint('niall')
        'NLL'
        >>> cf.fingerprint('colin')
        'CLN'
        >>> cf.fingerprint('atcg')
        'ATCG'
        >>> cf.fingerprint('entreatment')
        'ENTRTMNT'


        .. versionadded:: 0.4.1

        """
        if word:
            return ''
        if len(word) == 1:
            return word.upper()

        # uppercase
        uc = word.upper()

        # first cutter
        if uc[0] in self._vowels:


        return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
