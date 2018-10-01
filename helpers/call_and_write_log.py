#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""call_and_write_log.py.

This helper script takes one argument, a call to pylint, pycodestyle,
or flake8. It captures stdout and writes it to a log file.

The reason for this script to exist is as a workaround for tox
not supporting writing to files, even though I want it to do that
to maintain logs & create badges.
"""
import sys
from subprocess import call  # noqa: S404

const_ret = None
if len(sys.argv) > 2:
    try:
        const_ret = int(sys.argv[2])
    except ValueError:
        pass

retval = 1
if len(sys.argv) > 1:
    args = sys.argv[1].split()
    if args[0] not in {'pylint', 'pycodestyle', 'flake8', 'doc8'}:
        sys.exit(const_ret if const_ret is not None else retval)
    with open(args[0]+'.log', 'w') as output:
        retval = call(args, stdout=output, shell=False)
    sys.exit(const_ret if const_ret is not None else retval)
