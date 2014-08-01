# -*- coding: utf-8 -*-
"""abydos.bm

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

This file is based on Alexander Beider and Stephen P. Morse's implementation of
the Beider-Morse Phonetic Matching (BMPM) System, available at
http://stevemorse.org/phonetics/bmpm.htm.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import re
import unicodedata
from ._compat import _unicode, _long, _range
from .bmdata import bmdata, l_none, l_any, l_arabic, l_cyrillic, \
    l_czech, l_dutch, l_english, l_french, l_german, l_greek, l_greeklatin, \
    l_hebrew, l_hungarian, l_italian, l_polish, l_portuguese, l_romanian, \
    l_russian, l_spanish, l_turkish

lang_dict = {'any': l_any, 'arabic': l_arabic, 'cyrillic': l_cyrillic,
             'czech': l_czech, 'dutch': l_dutch, 'english': l_english,
             'french': l_french, 'german': l_german, 'greek': l_greek,
             'greeklatin': l_greeklatin, 'hebrew': l_hebrew,
             'hungarian': l_hungarian, 'italian': l_italian, 'polish': l_polish,
             'portuguese': l_portuguese, 'romanian': l_romanian,
             'russian': l_russian, 'spanish': l_spanish, 'turkish': l_turkish}

bmdata['gen']['discards'] = ('da ', 'dal ', 'de ', 'del ', 'dela ', 'de la ',
                             'della ', 'des ', 'di ', 'do ', 'dos ', 'du ',
                             'van ', 'von ', 'd\'')
bmdata['sep']['discards'] = set(['al', 'el', 'da', 'dal', 'de', 'del', 'dela',
                             'de la', 'della', 'des', 'di', 'do', 'dos', 'du',
                             'van', 'von'])
bmdata['ash']['discards'] = set(['bar', 'ben', 'da', 'de', 'van', 'von'])


# format of rules array
_pattern_pos = 0
_lcontext_pos = 1
_rcontext_pos = 2
_phonetic_pos = 3
_language_pos = 4
_logical_pos = 5


def language(name, name_mode):
    """Return the best guess language ID for the given word and set of language
    choices

    Arguments:
    name -- the term to guess the language of
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    """
    name = name.strip().lower()
    rules = bmdata[name_mode]['language_rules']
    all_langs = sum([lang_dict[_] for _ in bmdata[name_mode]['languages']])
    choices_remaining = all_langs
    for rule in rules:
        letters, languages, accept = rule
        if re.search(letters, name) != None:
            if accept:
                choices_remaining &= languages
            else:
                choices_remaining &= (~languages) % (all_langs+1)
    if choices_remaining == l_none:
        choices_remaining = l_any
    return choices_remaining


def redo_language(term, name_mode, rules, final_rules1, final_rules2, concat):
    """Using a split multi-work term, reassess the language of the terms and
    call the phonetic encoder

    Arguments:
    term -- the term to encode via Beider-Morse
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    rules -- the set of initial phonetic transform regexps
    final_rules1 -- the common set of final phonetic transform regexps
    final_rules2 -- the specific set of final phonetic transform regexps
    concat -- a flag to indicate concatenation
    """
    language_arg = language(term, name_mode)
    return phonetic(term, name_mode, rules, final_rules1, final_rules2, language_arg, concat)


def phonetic(term, name_mode, rules, final_rules1, final_rules2, language_arg=0, concat=False):
    """Return the Beider-Morse encoding(s) of a term

    Arguments:
    term -- the term to encode via Beider-Morse
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    rules -- the set of initial phonetic transform regexps
    final_rules1 -- the common set of final phonetic transform regexps
    final_rules2 -- the specific set of final phonetic transform regexps
    language_arg -- an integer representing the target language of the phonetic
                encoding
    concat -- a flag to indicate concatenation
    """
    term = term.replace('-', ' ').strip()

    if name_mode == 'gen': # generic case
        # both discard and concatenate certain words if at the start of the name
        for pfx in bmdata['gen']['discards']:
            if term.startswith(pfx):
                remainder = term[len(pfx):]
                combined = pfx[:-1]+remainder
                result = (redo_language(remainder, name_mode, rules,
                                        final_rules1, final_rules2, concat) +
                          '-' +
                          redo_language(combined, name_mode, rules,
                                        final_rules1, final_rules2, concat))
                return result

    words = term.split() # create array of the individual words in the name
    words2 = []

    if name_mode == 'sep': # Sephardic case
        # for each word in the name, delete portions of word preceding apostrophe
        # ex: d'avila d'aguilar --> avila aguilar
        # also discard certain words in the name

        # FIXME:
        # note that we can never get a match on "de la" because we are checking single words below
        # this is a bug, but I won't try to fix it now

        for word in words:
            word = word[word.rfind('\'')+1:]
            if word not in bmdata['sep']['discards']:
                words2.append(word)

    elif name_mode == 'ash': # Ashkenazic case
        # discard certain words if at the start of the name
        if len(words) > 1 and words[0] in bmdata['ash']['discards']:
            words2 = words[1:]
        else:
            words2 = list(words)
    else:
        words2 = list(words)

    if concat: #concatenate the separate words of a multi-word name (normally used for exact matches)
        term = ' '.join(words2)
    elif len(words2) == 1: # not a multi-word name
        term = words2[0]
    else: # encode each word in a multi-word name separately (normally used for approx matches)
        result = ''
        for word in words2:
            result += '-' + redo_language(word, name_mode, rules,
                                          final_rules1, final_rules2, concat)
        return result[1:] # strip off the leading dash

    term_length = len(term)

    # apply language rules to map to phonetic alphabet
    print 'before main: ' + term
    phonetic = ''
    skip = 0
    for i in _range(term_length):
        if skip:
            skip -= 1
            continue
        found = False
        for rule in rules:
            pattern = rule[_pattern_pos]
            pattern_length = len(pattern)
            lcontext = rule[_lcontext_pos]
            rcontext = rule[_rcontext_pos]

            # check to see if next sequence in input matches the string in the rule
            if (pattern_length > term_length - i) or (term[i:i+pattern_length] != pattern): # no match
                continue

            right = '^'+rcontext
            left = lcontext+'$'

            # check that right context is satisfied
            if rcontext != '':
                if not re.search(right, term[i+pattern_length:]):
                    continue

            # check that left context is satisfied
            if lcontext != '':
                if not re.search(left, term[:i]):
                    continue

            # check to see if language_arg is one of the allowable ones (used only with "any" rules)
            if language_arg != 1 and _language_pos < len(rule):
                language = rule[_language_pos] # the required language(s) for this rule to apply
                logical = rule[_logical_pos] # do we require ALL or ANY of the required languages
                if logical == 'ALL':
                    # check to see if language_arg contains all the required languages
                    if (language_arg & language) != language:
                        continue
                else: #any
                    # check to see if languageArg contains at least one required language
                    if (language_arg & language) == 0:
                        continue

            # check for incompatible attributes
            candidate = apply_rule_if_compatible(phonetic, rule[_phonetic_pos], language_arg)
            if candidate == '':
                continue
            phonetic = candidate
            found = True
            break

        if not found: # character in name that is not in table -- e.g., space
            pattern_length = 1
        skip = pattern_length-1

    print 'before common:  ' + phonetic
    # apply final rules on phonetic-alphabet, doing a substitution of certain characters
    phonetic = apply_final_rules(phonetic, final_rules1, language_arg, False) # apply common rules
    print 'after common:   ' + phonetic
    # final_rules1 are the common approx rules, final_rules2 are approx rules for specific language
    phonetic = apply_final_rules(phonetic, final_rules2, language_arg, True) # apply lang specific rules
    print 'after specific: ' + phonetic

    return phonetic


def apply_final_rules(phonetic, final_rules, language_arg, strip):
    """Apply a set of final rules to the phonetic encoding

    Arguments:
    phonetic -- the term to which to apply the final rules
    final_rules -- the set of final phonetic transform regexps
    language_arg -- an integer representing the target language of the phonetic
                encoding
    strip -- flag to indicate whether to normalize the language attributes
    """
    # optimization to save time
    if not final_rules:
        return phonetic

    # expand the result
    phonetic = expand_alternates(phonetic)
    phonetic_array = phonetic.split('|')

    for k in _range(len(phonetic_array)):
        phonetic = phonetic_array[k]
        phonetic2 = ''
        phoneticx = normalize_language_attributes(phonetic, True)

        i = 0
        while i < len(phonetic):
            found = False

            if phonetic[i] == '[': # skip over language attribute
                attrib_start = i
                i += 1
                while (True):
                    if phonetic[i] == ']':
                        i += 1
                        phonetic2 += phonetic[attrib_start:i]
                        break
                    i += 1
                continue

            for rule in final_rules:
                pattern = rule[_pattern_pos]
                pattern_length = len(pattern)
                lcontext = rule[_lcontext_pos]
                rcontext = rule[_rcontext_pos]

                right = '^'+rcontext
                left = lcontext+'$'

                # check to see if next sequence in phonetic matches the string in the rule
                if (pattern_length > len(phoneticx) - i) or phoneticx[i:i+pattern_length] != pattern:
                    continue

                # check that right context is satisfied
                if rcontext != '':
                    if not re.search(right, phoneticx[i + pattern_length:]):
                        continue

                # check that left context is satisfied
                if lcontext != '':
                    if not re.search(left, phoneticx[:i]):
                        continue

                # check to see if rule applies to languageArg (used only with "any" rules)
                if language_arg != 1 and _language_pos < len(rule):
                    language = rule[_language_pos] # the required language(s) for this rule to apply
                    logical = rule[_logical_pos] # do we require ALL or ANY of the required languages
                    if logical == 'ALL':
                        # check to see if languageArg contains all the required languages
                        if (language_arg & language) != language:
                            continue
                    else: # any
                        # check to see if languageArg contains at least one required language
                        if (language_arg & language) == 0:
                            continue

                # check for incompatible attributes
                candidate = apply_rule_if_compatible(phonetic2, rule[_phonetic_pos], language_arg)
                if candidate == None:
                    continue
                phonetic2 = candidate

                found = True
                break

            if not found: # character in name for which there is no subsitution in the table
                phonetic2 += phonetic[i]
                pattern_length = 1

            i += pattern_length

        phonetic_array[k] = expand_alternates(phonetic2)

    phonetic = '|'.join(phonetic_array)
    if strip:
        phonetic = normalize_language_attributes(phonetic, True)

    if '|' in phonetic:
        phonetic = '(' + remove_duplicate_alternates(phonetic) + ')'

    return phonetic


def phonetic_number(phonetic, hashed=True):
    bracket = phonetic.find('[')
    if (bracket != -1):
        return phonetic[:bracket]

    return phonetic # experimental !!!!

    phonetic_letters = '!bdfghjklmnNprsSt68vwzZxAa4oe5iI9uUEyQY' # true phonetic letters
    phonetic_letters += '1BCDEHJKLOTUVWX' # metaphonetic letters
    # dummy first letter, otherwise b would be treated as 0 and have no effect on result
    meta_phonetic_letters = '' # added letters to be used in finalxxx.php rules
    result = 0
    i = 0
    while i < len(phonetic):
        if phonetic[i:i+1] == '#': # it's a meta phonetic letter
            if i == len(phonetic)-1:
                raise ValueError('fatal error: invalid metaphonetic letter at position ' + _unicode(i + 1) + ' in ' + phonetic)
            i += 1
            j = meta_phonetic_letters.find(phonetic[i:i+1])
            if j != -1:
                j += len(phonetic_letters)
        else:
            j = phonetic_letters.find(phonetic[i:i+1])
        if j == False:
            raise ValueError('fatal error: invalid phonetic letter at position ' + _unicode(i + 1) + ' in ' + phonetic)
        result *= len(phonetic_letters) + len(meta_phonetic_letters)
        if hashed:
            # result = result & 0xff
            result = result & 0x7fffffff
            # result = Mod(result, 999999999)

        result += j
        i += 1
    return hex(result)


def expand_alternates(phonetic):
    """Expand phonetic alternates separated by |s

    Arguments:
    phonetic -- a Beider-Morse phonetic encoding
    """
    alt_start = phonetic.find('(')
    if alt_start == -1:
        return normalize_language_attributes(phonetic, False)

    prefix = phonetic[:alt_start]
    alt_start += 1 # get past the (
    alt_end = phonetic.find(')', alt_start)
    alt_string = phonetic[alt_start:alt_end]
    alt_end += 1 # get past the )
    suffix = phonetic[alt_end:]
    alt_array = alt_string.split('|')
    result = ''

    for i in _range(len(alt_array)):
        alt = alt_array[i];
        alternate = expand_alternates(prefix+alt+suffix)
        if alternate != '' and alternate != '[0]':
            if result != '':
                result += '|'
            result += alternate;

    return result


def phonetic_numbers_with_leading_space(phonetic):
    alt_start = phonetic.find('(')
    if alt_start == -1:
        return ' ' + phonetic_number(phonetic)

    prefix = phonetic[:alt_start]
    alt_start += 1 # get past the (
    alt_end = phonetic.find(')', alt_start)
    alt_string = phonetic[alt_start:alt_end]
    alt_end += 1 # get past the )
    suffix = phonetic[alt_end:]
    alt_array = alt_string.split('|')
    result = ''
    for alt in alt_array:
        result += phonetic_numbers_with_leading_space(prefix+alt+suffix)

    return result


def phonetic_numbers(phonetic):
    phonetic_array = phonetic.split('-') # for names with spaces in them
    result = ' '.join([phonetic_numbers_with_leading_space(i)[1:] for i in phonetic_array])
    return result


def remove_duplicate_alternates(phonetic):
    """Remove duplicates from a phonetic encoding list

    Arguments:
    phonetic -- a Beider-Morse phonetic encoding
    """
    alt_string = phonetic
    alt_array = alt_string.split('|')

    result = '|'
    altcount = 0
    for i in _range(len(alt_array)):
        alt = alt_array[i]
        if '|'+alt+'|' not in result:
            result += alt+'|'
            altcount += 1

    return result[1:-1] # remove leading and trailing |


def normalize_language_attributes(text, strip):
    """Remove embedded bracketed attributes and (potentially) and them together
    and add to the end

    Arguments:
    text -- a Beider-Morse phonetic encoding (in progress)
    strip -- remove the bracketed attributes (and throw away)

    this is applied to a single alternative at a time -- not to a parenthisized
        list
    it removes all embedded bracketed attributes, logically-ands them together,
        and places them at the end.
    however if strip is true, this can indeed remove embedded bracketed
        attributes from a parenthesized list
    """
    uninitialized = -1; # all 1's
    attrib = uninitialized
    while '[' in text:
        bracket_start = text.find('[')
        bracket_end = text.find(']', bracket_start)
        if bracket_end == -1:
            raise ValueError('No closing square bracket: text=(' +
                             text + ') strip=(' + _unicode(strip) + ')')
        attrib = attrib & int(text[bracket_start+1:bracket_end])
        text = text[:bracket_start] + text[bracket_end+1:]

    if attrib == uninitialized or strip:
        return text
    elif attrib == 0:
        return '[0]' # means that the attributes were incompatible and there is no alternative here
    else:
        return text + '[' + str(attrib) + ']'


def apply_rule_if_compatible(phonetic, target, language_arg):
    """Applies a phonetic regex if compatible

    Arguments:
    phoentic -- the Beider-Morse phonetic encoding (so far)
    target -- a proposed addition to the phonetic encoding
    language_arg -- an integer representing the target language of the phonetic
                encoding

    Description:
    tests for compatible language rules
    to do so, apply the rule, expand the results, and detect alternatives with
        incompatible attributes
    then drop each alternative that has incompatible attributes and keep those
        that are compatible
    if there are no compatible alternatives left, return false
    otherwise return the compatible alternatives
    apply the rule
    """
    candidate = phonetic + target
    if '[' not in candidate: # no attributes so we need test no further
        return candidate

    # expand the result, converting incompatible attributes to [0]
    candidate = expand_alternates(candidate);
    candidate_array = candidate.split('|')

    # drop each alternative that has incompatible attributes
    candidate = ''
    found = False

    for i in _range(len(candidate_array)):
        this_candidate = candidate_array[i]
        if language_arg != 1:
            this_candidate = normalize_language_attributes(this_candidate + '[' + str(language_arg) + ']', False)
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
        candidate = '('+candidate+')'
    return candidate


def language_index_from_code(code, name_mode):
    """Return the index value for a language code (or l_any if more than one
    is specified or the code is out of bounds)

    Arguments:
    code -- the language code to interpret
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    """
    if (code < 1 or
        code > sum([lang_dict[_] for _ in
                    bmdata[name_mode]['languages']])): # code out of range
        return l_any
    if ((code & (code - 1)) != 0): # choice was more than one language; use any
        return l_any
    return code


def bmpm(word, language_arg=0, name_mode='gen', match_mode='approx',
         concat=False, filter_langs=False):
    """Return the Beider-Morse Phonetic Matching algorithm encoding(s) of a
    term

    Arguments:
    word -- the term to which to apply the Beider-Morse Phonetic Matching
                algorithm
    language_arg -- the language of the term; supported values include:
                "any", "arabic", "cyrillic", "czech", "dutch", "english",
                "french", "german", "greek", "greeklatin", "hebrew",
                "hungarian", "italian", "polish", "portuguese","romanian",
                "russian", "spanish", "turkish"
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    match_mode -- matching mode: 'approx' or 'exact'
    concat -- concatenation mode
    filter_langs -- filter out incompatible languages

    Description:
    The Beider-Morse Phonetic Matching algorithm is described at:
    http://stevemorse.org/phonetics/bmpm.htm
    The reference implementation is licensed under GPLv3 and available at:
    http://stevemorse.org/phoneticinfo.htm
    """
    word = unicodedata.normalize('NFC', _unicode(word.strip().lower()))

    name_mode = name_mode.strip().lower()[:3]
    if name_mode not in set(['ash', 'sep', 'gen']):
        name_mode = 'gen'

    if match_mode != 'exact':
        match_mode = 'approx'

    # Translate the supplied language_arg value into an integer representing
    # a set of languages
    all_langs = sum([lang_dict[_] for _ in bmdata[name_mode]['languages']])
    lang_choices = 0
    if isinstance(language_arg, (int, float, _long)):
        lang_choices = int(language_arg)
    elif language_arg != '' and isinstance(language_arg, (_unicode, str)):
        for lang in language_arg.lower().split(','):
            if lang in lang_dict and (lang_dict[lang] & all_langs):
                lang_choices += lang_dict[lang]
            elif not filter_langs:
                raise ValueError('Unknown \'' + name_mode + '\' language: \'' +
                                 lang + '\'')

    # Language choices are either all incompatible with the name mode or
    # no choices were given, so try to autodetect
    if lang_choices == 0:
        language_arg = language(word, name_mode)
    else:
        language_arg = lang_choices
    language_arg2 = language_index_from_code(language_arg, name_mode)

    print language_arg, language_arg

    rules = bmdata[name_mode]['rules'][language_arg2]
    final_rules1 = bmdata[name_mode][match_mode]['common']
    final_rules2 = bmdata[name_mode][match_mode][language_arg2]

    print str(language_arg) + ' ' + name_mode
    result = phonetic(word, name_mode, rules, final_rules1,
                      final_rules2, language_arg, concat)
    print 'Results: ' + result
    result = phonetic_numbers(result)
    print 'after numbers: ' + result
    return result
