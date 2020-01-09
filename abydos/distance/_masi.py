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

"""abydos.distance._masi.

MASI similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['MASI']


class MASI(_TokenDistance):
    r"""MASI similarity.

    Measuring Agreement on Set-valued Items (MASI) similarity
    :cite:`Passonneau:2006` for two sets X and Y is based on Jaccard
    similarity:

        .. math::

            sim_{Jaccard}(X, Y) = \frac{|X \cap Y|}{|X \cup Y|}

    This Jaccard similarity is scaled by a value M, which is:
        - 1 if :math:`X = Y`
        - :math:`\frac{2}{3}` if :math:`X \subset Y` or :math:`Y \subset X`
        - :math:`\frac{1}{3}` if :math:`X \cap Y \neq \emptyset`,
          :math:`X \setminus Y \neq \emptyset`, and
          :math:`Y \setminus X \neq \emptyset`
        - 0 if :math:`X \cap Y = \emptyset`


    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize MASI instance.

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
        super(MASI, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the MASI similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            MASI similarity

        Examples
        --------
        >>> cmp = MASI()
        >>> cmp.sim('cat', 'hat')
        0.1111111111111111
        >>> cmp.sim('Niall', 'Neil')
        0.07407407407407407
        >>> cmp.sim('aluminum', 'Catalan')
        0.020833333333333332
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        abc = self._union_card()

        jaccard = a / abc
        if b == 0 or c == 0:
            monotonicity = 2 / 3
        elif a != 0:
            monotonicity = 1 / 3
        else:
            monotonicity = 0.0

        return jaccard * monotonicity


if __name__ == '__main__':
    import doctest

    doctest.testmod()
