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

"""abydos.distance._kulczynski_i.

Kulczynski I similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['KulczynskiI']


class KulczynskiI(_TokenDistance):
    r"""Kulczynski I similarity.

    For two sets X and Y, Kulczynski I similarity
    :cite:`Kulczynski:1927` is

        .. math::

            sim_{KulczynskiI}(X, Y) =
            \frac{|X \cap Y|}{|X \setminus Y| + |Y \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{KulczynskiI} =
            \frac{a}{b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize KulczynskiI instance.

        Parameters
        ----------
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
        super(KulczynskiI, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Kulczynski I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kulczynski I similarity

        Examples
        --------
        >>> cmp = KulczynskiI()
        >>> cmp.sim_score('cat', 'hat')
        0.5
        >>> cmp.sim_score('Niall', 'Neil')
        0.2857142857142857
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.06666666666666667
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        if not a:
            return 0.0
        if not b + c:
            return float('inf')
        return a / (b + c)

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
            Method disabled for Kulczynski I similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError(
            'Method disabled for Kulczynski I similarity.'
        )

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
            Method disabled for Kulczynski I similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError(
            'Method disabled for Kulczynski I similarity.'
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
