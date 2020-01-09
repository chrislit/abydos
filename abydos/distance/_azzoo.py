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

"""abydos.distance._azzoo.

AZZOO similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['AZZOO']


class AZZOO(_TokenDistance):
    r"""AZZOO similarity.

    For two sets X and Y, and alphabet N, and a parameter :math:`\sigma`,
    AZZOO similarity :cite:`Cha:2006` is

        .. math::

            sim_{AZZOO_{\sigma}}(X, Y) =
            \sum{s_i}

    where :math:`s_i = 1` if :math:`X_i = Y_i = 1`,
    :math:`s_i = \sigma` if :math:`X_i = Y_i = 0`,
    and :math:`s_i = 0` otherwise.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{AZZOO} = a + \sigma \cdot d

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        sigma=0.5,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize AZZOO instance.

        Parameters
        ----------
        sigma : float
            Sigma designates the contribution to similarity given by the
            0-0 samples in the set.
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
        super(AZZOO, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )
        self.set_params(sigma=sigma)

    def sim_score(self, src, tar):
        """Return the AZZOO similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            AZZOO similarity

        Examples
        --------
        >>> cmp = AZZOO()
        >>> cmp.sim_score('cat', 'hat')
        391.0
        >>> cmp.sim_score('Niall', 'Neil')
        389.5
        >>> cmp.sim_score('aluminum', 'Catalan')
        385.5
        >>> cmp.sim_score('ATCG', 'TAGC')
        387.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        d = self._total_complement_card()

        return a + self.params['sigma'] * d

    def sim(self, src, tar):
        """Return the AZZOO similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            AZZOO similarity

        Examples
        --------
        >>> cmp = AZZOO()
        >>> cmp.sim('cat', 'hat')
        0.9923857868020305
        >>> cmp.sim('Niall', 'Neil')
        0.9860759493670886
        >>> cmp.sim('aluminum', 'Catalan')
        0.9710327455919395
        >>> cmp.sim('ATCG', 'TAGC')
        0.9809885931558935


        .. versionadded:: 0.4.0

        """
        den = max(self.sim_score(src, src), self.sim_score(tar, tar))
        if den == 0.0:
            return 1.0

        return self.sim_score(src, tar) / den


if __name__ == '__main__':
    import doctest

    doctest.testmod()
