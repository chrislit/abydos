# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._jaccard.

Jaccard similarity coefficient, distance, & Tanimoto coefficient
"""

from math import log2

from ._tversky import Tversky

__all__ = ['Jaccard']


class Jaccard(Tversky):
    r"""Jaccard similarity.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901,Ruzicka:1958` is

        .. math::

            sim_{Jaccard}(X, Y) =
            \frac{|X \cap Y|}{|X \cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 1`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Jaccard} =
            \frac{a}{a+b+c}

    Notes
    -----
    The multiset variant is termed Ellenberg similarity :cite:`Ellenberg:1956`.

    .. versionadded:: 0.3.6

    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Jaccard instance.

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
        super(Jaccard, self).__init__(
            alpha=1,
            beta=1,
            bias=None,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        r"""Return the Jaccard similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Jaccard similarity

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super(Jaccard, self).sim(src, tar)

    def tanimoto_coeff(self, src, tar):
        """Return the Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2} sim_{Tanimoto}(X, Y)`.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tanimoto distance

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        coeff = self.sim(src, tar)
        if coeff != 0:
            return log2(coeff)

        return float('-inf')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
