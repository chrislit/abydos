# Copyright 2019-2020 by Christopher C. Little.
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

from ._fingerprint import _Fingerprint

__all__ = ['LACSS']


class LACSS(_Fingerprint):
    """L.A. County Sheriff's System fingerprint.

    Based on the description from :cite:`Taft:1970`.

    .. versionadded:: 0.4.1
    """

    _vowels = set('AEIOUYWH')

    _t1 = {_[0]: _[1] for _ in zip('RNLTSCMDKAGBPFVZXJQ', range(1, 20))}
    _t1.update({_: 0 for _ in _vowels})

    _t2 = {_[0]: _[1] for _ in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(1, 27))}

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
        >>> cf.fingerprint('hat')
        '4911211'
        >>> cf.fingerprint('niall')
        '6488374'
        >>> cf.fingerprint('colin')
        '3015957'
        >>> cf.fingerprint('atcg')
        '1772371'
        >>> cf.fingerprint('entreatment')
        '3882324'


        .. versionadded:: 0.4.1

        """
        # uppercase
        word = word.upper()

        # remove vowels
        word = word[:1] + ''.join(_ for _ in word[1:] if _ not in 'AEIOUWHY')
        word += 12 * 'A'

        # step 1
        code = 0
        i = 0
        while (not code) and (i < len(word)):
            if word[i] in self._t2:
                code = self._t2[word[i]] * 10
            i += 1

        letters = 11
        while letters and i < len(word):
            if word[i] in self._t1:
                code *= 10
                code += self._t1[word[i]]
                letters -= 1
            i += 1

        code *= 3
        code = str(int(code ** 0.5))

        return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
