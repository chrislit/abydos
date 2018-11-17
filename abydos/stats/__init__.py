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

r"""abydos.stats.

The stats module defines functions for calculating various statistical data
about linguistic objects.

A :py:class:`ConfusionTable` class if provided.

Functions are provided for calculating the following means:

    - arithmetic (:py:func:`amean`)
    - geometric (:py:func:`gmean`)
    - harmonic (:py:func:`hmean`)
    - quadratic (:py:func:`qmean`)
    - contraharmonic (:py:func:`cmean`)
    - logarithmic (:py:func:`lmean`)
    - identric (exponential) (:py:func:`imean`)
    - Seiffert's (:py:func:`seiffert_mean`)
    - Lehmer (:py:func:`lehmer_mean`)
    - Heronian (:py:func:`heronian_mean`)
    - Hölder (power/generalized) (:py:func:`hoelder_mean`)
    - arithmetic-geometric (:py:func:`agmean`)
    - geometric-harmonic (:py:func:`ghmean`)
    - arithmetic-geometric-harmonic (:py:func:`aghmean`)

And for calculating:

    - midrange (:py:func:`midrange`)
    - median (:py:func:`median`)
    - mode (:py:func:`mode`)
    - variance (:py:func:`var`)
    - standard deviation (:py:func:`std`)

And for the pairwise statistical algorithms:

    - mean pairwise similarity (:py:func:`mean_pairwise_similarity`)
    - pairwise similarity statistics
      (:py:func:`pairwise_similarity_statistics`)

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._confusion_table import ConfusionTable
from ._mean import (
    aghmean,
    agmean,
    amean,
    cmean,
    ghmean,
    gmean,
    heronian_mean,
    hmean,
    hoelder_mean,
    imean,
    lehmer_mean,
    lmean,
    median,
    midrange,
    mode,
    qmean,
    seiffert_mean,
    std,
    var,
)
from ._pairwise import mean_pairwise_similarity, pairwise_similarity_statistics

__all__ = [
    'ConfusionTable',
    'amean',
    'gmean',
    'hmean',
    'agmean',
    'ghmean',
    'aghmean',
    'cmean',
    'imean',
    'lmean',
    'qmean',
    'heronian_mean',
    'hoelder_mean',
    'lehmer_mean',
    'seiffert_mean',
    'median',
    'midrange',
    'mode',
    'std',
    'var',
    'mean_pairwise_similarity',
    'pairwise_similarity_statistics',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
