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

"""abydos.stats._pairwise.

The stats._pairwise module implements pairwise statistical algorithms.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._mean import amean, hmean, std
from ..distance import sim

__all__ = ['mean_pairwise_similarity', 'pairwise_similarity_statistics']


def mean_pairwise_similarity(
    collection, metric=sim, mean_func=hmean, symmetric=False
):
    """Calculate the mean pairwise similarity of a collection of strings.

    Takes the mean of the pairwise similarity between each member of a
    collection, optionally in both directions (for asymmetric similarity
    metrics.

    Parameters
    ----------
    collection : list
        A collection of terms or a string that can be split
    metric : function
        A similarity metric function
    mean_func : function
        A mean function that takes a list of values and returns a float
    symmetric : bool
        Set to True if all pairwise similarities should be calculated in both
        directions

    Returns
    -------
    float
        The mean pairwise similarity of a collection of strings

    Raises
    ------
    ValueError
        mean_func must be a function
    ValueError
        metric must be a function
    ValueError
        collection is neither a string nor iterable type
    ValueError
        collection has fewer than two members

    Examples
    --------
    >>> round(mean_pairwise_similarity(['Christopher', 'Kristof',
    ... 'Christobal']), 12)
    0.519801980198
    >>> round(mean_pairwise_similarity(['Niall', 'Neal', 'Neil']), 12)
    0.545454545455

    """
    if not callable(mean_func):
        raise ValueError('mean_func must be a function')
    if not callable(metric):
        raise ValueError('metric must be a function')

    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    collection = list(collection)

    pairwise_values = []

    for i in range(len(collection)):
        for j in range(i + 1, len(collection)):
            pairwise_values.append(metric(collection[i], collection[j]))
            if symmetric:
                pairwise_values.append(metric(collection[j], collection[i]))

    return mean_func(pairwise_values)


def pairwise_similarity_statistics(
    src_collection,
    tar_collection,
    metric=sim,
    mean_func=amean,
    symmetric=False,
):
    """Calculate the pairwise similarity statistics a collection of strings.

    Calculate pairwise similarities among members of two collections,
    returning the maximum, minimum, mean (according to a supplied function,
    arithmetic mean, by default), and (population) standard deviation
    of those similarities.

    Parameters
    ----------
    src_collection : list
        A collection of terms or a string that can be split
    tar_collection : list
        A collection of terms or a string that can be split
    metric : function
        A similarity metric function
    mean_func : function
        A mean function that takes a list of values and returns a float
    symmetric : bool
        Set to True if all pairwise similarities should be calculated in both
        directions

    Returns
    -------
    tuple
        The max, min, mean, and standard deviation of similarities

    Raises
    ------
    ValueError
        mean_func must be a function
    ValueError
        metric must be a function
    ValueError
        src_collection is neither a string nor iterable
    ValueError
        tar_collection is neither a string nor iterable

    Example
    -------
    >>> tuple(round(_, 12) for _ in pairwise_similarity_statistics(
    ... ['Christopher', 'Kristof', 'Christobal'], ['Niall', 'Neal', 'Neil']))
    (0.2, 0.0, 0.118614718615, 0.075070477184)

    """
    if not callable(mean_func):
        raise ValueError('mean_func must be a function')
    if not callable(metric):
        raise ValueError('metric must be a function')

    if hasattr(src_collection, 'split'):
        src_collection = src_collection.split()
    if not hasattr(src_collection, '__iter__'):
        raise ValueError('src_collection is neither a string nor iterable')

    if hasattr(tar_collection, 'split'):
        tar_collection = tar_collection.split()
    if not hasattr(tar_collection, '__iter__'):
        raise ValueError('tar_collection is neither a string nor iterable')

    src_collection = list(src_collection)
    tar_collection = list(tar_collection)

    pairwise_values = []

    for src in src_collection:
        for tar in tar_collection:
            pairwise_values.append(metric(src, tar))
            if symmetric:
                pairwise_values.append(metric(tar, src))

    return (
        max(pairwise_values),
        min(pairwise_values),
        mean_func(pairwise_values),
        std(pairwise_values, mean_func, 0),
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
