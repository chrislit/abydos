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
    - Jaccard similarity coefficient & distance
    - overlap similarity & distance
    - Tanimoto coefficient & distance
    - cosine similarity & distance
    - Bag similarity & distance
    - Monge-Elkan similarity & distance
"""

from __future__ import division, unicode_literals

from collections import Counter
from math import log, sqrt

from ._levenshtein import sim_levenshtein
from ._util import _get_qgrams
from ..tokenizer import QGrams

__all__ = [
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
    'sim_tanimoto',
    'sim_tversky',
    'tanimoto',
]


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    r"""Return the Tversky index of two strings.

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
    if alpha < 0 or beta < 0:
        raise ValueError(
            'Unsupported weight assignment; alpha and beta '
            + 'must be greater than or equal to 0.'
        )

    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
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

    a_val = min(q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag)
    b_val = max(q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag)
    c_val = q_intersection_mag + bias
    return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky distance between two strings.

    Tversky distance is the complement of the Tvesrsky index (similarity):
    :math:`dist_{Tversky} = 1-sim_{Tversky}`.

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
    return 1 - sim_tversky(src, tar, qval, alpha, beta, bias)


def sim_dice(src, tar, qval=2):
    r"""Return the Sørensen–Dice coefficient of two strings.

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948` is
    :math:`sim_{dice}(X, Y) = \\frac{2 \\cdot |X \\cap Y|}{|X| + |Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 0.5`.

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
    return sim_tversky(src, tar, qval, 0.5, 0.5)


def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance between two strings.

    Sørensen–Dice distance is the complemenjt of the Sørensen–Dice coefficient:
    :math:`dist_{dice} = 1 - sim_{dice}`.

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
    return 1 - sim_dice(src, tar, qval)


def sim_jaccard(src, tar, qval=2):
    r"""Return the Jaccard similarity of two strings.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901` is :math:`sim_{jaccard}(X, Y) =
    \\frac{|X \\cap Y|}{|X \\cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 1`.

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
    return sim_tversky(src, tar, qval, 1, 1)


def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance between two strings.

    Jaccard distance is the complement of the Jaccard similarity coefficient:
    :math:`dist_{Jaccard} = 1 - sim_{Jaccard}`.

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
    return 1 - sim_jaccard(src, tar, qval)


def sim_overlap(src, tar, qval=2):
    r"""Return the overlap coefficient of two strings.

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient, is
    :math:`sim_{overlap}(X, Y) = \\frac{|X \\cap Y|}{min(|X|, |Y|)}`.

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
    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / min(q_src_mag, q_tar_mag)


def dist_overlap(src, tar, qval=2):
    """Return the overlap distance between two strings.

    Overlap distance is the complement of the overlap coefficient:
    :math:`sim_{overlap} = 1 - dist_{overlap}`.

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
    return 1 - sim_overlap(src, tar, qval)


def sim_tanimoto(src, tar, qval=2):
    r"""Return the Tanimoto similarity of two strings.

    For two sets X and Y, the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` is
    :math:`sim_{Tanimoto}(X, Y) = \\frac{|X \\cap Y|}{|X \\cup Y|}`.

    This is identical to the Jaccard similarity coefficient
    :cite:`Jaccard:1901` and the Tversky index :cite:`Tversky:1977` for
    :math:`\\alpha = \\beta = 1`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :returns: Tanimoto similarity
    :rtype: float

    >>> sim_tanimoto('cat', 'hat')
    0.3333333333333333
    >>> sim_tanimoto('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tanimoto('aluminum', 'Catalan')
    0.0625
    >>> sim_tanimoto('ATCG', 'TAGC')
    0.0
    """
    return sim_jaccard(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Return the Tanimoto distance between two strings.

    Tanimoto distance is :math:`-log_{2}sim_{Tanimoto}`.

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
    coeff = sim_jaccard(src, tar, qval)
    if coeff != 0:
        return log(coeff, 2)

    return float('-inf')


def sim_cosine(src, tar, qval=2):
    r"""Return the cosine similarity of two strings.

    For two sets X and Y, the cosine similarity, Otsuka-Ochiai coefficient, or
    Ochiai coefficient :cite:`Otsuka:1936,Ochiai:1957` is:
    :math:`sim_{cosine}(X, Y) = \\frac{|X \\cap Y|}{\\sqrt{|X| \\cdot |Y|}}`.

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
    if src == tar:
        return 1.0
    if not src or not tar:
        return 0.0

    q_src, q_tar = _get_qgrams(src, tar, qval)
    q_src_mag = sum(q_src.values())
    q_tar_mag = sum(q_tar.values())
    q_intersection_mag = sum((q_src & q_tar).values())

    return q_intersection_mag / sqrt(q_src_mag * q_tar_mag)


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
    return 1 - sim_cosine(src, tar, qval)


def bag(src, tar):
    """Return the bag distance between two strings.

    Bag distance is proposed in :cite:`Bartolini:2002`. It is defined as:
    :math:`max(|multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)|)`.

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
    if tar == src:
        return 0
    elif not src:
        return len(tar)
    elif not tar:
        return len(src)

    src_bag = Counter(src)
    tar_bag = Counter(tar)
    return max(
        sum((src_bag - tar_bag).values()), sum((tar_bag - src_bag).values())
    )


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
    if tar == src:
        return 0.0
    if not src or not tar:
        return 1.0

    max_length = max(len(src), len(tar))

    return bag(src, tar) / max_length


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
    return 1 - dist_bag(src, tar)


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan similarity of two strings.

    Monge-Elkan is defined in :cite:`Monge:1996`.

    Note: Monge-Elkan is NOT a symmetric similarity algorithm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the symmetric argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).

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
        sim_em = (sim_em + sim_monge_elkan(tar, src, sim_func, False)) / 2

    return sim_em


def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan distance between two strings.

    Monge-Elkan distance is the complement of Monge-Elkan similarity:
    :math:`dist_{Monge-Elkan} = 1 - sim_{Monge-Elkan}`.

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
    return 1 - sim_monge_elkan(src, tar, sim_func, symmetric)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
