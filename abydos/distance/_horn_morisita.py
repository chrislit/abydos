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

"""abydos.distance._horn_morisita.

Horn-Morisita index of overlap
"""

from ._token_distance import _TokenDistance

__all__ = ['HornMorisita']


class HornMorisita(_TokenDistance):
    r"""Horn-Morisita index of overlap.

    Horn-Morisita index of overlap :cite:`Horn:1966`, given two populations X
    and Y drawn from S species, is:

    .. math::

        sim_{Horn-Morisita}(X, Y) =
        C_{\lambda} = \frac{2\sum_{i=1}^S x_i y_i}
        {(\hat{\lambda}_x + \hat{\lambda}_y)XY}

    where

    .. math::

        X = \sum_{i=1}^S x_i  ~~;~~  Y = \sum_{i=1}^S y_i

    .. math::

        \hat{\lambda}_x = \frac{\sum_{i=1}^S x_i^2}{X^2} ~~;~~
        \hat{\lambda}_y = \frac{\sum_{i=1}^S y_i^2}{Y^2}

    Observe that this is identical to Morisita similarity, except for the
    definition of the :math:`\lambda` values in the denominator.

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize HornMorisita instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(HornMorisita, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return the Horn-Morisita similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Horn-Morisita similarity

        Examples
        --------
        >>> cmp = HornMorisita()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3636363636363636
        >>> cmp.sim('aluminum', 'Catalan')
        0.10650887573964497
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        intersection = self._intersection()

        src_card = self._src_card()
        tar_card = self._tar_card()

        src_lambda = 0
        tar_lambda = 0
        for val in self._src_tokens.values():
            src_lambda += val * val
        if src_lambda:
            src_lambda /= src_card * src_card
        for val in self._tar_tokens.values():
            tar_lambda += val * val
        if tar_lambda:
            tar_lambda /= tar_card * tar_card

        sim = 0
        for symbol in intersection.keys():
            sim += self._src_tokens[symbol] * self._tar_tokens[symbol]
        sim *= 2
        if src_card:
            sim /= src_card
        if tar_card:
            sim /= tar_card
        if src_lambda + tar_lambda:
            sim /= src_lambda + tar_lambda

        return sim


if __name__ == '__main__':
    import doctest

    doctest.testmod()
