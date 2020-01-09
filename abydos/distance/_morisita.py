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

"""abydos.distance._morisita.

Morisita index of overlap
"""

from ._token_distance import _TokenDistance

__all__ = ['Morisita']


class Morisita(_TokenDistance):
    r"""Morisita index of overlap.

    Morisita index of overlap :cite:`Morisita:1959`, following the description
    of :cite:`Horn:1966`, given two populations X and Y drawn from S species,
    is:

    .. math::

        sim_{Morisita}(X, Y) =
        C_{\lambda} = \frac{2\sum_{i=1}^S x_i y_i}{(\lambda_x + \lambda_y)XY}

    where

    .. math::

        X = \sum_{i=1}^S x_i  ~~;~~  Y = \sum_{i=1}^S y_i

    .. math::

        \lambda_x = \frac{\sum_{i=1}^S x_i(x_i-1)}{X(X-1)} ~~;~~
        \lambda_y = \frac{\sum_{i=1}^S y_i(y_i-1)}{Y(Y-1)}

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Morisita instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Morisita, self).__init__(**kwargs)

    def sim_score(self, src, tar):
        """Return the Morisita similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Morisita similarity

        Examples
        --------
        >>> cmp = Morisita()
        >>> cmp.sim_score('cat', 'hat')
        0.25
        >>> cmp.sim_score('Niall', 'Neil')
        0.13333333333333333
        >>> cmp.sim_score('aluminum', 'Catalan')
        1.0
        >>> cmp.sim_score('ATCG', 'TAGC')
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
            src_lambda += val * (val - 1)
        if src_lambda:
            src_lambda /= src_card * (src_card - 1)
        for val in self._tar_tokens.values():
            tar_lambda += val * (val - 1)
        if tar_lambda:
            tar_lambda /= tar_card * (tar_card - 1)

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

    def sim(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Morisita similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Morisita similarity.')

    def dist(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Morisita similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Morisita similarity.')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
