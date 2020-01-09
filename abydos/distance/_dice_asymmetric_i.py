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

"""abydos.distance._dice_asymmetric_i.

Dice's Asymmetric I similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['DiceAsymmetricI']


class DiceAsymmetricI(_TokenDistance):
    r"""Dice's Asymmetric I similarity.

    For two sets X and Y and a population N, Dice's Asymmetric I similarity
    :cite:`Dice:1945` is

        .. math::

            sim_{DiceAsymmetricI}(X, Y) =
            \frac{|X \cap Y|}{|X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{DiceAsymmetricI} =
            \frac{a}{a+b}

    Notes
    -----
    In terms of a confusion matrix, this is equivalent to precision or
    positive predictive value :py:meth:`ConfusionTable.precision`.

    .. versionadded:: 0.4.0

    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize DiceAsymmetricI instance.

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
        super(DiceAsymmetricI, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the Dice's Asymmetric I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dice's Asymmetric I similarity

        Examples
        --------
        >>> cmp = DiceAsymmetricI()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3333333333333333
        >>> cmp.sim('aluminum', 'Catalan')
        0.1111111111111111
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        ab = self._src_card()

        if a == 0.0:
            return 0.0
        return a / ab


if __name__ == '__main__':
    import doctest

    doctest.testmod()
