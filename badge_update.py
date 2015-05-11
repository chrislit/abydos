#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re

ordered_badge_colors = ('brightgreen', 'green', 'yellowgreen', 'yellow',
                        'orange', 'red')

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
readme_text = re.sub(prefix+'([0-9\.]+)',
                     prefix+str(pylint_score), readme_text, 1)
prefix = 'https://img.shields.io/badge/PEP8-'
readme_text = re.sub(prefix+'([0-9\.]+)',
                     prefix+str(pep8_score), readme_text, 1)
with open('README.rst', 'w', encoding='utf-8') as f:
    f.write(readme_text)
