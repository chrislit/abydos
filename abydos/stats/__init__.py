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
"""

from __future__ import division, unicode_literals

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
