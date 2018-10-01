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

"""abydos.

Abydos NLP/IR library by Christopher C. Little
"""

from .clustering import *   # noqa: F403
from .compression import *  # noqa: F403
from .corpus import *       # noqa: F403
from .distance import *     # noqa: F403
from .fingerprint import *  # noqa: F403
from .ngram import *        # noqa: F403
from .phones import *       # noqa: F403
from .phonetic import *     # noqa: F403
from .qgram import *        # noqa: F403
from .stats import *        # noqa: F403
from .stemmer import *      # noqa: F403

__all__ = ['clustering', 'compression', 'corpus', 'distance', 'fingerprint',
           'ngram', 'phones', 'phonetic', 'qgram', 'stats', 'stemmer']
