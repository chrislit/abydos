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

"""abydos.distance._mutual_information.

Mutual Information similarity
"""

from math import log2

from ._token_distance import _TokenDistance

__all__ = ['MutualInformation']


class MutualInformation(_TokenDistance):
    r"""Mutual Information similarity.

    For two sets X and Y and a population N, Mutual Information similarity
    :cite:`Church:1991` is

        .. math::

            sim_{MI}(X, Y) =
            log_2(\frac{|X \cap Y| \cdot |N|}{|X| \cdot |Y|})

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{MI} =
            log_2(\frac{an}{(a+b)(a+c)})

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize MutualInformation instance.

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
        super(MutualInformation, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Mutual Information similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Mutual Information similarity

        Examples
        --------
        >>> cmp = MutualInformation()
        >>> cmp.sim_score('cat', 'hat')
        6.528166795717758
        >>> cmp.sim_score('Niall', 'Neil')
        5.661433326581222
        >>> cmp.sim_score('aluminum', 'Catalan')
        3.428560943378589
        >>> cmp.sim_score('ATCG', 'TAGC')
        -4.700439718141092


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        apb = self._src_card()
        apc = self._tar_card()
        n = self._population_unique_card()

        return log2((1 + a * n) / (1 + apb * apc))

    def sim(self, src, tar):
        """Return the normalized Mutual Information similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Mutual Information similarity

        Examples
        --------
        >>> cmp = MutualInformation()
        >>> cmp.sim('cat', 'hat')
        0.933609253088981
        >>> cmp.sim('Niall', 'Neil')
        0.8911684881725231
        >>> cmp.sim('aluminum', 'Catalan')
        0.7600321183863901
        >>> cmp.sim('ATCG', 'TAGC')
        0.17522996523538537


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score:
            norm = [
                _
                for _ in [self.sim_score(src, src), self.sim_score(tar, tar)]
                if _ != 0.0
            ]
            if not norm:
                norm = [1]

            return (1.0 + score / max(norm)) / 2.0
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
