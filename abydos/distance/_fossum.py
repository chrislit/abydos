# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._fossum.

Fossum similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Fossum']


class Fossum(_TokenDistance):
    r"""Fossum similarity.

    For two sets X and Y and a population N, the Fossum similarity
    :cite:`Fossum:1966` is

        .. math::

            sim_{Fossum}(X, Y) =
            \frac{|N| \cdot \Big(|X \cap Y|-\frac{1}{2}\Big)^2}{|X| \cdot |Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Fossum} =
            \frac{n(a-\frac{1}{2})^2}{(a+b)(a+c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Fossum instance.

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
        super(Fossum, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Fossum similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fossum similarity

        Examples
        --------
        >>> cmp = Fossum()
        >>> cmp.sim_score('cat', 'hat')
        110.25
        >>> cmp.sim_score('Niall', 'Neil')
        58.8
        >>> cmp.sim_score('aluminum', 'Catalan')
        2.7256944444444446
        >>> cmp.sim_score('ATCG', 'TAGC')
        7.84


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        n = self._population_unique_card()
        a = self._intersection_card()
        apb = max(1.0, self._src_card())
        apc = max(1.0, self._tar_card())

        num = n * (a - 0.5) ** 2
        if num:
            return num / (apb * apc)
        return 0.0

    def sim(self, src, tar):
        """Return the normalized Fossum similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Fossum similarity

        Examples
        --------
        >>> cmp = Fossum()
        >>> cmp.sim('cat', 'hat')
        0.1836734693877551
        >>> cmp.sim('Niall', 'Neil')
        0.08925619834710742
        >>> cmp.sim('aluminum', 'Catalan')
        0.0038927335640138415
        >>> cmp.sim('ATCG', 'TAGC')
        0.01234567901234568


        .. versionadded:: 0.4.0

        """
        num = self.sim_score(src, tar)
        if num:
            return num / max(
                self.sim_score(src, src), self.sim_score(tar, tar)
            )
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
