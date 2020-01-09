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

"""abydos.distance._brainerd_robinson.

Brainerd-Robinson similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['BrainerdRobinson']


class BrainerdRobinson(_TokenDistance):
    r"""Brainerd-Robinson similarity.

    For two multisets X and Y drawn from an alphabet S, Brainerd-Robinson
    similarity :cite:`Robinson:1951,Brainerd:1951` is

        .. math::

            sim_{BrainerdRobinson}(X, Y) =
            200 - 100 \cdot \sum_{i \in S} |\frac{X_i}{\sum_{i \in S} |X_i|} -
            \frac{Y_i}{\sum_{i \in S} |Y_i|}|

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize BrainerdRobinson instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.0

        """
        super(BrainerdRobinson, self).__init__(tokenizer=tokenizer, **kwargs)

    def sim_score(self, src, tar):
        """Return the Brainerd-Robinson similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Brainerd-Robinson similarity

        Examples
        --------
        >>> cmp = BrainerdRobinson()
        >>> cmp.sim_score('cat', 'hat')
        100.0
        >>> cmp.sim_score('Niall', 'Neil')
        66.66666666666669
        >>> cmp.sim_score('aluminum', 'Catalan')
        22.2222222222222
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()
        src_card = max(1, self._src_card())
        tar_card = max(1, self._tar_card())

        score = 200.0 - 100.0 * sum(
            abs(
                self._src_tokens[tok] / src_card
                - self._tar_tokens[tok] / tar_card
            )
            for tok in alphabet
        )
        if score < 1e-13:
            score = 0.0

        return score

    def sim(self, src, tar):
        """Return the normalized Brainerd-Robinson similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Brainerd-Robinson similarity

        Examples
        --------
        >>> cmp = BrainerdRobinson()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3333333333333334
        >>> cmp.sim('aluminum', 'Catalan')
        0.111111111111111
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return self.sim_score(src, tar) / 200.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
