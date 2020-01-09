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

"""abydos.distance._fager_mcgowan.

Fager & McGowan similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['FagerMcGowan']


class FagerMcGowan(_TokenDistance):
    r"""Fager & McGowan similarity.

    For two sets X and Y, the Fager & McGowan similarity
    :cite:`Fager:1957,Fager:1963` is

        .. math::

            sim_{FagerMcGowan}(X, Y) =
            \frac{|X \cap Y|}{\sqrt{|X|\cdot|Y|}} -
            \frac{1}{2\sqrt{max(|X|, |Y|)}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{FagerMcGowan} =
            \frac{a}{\sqrt{(a+b)(a+c)}} - \frac{1}{2\sqrt{max(a+b, a+c)}}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize FagerMcGowan instance.

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
        super(FagerMcGowan, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Fager & McGowan similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fager & McGowan similarity

        Examples
        --------
        >>> cmp = FagerMcGowan()
        >>> cmp.sim_score('cat', 'hat')
        0.25
        >>> cmp.sim_score('Niall', 'Neil')
        0.16102422643817918
        >>> cmp.sim_score('aluminum', 'Catalan')
        -0.048815536468908724
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.22360679774997896


        .. versionadded:: 0.4.0

        """
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        apb = self._src_card()
        apc = self._tar_card()

        first = a / (apb * apc) ** 0.5 if a else 0.0
        second = 1 / (2 * (max(apb, apc) ** 0.5))

        return first - second

    def sim(self, src, tar):
        r"""Return the normalized Fager & McGowan similarity of two strings.

        As this similarity ranges from :math:`(-\inf, 1.0)`, this normalization
        simply clamps the value to the range (0.0, 1.0).

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Fager & McGowan similarity

        Examples
        --------
        >>> cmp = FagerMcGowan()
        >>> cmp.sim('cat', 'hat')
        0.25
        >>> cmp.sim('Niall', 'Neil')
        0.16102422643817918
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return max(0.0, self.sim_score(src, tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
