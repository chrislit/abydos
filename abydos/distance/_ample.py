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

"""abydos.distance._ample.

AMPLE similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['AMPLE']


class AMPLE(_TokenDistance):
    r"""AMPLE similarity.

    The AMPLE similarity :cite:`Dallmeier:2005,Abreu:2007` is defined in
    getAverageSequenceWeight() in the AverageSequenceWeightEvaluator.java file
    of AMPLE's source code. For two sets X and Y and a population N, it is

        .. math::

            sim_{AMPLE}(X, Y) =
            \big|\frac{|X \cap Y|}{|X|} -
            \frac{|Y \setminus X|}{|N \setminus X|}\big|

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{AMPLE} =
            \big|\frac{a}{a+b}-\frac{c}{c+d}\big|

    Notes
    -----
    This measure is asymmetric. The first ratio considers how similar the two
    strings are, while the second considers how dissimilar the second string
    is. As a result, both very similar and very dissimilar strings will score
    high on this measure, provided the unique aspects are present chiefly
    in the latter string.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize AMPLE instance.

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
        super(AMPLE, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the AMPLE similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            AMPLE similarity

        Examples
        --------
        >>> cmp = AMPLE()
        >>> cmp.sim('cat', 'hat')
        0.49743589743589745
        >>> cmp.sim('Niall', 'Neil')
        0.32947729220222793
        >>> cmp.sim('aluminum', 'Catalan')
        0.10209049255441008
        >>> cmp.sim('ATCG', 'TAGC')
        0.006418485237483954


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        # If the denominators are 0, set them to 1.
        # This is a deviation from the formula, but prevents division by zero
        # while retaining the contribution of the other ratio.
        if a + b == 0:
            b = 1
        if c + d == 0:
            d = 1

        return abs((a / (a + b)) - (c / (c + d)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
