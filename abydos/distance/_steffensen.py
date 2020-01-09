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

"""abydos.distance._steffensen.

Steffensen similarity
"""

from numpy import array as np_array

from ._token_distance import _TokenDistance

__all__ = ['Steffensen']


class Steffensen(_TokenDistance):
    r"""Steffensen similarity.

    For two sets X and Y and a population N, Steffensen similarity
    :math:`\psi^2` :cite:`Steffensen:1934` is

        .. math::

            \begin{array}{ll}
            sim_{Steffensen_{\psi}}(X, Y) = \psi^2 &=
            \sum_{i \in X}\sum_{j \in Y} p_{ij} \phi_{ij}^2
            \\
            \\
            \phi_{ij}^2 &= \frac{(p_{ij} - p_{i*}p_{*i})^2}
            {p_{i*}(1-p_{i*})p_{*j}(1-p_{*j})}
            \end{array}

    Where each value :math:`p_{ij}` is drawn from the 2x2 contingency table:

    +-------------------+------------------+-------------------+---------+
    |                   | |s_in| ``tar``   | |s_notin| ``tar`` |         |
    +-------------------+------------------+-------------------+---------+
    | |s_in| ``src``    | |s_a|            | |s_b|             | |s_a+b| |
    +-------------------+------------------+-------------------+---------+
    | |s_notin| ``src`` | |s_c|            | |s_d|             | |s_c+d| |
    +-------------------+------------------+-------------------+---------+
    |                   | |s_a+c|          | |s_b+d|           | |s_n|   |
    +-------------------+------------------+-------------------+---------+

    .. |s_in| replace:: :math:`x \in`
    .. |s_notin| replace:: :math:`x \notin`

    .. |s_a| replace:: :math:`p_{11} = a`
    .. |s_b| replace:: :math:`p_{10} = b`
    .. |s_c| replace:: :math:`p_{01} = c`
    .. |s_d| replace:: :math:`p_{00} = d`
    .. |s_n| replace:: :math:`1`
    .. |s_a+b| replace:: :math:`p_{1*} = a+b`
    .. |s_a+c| replace:: :math:`p_{*1} = a+c`
    .. |s_c+d| replace:: :math:`p_{0*} = c+d`
    .. |s_b+d| replace:: :math:`p_{*0} = b+d`

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        normalizer='proportional',
        **kwargs
    ):
        """Initialize Steffensen instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        normalizer : str
            Specifies the normalization type. See :ref:`normalizer <alphabet>`
            description in :py:class:`_TokenDistance` for details.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Steffensen, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Steffensen similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Steffensen similarity

        Examples
        --------
        >>> cmp = Steffensen()
        >>> cmp.sim('cat', 'hat')
        0.24744247205786737
        >>> cmp.sim('Niall', 'Neil')
        0.1300991207720166
        >>> cmp.sim('aluminum', 'Catalan')
        0.011710186806836031
        >>> cmp.sim('ATCG', 'TAGC')
        4.1196952743871653e-05


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

        p = np_array([[a, b], [c, d]]) / n

        psisq = 0.0

        for i in range(len(p)):
            pi_star = p[i, :].sum()
            for j in range(len(p[i])):
                pj_star = p[:, j].sum()
                num = p[i, j] * (p[i, j] - pi_star * pj_star) ** 2
                if num:
                    psisq += num / (
                        pi_star * (1 - pi_star) * pj_star * (1 - pj_star)
                    )

        return psisq


if __name__ == '__main__':
    import doctest

    doctest.testmod()
