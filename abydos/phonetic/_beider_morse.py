# Copyright 2014-2022 by Christopher C. Little.
# This file is part of Abydos.
#
# This file is based on Alexander Beider and Stephen P. Morse's implementation
# of the Beider-Morse Phonetic Matching (BMPM) System, available at
# http://stevemorse.org/phonetics/bmpm.htm.
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

"""abydos.phonetic._beider_morse.

Beider-Morse Phonetic Matching (BMPM) algorithm
"""

from re import search
from typing import Any, Optional, Tuple, Union
from unicodedata import normalize

from ._beider_morse_data import (
    BMDATA,
    L_ANY,
    L_ARABIC,
    L_CYRILLIC,
    L_CZECH,
    L_DUTCH,
    L_ENGLISH,
    L_FRENCH,
    L_GERMAN,
    L_GREEK,
    L_GREEKLATIN,
    L_HEBREW,
    L_HUNGARIAN,
    L_ITALIAN,
    L_LATVIAN,
    L_NONE,
    L_POLISH,
    L_PORTUGUESE,
    L_ROMANIAN,
    L_RUSSIAN,
    L_SPANISH,
    L_TURKISH,
)
from ._phonetic import _Phonetic

__all__ = ['BeiderMorse']

_LANG_DICT = {
    'any': L_ANY,
    'arabic': L_ARABIC,
    'cyrillic': L_CYRILLIC,
    'czech': L_CZECH,
    'dutch': L_DUTCH,
    'english': L_ENGLISH,
    'french': L_FRENCH,
    'german': L_GERMAN,
    'greek': L_GREEK,
    'greeklatin': L_GREEKLATIN,
    'hebrew': L_HEBREW,
    'hungarian': L_HUNGARIAN,
    'italian': L_ITALIAN,
    'latvian': L_LATVIAN,
    'polish': L_POLISH,
    'portuguese': L_PORTUGUESE,
    'romanian': L_ROMANIAN,
    'russian': L_RUSSIAN,
    'spanish': L_SPANISH,
    'turkish': L_TURKISH,
}

BMDATA['gen']['discards'] = {
    'da ',
    'dal ',
    'de ',
    'del ',
    'dela ',
    'de la ',
    'della ',
    'des ',
    'di ',
    'do ',
    'dos ',
    'du ',
    'van ',
    'von ',
    "d'",
}
BMDATA['sep']['discards'] = {
    'al',
    'el',
    'da',
    'dal',
    'de',
    'del',
    'dela',
    'de la',
    'della',
    'des',
    'di',
    'do',
    'dos',
    'du',
    'van',
    'von',
}
BMDATA['ash']['discards'] = {'bar', 'ben', 'da', 'de', 'van', 'von'}

# format of rules array
_PATTERN_POS = 0
_LCONTEXT_POS = 1
_RCONTEXT_POS = 2
_PHONETIC_POS = 3


