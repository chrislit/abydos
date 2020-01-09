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

"""abydos.distance._tversky.

Tversky index
"""

from deprecation import deprecated

from ._token_distance import _TokenDistance
from .. import __version__

__all__ = ['Tversky', 'dist_tversky', 'sim_tversky']


class Tversky(_TokenDistance):
    r"""Tversky index.

    The Tversky index :cite:`Tversky:1977` is defined as:
    For two sets X and Y:

        .. math::

            sim_{Tversky}(X, Y) = \frac{|X \cap Y|}
            {|X \cap Y| + \alpha|X - Y| + \beta|Y - X|}

    :math:`\alpha = \beta = 1` is equivalent to the Jaccard & Tanimoto
    similarity coefficients.

    :math:`\alpha = \beta = 0.5` is equivalent to the Sørensen-Dice
    similarity coefficient :cite:`Dice:1945,Sorensen:1948`.

    Unequal α and β will tend to emphasize one or the other set's
    contributions:

        - :math:`\alpha > \beta` emphasizes the contributions of X over Y
        - :math:`\alpha < \beta` emphasizes the contributions of Y over X)

    Parameter values' relation to 1 emphasizes different types of
    contributions:

        - :math:`\alpha` and :math:`\beta > 1` emphsize unique contributions
          over the intersection
        - :math:`\alpha` and :math:`\beta < 1` emphsize the intersection over
          unique contributions

    The symmetric variant is defined in :cite:`Jiminez:2013`. This is activated
    by specifying a bias parameter.


    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        alpha=1.0,
        beta=1.0,
        bias=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Tversky instance.

        Parameters
        ----------
        alpha : float
            Tversky index parameter as described above
        beta : float
            Tversky index parameter as described above
        bias : float
            The symmetric Tversky index bias parameter
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
        super(Tversky, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )
        self.set_params(alpha=alpha, beta=beta, bias=bias)

    def sim(self, src, tar):
        """Return the Tversky index of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tversky similarity

        Raises
        ------
        ValueError
            Unsupported weight assignment; alpha and beta must be greater than
            or equal to 0.

        Examples
        --------
        >>> cmp = Tversky()
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
        if self.params['alpha'] < 0 or self.params['beta'] < 0:
            raise ValueError(
                'Unsupported weight assignment; alpha and beta '
                + 'must be greater than or equal to 0.'
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        q_src_mag = self._src_only_card()
        q_tar_mag = self._tar_only_card()
        q_intersection_mag = self._intersection_card()

        if not self._src_tokens or not self._tar_tokens:
            return 0.0

        if self.params['bias'] is None:
            return q_intersection_mag / (
                q_intersection_mag
                + self.params['alpha'] * q_src_mag
                + self.params['beta'] * q_tar_mag
            )

        a_val, b_val = sorted((q_src_mag, q_tar_mag))
        c_val = q_intersection_mag + self.params['bias']
        return c_val / (
            self.params['beta']
            * (
                self.params['alpha'] * a_val
                + (1 - self.params['alpha']) * b_val
            )
            + c_val
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Tversky.sim method instead.',
)
def sim_tversky(src, tar, qval=2, alpha=1.0, beta=1.0, bias=None):
    """Return the Tversky index of two strings.

    This is a wrapper for :py:meth:`Tversky.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    alpha : float
        Tversky index parameter as described above
    beta : float
        Tversky index parameter as described above
    bias : float
        The symmetric Tversky index bias parameter

    Returns
    -------
    float
        Tversky similarity

    Examples
    --------
    >>> sim_tversky('cat', 'hat')
    0.3333333333333333
    >>> sim_tversky('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tversky('aluminum', 'Catalan')
    0.0625
    >>> sim_tversky('ATCG', 'TAGC')
    0.0


    .. versionadded:: 0.1.0

    """
    return Tversky(alpha=alpha, beta=beta, bias=bias, qval=qval).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Tversky.dist method instead.',
)
def dist_tversky(src, tar, qval=2, alpha=1.0, beta=1.0, bias=None):
    """Return the Tversky distance between two strings.

    This is a wrapper for :py:meth:`Tversky.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    alpha : float
        Tversky index parameter as described above
    beta : float
        Tversky index parameter as described above
    bias : float
        The symmetric Tversky index bias parameter

    Returns
    -------
    float
        Tversky distance

    Examples
    --------
    >>> dist_tversky('cat', 'hat')
    0.6666666666666667
    >>> dist_tversky('Niall', 'Neil')
    0.7777777777777778
    >>> dist_tversky('aluminum', 'Catalan')
    0.9375
    >>> dist_tversky('ATCG', 'TAGC')
    1.0


    .. versionadded:: 0.1.0

    """
    return Tversky(alpha=alpha, beta=beta, bias=bias, qval=qval).dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
