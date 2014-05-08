# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import numpy
import sys
import abydos.util

def levenshtein(s, t, mode='lev', cost=(1,1,1,1)):
    """Return the Levenshtein distance between two string arguments

    Arguments:
    s, t -- two strings to be compared
    mode -- specifies a mode for computing the Levenshtein distance:
              'lev' (default) computes the ordinary Levenshtein distance,
                in which edits may include inserts, deletes, and substitutions
              'osa' computes the Optimal String Alignment distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions but substrings may only be edited once
              'dam' computes the Damerau-Levenshtein distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions and substrings may undergo repeated edits
    cost -- a 4-tuple representing the cost of the four possible edits:
              inserts, deletes, substitutions, and transpositions,
              respectively (by default: (1,1,1,1))
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if len(s) == 0:
        return len(t) * ins_cost
    if len(t) == 0:
        return len(s) * del_cost
    
    if 'dam' not in mode:
        d = numpy.zeros((len(s)+1)*(len(t)+1), dtype=numpy.int).reshape((len(s)+1, len(t)+1))
        for i in xrange(len(s)+1):
            d[i,0] = i
        for j in xrange(len(t)+1):
            d[0,j] = j

        for i in xrange(len(s)):
            for j in xrange(len(t)):
                d[i+1,j+1] = min(
                    d[i+1,j] + ins_cost, # ins
                    d[i,j+1] + del_cost, # del
                    d[i,j] + (sub_cost if s[i] != t[j] else 0) # sub (or equal)
                )

                if mode=='osa':
                    if (i+1 > 1 and j+1 > 1 and s[i] == t[j-1] and s[i-1] == t[j]):
                        d[i+1,j+1] = min(
                            d[i+1,j+1],
                            d[i-1,j-1] + trans_cost  # transposition
                        )

        return d[len(s),len(t)]

    else:
        """Damerau-Levenshtein code based on Java code by Kevin L. Stern,
        under the MIT license:
        https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java"""
        if 2*trans_cost < ins_cost + del_cost:
            raise ValueError('Unsupported cost assignment; the cost of two transpositions must not be less than the cost of an insert plus a delete.')

        d = numpy.zeros((len(s))*(len(t)), dtype=numpy.int).reshape((len(s), len(t)))
        
        if s[0] != t[0]:
            d[0,0] = min(sub_cost, ins_cost + del_cost)
        
        s_index_by_character = {}
        s_index_by_character[s[0]] = 0
        for i in xrange(1, len(s)):
            del_distance = d[i-1,0] + del_cost
            ins_distance = (i+1) * del_cost + ins_cost
            match_distance = i * del_cost + (0 if s[i] == t[0] else sub_cost)
            d[i,0] = min(del_distance, ins_distance, match_distance)

        for j in xrange(1, len(t)):
            del_distance = (j+1) * ins_cost + del_cost
            ins_distance = d[0,j-1] + ins_cost
            match_distance = j * ins_cost + (0 if s[0] == t[j] else sub_cost)
            d[0,j] = min(del_distance, ins_distance, match_distance)

        for i in xrange(1, len(s)):
            max_s_letter_match_index = (0 if s[i] == t[0] else -1)
            for j in xrange(1, len(t)):
                candidate_swap_index = -1 if t[j] not in s_index_by_character else s_index_by_character[t[j]]
                j_swap = max_s_letter_match_index
                del_distance = d[i-1,j] + del_cost
                ins_distance = d[i,j-1] + ins_cost
                match_distance = d[i-1,j-1]
                if s[i] != t[j]:
                    match_distance += sub_cost
                else:
                    max_s_letter_match_index = j

                if candidate_swap_index != -1 and j_swap != -1:
                    i_swap = candidate_swap_index
                    
                    if i_swap == 0 and j_swap == 0:
                        pre_swap_cost = 0
                    else:
                        pre_swap_cost = d[max(0, i_swap-1), max(0, j_swap-1)]
                    swap_distance = pre_swap_cost + (i - i_swap - 1) * del_cost + (j - j_swap - 1) * ins_cost + trans_cost
                else:
                    swap_distance = sys.maxint

                d[i,j] = min(del_distance, ins_distance, match_distance, swap_distance)
            s_index_by_character[s[i]] = i

        return d[len(s)-1, len(t)-1]

    

def hamming(s, t, allow_different_lengths=False):
    """Return the hamming distance between two string arguments.

    Arguments:
    s, t -- two strings to be compared
    allow_different_lengths --
      If False, an exception is raised in the case of strings of unequal
      lengths.
      If True, this returns the hamming distance for those characters that
      have a matching character in both strings plus the difference in the
      strings' lengths. This is equivalent to  extending the shorter string
      with obligatoriliy non-matching characters.
    """
    if not allow_different_lengths and len(s) != len(t):
        raise ValueError("Undefined for sequences of unequal length; set allow_different_lengths to True for Hamming distance between strings of unequal lengths.")        
    dist = 0
    if allow_different_lengths:
        dist += abs(len(s)-len(t))
    dist += sum(c1 != c2 for c1, c2 in zip(s, t))
    return dist

def sorensen(s, t, q=2):
    """Return the Sørensen–Dice coefficient of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    The coefficient is calculated according to the formula:
    coefficient = 2*(common q-grams in s & t)/((q-grams in s)+(q-grams in t))
    This measure is irrespective of q-gram alignment/ordering.
    """
    if s == t:
        return 1.0
    q_s, q_t, q_common = abydos.util.qgram_counts(s, t, q)
    return 2 * q_common / (q_s + q_t)

def jaccard(s, t, q=2):
    """Return the Jaccard similarity coefficient of two string arguments.

    Arguments:
    s, t -- two strings to be compared

    Description:
    The coefficient is calcaulated according to the formula:
    coefficient = intersection of q-gram sets / union of q-gram sets
    """
    if s == t:
        return 1.0
    elif len(s) == 0 and len(t) == 0:
        return 1.0
    q_s, q_t, q_common = abydos.util.qgram_counts(s, t, q)
    return q_common / (q_s + q_t - q_common)
