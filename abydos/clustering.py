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

"""abydos.clustering.

The clustering module implements clustering algorithms such as:
    - mean pair-wise similarity
"""

from __future__ import division, unicode_literals

from six.moves import range

from .distance import sim
from .stats import hmean


def mean_pairwise_similarity(collection, metric=sim,
                             meanfunc=hmean, symmetric=False):
    """Calculate the mean pairwise similarity of a collection of strings.

    Takes the mean of the pairwise similarity between each member of a
    collection, optionally in both directions (for asymmetric similarity
    metrics.

    :param list collection: a collection of terms or a string that can be split
    :param function metric: a similarity metric function
    :param function mean: a mean function that takes a list of values and
        returns a float
    :param bool symmetric: set to True if all pairwise similarities should be
        calculated in both directions
    :returns: the mean pairwise similarity of a collection of strings
    :rtype: str

    >>> mean_pairwise_similarity(['Christopher', 'Kristof', 'Christobal'])
    0.51980198019801982
    >>> mean_pairwise_similarity(['Niall', 'Neal', 'Neil'])
    0.54545454545454541
    """
    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    collection = list(collection)

    pairwise_values = []

    for i in range(len(collection)):
        for j in range(i+1, len(collection)):
            pairwise_values.append(metric(collection[i], collection[j]))
            if symmetric:
                pairwise_values.append(metric(collection[j], collection[i]))

    if not callable(meanfunc):
        raise ValueError('meanfunc must be a function')
    return meanfunc(pairwise_values)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
