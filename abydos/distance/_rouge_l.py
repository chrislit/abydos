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

"""abydos.distance._rouge_l.

Rouge-L similarity
"""

from . import LCSseq
from ._distance import _Distance

__all__ = ['RougeL']


class RougeL(_Distance):
    r"""Rouge-L similarity.

    Rouge-L similarity :cite:`Lin:2004`

    .. versionadded:: 0.4.0
    """

    _lcs = LCSseq()

    def __init__(self, **kwargs):
        """Initialize RougeL instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(RougeL, self).__init__(**kwargs)

    def sim(self, src, tar, beta=8):
        """Return the Rouge-L similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        beta : int or float
            A weighting factor to prejudice similarity towards src

        Returns
        -------
        float
            Rouge-L similarity

        Examples
        --------
        >>> cmp = RougeL()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.6018518518518519
        >>> cmp.sim('aluminum', 'Catalan')
        0.3757225433526012
        >>> cmp.sim('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        lcs_len = len(self._lcs.lcsseq(src, tar))
        r_lcs = lcs_len / len(src)
        p_lcs = lcs_len / len(tar)
        beta_sq = beta * beta

        if r_lcs and p_lcs:
            return (1 + beta_sq) * r_lcs * p_lcs / (r_lcs + beta_sq * p_lcs)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
