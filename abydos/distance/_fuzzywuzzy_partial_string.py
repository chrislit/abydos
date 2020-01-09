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

"""abydos.distance._fuzzywuzzy_partial_string.

FuzzyWuzzy Partial String similarity
"""

from difflib import SequenceMatcher

from ._distance import _Distance

__all__ = ['FuzzyWuzzyPartialString']


class FuzzyWuzzyPartialString(_Distance):
    """FuzzyWuzzy Partial String similarity.

    This follows the FuzzyWuzzy Partial String similarity algorithm
    :cite:`Cohen:2011`. Rather than returning an integer in the range [0, 100],
    as demonstrated in the blog post, this implementation returns a float in
    the range [0.0, 1.0].

    .. versionadded:: 0.4.0
    """

    def sim(self, src, tar):
        """Return the FuzzyWuzzy Partial String similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            FuzzyWuzzy Partial String similarity

        Examples
        --------
        >>> cmp = FuzzyWuzzyPartialString()
        >>> round(cmp.sim('cat', 'hat'), 12)
        0.666666666667
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.75
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.428571428571
        >>> cmp.sim('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        max_sim = 0.0
        start_pos = 0

        if len(src) > len(tar):
            src, tar = tar, src

        src_len = len(src)

        while max_sim < 1.0 and start_pos < len(tar) - src_len + 1:
            max_sim = max(
                max_sim,
                SequenceMatcher(
                    None, src, tar[start_pos : start_pos + src_len]
                ).ratio(),
            )
            start_pos += 1

        return max_sim


if __name__ == '__main__':
    import doctest

    doctest.testmod()
