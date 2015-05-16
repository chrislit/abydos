# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
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

"""abydos._compat.py

The _compat module defines some variables to enable Python 2 and Python 3
compatibility within a single codebase

The following are defined:
    _range   -- use in place of xrange/range
    _unicode -- use in place of unicode/str
    _unichr  -- use in place of unichr/chr
    _long    -- use in place of long/int
And:
    numeric_type -- defines the set of numeric types
"""

import sys

# pylint: disable=invalid-name
if sys.version_info[0] == 3:  # pragma: no cover
    _range = range
    _unicode = str
    _unichr = chr
    _long = int
    numeric_type = (int, float, complex)
else:  # pragma: no cover
    _range = xrange
    _unicode = unicode
    _unichr = unichr
    _long = long
    numeric_type = (int, long, float, complex)
