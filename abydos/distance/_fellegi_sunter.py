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

"""abydos.distance._fellegi_sunter.

Fellegi-Sunter similarity
"""

from math import exp, log
from sys import float_info

from ._token_distance import _TokenDistance

__all__ = ['FellegiSunter']


class FellegiSunter(_TokenDistance):
    r"""Fellegi-Sunter similarity.

    Fellegi-Sunter similarity is based on the description in
    :cite:`Cohen:2003` and implementation in :cite:`Cohen:2003b`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        tokenizer=None,
        intersection_type='crisp',
        simplified=False,
        mismatch_factor=0.5,
        **kwargs
    ):
        """Initialize FellegiSunter instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        simplified : bool
            Specifies to use the simplified scoring variant
        mismatch_factor : float
            Specifies the penalty factor for mismatches
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
        super(FellegiSunter, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )
        self._simplified = simplified
        self._mismatch_factor = mismatch_factor

    def sim_score(self, src, tar):
        """Return the Fellegi-Sunter similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fellegi-Sunter similarity

        Examples
        --------
        >>> cmp = FellegiSunter()
        >>> cmp.sim_score('cat', 'hat')
        0.8803433378011485
        >>> cmp.sim_score('Niall', 'Neil')
        0.6958768466635681
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.45410905865149187
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)
        src_tokens, tar_tokens = self._get_tokens()

        src_total = sum(src_tokens.values())
        tar_total = sum(tar_tokens.values())
        src_unique = len(src_tokens)
        tar_unique = len(tar_tokens)

        similarity = 0.0
        for _tok, count in self._intersection().items():
            if self._simplified:
                similarity += -log(count / tar_total)
            else:
                prob = count / tar_total
                similarity -= log(
                    1
                    + float_info.epsilon
                    - exp(
                        src_unique
                        * tar_unique
                        * log(1 + float_info.epsilon - prob * prob)
                    )
                )

        for _tok, count in self._src_only().items():
            if self._simplified:
                similarity -= -log(count / src_total) * self._mismatch_factor

        return similarity

    def sim(self, src, tar):
        """Return the normalized Fellegi-Sunter similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Fellegi-Sunter similarity

        Examples
        --------
        >>> cmp = FellegiSunter()
        >>> cmp.sim('cat', 'hat')
        0.2934477792670495
        >>> cmp.sim('Niall', 'Neil')
        0.13917536933271363
        >>> cmp.sim('aluminum', 'Catalan')
        0.056763632331436484
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score == 0.0:
            return 0.0
        if self._simplified:
            return max(0.0, score / (len(src) + len(tar)))
        return max(0.0, score / max(len(src), len(tar)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
