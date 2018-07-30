#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2015-2018 by Christopher C. Little.
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

"""badge_update.py.

This updates the Pylint, pycodestyle, & flake8 badges in README.rst.
"""

import os.path
import re

badge_colors = ('brightgreen', 'green', 'yellowgreen', 'yellow',
                'orange', 'red')


def pylint_color(score):
    """Return Pylint badge color."""
    # These are the score cutoffs for each color above.
    # I.e. score==10 -> brightgreen, down to 7.5 > score >= 5 -> orange
    score_cutoffs = (10, 9.5, 8.5, 7.5, 5)
    for i in range(len(score_cutoffs)):
        if score >= score_cutoffs[i]:
            return badge_colors[i]
    # and score < 5 -> red
    return badge_colors[-1]


def pycodestyle_color(score):
    """Return pycodestyle badge color."""
    # These are the score cutoffs for each color above.
    # I.e. score==0 -> brightgreen, down to 100 < score <= 200 -> orange
    score_cutoffs = (0, 20, 50, 100, 200)
    for i in range(len(score_cutoffs)):
        if score <= score_cutoffs[i]:
            return badge_colors[i]
    # and score > 200 -> red
    return badge_colors[-1]


def flake8_color(score):
    """Return flake8 badge color."""
    # These are the score cutoffs for each color above.
    # I.e. score==0 -> brightgreen, down to 100 < score <= 200 -> orange
    score_cutoffs = (0, 20, 50, 100, 200)
    for i in range(len(score_cutoffs)):
        if score <= score_cutoffs[i]:
            return badge_colors[i]
    # and score > 200 -> red
    return badge_colors[-1]


if not os.path.isfile('./README.rst'):
    exit('README.rst file missing.')

if not os.path.isfile('./pylint.log'):
    exit('Please direct Pylint output to pylint.log')
pylint_text = open('pylint.log', 'r', encoding='utf-8').read()
pylint_score = max(float(re.search('Your code has been rated at (\-?[0-9\.]+)',
                                   pylint_text).group(1)), 0.0)

if not os.path.isfile('./pycodestyle.log'):
    exit('Please direct pycodestyle output to pycodestyle.log')
pycodestyle_text = open('pycodestyle.log', 'r', encoding='utf-8').read()
pycodestyle_score = sum(int(n) for n in re.findall('\n([0-9]+)  +',
                                                   pycodestyle_text))

if not os.path.isfile('./flake8.log'):
    exit('Please direct flake8 output to flake8.log')
flake8_score = int(open('flake8.log', 'r', encoding='utf-8').read()
                   .split()[-1])

readme_text = open('README.rst', 'r', encoding='utf-8').read()

prefix = 'https://img.shields.io/badge/Pylint-'
readme_text = re.sub(prefix + '(\-?[0-9\.]+/10\-[a-z]+)',
                     prefix + str(pylint_score) + '/10-' +
                     pylint_color(pylint_score),
                     readme_text, 1)

prefix = 'https://img.shields.io/badge/pycodestyle-'
readme_text = re.sub(prefix + '([0-9\.]+-[a-z]+)',
                     prefix + str(pycodestyle_score) + '-' +
                     pycodestyle_color(pycodestyle_score),
                     readme_text, 1)

prefix = 'https://img.shields.io/badge/flake8-'
readme_text = re.sub(prefix + '([0-9\.]+-[a-z]+)',
                     prefix + str(flake8_score) + '-' +
                     pycodestyle_color(flake8_score),
                     readme_text, 1)

with open('README.rst', 'w', encoding='utf-8') as f:
    f.write(readme_text)
