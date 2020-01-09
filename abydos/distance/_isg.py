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

"""abydos.distance._isg.

Bouchard & Pouyez's Indice de Similitude-Guth (ISG)
"""

from ._distance import _Distance

__all__ = ['ISG']


class ISG(_Distance):
    """Indice de Similitude-Guth (ISG) similarity.

    This is an implementation of Bouchard & Pouyez's Indice de Similitude-Guth
    (ISG) :cite:`Bouchard:1980`. At its heart, ISG is Jaccard similarity, but
    limits on token matching are added according to part of Guth's matching
    criteria :cite:`Guth:1976`.

    :cite:`Bouchard:1980` is limited in its implementation details. Based on
    the examples given in the paper, it appears that only the first 4 of Guth's
    rules are considered (a letter in the first string must match a letter in
    the second string appearing in the same position, an adjacent position, or
    two positions ahead). It also appears that the distance in the paper is
    the greater of the distance from string 1 to string 2 and the distance
    from string 2 to string 1.

    These qualities can be specified as parameters. At initialization, specify
    ``full_guth=True`` to apply all of Guth's rules and ``symmetric=False`` to
    calculate only the distance from string 1 to string 2.

    .. versionadded:: 0.4.1
    """

    def __init__(self, full_guth=False, symmetric=True, **kwargs):
        """Initialize ISG instance.

        Parameters
        ----------
        full_guth : bool
            Whether to apply all of Guth's matching rules
        symmetric : bool
            Whether to calculate the symmetric distance
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(ISG, self).__init__(**kwargs)
        self._full_guth = full_guth
        self._symmetric = symmetric

    def _isg_i(self, src, tar):
        """Return an individual ISG similarity (not symmetric) for src to tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The ISG similarity


        .. versionadded:: 0.4.1

        """

        def _char_at(name, pos):
            if pos >= len(name):
                return None
            return name[pos]

        matches = 0
        for pos in range(len(src)):
            s = _char_at(src, pos)
            t = set(tar[max(0, pos - 1) : pos + 3])
            if s and s in t:
                matches += 1
                continue

            if self._full_guth:
                s = set(src[max(0, pos - 1) : pos + 3])
                t = _char_at(tar, pos)
                if t and t in s:
                    matches += 1
                    continue

                s = _char_at(src, pos + 1)
                t = _char_at(tar, pos + 1)
                if s and t and s == t:
                    matches += 1
                    continue

                s = _char_at(src, pos + 2)
                t = _char_at(tar, pos + 2)
                if s and t and s == t:
                    matches += 1
                    continue

        return matches / (len(src) + len(tar) - matches)

    def sim(self, src, tar):
        """Return the Indice de Similitude-Guth (ISG) similarity of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The ISG similarity

        Examples
        --------
        >>> cmp = ISG()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.5
        >>> cmp.sim('aluminum', 'Catalan')
        0.15384615384615385
        >>> cmp.sim('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        if len(src) > len(tar):
            src, tar = tar, src
        elif self._symmetric and len(src) == len(tar):
            return max(self._isg_i(src, tar), self._isg_i(tar, src))
        return self._isg_i(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
