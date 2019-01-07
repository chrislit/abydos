# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._goodman_kruskal_lambda.

Goodman & Kruskal's Lambda similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['GoodmanKruskalLambda']


class GoodmanKruskalLambda(_TokenDistance):
    r"""Goodman & Kruskal's Lambda similarity.

    For two sets X and Y and a population N, Goodman & Kruskal's lambda
    :cite:`Goodman:1954` is

        .. math::

            sim_{GK_\lambda}(X, Y) =
            \frac{(max(|X \cap Y|, |X \setminus Y|)+
            max(|Y \setminus X|, |(N \setminus X) \setminus Y|)+
            max(|X \cap Y|, |Y \setminus X|)+
            max(|X \setminus Y|, |(N \setminus X) \setminus Y|))-
            (max(|Y|, |N \setminus Y|)+max(|X|, |N \setminus X|))}
            {2|N|-(max(|Y|, |N \setminus Y|)+max(|X|, |N \setminus X|))}

    In 2x2 matrix, a+b+c+d=n terms, this is

        .. math::

            sim_{GK_\lambda} =
            \frac{(max(a,b)+max(c,d)+max(a,c)+max(b,d))-
            (max(a+b,b+d)+max(a+b,c+d))}{2n-(max(a+b,b+d)+max(a+b,c+d))}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GoodmanKruskalLambda instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.

                - If a Counter is supplied, it is used directly in computing
                  the complement of the tokens in both sets.
                - If a collection is supplied, it is converted to a Counter
                  and used directly. In the case of a single string being
                  supplied and the QGram tokenizer being used, the full
                  alphabet is inferred (i.e.
                  :math:`len(set(alphabet+QGrams.start_stop))^{QGrams.qval}` is
                  used as the cardinality of the full alphabet.
                - If an int is supplied, it is used as the cardinality of the
                  full alphabet.
                - If None is supplied, the cardinality of the full alphabet
                  is inferred if QGram tokenization is used (i.e.
                  :math:`28^{QGrams.qval}` is used as the cardinality of the
                  full alphabet or :math:`26` if QGrams.qval is 1, which
                  assumes the strings are English language strings). Otherwise,
                  The cardinality of the complement of the total will be 0.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:

                - 'crisp': Ordinary intersection, wherein items are entirely
                  members or non-members of the intersection. (Default)
                - 'fuzzy': Fuzzy intersection, defined by :cite:`Wang:2014`,
                  wherein items can be partially members of the intersection
                  if their similarity meets or exceeds a threshold value. This
                  also takes `metric` (by default :class:`Levenshtein()`) and
                  `threshold` (by default 0.8) parameters.
                - 'soft': Soft intersection, defined by :cite:`Russ:2014`,
                  wherein items can be partially members of the intersection
                  depending on their similarity. This also takes a `metric`
                  (by default :class:`DamerauLevenshtein()`) parameter.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the 'fuzzy' variant.


        .. versionadded:: 0.4.0

        """
        super(GoodmanKruskalLambda, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Goodman & Kruskal's Lambda similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Goodman & Kruskal's Lambda similarity

        Examples
        --------
        >>> cmp = GoodmanKruskalLambda()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self.tokenize(src, tar)

        a = self.intersection_card()
        b = self.src_only_card()
        c = self.tar_only_card()
        d = self.total_complement_card()

        sigma = max(a, b) + max(c + d) + max(a, c) + max(b, d)
        sigma_prime = max(a + c, b + d) + max(a + b, c + d)

        return sigma - sigma_prime / (2 * (a + b + c + d) - sigma_prime)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
