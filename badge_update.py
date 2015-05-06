#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re

if not os.path.isfile('./pylint.log'):
    exit('Please direct pylint output to pylint.log')
if not os.path.isfile('./README.rst'):
    exit('README.rst file missing.')

pylint_text = open('pylint.log', 'r', encoding='utf-8').read()
pylint_score = re.search('Your code has been rated at ([0-9\.]+)',
                         pylint_text).group(1)

readme_text = open('README.rst', 'r', encoding='utf-8').read()
prefix = 'https://img.shields.io/badge/pylint-'
readme_text = re.sub(prefix+'([0-9\.]+)',
                     prefix+pylint_score, readme_text, 1)
with open('README.rst', 'w', encoding='utf-8') as f:
    f.write(readme_text)
