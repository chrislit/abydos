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

"""abydos.phones.

The phones module implements phonetic feature coding, decoding, and comparison
functions. It has three functions:

    - :py:func:`.ipa_to_features` takes a string of IPA symbols and returns
      list of integers that represent the phonetic features bundled in the
      phone that the symbols represents.
    - :py:func:`.get_feature` takes a list of feature bundles produced by
      :py:func:`.ipa_to_features` and a feature name and returns a list
      representing whether that feature is present in each component of the
      list.
    - :py:func:`.cmp_features` takes two phonetic feature bundles, such as the
      components of the lists returned by :py:func:`.ipa_to_features`, and
      returns a measure of their similarity.


An example using these functions on two different pronunciations of the word
'international':

>>> int1 = 'ɪntənæʃənəɫ'
>>> int2 = 'ɪnɾənæʃɨnəɫ'
>>> feat1 = ipa_to_features(int1)
>>> feat1
[1826957413067434410,
 2711173160463936106,
 2783230754502126250,
 1828083331160779178,
 2711173160463936106,
 1826957425885227434,
 2783231556184615322,
 1828083331160779178,
 2711173160463936106,
 1828083331160779178,
 2693158721554917798]
>>> feat2 = ipa_to_features(int2)
>>> feat2
[1826957413067434410,
 2711173160463936106,
 2711173160463935914,
 1828083331160779178,
 2711173160463936106,
 1826957425885227434,
 2783231556184615322,
 1826957414069873066,
 2711173160463936106,
 1828083331160779178,
 2693158721554917798]
>>> get_feature(feat1, 'consonantal')
[-1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
>>> get_feature(feat1, 'nasal')
[-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]
>>> [cmp_features(f1, f2) for f1, f2 in zip(feat1, feat2)]
[1.0,
 1.0,
 0.9032258064516129,
 1.0,
 1.0,
 1.0,
 1.0,
 0.9193548387096774,
 1.0,
 1.0,
 1.0]
>>> sum(cmp_features(f1, f2) for f1, f2 in zip(feat1, feat2))/len(feat1)
0.9838709677419355

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._phones import cmp_features, get_feature, ipa_to_features

__all__ = ['ipa_to_features', 'get_feature', 'cmp_features']


if __name__ == '__main__':
    import doctest

    doctest.testmod()