class BeiderMorse(_Phonetic):
    """Beider-Morse Phonetic Matching.

    The Beider-Morse Phonetic Matching algorithm is described in
    :cite:`Beider:2008`.
    The reference implementation is licensed under GPLv3.

    .. versionadded:: 0.3.6
    """

    def _language(self, name: str, name_mode: str) -> int:
        """Return the best guess language ID for the word and language choices.

        Parameters
        ----------
        name : str
            The term to guess the language of
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)

        Returns
        -------
        int
            Language ID


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        name = name.strip().lower()
        rules = BMDATA[name_mode]['language_rules']
        all_langs = (
            sum(_LANG_DICT[_] for _ in BMDATA[name_mode]['languages']) - 1
        )
        choices_remaining = all_langs
        for rule in rules:
            letters, languages, accept = rule
            if search(letters, name) is not None:
                if accept:
                    choices_remaining &= languages
                else:
                    choices_remaining &= (~languages) % (all_langs + 1)
        if choices_remaining == L_NONE:
            choices_remaining = L_ANY
        return choices_remaining

    def _redo_language(
        self,
        term: str,
        name_mode: str,
        rules: Tuple[Any, ...],
        final_rules1: Tuple[Any, ...],
        final_rules2: Tuple[Any, ...],
        concat: bool,
    ) -> str:
        """Reassess the language of the terms and call the phonetic encoder.

        Uses a split multi-word term.

        Parameters
        ----------
        term : str
            The term to encode via Beider-Morse
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)
        rules : tuple
            The set of initial phonetic transform regexps
        final_rules1 : tuple
            The common set of final phonetic transform regexps
        final_rules2 : tuple
            The specific set of final phonetic transform regexps
        concat : bool
            A flag to indicate concatenation

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        language_arg = self._language(term, name_mode)
        return self._phonetic(
            term,
            name_mode,
            rules,
            final_rules1,
            final_rules2,
            language_arg,
            concat,
        )

    def _phonetic(
        self,
        term: str,
        name_mode: str,
        rules: Tuple[Any, ...],
        final_rules1: Tuple[Any, ...],
        final_rules2: Tuple[Any, ...],
        language_arg: int = 0,
        concat: bool = False,
    ) -> str:
        """Return the Beider-Morse encoding(s) of a term.

        Parameters
        ----------
        term : str
            The term to encode via Beider-Morse
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)
        rules : tuple
            The set of initial phonetic transform regexps
        final_rules1 : tuple
            The common set of final phonetic transform regexps
        final_rules2 : tuple
            The specific set of final phonetic transform regexps
        language_arg : int
            The language of the term
        concat : bool
            A flag to indicate concatenation

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        term = term.replace('-', ' ').strip()

        if name_mode == 'gen':  # generic case
            # discard and concatenate certain words if at the start of the name
            for pfx in BMDATA['gen']['discards']:
                if term.startswith(pfx):
                    remainder = term[len(pfx) :]
                    combined = pfx[:-1] + remainder
                    result = (
                        self._redo_language(
                            remainder,
                            name_mode,
                            rules,
                            final_rules1,
                            final_rules2,
                            concat,
                        )
                        + '-'
                        + self._redo_language(
                            combined,
                            name_mode,
                            rules,
                            final_rules1,
                            final_rules2,
                            concat,
                        )
                    )
                    return result

        words = (
            term.split()
        )  # create array of the individual words in the name
        words2 = []

        if name_mode == 'sep':  # Sephardic case
            # for each word in the name, delete portions of word preceding
            # apostrophe
            # ex: d'avila d'aguilar --> avila aguilar
            # also discard certain words in the name

            # note that we can never get a match on "de la" because we are
            # checking single words below
            # this is a bug, but I won't try to fix it now

            for word in words:
                word = word[word.rfind("'") + 1 :]
                if word not in BMDATA['sep']['discards']:
                    words2.append(word)

        elif name_mode == 'ash':  # Ashkenazic case
            # discard certain words if at the start of the name
            if len(words) > 1 and words[0] in BMDATA['ash']['discards']:
                words2 = words[1:]
            else:
                words2 = list(words)
        else:
            words2 = list(words)

        if concat:
            # concatenate the separate words of a multi-word name
            # (normally used for exact matches)
            term = ' '.join(words2)
        elif len(words2) == 1:  # not a multi-word name
            term = words2[0]
        else:
            # encode each word in a multi-word name separately
            # (normally used for approx matches)
            result = '-'.join(
                [
                    self._redo_language(
                        w, name_mode, rules, final_rules1, final_rules2, concat
                    )
                    for w in words2
                ]
            )
            return result

        term_length = len(term)

        # apply language rules to map to phonetic alphabet
        phonetic = ''
        skip = 0
        for i in range(term_length):
            if skip:
                skip -= 1
                continue
            found = False
            for rule in rules:
                pattern = rule[_PATTERN_POS]
                pattern_length = len(pattern)
                lcontext = rule[_LCONTEXT_POS]
                rcontext = rule[_RCONTEXT_POS]

                # check to see if next sequence in input matches the string in
                # the rule
                if (pattern_length > term_length - i) or (
                    term[i : i + pattern_length] != pattern
                ):  # no match
                    continue

                right = f'^{rcontext}'
                left = f'{lcontext}$'

                # check that right context is satisfied
                if rcontext != '':
                    if not search(right, term[i + pattern_length :]):
                        continue

                # check that left context is satisfied
                if lcontext != '':
                    if not search(left, term[:i]):
                        continue

                # check for incompatible attributes
                candidate = self._apply_rule_if_compat(
                    phonetic, rule[_PHONETIC_POS], language_arg
                )
                # The below condition shouldn't ever be false
                if candidate is not None:  # pragma: no branch
                    phonetic = candidate
                    found = True
                    break

            if (
                not found
            ):  # character in name that is not in table -- e.g., space
                pattern_length = 1
            skip = pattern_length - 1

        # apply final rules on phonetic-alphabet,
        # doing a substitution of certain characters
        phonetic = self._apply_final_rules(
            phonetic, final_rules1, language_arg, False
        )  # apply common rules
        # final_rules1 are the common approx rules,
        # final_rules2 are approx rules for specific language
        phonetic = self._apply_final_rules(
            phonetic, final_rules2, language_arg, True
        )  # apply lang specific rules

        return phonetic

    def _apply_final_rules(
        self,
        phonetic: str,
        final_rules: Tuple[Any, ...],
        language_arg: int,
        strip: bool,
    ) -> str:
        """Apply a set of final rules to the phonetic encoding.

        Parameters
        ----------
        phonetic : str
            The term to which to apply the final rules
        final_rules : tuple
            The set of final phonetic transform regexps
        language_arg : int
            An integer representing the target language of the phonetic
            encoding
        strip : bool
            Flag to indicate whether to normalize the language attributes

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # optimization to save time
        if not final_rules:
            return phonetic

        # expand the result
        phonetic = self._expand_alternates(phonetic)
        phonetic_array = phonetic.split('|')

        for k in range(len(phonetic_array)):
            phonetic = phonetic_array[k]
            phonetic2 = ''
            phoneticx = self._normalize_lang_attrs(phonetic, True)

            i = 0
            while i < len(phonetic):
                found = False

                if phonetic[i] == '[':  # skip over language attribute
                    attrib_start = i
                    i += 1
                    while True:
                        if phonetic[i] == ']':
                            i += 1
                            phonetic2 += phonetic[attrib_start:i]
                            break
                        i += 1
                    continue

                for rule in final_rules:
                    pattern = rule[_PATTERN_POS]
                    pattern_length = len(pattern)
                    lcontext = rule[_LCONTEXT_POS]
                    rcontext = rule[_RCONTEXT_POS]

                    right = f'^{rcontext}'
                    left = f'{lcontext}$'

                    # check to see if next sequence in phonetic matches the
                    # string in the rule
                    if (pattern_length > len(phoneticx) - i) or phoneticx[
                        i : i + pattern_length
                    ] != pattern:
                        continue

                    # check that right context is satisfied
                    if rcontext != '':
                        if not search(right, phoneticx[i + pattern_length :]):
                            continue

                    # check that left context is satisfied
                    if lcontext != '':
                        if not search(left, phoneticx[:i]):
                            continue

                    # check for incompatible attributes
                    candidate = self._apply_rule_if_compat(
                        phonetic2, rule[_PHONETIC_POS], language_arg
                    )
                    # The below condition shouldn't ever be false
                    if candidate is not None:  # pragma: no branch
                        phonetic2 = candidate
                        found = True
                        break

                if not found:
                    # character in name for which there is no substitution in
                    # the table
                    phonetic2 += phonetic[i]
                    pattern_length = 1

                i += pattern_length

            phonetic_array[k] = self._expand_alternates(phonetic2)

        phonetic = '|'.join(phonetic_array)
        if strip:
            phonetic = self._normalize_lang_attrs(phonetic, True)

        if '|' in phonetic:
            phonetic = f'({self._remove_dupes(phonetic)})'

        return phonetic

    def _phonetic_number(self, phonetic: str) -> str:
        """Remove bracketed text from the end of a string.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if '[' in phonetic:
            return phonetic[: phonetic.find('[')]

        return phonetic  # experimental !!!!

    def _expand_alternates(self, phonetic: str) -> str:
        r"""Expand phonetic alternates separated by \|s.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        alt_start = phonetic.find('(')
        if alt_start == -1:
            return self._normalize_lang_attrs(phonetic, False)

        prefix = phonetic[:alt_start]
        alt_start += 1  # get past the (
        alt_end = phonetic.find(')', alt_start)
        alt_string = phonetic[alt_start:alt_end]
        alt_end += 1  # get past the )
        suffix = phonetic[alt_end:]
        alt_array = alt_string.split('|')
        result = ''

        for i in range(len(alt_array)):
            alt = alt_array[i]
            alternate = self._expand_alternates(prefix + alt + suffix)
            if alternate != '' and alternate != '[0]':
                if result != '':
                    result += '|'
                result += alternate

        return result

    def _pnums_with_leading_space(self, phonetic: str) -> str:
        """Join prefixes & suffixes in cases of alternate phonetic values.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        alt_start = phonetic.find('(')
        if alt_start == -1:
            return f' {self._phonetic_number(phonetic)}'

        prefix = phonetic[:alt_start]
        alt_start += 1  # get past the (
        alt_end = phonetic.find(')', alt_start)
        alt_string = phonetic[alt_start:alt_end]
        alt_end += 1  # get past the )
        suffix = phonetic[alt_end:]
        alt_array = alt_string.split('|')
        result = ''
        for alt in alt_array:
            result += self._pnums_with_leading_space(prefix + alt + suffix)

        return result

    def _phonetic_numbers(self, phonetic: str) -> str:
        """Prepare & join phonetic numbers.

        Split phonetic value on '-', run through _pnums_with_leading_space,
        and join with ' '

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        phonetic_array = phonetic.split('-')  # for names with spaces in them
        result = ' '.join(
            [self._pnums_with_leading_space(i)[1:] for i in phonetic_array]
        )
        return result

    def _remove_dupes(self, phonetic: str) -> str:
        """Remove duplicates from a phonetic encoding list.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        alt_string = phonetic
        alt_array = alt_string.split('|')

        result = '|'
        for i in range(len(alt_array)):
            alt = alt_array[i]
            if alt and f'|{alt}|' not in result:
                result += f'{alt}|'

        return result[1:-1]  # remove leading and trailing |

    def _normalize_lang_attrs(self, text: str, strip: bool) -> str:
        """Remove embedded bracketed attributes.

        This (potentially) bitwise-ands bracketed attributes together and adds
        to the end.
        This is applied to a single alternative at a time -- not to a
        parenthesized list.
        It removes all embedded bracketed attributes, logically-ands them
        together, and places them at the end.
        However if strip is true, this can indeed remove embedded bracketed
        attributes from a parenthesized list.

        Parameters
        ----------
        text : str
            A Beider-Morse phonetic encoding (in progress)
        strip : bool
            Remove the bracketed attributes (and throw away)

        Returns
        -------
        str
            A Beider-Morse phonetic code

        Raises
        ------
        ValueError
            No closing square bracket


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        uninitialized = -1  # all 1's
        attrib = uninitialized
        while '[' in text:
            bracket_start = text.find('[')
            bracket_end = text.find(']', bracket_start)
            if bracket_end == -1:
                raise ValueError(
                    f'No closing square bracket: text=({text}) '
                    f'strip=({strip})'
                )
            attrib &= int(text[bracket_start + 1 : bracket_end])
            text = text[:bracket_start] + text[bracket_end + 1 :]

        if attrib == uninitialized or strip:
            return text
        elif attrib == 0:
            # means that the attributes were incompatible and there is no
            # alternative here
            return '[0]'
        return f'{text}[{attrib}]'

    def _apply_rule_if_compat(
        self, phonetic: str, target: str, language_arg: int
    ) -> Optional[str]:
        """Apply a phonetic regex if compatible.

        tests for compatible language rules

        to do so, apply the rule, expand the results, and detect alternatives
            with incompatible attributes

        then drop each alternative that has incompatible attributes and keep
            those that are compatible

        if there are no compatible alternatives left, return false

        otherwise return the compatible alternatives

        apply the rule

        Parameters
        ----------
        phonetic : str
            The Beider-Morse phonetic encoding (so far)
        target : str
            A proposed addition to the phonetic encoding
        language_arg : int
            An integer representing the target language of the phonetic
            encoding

        Returns
        -------
        str
            A candidate encoding


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        candidate = phonetic + target
        if '[' not in candidate:  # no attributes so we need test no further
            return candidate

        # expand the result, converting incompatible attributes to [0]
        candidate = self._expand_alternates(candidate)
        candidate_array = candidate.split('|')

        # drop each alternative that has incompatible attributes
        candidate = ''
        found = False

        for i in range(len(candidate_array)):
            this_candidate = candidate_array[i]
            if language_arg != 1:
                this_candidate = self._normalize_lang_attrs(
                    f'{this_candidate}[{language_arg}]', False
                )
            if this_candidate != '[0]':
                found = True
                if candidate:
                    candidate += '|'
                candidate += this_candidate

        # return false if no compatible alternatives remain
        if not found:
            return None

        # return the result of applying the rule
        if '|' in candidate:
            candidate = f'({candidate})'
        return candidate

    def _language_index_from_code(self, code: int, name_mode: str) -> int:
        """Return the index value for a language code.

        This returns l_any if more than one code is specified or the code is
        out of bounds.

        Parameters
        ----------
        code : int
            The language code to interpret
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)

        Returns
        -------
        int
            Language code index


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if code < 1 or code > sum(
            _LANG_DICT[_] for _ in BMDATA[name_mode]['languages']
        ):  # code out of range
            return L_ANY
        if (
            code & (code - 1)
        ) != 0:  # choice was more than one language; use any
            return L_ANY
        return code

    def __init__(
        self,
        language_arg: Union[str, int] = 0,
        name_mode: str = 'gen',
        match_mode: str = 'approx',
        concat: bool = False,
        filter_langs: bool = False,
    ) -> None:
        """Initialize BeiderMorse instance.

        Parameters
        ----------
        language_arg : str or int
            The language of the term; supported values include:

                - ``any``
                - ``arabic`` (Arabic written in the Arabic script)
                - ``cyrillic`` (Russian written in the Cyrillic script)
                - ``czech``
                - ``dutch``
                - ``english``
                - ``french``
                - ``german``
                - ``greek`` (Greek written in the Greek script)
                - ``greeklatin`` (Greek transliterated to the Latin script)
                - ``hebrew`` (Hebrew written in the Hebrew script)
                - ``hungarian``
                - ``italian``
                - ``latvian``
                - ``polish``
                - ``portuguese``
                - ``romanian``
                - ``russian`` (Russian transliterated to the Latin script)
                - ``spanish``
                - ``turkish``

        name_mode : str
            The name mode of the algorithm:

                - ``gen`` -- general (default)
                - ``ash`` -- Ashkenazi
                - ``sep`` -- Sephardic

        match_mode : str
            Matching mode: ``approx`` or ``exact``
        concat : bool
            Concatenation mode
        filter_langs : bool
            Filter out incompatible languages


        .. versionadded:: 0.4.0

        """
        name_mode = name_mode.strip().lower()[:3]
        if name_mode not in {'ash', 'sep', 'gen'}:
            name_mode = 'gen'

        if match_mode != 'exact':
            match_mode = 'approx'

        # Translate the supplied language_arg value into an integer
        # representing a set of languages
        all_langs = (
            sum(_LANG_DICT[_] for _ in BMDATA[name_mode]['languages']) - 1
        )
        lang_choices = 0
        if isinstance(language_arg, (int, float)):
            self._lang_choices = int(language_arg)
        elif language_arg != '' and isinstance(language_arg, str):
            for lang in language_arg.lower().split(','):
                if lang in _LANG_DICT and (_LANG_DICT[lang] & all_langs):
                    lang_choices += _LANG_DICT[lang]
                elif not filter_langs:
                    raise ValueError(
                        f"Unknown '{name_mode}' language: '{lang}'"
                    )

        self._language_arg = language_arg
        self._name_mode = name_mode
        self._match_mode = match_mode
        self._concat = concat
        self._filter_langs = filter_langs
        self._lang_choices = lang_choices

    def encode(self, word: str) -> str:
        """Return the Beider-Morse Phonetic Matching encoding(s) of a term.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        tuple
            The Beider-Morse phonetic value(s)

        Raises
        ------
        ValueError
            Unknown language

        Examples
        --------
        >>> pe = BeiderMorse()
        >>> pe.encode('Christopher').split(',')
        ['xrQstopir', 'xrQstYpir', 'xristopir', 'xristYpir', 'xrQstofir',
        'xrQstYfir', 'xristofir', 'xristYfir', 'xristopi', 'xritopir',
        'xritopi', 'xristofi', 'xritofir', 'xritofi', 'tzristopir',
        'tzristofir', 'zristopir', 'zristopi', 'zritopir', 'zritopi',
        'zristofir', 'zristofi', 'zritofir', 'zritofi']
        >>> pe.encode('Niall')
        'nial,niol'
        >>> pe.encode('Smith')
        'zmit'
        >>> pe.encode('Schmidt')
        'zmit,stzmit'

        >>> BeiderMorse(language_arg='German').encode('Christopher').split(',')
        ['xrQstopir', 'xrQstYpir', 'xristopir', 'xristYpir', 'xrQstofir',
        'xrQstYfir', 'xristofir', 'xristYfir']
        >>> BeiderMorse(language_arg='English').encode(
        ... 'Christopher').split(',')
        ['tzristofir', 'tzrQstofir', 'tzristafir', 'tzrQstafir', 'xristofir',
        'xrQstofir', 'xristafir', 'xrQstafir']
        >>> BeiderMorse(language_arg='German',
        ... name_mode='ash').encode('Christopher').split(',')
        ['xrQstopir', 'xrQstYpir', 'xristopir', 'xristYpir', 'xrQstofir',
        'xrQstYfir', 'xristofir', 'xristYfir']

        >>> BeiderMorse(language_arg='German',
        ... match_mode='exact').encode('Christopher')
        'xriStopher,xriStofer,xristopher,xristofer'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class
        .. versionchanged:: 0.6.0
            Made comma-sepated instead of space-separated output

        """
        word = normalize('NFC', word.strip().lower())

        # Language choices are either all incompatible with the name mode or
        # no choices were given, so try to autodetect
        if self._lang_choices == 0:
            language_arg = self._language(word, self._name_mode)
        else:
            language_arg = self._lang_choices
        language_arg2 = self._language_index_from_code(
            language_arg, self._name_mode
        )

        rules = BMDATA[self._name_mode]['rules'][language_arg2]
        final_rules1 = BMDATA[self._name_mode][self._match_mode]['common']
        final_rules2 = BMDATA[self._name_mode][self._match_mode][language_arg2]

        result = self._phonetic(
            word,
            self._name_mode,
            rules,
            final_rules1,
            final_rules2,
            language_arg,
            self._concat,
        )
        result = self._phonetic_numbers(result).replace(' ', ',')

        return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()
