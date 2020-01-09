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

"""abydos.distance._chao_dice.

Chao's Dice similarity
"""

from ._chao_jaccard import ChaoJaccard

__all__ = ['ChaoDice']


class ChaoDice(ChaoJaccard):
    r"""Chao's Dice similarity.

    Chao's Dice similarity :cite:`Chao:2004`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize ChaoDice instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(ChaoDice, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return the normalized Chao's Dice similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Chao's Dice similarity

        Examples
        --------
        >>> import random
        >>> random.seed(0)
        >>> cmp = ChaoDice()
        >>> cmp.sim('cat', 'hat')
        0.36666666666666664
        >>> cmp.sim('Niall', 'Neil')
        0.27868852459016397
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        return max(0.0, min(1.0, self.sim_score(src, tar)))

    def sim_score(self, src, tar):
        """Return the Chao's Dice similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Chao's Dice similarity

        Examples
        --------
        >>> import random
        >>> random.seed(0)
        >>> cmp = ChaoDice()
        >>> cmp.sim_score('cat', 'hat')
        0.36666666666666664
        >>> cmp.sim_score('Niall', 'Neil')
        0.27868852459016397
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        u_hat, v_hat = self._get_estimates(src, tar)

        num = u_hat * v_hat
        if num:
            return 2 * num / (u_hat + v_hat)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
