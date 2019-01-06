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

"""abydos.distance._generalized_fleiss.

Generalized Fleiss similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance
import stats as mean

__all__ = ['GeneralizedFleiss']


means = {'arithmetic': mean.amean,
         'geometric': mean.gmean,
         'harmonic': mean.hmean,
         'ag': mean.agmean,
         'gh': mean.ghmean,
         'agh': mean.aghmean,
         'contraharmonic': mean.cmean,
         'identric': mean.imean,
         'logarithmic': mean.lmean,
         'quadratic': mean.qmean,
         'heronian': mean.heronian_mean,
         'hoelder': mean.hoelder_mean,
         'lehmer': mean.lehmer_mean,
         'seiffert': mean.seiffert_mean}


class GeneralizedFleiss(_TokenDistance):
    r"""Generalized Fleiss similarity.

    For two sets X and Y and a population N, Generalized Fleiss similarity
    :cite:`CITATION` is

        .. math::

            sim_{GeneralizedFleiss}(X, Y) =

    In 2x2 matrix, a+b+c+d=n terms, this is

        .. math::

            sim_{GeneralizedFleiss} =

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        mean_func='arithmetic',
        marginals='a',
        proportional=False,
        **kwargs
    ):
        """Initialize GeneralizedFleiss instance.

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
            A tokenizer instance from the abydos.tokenizer package
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
        mean_func : str or function
            Specifies the mean function to use. A function taking a list of
            numbers as its only required argument may be supplied, or one of
            the following strings will select the specified mean function from
            :py:module:`abydos.stats.mean`:

                - 'arithmetic' employs :py:function:`amean`, and this measure
                  will be identical to :py:class:`MaxwellPilliner` with
                  otherwise default parameters
                - 'geometric' employs :py:function:`gmean`, and this measure
                  will be identical to :py:class:`PearsonPhi` with otherwise
                  default parameters
                - 'harmonic' employs :py:function:`hmean`, and this measure
                  will be identical to :py:class:`Fleiss` with otherwise
                  default parameters
                - 'ag' employs the arithmetic-geometric mean
                  :py:function:`agmean`
                - 'gh' employs the geometric-harmonic mean
                  :py:function:`ghmean`
                - 'agh' employs the arithmetic-geometric-harmonic mean
                  :py:function:`aghmean`
                - 'contraharmonic' employs the contraharmonic mean
                  :py:function:`cmean`
                - 'identric' employs the identric mean :py:function:`imean`
                - 'logarithmic' employs the logarithmic mean
                  :py:function:`lmean`
                - 'quadratic' employs the quadratic mean :py:function:`qmean`
                - 'heronian' employs the Heronian mean
                  :py:function:`heronian_mean`
                - 'hoelder' employs the Hölder mean :py:function:`hoelder_mean`
                - 'lehmer' employs the Lehmer mean :py:function:`lehmer_mean`
                - 'seiffert' employs Seiffert's mean
                  :py:function:`seiffert_mean`
        marginals : str
            Specifies the pairs of marginals to multiply and calculate the
            resulting mean of. Can be:

                - 'a' : :math:`p_1q_1 = (a+b)(c+d)` &
                  :math:`p_2q_2 = (a+c)(b+d)`
                - 'b' : :math:`p_1p_2 = (a+b)(a+c)` &
                  :math:`q_1q_2 = (c+d)(b+d)`
                - 'c' : :math:`p_1q_2 = (a+b)(b+d)` &
                  :math:`p_2q_1 = (a+c)(c+d)`
        proportional : bool
            If true, each of the values, :math:`a, b, c, d` and the marginals
            will be divided by the total :math:`a+b+c+d=n`.
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
        self.mean_func = mean_func
        self.marginals = marginals
        self.proportional = proportional

        super(GeneralizedFleiss, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Generalized Fleiss similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Generalized Fleiss similarity

        Examples
        --------
        >>> cmp = GeneralizedFleiss()
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
        n = self.population_card()
        
        if self.proportional:
            a /= n
            b /= n
            c /= n
            d /= n

        if self.marginals == 'b':
            mps = [(a+b)*(a+c), (c+d)*(b+d)]
        elif self.marginals == 'c':
            mps = [(a+b)*(b+d), (a+c)*(c+d)]
        else:
            mps = [(a+b)*(c+d), (a+c)*(c+d)]

        mean_value = (self.mean_func(mps) if callable(self.mean_func) else
                      means[self.mean_func](mps))

        return (a*d-b*c)/mean_value


if __name__ == '__main__':
    import doctest

    doctest.testmod()
