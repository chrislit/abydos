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

"""abydos.distance._vps.

Victorian Panel Study (VPS) score
"""

from collections import defaultdict

from ._distance import _Distance

__all__ = ['VPS']


class VPS(_Distance):
    """Victorian Panel Study (VPS) score.

    VPS score is presented in :cite:`Schurer:2007`.

    .. versionadded:: 0.4.1
    """

    def sim(self, src, tar):
        """Return the Victorian Panel Study score of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The VPS score

        Examples
        --------
        >>> cmp = VPS()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3
        >>> cmp.sim('aluminum', 'Catalan')
        0.14285714285714285
        >>> cmp.sim('ATCG', 'TAGC')
        0.3333333333333333


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        if len(src) < len(tar):
            src, tar = tar, src

        score = 0
        discount = 0

        src_tokens = defaultdict(set)
        tar_tokens = defaultdict(set)
        for slen in range(1, 4):
            for i in range(len(src) - slen + 1):
                src_tokens[src[i : i + slen]].add(i)
            for i in range(len(tar) - slen + 1):
                tar_tokens[tar[i : i + slen]].add(i)

        for token in src_tokens.keys():
            if token in tar_tokens:
                for src_pos in src_tokens[token]:
                    score += 1
                    if src_pos not in tar_tokens[token]:
                        discount += min(
                            abs(src_pos - tar_pos)
                            for tar_pos in tar_tokens[token]
                        )

        score -= discount / max(len(src), len(tar))
        if score:
            score /= 3 * len(src) - 3

        return score


if __name__ == '__main__':
    import doctest

    doctest.testmod()
