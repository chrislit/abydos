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

"""abydos.distance._generalized_fleiss.

Generalized Fleiss correlation
"""

from ._token_distance import _TokenDistance
from ..stats._mean import (
    aghmean,
    agmean,
    amean,
    cmean,
    ghmean,
    gmean,
    heronian_mean,
    hmean,
    hoelder_mean,
    imean,
    lehmer_mean,
    lmean,
    qmean,
    seiffert_mean,
)

__all__ = ['GeneralizedFleiss']


def _agmean_prec6(l):
    return agmean(l, prec=6)


def _ghmean_prec6(l):
    return ghmean(l, prec=6)


def _aghmean_prec6(l):
    return aghmean(l, prec=6)


means = {
    'arithmetic': amean,
    'geometric': gmean,
    'harmonic': hmean,
    'ag': _agmean_prec6,
    'gh': _ghmean_prec6,
    'agh': _aghmean_prec6,
    'contraharmonic': cmean,
    'identric': imean,
    'logarithmic': lmean,
    'quadratic': qmean,
    'heronian': heronian_mean,
    'hoelder': hoelder_mean,
    'lehmer': lehmer_mean,
    'seiffert': seiffert_mean,
}


class GeneralizedFleiss(_TokenDistance):
    r"""Generalized Fleiss correlation.

    For two sets X and Y and a population N, Generalized Fleiss correlation
    is based on observations from :cite:`Fleiss:1975`.

        .. math::

            corr_{GeneralizedFleiss}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {\mu_{products~of~marginals}}

    The mean function :math:`\mu` may be any of the mean functions in
    :py:mod:`abydos.stats`. The products of marginals may be one of the
    following:

        - ``a`` : :math:`|X| \cdot |N \setminus X|` &
          :math:`|Y| \cdot |N \setminus Y|`
        - ``b`` : :math:`|X| \cdot |Y|` &
          :math:`|N \setminus X| \cdot |N \setminus Y|`
        - ``c`` : :math:`|X| \cdot |N| \setminus Y|` &
          :math:`|Y| \cdot |N \setminus X|`

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{GeneralizedFleiss} =
            \frac{ad-bc}{\mu_{products~of~marginals}}

    And the products of marginals are:

        - ``a`` : :math:`p_1q_1 = (a+b)(c+d)` & :math:`p_2q_2 = (a+c)(b+d)`
        - ``b`` : :math:`p_1p_2 = (a+b)(a+c)` & :math:`q_1q_2 = (c+d)(b+d)`
        - ``c`` : :math:`p_1q_2 = (a+b)(b+d)` & :math:`p_2q_1 = (a+c)(c+d)`

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
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        mean_func : str or function
            Specifies the mean function to use. A function taking a list of
            numbers as its only required argument may be supplied, or one of
            the following strings will select the specified mean function from
            :py:mod:`abydos.stats`:

                - ``arithmetic`` employs :py:func:`amean`, and this measure
                  will be identical to :py:class:`MaxwellPilliner` with
                  otherwise default parameters
                - ``geometric`` employs :py:func:`gmean`, and this measure
                  will be identical to :py:class:`PearsonPhi` with otherwise
                  default parameters
                - ``harmonic`` employs :py:func:`hmean`, and this measure
                  will be identical to :py:class:`Fleiss` with otherwise
                  default parameters
                - ``ag`` employs the arithmetic-geometric mean
                  :py:func:`agmean`
                - ``gh`` employs the geometric-harmonic mean
                  :py:func:`ghmean`
                - ``agh`` employs the arithmetic-geometric-harmonic mean
                  :py:func:`aghmean`
                - ``contraharmonic`` employs the contraharmonic mean
                  :py:func:`cmean`
                - ``identric`` employs the identric mean :py:func:`imean`
                - ``logarithmic`` employs the logarithmic mean
                  :py:func:`lmean`
                - ``quadratic`` employs the quadratic mean :py:func:`qmean`
                - ``heronian`` employs the Heronian mean
                  :py:func:`heronian_mean`
                - ``hoelder`` employs the Hölder mean :py:func:`hoelder_mean`
                - ``lehmer`` employs the Lehmer mean :py:func:`lehmer_mean`
                - ``seiffert`` employs Seiffert's mean
                  :py:func:`seiffert_mean`
        marginals : str
            Specifies the pairs of marginals to multiply and calculate the
            resulting mean of. Can be:

                - ``a`` : :math:`p_1q_1 = (a+b)(c+d)` &
                  :math:`p_2q_2 = (a+c)(b+d)`
                - ``b`` : :math:`p_1p_2 = (a+b)(a+c)` &
                  :math:`q_1q_2 = (c+d)(b+d)`
                - ``c`` : :math:`p_1q_2 = (a+b)(b+d)` &
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
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


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

    def corr(self, src, tar):
        """Return the Generalized Fleiss correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Generalized Fleiss correlation

        Examples
        --------
        >>> cmp = GeneralizedFleiss()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.35921989956790845
        >>> cmp.corr('aluminum', 'Catalan')
        0.10803030303030303
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237483954


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        if self.proportional:
            a /= n
            b /= n
            c /= n
            d /= n

        num = a * d - b * c
        if not num:
            return 0.0

        if self.marginals == 'b':
            mps = [(a + b) * (a + c), (c + d) * (b + d)]
        elif self.marginals == 'c':
            mps = [(a + b) * (b + d), (a + c) * (c + d)]
        else:
            mps = [(a + b) * (c + d), (a + c) * (b + d)]

        mean_value = (
            self.mean_func(mps)
            if callable(self.mean_func)
            else means[self.mean_func](mps)
        )

        return num / mean_value

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
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6796099497839543
        >>> cmp.sim('aluminum', 'Catalan')
        0.5540151515151515
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
