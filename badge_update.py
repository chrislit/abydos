#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re

badge_colors = ('brightgreen', 'green', 'yellowgreen', 'yellow',
                'orange', 'red')


def pylint_color(score):
    # These are the score cutoffs for each color above.
    # I.e. score==10 -> brightgreen, down to 7.5 > score >= 5 -> orange
    score_cutoffs = (10, 9.5, 8.5, 7.5, 5)
    for i in range(len(score_cutoffs)):
        if score >= score_cutoffs[i]:
            return badge_colors[i]
    # and score < 5 -> red
    return badge_colors[-1]


def pep8_color(score):
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
pylint_score = float(re.search('Your code has been rated at ([0-9\.]+)',
                               pylint_text).group(1))

if not os.path.isfile('./pep8.log'):
    exit('Please direct PEP8 output to pep8.log')
pep8_text = open('pep8.log', 'r', encoding='utf-8').read()
pep8_score = sum([int(n) for n in re.findall('\n([0-9]+)  +', pep8_text)])

readme_text = open('README.rst', 'r', encoding='utf-8').read()
prefix = 'https://img.shields.io/badge/Pylint-'
readme_text = re.sub(prefix + '([0-9\.]+/10\-[a-z]+)',
                     prefix + str(pylint_score) + '/10-' +
                     pylint_color(pylint_score),
                     readme_text, 1)
prefix = 'https://img.shields.io/badge/PEP8-'
readme_text = re.sub(prefix + '([0-9\.]+-[a-z]+)',
                     prefix + str(pep8_score) + '-' +
                     pep8_color(pep8_score),
                     readme_text, 1)
with open('README.rst', 'w', encoding='utf-8') as f:
    f.write(readme_text)
