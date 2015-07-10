# -*- coding: utf-8 -*-

# Copyright 2015 by Christopher C. Little.
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

"""abydos.lm

The lm module implements language model classes, including:

    - maximum likelihood estimated
    - additive (Laplacian) smoothed
    - Good-Turing estimated
    - Jelinek-Mercer smoothed
    - Katz smoothed
    - Witten-Bell smoothed
    - absolute discounted
    - Kneser-Ney smoothed
    - Church-Gale smoothed
    - Modified Kneser-Ney smoothed

"""