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

"""abydos.distance._cao.

Cao's CY dissimilarity.
"""

from math import log10

from ._token_distance import _TokenDistance

__all__ = ['Cao']


class Cao(_TokenDistance):
    r"""Cao's CY dissimilarity.

    Given :math:`X_{ij}` (the number of individuals of speecies :math:`j` in
    sample :math:`i`), :math:`X_{kj}` (the number of individuals of speecies
    :math:`j` in sample :math:`k`), and :math:`N` (the total number of speecies
    present in both samples), Cao dissimilarity (CYd) :cite:`Cao:1997` is:

    .. math::

        dist_{Cao}(X, Y) =
        CYd = \frac{1}{N}\sum\Bigg(\frac{(X_{ij} + X_{kj})log_{10}\big(
        \frac{X_{ij}+X_{kj}}{2}\big)-X_{ij}log_{10}X_{kj}-X_{kj}log_{10}X_{ij}}
        {X_{ij}+X_{kj}}\Bigg)

    In the above formula, whenever :math:`X_{ij} = 0` or :math:`X_{kj} = 0`,
    the value 0.1 is substituted.

    Since this measure ranges from 0 to :math:`\infty`, a similarity measure,
    CYs, ranging from 0 to 1 was also developed.

    .. math::

        sim_{Cao}(X, Y) = CYs = 1 - \frac{Observed~CYd}{Maximum~CYd}

    where

    .. math::

        Observed~CYd = \sum\Bigg(\frac{(X_{ij} + X_{kj})log_{10}\big(
        \frac{X_{ij}+X_{kj}}{2}\big)-X_{ij}log_{10}X_{kj}-X_{kj}log_{10}X_{ij}}
        {X_{ij}+X_{kj}}\Bigg)

    and with :math:`a` (the number of species present in both samples),
    :math:`b` (the number of species present in sample :math:`i` only), and
    :math:`c` (the number of species present in sample :math:`j` only),

    .. math::

        Maximum~CYd = D_1 + D_2 + D_3

    with

    .. math::

        D_1 = \sum_{j=1}^b \Bigg(\frac{(X_{ij} + 0.1) log_{10} \big(
        \frac{X_{ij}+0.1}{2}\big)-X_{ij}log_{10}0.1-0.1log_{10}X_{ij}}
        {X_{ij}+0.1}\Bigg)

        D_2 = \sum_{j=1}^c \Bigg(\frac{(X_{kj} + 0.1) log_{10} \big(
        \frac{X_{kj}+0.1}{2}\big)-X_{kj}log_{10}0.1-0.1log_{10}X_{kj}}
        {X_{kj}+0.1}\Bigg)

        D_1 = \sum_{j=1}^a \frac{a}{2} \Bigg(\frac{(D_i + 1) log_{10}
        \big(\frac{D_i+1}{2}\big)-log_{10}D_i}{D_i+1} + \frac{(D_k + 1) log_{10}
        \big(\frac{D_k+1}{2}\big)-log_{10}D_k}{D_k+1}\Bigg)

    with

    .. math::

        D_i = \frac{\sum X_{ij} - \frac{a}{2}}{\frac{a}{2}}

        D_k = \frac{\sum X_{kj} - \frac{a}{2}}{\frac{a}{2}}

    for

    .. math::

        X_{ij} \geq 1

        X_{kj} \geq 1

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Cao instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Cao, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return Cao's CY similarity (CYs) of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cao's CY similarity

        Examples
        --------
        >>> cmp = Cao()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        alphabet = self._total().keys()
        in_both_samples_half = len(self._intersection().keys()) / 2
        if not in_both_samples_half:
            return 0.0

        observed_cyd = 0
        maximum_cyd = 0
        for symbol in alphabet:
            src_tok = max(0.1, self._src_tokens[symbol])
            tar_tok = max(0.1, self._tar_tokens[symbol])
            tok_sum = src_tok + tar_tok
            observed_cyd += (
                tok_sum * log10(tok_sum / 2)
                - src_tok * log10(tar_tok)
                - tar_tok * log10(src_tok)
            ) / tok_sum

            if self._tar_tokens[symbol] == 0:
                maximum_cyd += (
                    (self._src_tokens[symbol] + 0.1)
                    * log10((self._src_tokens[symbol] + 0.1) / 2)
                    - self._src_tokens[symbol] * log10(0.1)
                    - 0.1 * log10(self._src_tokens[symbol])
                ) / (self._src_tokens[symbol] + 0.1)
            elif self._src_tokens[symbol] == 0:
                maximum_cyd += (
                    (self._tar_tokens[symbol] + 0.1)
                    * log10((self._tar_tokens[symbol] + 0.1) / 2)
                    - self._tar_tokens[symbol] * log10(0.1)
                    - 0.1 * log10(self._tar_tokens[symbol])
                ) / (self._tar_tokens[symbol] + 0.1)

        d_i = 0
        d_k = 0
        for symbol in self._intersection().keys():
            d_i += self._src_tokens[symbol]
            d_k += self._tar_tokens[symbol]
        d_i = (d_i - in_both_samples_half) / in_both_samples_half
        d_k = (d_k - in_both_samples_half) / in_both_samples_half

        maximum_cyd += in_both_samples_half * (
            ((d_i + 1) * log10((d_i + 1) / 2) - log10(d_i)) / (d_i + 1)
            + ((d_k + 1) * log10((d_k + 1) / 2) - log10(d_k)) / (d_k + 1)
        )

        return max(0.0, min(1.0, 1 - (observed_cyd / maximum_cyd)))

    def dist_abs(self, src, tar):
        """Return Cao's CY dissimilarity (CYd) of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cao's CY dissimilarity

        Examples
        --------
        >>> cmp = Cao()
        >>> cmp.dist_abs('cat', 'hat')
        0.3247267992925765
        >>> cmp.dist_abs('Niall', 'Neil')
        0.4132886536450973
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.5530666041976232
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.6494535985851531


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        alphabet = self._total().keys()

        score = 0
        for symbol in alphabet:
            src_tok = max(0.1, self._src_tokens[symbol])
            tar_tok = max(0.1, self._tar_tokens[symbol])
            tok_sum = src_tok + tar_tok
            score += (
                tok_sum * log10(tok_sum / 2)
                - src_tok * log10(tar_tok)
                - tar_tok * log10(src_tok)
            ) / tok_sum

        return score / sum(self._total().values())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
