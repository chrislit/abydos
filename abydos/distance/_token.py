# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.distance.token.

The distance.token module implements token-based distance measures (excluding
those that are Minkowski distance measures):

    - Tversky index
    - Sørensen–Dice coefficient & distance
    - Jaccard similarity coefficient, distance, & Tanimoto coefficient
    - overlap similarity & distance
    - cosine similarity & distance
    - Bag similarity & distance
    - Monge-Elkan similarity & distance
"""

from __future__ import division, unicode_literals

from collections import Counter
from math import log, sqrt

from ._distance import Distance, TokenDistance
from ._levenshtein import sim_levenshtein
from ..tokenizer import QGrams

__all__ = [
    'Bag',
    'Cosine',
    'Dice',
    'Jaccard',
    'MongeElkan',
    'Overlap',
    'Tversky',
    'bag',
    'dist_bag',
    'dist_cosine',
    'dist_dice',
    'dist_jaccard',
    'dist_monge_elkan',
    'dist_overlap',
    'dist_tversky',
    'sim_bag',
    'sim_cosine',
    'sim_dice',
    'sim_jaccard',
    'sim_monge_elkan',
    'sim_overlap',
    'sim_tversky',
    'tanimoto',
]


class Tversky(TokenDistance):
    r"""Tversky index.

    The Tversky index :cite:`Tversky:1977` is defined as:
    For two sets X and Y:
    :math:`sim_{Tversky}(X, Y) = \\frac{|X \\cap Y|}
    {|X \\cap Y| + \\alpha|X - Y| + \\beta|Y - X|}`.

    :math:`\\alpha = \\beta = 1` is equivalent to the Jaccard & Tanimoto
    similarity coefficients.

    :math:`\\alpha = \\beta = 0.5` is equivalent to the Sørensen-Dice
    similarity coefficient :cite:`Dice:1945,Sorensen:1948`.

    Unequal α and β will tend to emphasize one or the other set's
    contributions:

        - :math:`\\alpha > \\beta` emphasizes the contributions of X over Y
        - :math:`\\alpha < \\beta` emphasizes the contributions of Y over X)

    Parameter values' relation to 1 emphasizes different types of
    contributions:

        - :math:`\\alpha and \\beta > 1` emphsize unique contributions over the
          intersection
        - :math:`\\alpha and \\beta < 1` emphsize the intersection over unique
          contributions

    The symmetric variant is defined in :cite:`Jiminez:2013`. This is activated
    by specifying a bias parameter.
    """

    def sim(self, src, tar, qval=2, alpha=1, beta=1, bias=None):
        """Return the Tversky index of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param float alpha: Tversky index parameter as described above
        :param float beta: Tversky index parameter as described above
        :param float bias: The symmetric Tversky index bias parameter
        :returns: Tversky similarity
        :rtype: float

        >>> cmp = Tversky()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        if alpha < 0 or beta < 0:
            raise ValueError(
                'Unsupported weight assignment; alpha and beta '
                + 'must be greater than or equal to 0.'
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        if not q_src or not q_tar:
            return 0.0

        if bias is None:
            return q_intersection_mag / (
                q_intersection_mag
                + alpha * (q_src_mag - q_intersection_mag)
                + beta * (q_tar_mag - q_intersection_mag)
            )

        a_val = min(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        b_val = max(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        c_val = q_intersection_mag + bias
        return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky index of two strings.

    This is a wrapper for :py:meth:`Tversky.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param float alpha: Tversky index parameter as described above
    :param float beta: Tversky index parameter as described above
    :param float bias: The symmetric Tversky index bias parameter
    :returns: Tversky similarity
    :rtype: float

    >>> sim_tversky('cat', 'hat')
    0.3333333333333333
    >>> sim_tversky('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tversky('aluminum', 'Catalan')
    0.0625
    >>> sim_tversky('ATCG', 'TAGC')
    0.0
    """
    return Tversky().sim(src, tar, qval, alpha, beta, bias)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky distance between two strings.

    This is a wrapper for :py:meth:`Tversky.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
        version
    :param float alpha: the Tversky index's alpha parameter
    :param float beta: the Tversky index's beta parameter
    :param float bias: The symmetric Tversky index bias parameter
    :returns: Tversky distance
    :rtype: float

    >>> dist_tversky('cat', 'hat')
    0.6666666666666667
    >>> dist_tversky('Niall', 'Neil')
    0.7777777777777778
    >>> dist_tversky('aluminum', 'Catalan')
    0.9375
    >>> dist_tversky('ATCG', 'TAGC')
    1.0
    """
    return Tversky().dist(src, tar, qval, alpha, beta, bias)


class Dice(Tversky):
    r"""Sørensen–Dice coefficient.

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948` is
    :math:`sim_{dice}(X, Y) = \\frac{2 \\cdot |X \\cap Y|}{|X| + |Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 0.5`.
    """

    def sim(self, src, tar, qval=2):
        """Return the Sørensen–Dice coefficient of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram
            version
        :returns: Sørensen–Dice similarity
        :rtype: float

        >>> cmp = Dice()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        return super(self.__class__, self).sim(src, tar, qval, 0.5, 0.5)


def sim_dice(src, tar, qval=2):
    """Return the Sørensen–Dice coefficient of two strings.

    This is a wrapper for :py:meth:`Dice.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
        version
    :returns: Sørensen–Dice similarity
    :rtype: float

    >>> sim_dice('cat', 'hat')
    0.5
    >>> sim_dice('Niall', 'Neil')
    0.36363636363636365
    >>> sim_dice('aluminum', 'Catalan')
    0.11764705882352941
    >>> sim_dice('ATCG', 'TAGC')
    0.0
    """
    return Dice().sim(src, tar, qval)


def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance between two strings.

    This is a wrapper for :py:meth:`Dice.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
        version
    :returns: Sørensen–Dice distance
    :rtype: float

    >>> dist_dice('cat', 'hat')
    0.5
    >>> dist_dice('Niall', 'Neil')
    0.6363636363636364
    >>> dist_dice('aluminum', 'Catalan')
    0.8823529411764706
    >>> dist_dice('ATCG', 'TAGC')
    1.0
    """
    return Dice().dist(src, tar, qval)


class Jaccard(Tversky):
    r"""Jaccard similarity.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901` is :math:`sim_{jaccard}(X, Y) =
    \\frac{|X \\cap Y|}{|X \\cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 1`.
    """

    def sim(self, src, tar, qval=2):
        r"""Return the Jaccard similarity of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram
            version
        :returns: Jaccard similarity
        :rtype: float

        >>> cmp = Jaccard()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        return super(self.__class__, self).sim(src, tar, qval, 1, 1)

    def tanimoto_coeff(self, src, tar, qval=2):
        """Return the Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2}sim_{Tanimoto}`.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :returns: Tanimoto distance
        :rtype: float

        >>> cmp = Jaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf
        """
        coeff = self.sim(src, tar, qval)
        if coeff != 0:
            return log(coeff, 2)

        return float('-inf')


def sim_jaccard(src, tar, qval=2):
    """Return the Jaccard similarity of two strings.

    This is a wrapper for :py:meth:`Jaccard.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram
        version
    :returns: Jaccard similarity
    :rtype: float

    >>> sim_jaccard('cat', 'hat')
    0.3333333333333333
    >>> sim_jaccard('Niall', 'Neil')
    0.2222222222222222
    >>> sim_jaccard('aluminum', 'Catalan')
    0.0625
    >>> sim_jaccard('ATCG', 'TAGC')
    0.0
    """
    return Jaccard().sim(src, tar, qval)


def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance between two strings.

    This is a wrapper for :py:meth:`Jaccard.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: Jaccard distance
    :rtype: float

    >>> dist_jaccard('cat', 'hat')
    0.6666666666666667
    >>> dist_jaccard('Niall', 'Neil')
    0.7777777777777778
    >>> dist_jaccard('aluminum', 'Catalan')
    0.9375
    >>> dist_jaccard('ATCG', 'TAGC')
    1.0
    """
    return Jaccard().dist(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Return the Tanimoto coefficient of two strings.

    The Tanimoto coefficient :cite:`Tanimoto:1958` is
    :math:`-log_{2}sim_{Tanimoto}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: Tanimoto distance
    :rtype: float

    >>> tanimoto('cat', 'hat')
    -1.5849625007211563
    >>> tanimoto('Niall', 'Neil')
    -2.1699250014423126
    >>> tanimoto('aluminum', 'Catalan')
    -4.0
    >>> tanimoto('ATCG', 'TAGC')
    -inf
    """
    return Jaccard().tanimoto_coeff(src, tar, qval)


class Overlap(TokenDistance):
    r"""Overlap coefficient.

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient, is
    :math:`sim_{overlap}(X, Y) = \\frac{|X \\cap Y|}{min(|X|, |Y|)}`.
    """

    def sim(self, src, tar, qval=2):
        r"""Return the overlap coefficient of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :returns: overlap similarity
        :rtype: float

        >>> cmp = Overlap()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.125
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        return q_intersection_mag / min(q_src_mag, q_tar_mag)


def sim_overlap(src, tar, qval=2):
    r"""Return the overlap coefficient of two strings.

    This is a wrapper for :py:meth:`Overlap.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: overlap similarity
    :rtype: float

    >>> sim_overlap('cat', 'hat')
    0.5
    >>> sim_overlap('Niall', 'Neil')
    0.4
    >>> sim_overlap('aluminum', 'Catalan')
    0.125
    >>> sim_overlap('ATCG', 'TAGC')
    0.0
    """
    return Overlap().sim(src, tar, qval)


def dist_overlap(src, tar, qval=2):
    """Return the overlap distance between two strings.

    This is a wrapper for :py:meth:`Overlap.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: overlap distance
    :rtype: float

    >>> dist_overlap('cat', 'hat')
    0.5
    >>> dist_overlap('Niall', 'Neil')
    0.6
    >>> dist_overlap('aluminum', 'Catalan')
    0.875
    >>> dist_overlap('ATCG', 'TAGC')
    1.0
    """
    return Overlap().dist(src, tar, qval)


class Cosine(TokenDistance):
    r"""Cosine similarity.

    For two sets X and Y, the cosine similarity, Otsuka-Ochiai coefficient, or
    Ochiai coefficient :cite:`Otsuka:1936,Ochiai:1957` is:
    :math:`sim_{cosine}(X, Y) = \\frac{|X \\cap Y|}{\\sqrt{|X| \\cdot |Y|}}`.
    """

    def sim(self, src, tar, qval=2):
        r"""Return the cosine similarity of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :returns: cosine similarity
        :rtype: float

        >>> cmp = Cosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.11785113019775793
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        return q_intersection_mag / sqrt(q_src_mag * q_tar_mag)


def sim_cosine(src, tar, qval=2):
    r"""Return the cosine similarity of two strings.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: cosine similarity
    :rtype: float

    >>> sim_cosine('cat', 'hat')
    0.5
    >>> sim_cosine('Niall', 'Neil')
    0.3651483716701107
    >>> sim_cosine('aluminum', 'Catalan')
    0.11785113019775793
    >>> sim_cosine('ATCG', 'TAGC')
    0.0
    """
    return Cosine().sim(src, tar, qval)


def dist_cosine(src, tar, qval=2):
    """Return the cosine distance between two strings.

    Cosine distance is the complement of cosine similarity:
    :math:`dist_{cosine} = 1 - sim_{cosine}`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: cosine distance
    :rtype: float

    >>> dist_cosine('cat', 'hat')
    0.5
    >>> dist_cosine('Niall', 'Neil')
    0.6348516283298893
    >>> dist_cosine('aluminum', 'Catalan')
    0.882148869802242
    >>> dist_cosine('ATCG', 'TAGC')
    1.0
    """
    return Cosine().dist(src, tar, qval)


class Bag(TokenDistance):
    """Bag distance.

    Bag distance is proposed in :cite:`Bartolini:2002`. It is defined as:
    :math:`max(|multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)|)`.
    """

    def dist_abs(self, src, tar):
        """Return the bag distance between two strings.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: bag distance
        :rtype: int

        >>> cmp = Bag()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0
        >>> cmp.dist_abs('abcdefg', 'hijklm')
        7
        >>> cmp.dist_abs('abcdefg', 'hijklmno')
        8
        """
        if tar == src:
            return 0
        elif not src:
            return len(tar)
        elif not tar:
            return len(src)

        src_bag = Counter(src)
        tar_bag = Counter(tar)
        return max(
            sum((src_bag - tar_bag).values()),
            sum((tar_bag - src_bag).values()),
        )

    def dist(self, src, tar):
        """Return the normalized bag distance between two strings.

        Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: normalized bag distance
        :rtype: float

        >>> cmp = Bag()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.0
        """
        if tar == src:
            return 0.0
        if not src or not tar:
            return 1.0

        max_length = max(len(src), len(tar))

        return self.dist_abs(src, tar) / max_length


def bag(src, tar):
    """Return the bag distance between two strings.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: bag distance
    :rtype: int

    >>> bag('cat', 'hat')
    1
    >>> bag('Niall', 'Neil')
    2
    >>> bag('aluminum', 'Catalan')
    5
    >>> bag('ATCG', 'TAGC')
    0
    >>> bag('abcdefg', 'hijklm')
    7
    >>> bag('abcdefg', 'hijklmno')
    8
    """
    return Bag().dist_abs(src, tar)


def dist_bag(src, tar):
    """Return the normalized bag distance between two strings.

    Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: normalized bag distance
    :rtype: float

    >>> dist_bag('cat', 'hat')
    0.3333333333333333
    >>> dist_bag('Niall', 'Neil')
    0.4
    >>> dist_bag('aluminum', 'Catalan')
    0.625
    >>> dist_bag('ATCG', 'TAGC')
    0.0
    """
    return Bag().dist(src, tar)


def sim_bag(src, tar):
    """Return the normalized bag similarity of two strings.

    Normalized bag similarity is the complement of normalized bag distance:
    :math:`sim_{bag} = 1 - dist_{bag}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: normalized bag similarity
    :rtype: float

    >>> round(sim_bag('cat', 'hat'), 12)
    0.666666666667
    >>> sim_bag('Niall', 'Neil')
    0.6
    >>> sim_bag('aluminum', 'Catalan')
    0.375
    >>> sim_bag('ATCG', 'TAGC')
    1.0
    """
    return Bag().sim(src, tar)


class MongeElkan(Distance):
    """Monge-Elkan similarity.

    Monge-Elkan is defined in :cite:`Monge:1996`.

    Note: Monge-Elkan is NOT a symmetric similarity algorithm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the symmetric argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).
    """

    def sim(self, src, tar, sim_func=sim_levenshtein, symmetric=False):
        """Return the Monge-Elkan similarity of two strings.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :param function sim_func: the internal similarity metric to employ
        :param bool symmetric: return a symmetric similarity measure
        :returns: Monge-Elkan similarity
        :rtype: float

        >>> cmp = MongeElkan()
        >>> cmp.sim('cat', 'hat')
        0.75
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.666666666667
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.388888888889
        >>> cmp.sim('ATCG', 'TAGC')
        0.5
        """
        if src == tar:
            return 1.0

        q_src = sorted(QGrams(src).elements())
        q_tar = sorted(QGrams(tar).elements())

        if not q_src or not q_tar:
            return 0.0

        sum_of_maxes = 0
        for q_s in q_src:
            max_sim = float('-inf')
            for q_t in q_tar:
                max_sim = max(max_sim, sim_func(q_s, q_t))
            sum_of_maxes += max_sim
        sim_em = sum_of_maxes / len(q_src)

        if symmetric:
            sim_em = (sim_em + self.sim(tar, src, sim_func, False)) / 2

        return sim_em


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan similarity of two strings.

    This is a wrapper for :py:meth:`MongeElkan.sim`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function sim_func: the internal similarity metric to employ
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan similarity
    :rtype: float

    >>> sim_monge_elkan('cat', 'hat')
    0.75
    >>> round(sim_monge_elkan('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_monge_elkan('aluminum', 'Catalan'), 12)
    0.388888888889
    >>> sim_monge_elkan('ATCG', 'TAGC')
    0.5
    """
    return MongeElkan().sim(src, tar, sim_func, symmetric)


def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan distance between two strings.

    This is a wrapper for :py:meth:`MongeElkan.dist`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function sim_func: the internal similarity metric to employ
    :param bool symmetric: return a symmetric similarity measure
    :returns: Monge-Elkan distance
    :rtype: float

    >>> dist_monge_elkan('cat', 'hat')
    0.25
    >>> round(dist_monge_elkan('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_monge_elkan('aluminum', 'Catalan'), 12)
    0.611111111111
    >>> dist_monge_elkan('ATCG', 'TAGC')
    0.5
    """
    return MongeElkan().dist(src, tar, sim_func, symmetric)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
