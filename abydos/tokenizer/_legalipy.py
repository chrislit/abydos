# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tokenizer._legalipy.

LegaliPy tokenizer class
"""

from ._tokenizer import _Tokenizer

try:
    from syllabipy.legalipy import LegaliPy
    from syllabipy.legalipy import getOnsets as gen_onsets  # noqa: N813
except ImportError:  # pragma: no cover
    # If the system lacks the SyllabiPy library, that's fine, but SyllabiPy
    # tokenization won't be supported.
    gen_onsets = None
    LegaliPy = None


class LegaliPyTokenizer(_Tokenizer):
    """LegaliPy tokenizer.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None):
        """Initialize Tokenizer.

        Parameters
        ----------
        scaler : None, str, or function
            A scaling function for the Counter:

                - None : no scaling
                - 'set' : All non-zero values are set to 1.
                - 'length' : Each token has weight equal to its length.
                - 'length-log' : Each token has weight equal to the log of its
                   length + 1.
                - 'length-exp' : Each token has weight equal to e raised to its
                   length.
                - a callable function : The function is applied to each value
                  in the Counter. Some useful functions include math.exp,
                  math.log1p, math.sqrt, and indexes into interesting integer
                  sequences such as the Fibonacci sequence.


        .. versionadded:: 0.4.0

        """
        if LegaliPy is None:
            raise TypeError(  # pragma: no cover
                'LegaliPy tokenizer requires installation of SyllabiPy'
                + ' package.'
            )

        super(LegaliPyTokenizer, self).__init__(scaler)

        self._onsets = ['']

    def train_onsets(self, text, threshold=0.0002, clean=True, append=False):
        """Train the onsets on a text.

        Parameters
        ----------
        text : str
            The text on which to train
        threshold : float
            Threshold proportion above which to include onset into onset list
        clean : bool
            If True, the text is stripped of numerals and punctuation
        append : bool
            If True, the current onset list is extended


        .. versionadded:: 0.4.0

        """
        new_onsets = gen_onsets(text, threshold, clean)
        if append:
            self._onsets = list(set(self._onsets + new_onsets))
        else:
            self._onsets = new_onsets

    def tokenize(self, string, ipa=False):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Parameters
        ----------
        string : str
            The string to tokenize
        ipa : bool
            If True, indicates that the string is in IPA

        Examples
        --------
        >>> LegaliPyTokenizer().tokenize('seven-twelfths')
        LegaliPyTokenizer({'s': 1, 'ev': 1, 'en-tw': 1, 'elfths': 1})

        >>> LegaliPyTokenizer().tokenize('character')
        LegaliPyTokenizer({'ch': 1, 'ar': 1, 'act': 1, 'er': 1})

        .. versionadded:: 0.4.0

        """
        self._string = string

        self._ordered_tokens = []
        for word in string.split():
            self._ordered_tokens += LegaliPy(word, self._onsets)
        if not self._ordered_tokens:
            self._ordered_tokens = [self._string]

        super(LegaliPyTokenizer, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod()
