# -*- coding: utf-8 -*-
"""abydos._compat.py

The _compat module defines some variables to enable Python 2 and Python 3
compatability within a single codebase


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

import sys

if sys.version_info[0] == 3:
    _range = range
    _unicode = str
else:
    _range = xrange
    _unicode = unicode
