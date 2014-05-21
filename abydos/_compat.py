# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] == 3:
    _range = range
    _unicode = str
else:
    _range = xrange
    _unicode = unicode
