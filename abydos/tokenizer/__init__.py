# -*- coding: utf-8 -*-

# Copyright 2014-2019 by Christopher C. Little.
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

"""abydos.tokenizer.

The tokenizer package collects classes whose purpose is to tokenize
text or individual words. Each tokenizer also supports a scaler attribute when
constructed, which adjusts count scaling. The scaler defaults to None,
which performs no scaling. Setting scaler to 'set' is used to convert token
counters from multi-sets to sets, so even if multiple instances of a token are
present, they will be counted as one. Additionally, a callable function (of one
argument, such as log, exp, or lambda x: x + 1) may be passed to scaler and
this function will be applied to each count value.

The following general tokenizers are provided:

    - :py:class:`.QGrams` tokenizes a string into q-grams, substrings of length
      q. The class supports different values of q, the addition of start and
      stop symbols, and skip values. It even supports multiple values for q and
      skip, using lists or ranges.

>>> QGrams(qval=2, start_stop='$#').tokenize('interning')
QGrams({'in': 2, '$i': 1, 'nt': 1, 'te': 1, 'er': 1, 'rn': 1, 'ni': 1, 'ng': 1,
 'g#': 1})

>>> QGrams(start_stop='', skip=1).tokenize('AACTAGAAC')
QGrams({'AC': 2, 'AT': 1, 'CA': 1, 'TG': 1, 'AA': 1, 'GA': 1, 'A': 1})

>>> QGrams(start_stop='', skip=[0, 1]).tokenize('AACTAGAAC')
QGrams({'AC': 4, 'AA': 3, 'GA': 2, 'CT': 1, 'TA': 1, 'AG': 1, 'AT': 1, 'CA': 1,
 'TG': 1, 'A': 1})

>>> QGrams(qval=range(3), skip=[0, 1]).tokenize('interdisciplinarian')
QGrams({'i': 10, 'n': 7, 'r': 4, 'a': 4, 'in': 3, 't': 2, 'e': 2, 'd': 2,
 's': 2, 'c': 2, 'p': 2, 'l': 2, 'ri': 2, 'ia': 2, '$i': 1, 'nt': 1, 'te': 1,
 'er': 1, 'rd': 1, 'di': 1, 'is': 1, 'sc': 1, 'ci': 1, 'ip': 1, 'pl': 1,
 'li': 1, 'na': 1, 'ar': 1, 'an': 1, 'n#': 1, '$n': 1, 'it': 1, 'ne': 1,
 'tr': 1, 'ed': 1, 'ds': 1, 'ic': 1, 'si': 1, 'cp': 1, 'il': 1, 'pi': 1,
 'ln': 1, 'nr': 1, 'ai': 1, 'ra': 1, 'a#': 1})

    - :py:class:`.QSkipgrams` tokenizes a string into skipgrams of length q. A
      skipgram is a sequence of letters from a string with q, often
      discontinuous, characters. For example, the string 'ABCD' has the
      following 2-skipgrams: 'AB', 'AC', 'AD', 'BC', 'BD', 'CD'.

>>> QSkipgrams(start_stop='').tokenize('ABCD')
QSkipgrams({'AB': 1, 'AC': 1, 'AD': 1, 'BC': 1, 'BD': 1, 'CD': 1})

>>> QSkipgrams().tokenize('Colin')
QSkipgrams({'$C': 1, '$o': 1, '$l': 1, '$i': 1, '$n': 1, '$#': 1, 'Co': 1,
 'Cl': 1, 'Ci': 1, 'Cn': 1, 'C#': 1, 'ol': 1, 'oi': 1, 'on': 1, 'o#': 1,
 'li': 1, 'ln': 1, 'l#': 1, 'in': 1, 'i#': 1, 'n#': 1})

>>> QSkipgrams(qval=3).tokenize('AACTAGAAC')
QSkipgrams({'$AA': 20, '$A#': 20, 'AA#': 20, '$AC': 14, 'AC#': 14, 'AAC': 11,
 'AAA': 10, '$C#': 8, '$AG': 6, '$CA': 6, '$TA': 6, 'ACA': 6, 'ATA': 6,
 'AGA': 6, 'AG#': 6, 'CA#': 6, 'TA#': 6, '$$A': 5, 'A##': 5, '$AT': 4,
 '$T#': 4, '$GA': 4, '$G#': 4, 'AT#': 4, 'GA#': 4, 'AAG': 3, 'AGC': 3,
 'CTA': 3, 'CAA': 3, 'CAC': 3, 'TAA': 3, 'TAC': 3, '$$C': 2, '$$#': 2,
 '$CT': 2, '$CG': 2, '$CC': 2, '$TG': 2, '$TC': 2, '$GC': 2, '$##': 2,
 'ACT': 2, 'ACG': 2, 'ACC': 2, 'ATG': 2, 'ATC': 2, 'CT#': 2, 'CGA': 2,
 'CG#': 2, 'CC#': 2, 'C##': 2, 'TGA': 2, 'TG#': 2, 'TC#': 2, 'GAC': 2,
 'GC#': 2, '$$T': 1, '$$G': 1, 'AAT': 1, 'CTG': 1, 'CTC': 1, 'CAG': 1,
 'CGC': 1, 'TAG': 1, 'TGC': 1, 'T##': 1, 'GAA': 1, 'G##': 1})

    QSkipgrams may also be used to produce weights in accordance with the
    substring kernel rules of :cite:`Lodhi:2002` by passing the scaler value
    ``SSK``:

>>> QSkipgrams(scaler='SSK').tokenize('AACTAGAAC')
QSkipgrams({'AA': 6.170192010000001, 'AC': 4.486377699,
'$A': 2.8883286990000006, 'A#': 2.6526399291000002, 'TA': 2.05659,
'AG': 1.931931, 'CA': 1.850931, 'GA': 1.5390000000000001, 'AT': 1.3851,
'C#': 1.2404672100000003, '$C': 1.0047784401000002, 'CT': 0.81,
'TG': 0.7290000000000001, 'CG': 0.6561, 'GC': 0.6561, '$T': 0.5904900000000001,
'G#': 0.5904900000000001, 'TC': 0.531441, '$G': 0.4782969000000001,
'CC': 0.4782969000000001, 'T#': 0.4782969000000001, '$#': 0.31381059609000006})

    - :py:class:`.CharacterTokenizer` tokenizes a string into individual
      characters.

>>> CharacterTokenizer().tokenize('AACTAGAAC')
CharacterTokenizer({'A': 5, 'C': 2, 'T': 1, 'G': 1})

    - :py:class:`.RegexpTokenizer` tokenizes a string according to a supplied
      regular expression.

>>> RegexpTokenizer(regexp=r'[^-]+').tokenize('AA-CT-AG-AA-CD')
RegexpTokenizer({'AA': 2, 'CT': 1, 'AG': 1, 'CD': 1})

    - :py:class:`.WhitespaceTokenizer` tokenizes a string by dividing it at
      instances of whitespace.

>>> WhitespaceTokenizer().tokenize('a b c f a c g e a b')
WhitespaceTokenizer({'a': 3, 'b': 2, 'c': 2, 'f': 1, 'g': 1, 'e': 1})

    - :py:class:`.WordpunctTokenizer` tokenizes a string by dividing it into
      strings of letters and strings of punctuation.

>>> WordpunctTokenizer().tokenize('Can\'t stop the feelin\'!')
WordpunctTokenizer({'Can': 1, "'": 1, 't': 1, 'stop': 1, 'the': 1, 'feelin': 1,
 "'!": 1})

Six syllable-oriented tokenizers are provided:

    - :py:class:`.COrVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants, vowels, or other characters:

>>> COrVClusterTokenizer().tokenize('seven-twelfths')
COrVClusterTokenizer({'e': 3, 's': 1, 'v': 1, 'n': 1, '-': 1, 'tw': 1,
 'lfths': 1})

>>> COrVClusterTokenizer().tokenize('character')
COrVClusterTokenizer({'a': 2, 'r': 2, 'ch': 1, 'ct': 1, 'e': 1})

    - :py:class:`.COrVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants (C* clusters), vowels (V* clusters, or non-letter
      characters:

>>> COrVClusterTokenizer().tokenize('seven-twelfths')
COrVClusterTokenizer({'e': 3, 's': 1, 'v': 1, 'n': 1, '-': 1, 'tw': 1,
 'lfths': 1})

>>> COrVClusterTokenizer().tokenize('character')
COrVClusterTokenizer({'a': 2, 'r': 2, 'ch': 1, 'ct': 1, 'e': 1})

    - :py:class:`.CVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants then vowels (C*V* clusters) or non-letter
      characters:

>>> CVClusterTokenizer().tokenize('seven-twelfths')
CVClusterTokenizer({'se': 1, 've': 1, 'n': 1, '-': 1, 'twe': 1, 'lfths': 1})

>>> CVClusterTokenizer().tokenize('character')
CVClusterTokenizer({'cha': 1, 'ra': 1, 'cte': 1, 'r': 1})

    - :py:class:`.VCClusterTokenizer` tokenizes a string by dividing it into
      strings of vowels then characters (V*C* clusters) or non-letter
      characters:

>>> VCClusterTokenizer().tokenize('seven-twelfths')
CVClusterTokenizer({'se': 1, 've': 1, 'n': 1, '-': 1, 'twe': 1, 'lfths': 1})

>>> VCClusterTokenizer().tokenize('character')
CVClusterTokenizer({'cha': 1, 'ra': 1, 'cte': 1, 'r': 1})

    - :py:class:`.SAPSTokenizer` tokenizes a string according to the rules
      specified by the SAPS syllabification algorithm :cite:`Ruibin:2005`:

>>> SAPSTokenizer().tokenize('seven-twelfths')
SAPSTokenizer({'t': 2, 'se': 1, 'ven': 1, '-': 1, 'wel': 1, 'f': 1, 'h': 1,
's': 1})

>>> SAPSTokenizer().tokenize('character')
SAPSTokenizer({'c': 1, 'ha': 1, 'rac': 1, 'ter': 1})

    - :py:class:`.SonoriPyTokenizer` does syllabification according to the
      sonority sequencing principle, using SyllabiPy. It requires that
      SyllabiPy_ be installed.

>>> SonoriPyTokenizer().tokenize('seven-twelfths')
SonoriPyTokenizer({'se': 1, 'ven-': 1, 'twelfths': 1})

>>> SonoriPyTokenizer().tokenize('character')
SonoriPyTokenizer({'cha': 1, 'rac': 1, 'ter': 1})

    - :py:class:`.LegaliPyTokenizer` does syllabification according to the
      onset maximization principle (principle of legality), using SyllabiPy.
      It requires that SyllabiPy_ be installed, and works best if it has been
      trained on a corpus of text.

>>> LegaliPyTokenizer().tokenize('seven-twelfths')
LegaliPyTokenizer({'s': 1, 'ev': 1, 'en-tw': 1, 'elfths': 1})

>>> LegaliPyTokenizer().tokenize('character')
LegaliPyTokenizer({'ch': 1, 'ar': 1, 'act': 1, 'er': 1})

.. _SyllabiPy: https://pypi.org/project/syllabipy/

Finally, an NLTK tokenizer is provided:

    - :py:class:`.NLTKTokenizer` does tokenization using an instantiated NLTK
      tokenizer. Accordingly, NLTK_ needs to be installed.

>>> from nltk.tokenize.casual import TweetTokenizer
>>> nltk_tok = TweetTokenizer()
>>> NLTKTokenizer(nltk_tokenizer=nltk_tok).tokenize('.@Twitter Today is #lit!')
NLTKTokenizer({'.': 1, '@Twitter': 1, 'Today': 1, 'is': 1, '#lit': 1, '!': 1})

.. _NLTK: https://www.nltk.org/


----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._c_or_v_cluster import COrVClusterTokenizer
from ._character import CharacterTokenizer
from ._cv_cluster import CVClusterTokenizer
from ._legalipy import LegaliPyTokenizer
from ._nltk import NLTKTokenizer
from ._q_grams import QGrams
from ._q_skipgrams import QSkipgrams
from ._regexp import RegexpTokenizer
from ._saps import SAPSTokenizer
from ._sonoripy import SonoriPyTokenizer
from ._tokenizer import _Tokenizer
from ._vc_cluster import VCClusterTokenizer
from ._whitespace import WhitespaceTokenizer
from ._wordpunct import WordpunctTokenizer

__all__ = [
    '_Tokenizer',
    'QGrams',
    'QSkipgrams',
    'CharacterTokenizer',
    'RegexpTokenizer',
    'WhitespaceTokenizer',
    'WordpunctTokenizer',
    'COrVClusterTokenizer',
    'CVClusterTokenizer',
    'VCClusterTokenizer',
    'SAPSTokenizer',
    'SonoriPyTokenizer',
    'LegaliPyTokenizer',
    'NLTKTokenizer',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
