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

"""abydos.phonetic._metaphone.

Metaphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['Metaphone', 'metaphone']


class Metaphone(_Phonetic):
    """Metaphone.

    Based on Lawrence Philips' Pick BASIC code from 1990 :cite:`Philips:1990`,
    as described in :cite:`Philips:1990b`.
    This incorporates some corrections to the above code, particularly
    some of those suggested by Michael Kuhn in :cite:`Kuhn:1995`.
    """

    _frontv = {'E', 'I', 'Y'}
    _varson = {'C', 'G', 'P', 'S', 'T'}

    def encode(self, word, max_length=-1):
        """Return the Metaphone code for a word.

        Based on Lawrence Philips' Pick BASIC code from 1990
        :cite:`Philips:1990`, as described in :cite:`Philips:1990b`.
        This incorporates some corrections to the above code, particularly
        some of those suggested by Michael Kuhn in :cite:`Kuhn:1995`.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length of the returned Metaphone code (defaults to 64,
            but in Philips' original implementation this was 4)

        Returns
        -------
        str
            The Metaphone value

        Examples
        --------
        >>> pe = Metaphone()
        >>> pe.encode('Christopher')
        'KRSTFR'
        >>> pe.encode('Niall')
        'NL'
        >>> pe.encode('Smith')
        'SM0'
        >>> pe.encode('Schmidt')
        'SKMTT'

        """
        # Require a max_length of at least 4
        if max_length != -1:
            max_length = max(4, max_length)
        else:
            max_length = 64

        # As in variable sound--those modified by adding an "h"
        ename = ''.join(c for c in word.upper() if c.isalnum())
        ename = ename.replace('ß', 'SS')

        # Delete non-alphanumeric characters and make all caps
        if not ename:
            return ''
        if ename[0:2] in {'PN', 'AE', 'KN', 'GN', 'WR'}:
            ename = ename[1:]
        elif ename[0] == 'X':
            ename = 'S' + ename[1:]
        elif ename[0:2] == 'WH':
            ename = 'W' + ename[2:]

        # Convert to metaphone
        elen = len(ename) - 1
        metaph = ''
        for i in range(len(ename)):
            if len(metaph) >= max_length:
                break
            if (
                ename[i] not in {'G', 'T'}
                and i > 0
                and ename[i - 1] == ename[i]
            ):
                continue

            if ename[i] in self._uc_v_set and i == 0:
                metaph = ename[i]

            elif ename[i] == 'B':
                if i != elen or ename[i - 1] != 'M':
                    metaph += ename[i]

            elif ename[i] == 'C':
                if not (
                    i > 0
                    and ename[i - 1] == 'S'
                    and ename[i + 1 : i + 2] in self._frontv
                ):
                    if ename[i + 1 : i + 3] == 'IA':
                        metaph += 'X'
                    elif ename[i + 1 : i + 2] in self._frontv:
                        metaph += 'S'
                    elif i > 0 and ename[i - 1 : i + 2] == 'SCH':
                        metaph += 'K'
                    elif ename[i + 1 : i + 2] == 'H':
                        if (
                            i == 0
                            and i + 1 < elen
                            and ename[i + 2 : i + 3] not in self._uc_v_set
                        ):
                            metaph += 'K'
                        else:
                            metaph += 'X'
                    else:
                        metaph += 'K'

            elif ename[i] == 'D':
                if (
                    ename[i + 1 : i + 2] == 'G'
                    and ename[i + 2 : i + 3] in self._frontv
                ):
                    metaph += 'J'
                else:
                    metaph += 'T'

            elif ename[i] == 'G':
                if ename[i + 1 : i + 2] == 'H' and not (
                    i + 1 == elen or ename[i + 2 : i + 3] not in self._uc_v_set
                ):
                    continue
                elif i > 0 and (
                    (i + 1 == elen and ename[i + 1] == 'N')
                    or (i + 3 == elen and ename[i + 1 : i + 4] == 'NED')
                ):
                    continue
                elif (
                    i - 1 > 0
                    and i + 1 <= elen
                    and ename[i - 1] == 'D'
                    and ename[i + 1] in self._frontv
                ):
                    continue
                elif ename[i + 1 : i + 2] == 'G':
                    continue
                elif ename[i + 1 : i + 2] in self._frontv:
                    if i == 0 or ename[i - 1] != 'G':
                        metaph += 'J'
                    else:
                        metaph += 'K'
                else:
                    metaph += 'K'

            elif ename[i] == 'H':
                if (
                    i > 0
                    and ename[i - 1] in self._uc_v_set
                    and ename[i + 1 : i + 2] not in self._uc_v_set
                ):
                    continue
                elif i > 0 and ename[i - 1] in self._varson:
                    continue
                else:
                    metaph += 'H'

            elif ename[i] in {'F', 'J', 'L', 'M', 'N', 'R'}:
                metaph += ename[i]

            elif ename[i] == 'K':
                if i > 0 and ename[i - 1] == 'C':
                    continue
                else:
                    metaph += 'K'

            elif ename[i] == 'P':
                if ename[i + 1 : i + 2] == 'H':
                    metaph += 'F'
                else:
                    metaph += 'P'

            elif ename[i] == 'Q':
                metaph += 'K'

            elif ename[i] == 'S':
                if (
                    i > 0
                    and i + 2 <= elen
                    and ename[i + 1] == 'I'
                    and ename[i + 2] in 'OA'
                ):
                    metaph += 'X'
                elif ename[i + 1 : i + 2] == 'H':
                    metaph += 'X'
                else:
                    metaph += 'S'

            elif ename[i] == 'T':
                if (
                    i > 0
                    and i + 2 <= elen
                    and ename[i + 1] == 'I'
                    and ename[i + 2] in {'A', 'O'}
                ):
                    metaph += 'X'
                elif ename[i + 1 : i + 2] == 'H':
                    metaph += '0'
                elif ename[i + 1 : i + 3] != 'CH':
                    if ename[i - 1 : i] != 'T':
                        metaph += 'T'

            elif ename[i] == 'V':
                metaph += 'F'

            elif ename[i] in 'WY':
                if ename[i + 1 : i + 2] in self._uc_v_set:
                    metaph += ename[i]

            elif ename[i] == 'X':
                metaph += 'KS'

            elif ename[i] == 'Z':
                metaph += 'S'

        return metaph


def metaphone(word, max_length=-1):
    """Return the Metaphone code for a word.

    This is a wrapper for :py:meth:`Metaphone.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length of the returned Metaphone code (defaults to 64, but
        in Philips' original implementation this was 4)

    Returns
    -------
    str
        The Metaphone value

    Examples
    --------
    >>> metaphone('Christopher')
    'KRSTFR'
    >>> metaphone('Niall')
    'NL'
    >>> metaphone('Smith')
    'SM0'
    >>> metaphone('Schmidt')
    'SKMTT'

    """
    return Metaphone().encode(word, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
