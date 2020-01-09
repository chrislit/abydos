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

"""abydos.distance._jensen_shannon.

Jensen-Shannon divergence
"""

from math import log

from ._token_distance import _TokenDistance

__all__ = ['JensenShannon']


class JensenShannon(_TokenDistance):
    r"""Jensen-Shannon divergence.

    Jensen-Shannon divergence :cite:`Dagan:1999` of two multi-sets X and Y is

        .. math::

            \begin{array}{rl}
            dist_{JS}(X, Y) &= log 2 + \frac{1}{2} \sum_{i \in X \cap Y}
            h(p(X_i) + p(Y_i)) - h(p(X_i)) - h(p(Y_i))

            h(x) &= -x log x

            p(X_i \in X) &= \frac{|X_i|}{|X|}
            \end{array}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize JensenShannon instance.

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


        .. versionadded:: 0.4.0

        """
        super(JensenShannon, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist_abs(self, src, tar):
        """Return the Jensen-Shannon divergence of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Jensen-Shannon divergence

        Examples
        --------
        >>> cmp = JensenShannon()
        >>> cmp.dist_abs('cat', 'hat')
        0.3465735902799726
        >>> cmp.dist_abs('Niall', 'Neil')
        0.44051045978517045
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.6115216713968132
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.6931471805599453


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        def entropy(prob):
            """Return the entropy of prob."""
            if not prob:
                return 0.0
            return -(prob * log(prob))

        src_total = sum(self._src_tokens.values())
        tar_total = sum(self._tar_tokens.values())

        diverg = log(2)
        for key in self._intersection().keys():
            p_src = self._src_tokens[key] / src_total
            p_tar = self._tar_tokens[key] / tar_total

            diverg += (
                entropy(p_src + p_tar) - entropy(p_src) - entropy(p_tar)
            ) / 2

        return diverg

    def dist(self, src, tar):
        """Return the normalized Jensen-Shannon distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Jensen-Shannon distance

        Examples
        --------
        >>> cmp = JensenShannon()
        >>> cmp.dist('cat', 'hat')
        0.49999999999999994
        >>> cmp.dist('Niall', 'Neil')
        0.6355222557917826
        >>> cmp.dist('aluminum', 'Catalan')
        0.8822392827203127
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        return self.dist_abs(src, tar) / log(2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
