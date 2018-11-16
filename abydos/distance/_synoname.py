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

"""abydos.distance._synoname.

Synoname.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Iterable

from ._distance import _Distance
from ._levenshtein import levenshtein
from ._ratcliff_obershelp import sim_ratcliff_obershelp

# noinspection PyProtectedMember
from ..fingerprint._synoname import SynonameToolcode

__all__ = ['Synoname', 'synoname']


class Synoname(_Distance):
    """Synoname.

    Cf. :cite:`Getty:1991,Gross:1991`
    """

    _stc = SynonameToolcode()

    _test_dict = {
        val: 2 ** n
        for n, val in enumerate(
            (
                'exact',
                'omission',
                'substitution',
                'transposition',
                'punctuation',
                'initials',
                'extension',
                'inclusion',
                'no_first',
                'word_approx',
                'confusions',
                'char_approx',
            )
        )
    }
    _match_name = (
        '',
        'exact',
        'omission',
        'substitution',
        'transposition',
        'punctuation',
        'initials',
        'extension',
        'inclusion',
        'no_first',
        'word_approx',
        'confusions',
        'char_approx',
        'no_match',
    )
    _match_type_dict = {val: n for n, val in enumerate(_match_name)}

    def _synoname_strip_punct(self, word):
        """Return a word with punctuation stripped out.

        Parameters
        ----------
        word : str
            A word to strip punctuation from

        Returns
        -------
        str
            The word stripped of punctuation

        Examples
        --------
        >>> pe = Synoname()
        >>> pe._synoname_strip_punct('AB;CD EF-GH$IJ')
        'ABCD EFGHIJ'

        """
        stripped = ''
        for char in word:
            if char not in set(',-./:;"&\'()!{|}?$%*+<=>[\\]^_`~'):
                stripped += char
        return stripped.strip()

    def _synoname_word_approximation(
        self, src_ln, tar_ln, src_fn='', tar_fn='', features=None
    ):
        """Return the Synoname word approximation score for two names.

        Parameters
        ----------
        src_ln : str
            Last name of the source
        tar_ln : str
            Last name of the target
        src_fn : str
            First name of the source (optional)
        tar_fn : str
            First name of the target (optional)
        features : dict
            A dict containing special features calculated using
            :py:class:`fingerprint.SynonameToolcode` (optional)

        Returns
        -------
        float
            The word approximation score

        Examples
        --------
        >>> pe = Synoname()
        >>> pe._synoname_word_approximation('Smith Waterman', 'Waterman',
        ... 'Tom Joe Bob', 'Tom Joe')
        0.6

        """
        if features is None:
            features = {}
        if 'src_specials' not in features:
            features['src_specials'] = []
        if 'tar_specials' not in features:
            features['tar_specials'] = []

        src_len_specials = len(features['src_specials'])
        tar_len_specials = len(features['tar_specials'])

        # 1
        if ('gen_conflict' in features and features['gen_conflict']) or (
            'roman_conflict' in features and features['roman_conflict']
        ):
            return 0

        # 3 & 7
        full_tar1 = ' '.join((tar_ln, tar_fn)).replace('-', ' ').strip()
        for s_pos, s_type in features['tar_specials']:
            if s_type == 'a':
                full_tar1 = full_tar1[
                    : -(
                        1
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        )
                    )
                ]
            elif s_type == 'b':
                loc = (
                    full_tar1.find(
                        ' '
                        + self._stc._synoname_special_table[  # noqa: SF01
                            s_pos
                        ][1]
                        + ' '
                    )
                    + 1
                )
                full_tar1 = (
                    full_tar1[:loc]
                    + full_tar1[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )
            elif s_type == 'c':
                full_tar1 = full_tar1[
                    1
                    + len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]

        full_src1 = ' '.join((src_ln, src_fn)).replace('-', ' ').strip()
        for s_pos, s_type in features['src_specials']:
            if s_type == 'a':
                full_src1 = full_src1[
                    : -(
                        1
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        )
                    )
                ]
            elif s_type == 'b':
                loc = (
                    full_src1.find(
                        ' '
                        + self._stc._synoname_special_table[  # noqa: SF01
                            s_pos
                        ][1]
                        + ' '
                    )
                    + 1
                )
                full_src1 = (
                    full_src1[:loc]
                    + full_src1[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )
            elif s_type == 'c':
                full_src1 = full_src1[
                    1
                    + len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]

        full_tar2 = full_tar1
        for s_pos, s_type in features['tar_specials']:
            if s_type == 'd':
                full_tar2 = full_tar2[
                    len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]
            elif (
                s_type == 'X'
                and self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                in full_tar2
            ):
                loc = full_tar2.find(
                    ' '
                    + self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                )
                full_tar2 = (
                    full_tar2[:loc]
                    + full_tar2[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )

        full_src2 = full_src1
        for s_pos, s_type in features['src_specials']:
            if s_type == 'd':
                full_src2 = full_src2[
                    len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]
            elif (
                s_type == 'X'
                and self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                in full_src2
            ):
                loc = full_src2.find(
                    ' '
                    + self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                )
                full_src2 = (
                    full_src2[:loc]
                    + full_src2[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )

        full_tar1 = self._synoname_strip_punct(full_tar1)
        tar1_words = full_tar1.split()
        tar1_num_words = len(tar1_words)

        full_src1 = self._synoname_strip_punct(full_src1)
        src1_words = full_src1.split()
        src1_num_words = len(src1_words)

        full_tar2 = self._synoname_strip_punct(full_tar2)
        tar2_words = full_tar2.split()
        tar2_num_words = len(tar2_words)

        full_src2 = self._synoname_strip_punct(full_src2)
        src2_words = full_src2.split()
        src2_num_words = len(src2_words)

        # 2
        if (
            src1_num_words < 2
            and src_len_specials == 0
            and src2_num_words < 2
            and tar_len_specials == 0
        ):
            return 0

        # 4
        if (
            tar1_num_words == 1
            and src1_num_words == 1
            and tar1_words[0] == src1_words[0]
        ):
            return 1
        if tar1_num_words < 2 and tar_len_specials == 0:
            return 0

        # 5
        last_found = False
        for word in tar1_words:
            if src_ln.endswith(word) or word + ' ' in src_ln:
                last_found = True

        if not last_found:
            for word in src1_words:
                if tar_ln.endswith(word) or word + ' ' in tar_ln:
                    last_found = True

        # 6
        matches = 0
        if last_found:
            for i, s_word in enumerate(src1_words):
                for j, t_word in enumerate(tar1_words):
                    if s_word == t_word:
                        src1_words[i] = '@'
                        tar1_words[j] = '@'
                        matches += 1
        w_ratio = matches / max(tar1_num_words, src1_num_words)
        if matches > 1 or (
            matches == 1
            and src1_num_words == 1
            and tar1_num_words == 1
            and (tar_len_specials > 0 or src_len_specials > 0)
        ):
            return w_ratio

        # 8
        if (
            tar2_num_words == 1
            and src2_num_words == 1
            and tar2_words[0] == src2_words[0]
        ):
            return 1
        # I see no way that the following can be True if the equivalent in
        # #4 was False.
        if tar2_num_words < 2 and tar_len_specials == 0:  # pragma: no cover
            return 0

        # 9
        last_found = False
        for word in tar2_words:
            if src_ln.endswith(word) or word + ' ' in src_ln:
                last_found = True

        if not last_found:
            for word in src2_words:
                if tar_ln.endswith(word) or word + ' ' in tar_ln:
                    last_found = True

        if not last_found:
            return 0

        # 10
        matches = 0
        if last_found:
            for i, s_word in enumerate(src2_words):
                for j, t_word in enumerate(tar2_words):
                    if s_word == t_word:
                        src2_words[i] = '@'
                        tar2_words[j] = '@'
                        matches += 1
        w_ratio = matches / max(tar2_num_words, src2_num_words)
        if matches > 1 or (
            matches == 1
            and src2_num_words == 1
            and tar2_num_words == 1
            and (tar_len_specials > 0 or src_len_specials > 0)
        ):
            return w_ratio

        return 0

    def dist_abs(
        self,
        src,
        tar,
        word_approx_min=0.3,
        char_approx_min=0.73,
        tests=2 ** 12 - 1,
        ret_name=False,
    ):
        """Return the Synoname similarity type of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        word_approx_min : float
            The minimum word approximation value to signal a 'word_approx'
            match
        char_approx_min : float
            The minimum character approximation value to signal a 'char_approx'
            match
        tests : int or Iterable
            Either an integer indicating tests to perform or a list of test
            names to perform (defaults to performing all tests)
        ret_name : bool
            If True, returns the match name rather than its integer equivalent

        Returns
        -------
        int (or str if ret_name is True)
            Synoname value

        Examples
        --------
        >>> cmp = Synoname()
        >>> cmp.dist_abs(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''))
        2
        >>> cmp.dist_abs(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''),
        ... ret_name=True)
        'omission'
        >>> cmp.dist_abs(('Dore', 'Gustave', ''),
        ... ('Dore', 'Paul Gustave Louis Christophe', ''), ret_name=True)
        'inclusion'
        >>> cmp.dist_abs(('Pereira', 'I. R.', ''), ('Pereira', 'I. Smith', ''),
        ... ret_name=True)
        'word_approx'

        """
        if isinstance(tests, Iterable):
            new_tests = 0
            for term in tests:
                if term in self._test_dict:
                    new_tests += self._test_dict[term]
            tests = new_tests

        if isinstance(src, tuple):
            src_ln, src_fn, src_qual = src
        elif '#' in src:
            src_ln, src_fn, src_qual = src.split('#')[-3:]
        else:
            src_ln, src_fn, src_qual = src, '', ''

        if isinstance(tar, tuple):
            tar_ln, tar_fn, tar_qual = tar
        elif '#' in tar:
            tar_ln, tar_fn, tar_qual = tar.split('#')[-3:]
        else:
            tar_ln, tar_fn, tar_qual = tar, '', ''

        def _split_special(spec):
            spec_list = []
            while spec:
                spec_list.append((int(spec[:3]), spec[3:4]))
                spec = spec[4:]
            return spec_list

        def _fmt_retval(val):
            if ret_name:
                return self._match_name[val]
            return val

        # 1. Preprocessing

        # Lowercasing
        src_fn = src_fn.strip().lower()
        src_ln = src_ln.strip().lower()
        src_qual = src_qual.strip().lower()

        tar_fn = tar_fn.strip().lower()
        tar_ln = tar_ln.strip().lower()
        tar_qual = tar_qual.strip().lower()

        # Create toolcodes
        src_ln, src_fn, src_tc = self._stc.fingerprint(
            src_ln, src_fn, src_qual
        )
        tar_ln, tar_fn, tar_tc = self._stc.fingerprint(
            tar_ln, tar_fn, tar_qual
        )

        src_generation = int(src_tc[2])
        src_romancode = int(src_tc[3:6])
        src_len_fn = int(src_tc[6:8])
        src_tc = src_tc.split('$')
        src_specials = _split_special(src_tc[1])

        tar_generation = int(tar_tc[2])
        tar_romancode = int(tar_tc[3:6])
        tar_len_fn = int(tar_tc[6:8])
        tar_tc = tar_tc.split('$')
        tar_specials = _split_special(tar_tc[1])

        gen_conflict = (src_generation != tar_generation) and bool(
            src_generation or tar_generation
        )
        roman_conflict = (src_romancode != tar_romancode) and bool(
            src_romancode or tar_romancode
        )

        ln_equal = src_ln == tar_ln
        fn_equal = src_fn == tar_fn

        # approx_c
        def _approx_c():
            if gen_conflict or roman_conflict:
                return False, 0

            full_src = ' '.join((src_ln, src_fn))
            if full_src.startswith('master '):
                full_src = full_src[len('master ') :]
                for intro in [
                    'of the ',
                    'of ',
                    'known as the ',
                    'with the ',
                    'with ',
                ]:
                    if full_src.startswith(intro):
                        full_src = full_src[len(intro) :]

            full_tar = ' '.join((tar_ln, tar_fn))
            if full_tar.startswith('master '):
                full_tar = full_tar[len('master ') :]
                for intro in [
                    'of the ',
                    'of ',
                    'known as the ',
                    'with the ',
                    'with ',
                ]:
                    if full_tar.startswith(intro):
                        full_tar = full_tar[len(intro) :]

            loc_ratio = sim_ratcliff_obershelp(full_src, full_tar)
            return loc_ratio >= char_approx_min, loc_ratio

        approx_c_result, ca_ratio = _approx_c()

        if tests & self._test_dict['exact'] and fn_equal and ln_equal:
            return _fmt_retval(self._match_type_dict['exact'])
        if tests & self._test_dict['omission']:
            if (
                fn_equal
                and levenshtein(src_ln, tar_ln, cost=(1, 1, 99, 99)) == 1
            ):
                if not roman_conflict:
                    return _fmt_retval(self._match_type_dict['omission'])
            elif (
                ln_equal
                and levenshtein(src_fn, tar_fn, cost=(1, 1, 99, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['omission'])
        if tests & self._test_dict['substitution']:
            if (
                fn_equal
                and levenshtein(src_ln, tar_ln, cost=(99, 99, 1, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['substitution'])
            elif (
                ln_equal
                and levenshtein(src_fn, tar_fn, cost=(99, 99, 1, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['substitution'])
        if tests & self._test_dict['transposition']:
            if fn_equal and (
                levenshtein(src_ln, tar_ln, mode='osa', cost=(99, 99, 99, 1))
                == 1
            ):
                return _fmt_retval(self._match_type_dict['transposition'])
            elif ln_equal and (
                levenshtein(src_fn, tar_fn, mode='osa', cost=(99, 99, 99, 1))
                == 1
            ):
                return _fmt_retval(self._match_type_dict['transposition'])
        if tests & self._test_dict['punctuation']:
            np_src_fn = self._synoname_strip_punct(src_fn)
            np_tar_fn = self._synoname_strip_punct(tar_fn)
            np_src_ln = self._synoname_strip_punct(src_ln)
            np_tar_ln = self._synoname_strip_punct(tar_ln)

            if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
                return _fmt_retval(self._match_type_dict['punctuation'])

            np_src_fn = self._synoname_strip_punct(src_fn.replace('-', ' '))
            np_tar_fn = self._synoname_strip_punct(tar_fn.replace('-', ' '))
            np_src_ln = self._synoname_strip_punct(src_ln.replace('-', ' '))
            np_tar_ln = self._synoname_strip_punct(tar_ln.replace('-', ' '))

            if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
                return _fmt_retval(self._match_type_dict['punctuation'])

        if tests & self._test_dict['initials'] and ln_equal:
            if src_fn and tar_fn:
                src_initials = self._synoname_strip_punct(src_fn).split()
                tar_initials = self._synoname_strip_punct(tar_fn).split()
                initials = bool(
                    (len(src_initials) == len(''.join(src_initials)))
                    or (len(tar_initials) == len(''.join(tar_initials)))
                )
                if initials:
                    src_initials = ''.join(_[0] for _ in src_initials)
                    tar_initials = ''.join(_[0] for _ in tar_initials)
                    if src_initials == tar_initials:
                        return _fmt_retval(self._match_type_dict['initials'])
                    initial_diff = abs(len(src_initials) - len(tar_initials))
                    if initial_diff and (
                        (
                            initial_diff
                            == levenshtein(
                                src_initials,
                                tar_initials,
                                cost=(1, 99, 99, 99),
                            )
                        )
                        or (
                            initial_diff
                            == levenshtein(
                                tar_initials,
                                src_initials,
                                cost=(1, 99, 99, 99),
                            )
                        )
                    ):
                        return _fmt_retval(self._match_type_dict['initials'])
        if tests & self._test_dict['extension']:
            if src_ln[1] == tar_ln[1] and (
                src_ln.startswith(tar_ln) or tar_ln.startswith(src_ln)
            ):
                if (
                    (not src_len_fn and not tar_len_fn)
                    or (tar_fn and src_fn.startswith(tar_fn))
                    or (src_fn and tar_fn.startswith(src_fn))
                ) and not roman_conflict:
                    return _fmt_retval(self._match_type_dict['extension'])
        if tests & self._test_dict['inclusion'] and ln_equal:
            if (src_fn and src_fn in tar_fn) or (tar_fn and tar_fn in src_ln):
                return _fmt_retval(self._match_type_dict['inclusion'])
        if tests & self._test_dict['no_first'] and ln_equal:
            if src_fn == '' or tar_fn == '':
                return _fmt_retval(self._match_type_dict['no_first'])
        if tests & self._test_dict['word_approx']:
            ratio = self._synoname_word_approximation(
                src_ln,
                tar_ln,
                src_fn,
                tar_fn,
                {
                    'gen_conflict': gen_conflict,
                    'roman_conflict': roman_conflict,
                    'src_specials': src_specials,
                    'tar_specials': tar_specials,
                },
            )
            if ratio == 1 and tests & self._test_dict['confusions']:
                if (
                    ' '.join((src_fn, src_ln)).strip()
                    == ' '.join((tar_fn, tar_ln)).strip()
                ):
                    return _fmt_retval(self._match_type_dict['confusions'])
            if ratio >= word_approx_min:
                return _fmt_retval(self._match_type_dict['word_approx'])
        if tests & self._test_dict['char_approx']:
            if ca_ratio >= char_approx_min:
                return _fmt_retval(self._match_type_dict['char_approx'])
        return _fmt_retval(self._match_type_dict['no_match'])

    def dist(
        self,
        src,
        tar,
        word_approx_min=0.3,
        char_approx_min=0.73,
        tests=2 ** 12 - 1,
    ):
        """Return the normalized Synoname distance between two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        word_approx_min : float
            The minimum word approximation value to signal a 'word_approx'
            match
        char_approx_min : float
            The minimum character approximation value to signal a 'char_approx'
            match
        tests : int or Iterable
            Either an integer indicating tests to perform or a list of test
            names to perform (defaults to performing all tests)

        Returns
        -------
        float
            Normalized Synoname distance

        """
        return (
            synoname(src, tar, word_approx_min, char_approx_min, tests, False)
            / 14
        )


def synoname(
    src,
    tar,
    word_approx_min=0.3,
    char_approx_min=0.73,
    tests=2 ** 12 - 1,
    ret_name=False,
):
    """Return the Synoname similarity type of two words.

    This is a wrapper for :py:meth:`Synoname.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    word_approx_min : float
        The minimum word approximation value to signal a 'word_approx' match
    char_approx_min : float
        The minimum character approximation value to signal a 'char_approx'
        match
    tests : int or Iterable
        Either an integer indicating tests to perform or a list of test names
        to perform (defaults to performing all tests)
    ret_name : bool
        If True, returns the match name rather than its integer equivalent

    Returns
    -------
    int (or str if ret_name is True)
        Synoname value

    Examples
    --------
    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''))
    2
    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''),
    ... ret_name=True)
    'omission'
    >>> synoname(('Dore', 'Gustave', ''),
    ... ('Dore', 'Paul Gustave Louis Christophe', ''), ret_name=True)
    'inclusion'
    >>> synoname(('Pereira', 'I. R.', ''), ('Pereira', 'I. Smith', ''),
    ... ret_name=True)
    'word_approx'

    """
    return Synoname().dist_abs(
        src, tar, word_approx_min, char_approx_min, tests, ret_name
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
