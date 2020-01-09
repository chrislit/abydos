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

"""abydos.distance._rouge_su.

Rouge-SU similarity
"""

from . import RougeS

__all__ = ['RougeSU']


class RougeSU(RougeS):
    r"""Rouge-SU similarity.

    Rouge-SU similarity :cite:`Lin:2004`, operating on character-level
    skipgrams

    .. versionadded:: 0.4.0
    """

    def __init__(self, qval=2, **kwargs):
        """Initialize RougeSU instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(RougeSU, self).__init__(qval=qval, **kwargs)

    def sim(self, src, tar, beta=8):
        """Return the Rouge-SU similarity of two strings.

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
            Rouge-SU similarity

        Examples
        --------
        >>> cmp = RougeSU()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4020618556701031
        >>> cmp.sim('aluminum', 'Catalan')
        0.1672384219554031
        >>> cmp.sim('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.4.0

        """
        return super(RougeSU, self).sim(
            '$' * (self._qval - 1) + src, '$' * (self._qval - 1) + tar, beta
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
