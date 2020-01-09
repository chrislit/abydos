# Copyright 2014-2020 by Christopher C. Little.
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

r"""abydos.tokenizer.

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

    - :py:class:`.QSkipgrams` tokenizes a string into skipgrams of length q. A
      skipgram is a sequence of letters from a string with q, often
      discontinuous, characters. For example, the string 'ABCD' has the
      following 2-skipgrams: 'AB', 'AC', 'AD', 'BC', 'BD', 'CD'.

    - :py:class:`.CharacterTokenizer` tokenizes a string into individual
      characters.

    - :py:class:`.RegexpTokenizer` tokenizes a string according to a supplied
      regular expression.

    - :py:class:`.WhitespaceTokenizer` tokenizes a string by dividing it at
      instances of whitespace.

    - :py:class:`.WordpunctTokenizer` tokenizes a string by dividing it into
      strings of letters and strings of punctuation.

Six syllable-oriented tokenizers are provided:

    - :py:class:`.COrVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants, vowels, or other characters:

    - :py:class:`.COrVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants (C* clusters), vowels (V* clusters, or non-letter
      characters:

    - :py:class:`.CVClusterTokenizer` tokenizes a string by dividing it into
      strings of consonants then vowels (C*V* clusters) or non-letter
      characters:

    - :py:class:`.VCClusterTokenizer` tokenizes a string by dividing it into
      strings of vowels then characters (V*C* clusters) or non-letter
      characters:

    - :py:class:`.SAPSTokenizer` tokenizes a string according to the rules
      specified by the SAPS syllabification algorithm :cite:`Ruibin:2005`:

    - :py:class:`.SonoriPyTokenizer` does syllabification according to the
      sonority sequencing principle, using SyllabiPy. It requires that
      SyllabiPy_ be installed.

    - :py:class:`.LegaliPyTokenizer` does syllabification according to the
      onset maximization principle (principle of legality), using SyllabiPy.
      It requires that SyllabiPy_ be installed, and works best if it has been
      trained on a corpus of text.

Finally, an NLTK tokenizer is provided:

    - :py:class:`.NLTKTokenizer` does tokenization using an instantiated NLTK
      tokenizer. Accordingly, NLTK_ needs to be installed.

.. _SyllabiPy: https://pypi.org/project/syllabipy/
.. _NLTK: https://www.nltk.org/


----

"""

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
