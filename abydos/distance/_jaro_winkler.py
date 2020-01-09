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

"""abydos.distance._jaro_winkler.

The distance._JaroWinkler module implements distance metrics based on
:cite:`Jaro:1989` and subsequent works:

    - Jaro distance
    - Jaro-Winkler distance
"""

from deprecation import deprecated

from ._distance import _Distance
from .. import __version__
from ..tokenizer import QGrams

__all__ = ['JaroWinkler', 'dist_jaro_winkler', 'sim_jaro_winkler']


class JaroWinkler(_Distance):
    """Jaro-Winkler distance.

    Jaro(-Winkler) distance is a string edit distance initially proposed by
    Jaro and extended by Winkler :cite:`Jaro:1989,Winkler:1990`.

    This is Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`. The above file is a US Government publication and,
    accordingly, in the public domain.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        qval=1,
        mode='winkler',
        long_strings=False,
        boost_threshold=0.7,
        scaling_factor=0.1,
        **kwargs
    ):
        """Initialize JaroWinkler instance.

        Parameters
        ----------
        qval : int
            The length of each q-gram (defaults to 1: character-wise matching)
        mode : str
            Indicates which variant of this distance metric to compute:

                - ``winkler`` -- computes the Jaro-Winkler distance (default)
                  which increases the score for matches near the start of the
                  word
                - ``jaro`` -- computes the Jaro distance

        long_strings : bool
            Set to True to "Increase the probability of a match when the number
            of matched characters is large. This option allows for a little
            more tolerance when the strings are large. It is not an appropriate
            test when comparing fixed length fields such as phone and social
            security numbers." (Used in 'winkler' mode only.)
        boost_threshold : float
            A value between 0 and 1, below which the Winkler boost is not
            applied (defaults to 0.7). (Used in 'winkler' mode only.)
        scaling_factor : float
            A value between 0 and 0.25, indicating by how much to boost scores
            for matching prefixes (defaults to 0.1). (Used in 'winkler' mode
            only.)


        .. versionadded:: 0.4.0

        """
        super(JaroWinkler, self).__init__(**kwargs)
        self._qval = qval
        self._mode = mode
        self._long_strings = long_strings
        self._boost_threshold = boost_threshold
        self._scaling_factor = scaling_factor

    def sim(self, src, tar):
        """Return the Jaro or Jaro-Winkler similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Jaro or Jaro-Winkler similarity

        Raises
        ------
        ValueError
            Unsupported boost_threshold assignment; boost_threshold must be
            between 0 and 1.
        ValueError
            Unsupported scaling_factor assignment; scaling_factor must be
            between 0 and 0.25.'

        Examples
        --------
        >>> round(sim_jaro_winkler('cat', 'hat'), 12)
        0.777777777778
        >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
        0.805
        >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
        0.60119047619
        >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
        0.833333333333

        >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
        0.777777777778
        >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
        0.783333333333
        >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
        0.60119047619
        >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
        0.833333333333


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if self._mode == 'winkler':
            if self._boost_threshold > 1 or self._boost_threshold < 0:
                raise ValueError(
                    'Unsupported boost_threshold assignment; '
                    + 'boost_threshold must be between 0 and 1.'
                )
            if self._scaling_factor > 0.25 or self._scaling_factor < 0:
                raise ValueError(
                    'Unsupported scaling_factor assignment; '
                    + 'scaling_factor must be between 0 and 0.25.'
                )

        if src == tar:
            return 1.0

        src = QGrams(self._qval).tokenize(src.strip()).get_list()
        tar = QGrams(self._qval).tokenize(tar.strip()).get_list()

        lens = len(src)
        lent = len(tar)

        # If either string is blank - return - added in Version 2
        if lens == 0 or lent == 0:
            return 0.0

        if lens > lent:
            search_range = lens
            minv = lent
        else:
            search_range = lent
            minv = lens

        # Zero out the flags
        src_flag = [0] * search_range
        tar_flag = [0] * search_range
        search_range = max(0, search_range // 2 - 1)

        # Looking only within the search range,
        # count and flag the matched pairs.
        num_com = 0
        yl1 = lent - 1
        for i in range(lens):
            low_lim = (i - search_range) if (i >= search_range) else 0
            hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
            for j in range(low_lim, hi_lim + 1):
                if (tar_flag[j] == 0) and (tar[j] == src[i]):
                    tar_flag[j] = 1
                    src_flag[i] = 1
                    num_com += 1
                    break

        # If no characters in common - return
        if num_com == 0:
            return 0.0

        # Count the number of transpositions
        k = n_trans = 0
        for i in range(lens):
            if src_flag[i] != 0:
                j = 0
                for j in range(k, lent):  # pragma: no branch
                    if tar_flag[j] != 0:
                        k = j + 1
                        break
                if src[i] != tar[j]:
                    n_trans += 1
        n_trans //= 2

        # Main weight computation for Jaro distance
        weight = (
            num_com / lens + num_com / lent + (num_com - n_trans) / num_com
        )
        weight /= 3.0

        # Continue to boost the weight if the strings are similar
        # This is the Winkler portion of Jaro-Winkler distance
        if self._mode == 'winkler' and weight > self._boost_threshold:

            # Adjust for having up to the first 4 characters in common
            j = 4 if (minv >= 4) else minv
            i = 0
            while (i < j) and (src[i] == tar[i]):
                i += 1
            weight += i * self._scaling_factor * (1.0 - weight)

            # Optionally adjust for long strings.

            # After agreeing beginning chars, at least two more must agree and
            # the agreeing characters must be > .5 of remaining characters.
            if (
                self._long_strings
                and (minv > 4)
                and (num_com > i + 1)
                and (2 * num_com >= minv + i)
            ):
                weight += (1.0 - weight) * (
                    (num_com - i - 1) / (lens + lent - i * 2 + 2)
                )

        return weight


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the JaroWinkler.sim method instead.',
)
def sim_jaro_winkler(
    src,
    tar,
    qval=1,
    mode='winkler',
    long_strings=False,
    boost_threshold=0.7,
    scaling_factor=0.1,
):
    """Return the Jaro or Jaro-Winkler similarity of two strings.

    This is a wrapper for :py:meth:`JaroWinkler.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    qval : int
        The length of each q-gram (defaults to 1: character-wise matching)
    mode : str
        Indicates which variant of this distance metric to compute:

            - ``winkler`` -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - ``jaro`` -- computes the Jaro distance

    long_strings : bool
        Set to True to "Increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixedlength fields such as phone and social security
        numbers." (Used in 'winkler' mode only.)
    boost_threshold : float
        A value between 0 and 1, below which the Winkler boost is not applied
        (defaults to 0.7). (Used in 'winkler' mode only.)
    scaling_factor : float
        A value between 0 and 0.25, indicating by how much to boost scores for
        matching prefixes (defaults to 0.1). (Used in 'winkler' mode only.)

    Returns
    -------
    float
        Jaro or Jaro-Winkler similarity

    Examples
    --------
    >>> round(sim_jaro_winkler('cat', 'hat'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
    0.805
    >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
    0.833333333333

    >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.783333333333
    >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.833333333333

    .. versionadded:: 0.1.0

    """
    return JaroWinkler(
        qval, mode, long_strings, boost_threshold, scaling_factor
    ).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the JaroWinkler.dist method instead.',
)
def dist_jaro_winkler(
    src,
    tar,
    qval=1,
    mode='winkler',
    long_strings=False,
    boost_threshold=0.7,
    scaling_factor=0.1,
):
    """Return the Jaro or Jaro-Winkler distance between two strings.

    This is a wrapper for :py:meth:`JaroWinkler.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    qval : int
        The length of each q-gram (defaults to 1: character-wise matching)
    mode : str
        Indicates which variant of this distance metric to compute:

            - ``winkler`` -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - ``jaro`` -- computes the Jaro distance

    long_strings : bool
        Set to True to "Increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixedlength fields such as phone and social security
        numbers." (Used in 'winkler' mode only.)
    boost_threshold : float
        A value between 0 and 1, below which the Winkler boost is not applied
        (defaults to 0.7). (Used in 'winkler' mode only.)
    scaling_factor : float
        A value between 0 and 0.25, indicating by how much to boost scores for
        matching prefixes (defaults to 0.1). (Used in 'winkler' mode only.)

    Returns
    -------
    float
        Jaro or Jaro-Winkler distance

    Examples
    --------
    >>> round(dist_jaro_winkler('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil'), 12)
    0.195
    >>> round(dist_jaro_winkler('aluminum', 'Catalan'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC'), 12)
    0.166666666667

    >>> round(dist_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.216666666667
    >>> round(dist_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.166666666667

    .. versionadded:: 0.1.0

    """
    return JaroWinkler(
        qval, mode, long_strings, boost_threshold, scaling_factor
    ).dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
