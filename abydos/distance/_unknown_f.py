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

"""abydos.distance._unknown_f.

Unknown F similarity
"""

from math import log

from ._token_distance import _TokenDistance

__all__ = ['UnknownF']


class UnknownF(_TokenDistance):
    r"""Unknown F similarity.

    For two sets X and Y and a population N, Unknown F similarity, which
    :cite:`Choi:2010` attributes to :cite:`Gilbert:1966` but could not be
    located in that source, is given as

        .. math::

            sim(X, Y) =
            log(|X \cap Y|) - log(|N|) - log\Big(\frac{|X|}{|N|}\Big) -
            log\Big(\frac{|Y|}{|N|}\Big)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim =
            log(a) - log(n) - log\Big(\frac{a+b}{n}\Big) -
            log\Big(\frac{a+c}{n}\Big)

    This formula is not very normalizable, so the following formula is used
    instead:

        .. math::

            sim_{UnknownF}(X, Y) =
            min\Bigg(1, 1+log\Big(\frac{|X \cap Y|}{|N|}\Big) -
            \frac{1}{2}\Bigg(log\Big(\frac{|X|}{|N|}\Big) +
            log\Big(\frac{|Y|}{|N|}\Big)\Bigg)\Bigg)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownF} =
            min\Bigg(1, 1+log\Big(\frac{a}{n}\Big) -
            \frac{1}{2}\Bigg(log\Big(\frac{a+b}{n}\Big) +
            log\Big(\frac{a+c}{n}\Big)\Bigg)\Bigg)


    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownF instance.

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
        super(UnknownF, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Unknown F similarity between two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown F similarity

        Examples
        --------
        >>> cmp = UnknownF()
        >>> cmp.sim_score('cat', 'hat')
        0.3068528194400555
        >>> cmp.sim_score('Niall', 'Neil')
        -0.007451510271132555
        >>> cmp.sim_score('aluminum', 'Catalan')
        -1.1383330595080272
        >>> cmp.sim_score('ATCG', 'TAGC')
        1.0


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
        n = self._population_unique_card()

        part1 = a / n
        if part1 == 0:
            part1 = 1

        return min(
            1.0, 1 + log(part1) - (log((a + b) / n) + log((a + c) / n)) / 2
        )

    def sim(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Unknown F similarity


        .. versionadded:: 0.4.0

        """
        raise NotImplementedError('Method disabled for Unknown F similarity.')

    def dist(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Unknown F similarity


        .. versionadded:: 0.4.0

        """
        raise NotImplementedError('Method disabled for Unknown F similarity.')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
