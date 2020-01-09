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

"""abydos.distance._cole.

Cole correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Cole']


class Cole(_TokenDistance):
    r"""Cole correlation.

    For two sets X and Y and a population N, the Cole correlation
    :cite:`Cole:1949` has three formulae:

    - If :math:`|X \cap Y| \cdot |(N \setminus X) \setminus Y| \geq
      |X \setminus Y| \cdot |Y \setminus Y|` then

        .. math::

            corr_{Cole}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {(|X \cap Y| + |X \setminus Y|) \cdot
            (|X \setminus Y| + |(N \setminus X) \setminus Y|)}

    - If :math:`|(N \setminus X) \setminus Y| \geq |X \cap Y|` then

        .. math::

            corr_{Cole}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {(|X \cap Y| + |X \setminus Y|) \cdot
            (|X \cap Y| + |Y \setminus X|)}

    - Otherwise

        .. math::

            corr_{Cole}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {(|X \setminus Y| + |(N \setminus X) \setminus Y|) \cdot
            (|Y \setminus X| + |(N \setminus X) \setminus Y|)}

    Cole terms this measurement the Coefficient of Interspecific Association.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Cole} =
            \left\{
            \begin{array}{ll}
                \frac{ad-bc}{(a+b)(b+d)} & \textup{if} ~ad \geq bc \\
                \\
                \frac{ad-bc}{(a+b)(a+c)} & \textup{if} ~d \geq a \\
                \\
                \frac{ad-bc}{(b+d)(c+d)} & \textup{otherwise}
            \end{array}
            \right.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Cole instance.

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
        super(Cole, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Cole correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Cole correlation

        Examples
        --------
        >>> cmp = Cole()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.3290543431750107
        >>> cmp.corr('aluminum', 'Catalan')
        0.10195910195910196
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        admbc = a * d - b * c

        if admbc == 0.0:
            return 0.0

        if a * d >= b * c:
            return admbc / ((a + b) * (b + d))
        if d >= a:
            return admbc / ((a + b) * (a + c))
        return admbc / ((b + d) * (c + d))

    def sim(self, src, tar):
        """Return the Cole similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for similarity
        tar : str
            Target string (or QGrams/Counter objects) for similarity

        Returns
        -------
        float
            Cole similarity

        Examples
        --------
        >>> cmp = Cole()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6645271715875054
        >>> cmp.sim('aluminum', 'Catalan')
        0.550979550979551
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1 + self.corr(src, tar)) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
