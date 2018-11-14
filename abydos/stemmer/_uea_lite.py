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

"""abydos.stemmer._uea_lite.

UEA-Lite stemmer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from re import match as re_match

from six.moves import range

from ._stemmer import _Stemmer

__all__ = ['UEALite', 'uealite']


class UEALite(_Stemmer):
    """UEA-Lite stemmer.

    The UEA-Lite stemmer is discussed in :cite:`Jenkins:2005`.

    This is chiefly based on the Java implementation of the algorithm, with
    variants based on the Perl implementation and Jason Adams' Ruby port.

    Java version: :cite:`Churchill:2005`
    Perl version: :cite:`Jenkins:2005`
    Ruby version: :cite:`Adams:2017`
    """

    _problem_words = {'is', 'as', 'this', 'has', 'was', 'during'}

    # rule table format:
    # top-level dictionary: length-of-suffix: dict-of-rules
    # dict-of-rules: suffix: (rule_no, suffix_length_to_delete,
    #                         suffix_to_append)
    _standard_rule_table = {
        7: {
            'titudes': (30, 1, None),
            'fulness': (34, 4, None),
            'ousness': (35, 4, None),
            'eadings': (40.7, 4, None),
            'oadings': (40.6, 4, None),
            'ealings': (42.4, 4, None),
            'ailings': (42.2, 4, None),
        },
        6: {
            'aceous': (1, 6, None),
            'aining': (24, 3, None),
            'acting': (25, 3, None),
            'ttings': (26, 5, None),
            'viding': (27, 3, 'e'),
            'ssings': (37, 4, None),
            'ulting': (38, 3, None),
            'eading': (40.7, 3, None),
            'oading': (40.6, 3, None),
            'edings': (40.5, 4, None),
            'ddings': (40.4, 5, None),
            'ldings': (40.3, 4, None),
            'rdings': (40.2, 4, None),
            'ndings': (40.1, 4, None),
            'llings': (41, 5, None),
            'ealing': (42.4, 3, None),
            'olings': (42.3, 4, None),
            'ailing': (42.2, 3, None),
            'elings': (42.1, 4, None),
            'mmings': (44.3, 5, None),
            'ngings': (45.2, 4, None),
            'ggings': (45.1, 5, None),
            'stings': (47, 4, None),
            'etings': (48.4, 4, None),
            'ntings': (48.2, 4, None),
            'irings': (54.4, 4, 'e'),
            'urings': (54.3, 4, 'e'),
            'ncings': (54.2, 4, 'e'),
            'things': (58.1, 1, None),
        },
        5: {
            'iases': (11.4, 2, None),
            'ained': (13.6, 2, None),
            'erned': (13.5, 2, None),
            'ifted': (14, 2, None),
            'ected': (15, 2, None),
            'vided': (16, 1, None),
            'erred': (19, 3, None),
            'urred': (20.5, 3, None),
            'lored': (20.4, 2, None),
            'eared': (20.3, 2, None),
            'tored': (20.2, 1, None),
            'noted': (22.4, 1, None),
            'leted': (22.3, 1, None),
            'anges': (23, 1, None),
            'tting': (26, 4, None),
            'ulted': (32, 2, None),
            'uming': (33, 3, 'e'),
            'rabed': (36.1, 1, None),
            'rebed': (36.1, 1, None),
            'ribed': (36.1, 1, None),
            'robed': (36.1, 1, None),
            'rubed': (36.1, 1, None),
            'ssing': (37, 3, None),
            'vings': (39, 4, 'e'),
            'eding': (40.5, 3, None),
            'dding': (40.4, 4, None),
            'lding': (40.3, 3, None),
            'rding': (40.2, 3, None),
            'nding': (40.1, 3, None),
            'dings': (40, 4, 'e'),
            'lling': (41, 4, None),
            'oling': (42.3, 3, None),
            'eling': (42.1, 3, None),
            'lings': (42, 4, 'e'),
            'mming': (44.3, 4, None),
            'rming': (44.2, 3, None),
            'lming': (44.1, 3, None),
            'mings': (44, 4, 'e'),
            'nging': (45.2, 3, None),
            'gging': (45.1, 4, None),
            'gings': (45, 4, 'e'),
            'aning': (46.6, 3, None),
            'ening': (46.5, 3, None),
            'gning': (46.4, 3, None),
            'nning': (46.3, 4, None),
            'oning': (46.2, 3, None),
            'rning': (46.1, 3, None),
            'sting': (47, 3, None),
            'eting': (48.4, 3, None),
            'pting': (48.3, 3, None),
            'nting': (48.2, 3, None),
            'cting': (48.1, 3, None),
            'tings': (48, 4, 'e'),
            'iring': (54.4, 3, 'e'),
            'uring': (54.3, 3, 'e'),
            'ncing': (54.2, 3, 'e'),
            'sings': (54, 4, 'e'),
            # 'lling': (55, 3, None),  # masked by 41
            'ating': (57, 3, 'e'),
            'thing': (58.1, 0, None),
        },
        4: {
            'eeds': (7, 1, None),
            'uses': (11.3, 1, None),
            'sses': (11.2, 2, None),
            'eses': (11.1, 2, 'is'),
            'tled': (12.5, 1, None),
            'pled': (12.4, 1, None),
            'bled': (12.3, 1, None),
            'eled': (12.2, 2, None),
            'lled': (12.1, 2, None),
            'ened': (13.7, 2, None),
            'rned': (13.4, 2, None),
            'nned': (13.3, 3, None),
            'oned': (13.2, 2, None),
            'gned': (13.1, 2, None),
            'ered': (20.1, 2, None),
            'reds': (20, 2, None),
            'tted': (21, 3, None),
            'uted': (22.2, 1, None),
            'ated': (22.1, 1, None),
            'ssed': (28, 2, None),
            'umed': (31, 1, None),
            'beds': (36, 3, None),
            'ving': (39, 3, 'e'),
            'ding': (40, 3, 'e'),
            'ling': (42, 3, 'e'),
            'nged': (43.2, 1, None),
            'gged': (43.1, 3, None),
            'ming': (44, 3, 'e'),
            'ging': (45, 3, 'e'),
            'ning': (46, 3, 'e'),
            'ting': (48, 3, 'e'),
            # 'ssed': (49, 2, None),  # masked by 28
            # 'lled': (53, 2, None),  # masked by 12.1
            'zing': (54.1, 3, 'e'),
            'sing': (54, 3, 'e'),
            'lves': (60.1, 3, 'f'),
            'aped': (61.3, 1, None),
            'uded': (61.2, 1, None),
            'oded': (61.1, 1, None),
            # 'ated': (61, 1, None),  # masked by 22.1
            'ones': (63.6, 1, None),
            'izes': (63.5, 1, None),
            'ures': (63.4, 1, None),
            'ines': (63.3, 1, None),
            'ides': (63.2, 1, None),
        },
        3: {
            'ces': (2, 1, None),
            'sis': (4, 0, None),
            'tis': (5, 0, None),
            'eed': (7, 0, None),
            'ued': (8, 1, None),
            'ues': (9, 1, None),
            'ees': (10, 1, None),
            'ses': (11, 1, None),
            'led': (12, 2, None),
            'ned': (13, 1, None),
            'ved': (17, 1, None),
            'ced': (18, 1, None),
            'red': (20, 1, None),
            'ted': (22, 2, None),
            'sed': (29, 1, None),
            'bed': (36, 2, None),
            'ged': (43, 1, None),
            'les': (50, 1, None),
            'tes': (51, 1, None),
            'zed': (52, 1, None),
            'ied': (56, 3, 'y'),
            'ies': (59, 3, 'y'),
            'ves': (60, 1, None),
            'pes': (63.8, 1, None),
            'mes': (63.7, 1, None),
            'ges': (63.1, 1, None),
            'ous': (65, 0, None),
            'ums': (66, 0, None),
        },
        2: {
            'cs': (3, 0, None),
            'ss': (6, 0, None),
            'es': (63, 2, None),
            'is': (64, 2, 'e'),
            'us': (67, 0, None),
        },
    }

    _perl_rule_table = {
        7: {
            'titudes': (30, 1, None),
            'fulness': (34, 4, None),
            'ousness': (35, 4, None),
        },
        6: {
            'aceous': (1, 6, None),
            'aining': (24, 3, None),
            'acting': (25, 3, None),
            'viding': (27, 3, 'e'),
            'ulting': (38, 3, None),
            'eading': (40.7, 3, None),
            'oading': (40.6, 3, None),
            'ealing': (42.4, 3, None),
            'ailing': (42.2, 3, None),
        },
        5: {
            'iases': (11.4, 2, None),
            'ained': (13.6, 2, None),
            'erned': (13.5, 2, None),
            'ifted': (14, 2, None),
            'ected': (15, 2, None),
            'vided': (16, 1, None),
            'erred': (19, 3, None),
            'urred': (20.5, 3, None),
            'lored': (20.4, 2, None),
            'eared': (20.3, 2, None),
            'tored': (20.2, 1, None),
            'noted': (22.4, 1, None),
            'leted': (22.3, 1, None),
            'anges': (23, 1, None),
            'tting': (26, 4, None),
            'ulted': (32, 2, None),
            'uming': (33, 3, 'e'),
            'rabed': (36.1, 1, None),
            'rebed': (36.1, 1, None),
            'ribed': (36.1, 1, None),
            'robed': (36.1, 1, None),
            'rubed': (36.1, 1, None),
            'ssing': (37, 3, None),
            'eding': (40.5, 3, None),
            'dding': (40.4, 4, None),
            'lding': (40.3, 3, None),
            'rding': (40.2, 3, None),
            'nding': (40.1, 3, None),
            'lling': (41, 4, None),
            'oling': (42.3, 3, None),
            'eling': (42.1, 3, None),
            'mming': (44.3, 4, None),
            'rming': (44.2, 3, None),
            'lming': (44.1, 3, None),
            'nging': (45.2, 3, None),
            'gging': (45.1, 4, None),
            'aning': (46.6, 3, None),
            'ening': (46.5, 3, None),
            'gning': (46.4, 3, None),
            'nning': (46.3, 4, None),
            'oning': (46.2, 3, None),
            'rning': (46.1, 3, None),
            'sting': (47, 3, None),
            'eting': (48.4, 3, None),
            'pting': (48.3, 3, None),
            'nting': (48.2, 3, None),
            'cting': (48.1, 3, None),
            'iring': (54.4, 3, 'e'),
            'uring': (54.3, 3, 'e'),
            'ncing': (54.2, 3, 'e'),
            # 'lling': (55, 3, None),  # masked by 41
            'ating': (57, 3, 'e'),
            'thing': (58.1, 0, None),
        },
        4: {
            'uses': (11.3, 1, None),
            'sses': (11.2, 2, None),
            'eses': (11.1, 2, 'is'),
            'tled': (12.5, 1, None),
            'pled': (12.4, 1, None),
            'bled': (12.3, 1, None),
            'eled': (12.2, 2, None),
            'lled': (12.1, 2, None),
            'ened': (13.7, 2, None),
            'rned': (13.4, 2, None),
            'nned': (13.3, 3, None),
            'oned': (13.2, 2, None),
            'gned': (13.1, 2, None),
            'ered': (20.1, 2, None),
            'tted': (21, 3, None),
            'uted': (22.2, 1, None),
            'ated': (22.1, 1, None),
            'ssed': (28, 2, None),
            'umed': (31, 1, None),
            'ving': (39, 3, 'e'),
            'ding': (40, 3, 'e'),
            'ling': (42, 3, 'e'),
            'nged': (43.2, 1, None),
            'gged': (43.1, 3, None),
            'ming': (44, 3, 'e'),
            'ging': (45, 3, 'e'),
            'ning': (46, 3, 'e'),
            'ting': (48, 3, 'e'),
            # 'ssed': (49, 2, None),  # masked by 28
            # 'lled': (53, 2, None),  # masked by 12.1
            'zing': (54.1, 3, 'e'),
            'sing': (54, 3, 'e'),
            'lves': (60.1, 3, 'f'),
            'aped': (61.3, 1, None),
            'uded': (61.2, 1, None),
            'oded': (61.1, 1, None),
            # 'ated': (61, 1, None),  # masked by 22.1
            'ones': (63.6, 1, None),
            'izes': (63.5, 1, None),
            'ures': (63.4, 1, None),
            'ines': (63.3, 1, None),
            'ides': (63.2, 1, None),
        },
        3: {
            'ces': (2, 1, None),
            'sis': (4, 0, None),
            'tis': (5, 0, None),
            'eed': (7, 0, None),
            'ued': (8, 1, None),
            'ues': (9, 1, None),
            'ees': (10, 1, None),
            'ses': (11, 1, None),
            'led': (12, 2, None),
            'ned': (13, 1, None),
            'ved': (17, 1, None),
            'ced': (18, 1, None),
            'red': (20, 1, None),
            'ted': (22, 2, None),
            'sed': (29, 1, None),
            'bed': (36, 2, None),
            'ged': (43, 1, None),
            'les': (50, 1, None),
            'tes': (51, 1, None),
            'zed': (52, 1, None),
            'ied': (56, 3, 'y'),
            'ies': (59, 3, 'y'),
            'ves': (60, 1, None),
            'pes': (63.8, 1, None),
            'mes': (63.7, 1, None),
            'ges': (63.1, 1, None),
            'ous': (65, 0, None),
            'ums': (66, 0, None),
        },
        2: {
            'cs': (3, 0, None),
            'ss': (6, 0, None),
            'es': (63, 2, None),
            'is': (64, 2, 'e'),
            'us': (67, 0, None),
        },
    }

    _adams_rule_table = {
        7: {
            'titudes': (30, 1, None),
            'fulness': (34, 4, None),
            'ousness': (35, 4, None),
            'eadings': (40.7, 4, None),
            'oadings': (40.6, 4, None),
            'ealings': (42.4, 4, None),
            'ailings': (42.2, 4, None),
        },
        6: {
            'aceous': (1, 6, None),
            'aining': (24, 3, None),
            'acting': (25, 3, None),
            'ttings': (26, 5, None),
            'viding': (27, 3, 'e'),
            'ssings': (37, 4, None),
            'ulting': (38, 3, None),
            'eading': (40.7, 3, None),
            'oading': (40.6, 3, None),
            'edings': (40.5, 4, None),
            'ddings': (40.4, 5, None),
            'ldings': (40.3, 4, None),
            'rdings': (40.2, 4, None),
            'ndings': (40.1, 4, None),
            'llings': (41, 5, None),
            'ealing': (42.4, 3, None),
            'olings': (42.3, 4, None),
            'ailing': (42.2, 3, None),
            'elings': (42.1, 4, None),
            'mmings': (44.3, 5, None),
            'ngings': (45.2, 4, None),
            'ggings': (45.1, 5, None),
            'stings': (47, 4, None),
            'etings': (48.4, 4, None),
            'ntings': (48.2, 4, None),
            'irings': (54.4, 4, 'e'),
            'urings': (54.3, 4, 'e'),
            'ncings': (54.2, 4, 'e'),
            'things': (58.1, 1, None),
            'chited': (22.8, 1, None),
        },
        5: {
            'iases': (11.4, 2, None),
            'ained': (13.6, 2, None),
            'erned': (13.5, 2, None),
            'ifted': (14, 2, None),
            'ected': (15, 2, None),
            # 'vided': (16, 1, None),
            'erred': (19, 3, None),
            'urred': (20.5, 3, None),
            'lored': (20.4, 2, None),
            'eared': (20.3, 2, None),
            'tored': (20.2, 1, None),
            'noted': (22.4, 1, None),
            'leted': (22.3, 1, None),
            'anges': (23, 1, None),
            'tting': (26, 4, None),
            'ulted': (32, 2, None),
            'uming': (33, 3, 'e'),
            'rabed': (36.1, 1, None),
            'rebed': (36.1, 1, None),
            'ribed': (36.1, 1, None),
            'robed': (36.1, 1, None),
            'rubed': (36.1, 1, None),
            'ssing': (37, 3, None),
            'vings': (39, 4, 'e'),
            'eding': (40.5, 3, None),
            'dding': (40.4, 4, None),
            'lding': (40.3, 3, None),
            'rding': (40.2, 3, None),
            'nding': (40.1, 3, None),
            'dings': (40, 4, 'e'),
            'lling': (41, 4, None),
            'oling': (42.3, 3, None),
            'eling': (42.1, 3, None),
            'lings': (42, 4, 'e'),
            'mming': (44.3, 4, None),
            'rming': (44.2, 3, None),
            'lming': (44.1, 3, None),
            'mings': (44, 4, 'e'),
            'nging': (45.2, 3, None),
            'gging': (45.1, 4, None),
            'gings': (45, 4, 'e'),
            'aning': (46.6, 3, None),
            'ening': (46.5, 3, None),
            'gning': (46.4, 3, None),
            'nning': (46.3, 4, None),
            'oning': (46.2, 3, None),
            'rning': (46.1, 3, None),
            'sting': (47, 3, None),
            'eting': (48.4, 3, None),
            'pting': (48.3, 3, None),
            'nting': (48.2, 3, None),
            'cting': (48.1, 3, None),
            'tings': (48, 4, 'e'),
            'iring': (54.4, 3, 'e'),
            'uring': (54.3, 3, 'e'),
            'ncing': (54.2, 3, 'e'),
            'sings': (54, 4, 'e'),
            # 'lling': (55, 3, None),  # masked by 41
            'ating': (57, 3, 'e'),
            'thing': (58.1, 0, None),
            'dying': (58.2, 4, 'ie'),
            'tying': (58.2, 4, 'ie'),
            'vited': (22.6, 1, None),
            'mited': (22.5, 1, None),
            'vided': (22.9, 1, None),
            'mided': (22.10, 1, None),
            'lying': (58.2, 4, 'ie'),
            'arred': (19.1, 3, None),
        },
        4: {
            'eeds': (7, 1, None),
            'uses': (11.3, 1, None),
            'sses': (11.2, 2, None),
            'eses': (11.1, 2, 'is'),
            'tled': (12.5, 1, None),
            'pled': (12.4, 1, None),
            'bled': (12.3, 1, None),
            'eled': (12.2, 2, None),
            'lled': (12.1, 2, None),
            'ened': (13.7, 2, None),
            'rned': (13.4, 2, None),
            'nned': (13.3, 3, None),
            'oned': (13.2, 2, None),
            'gned': (13.1, 2, None),
            'ered': (20.1, 2, None),
            'reds': (20, 2, None),
            'tted': (21, 3, None),
            'uted': (22.2, 1, None),
            'ated': (22.1, 1, None),
            'ssed': (28, 2, None),
            'umed': (31, 1, None),
            'beds': (36, 3, None),
            'ving': (39, 3, 'e'),
            'ding': (40, 3, 'e'),
            'ling': (42, 3, 'e'),
            'nged': (43.2, 1, None),
            'gged': (43.1, 3, None),
            'ming': (44, 3, 'e'),
            'ging': (45, 3, 'e'),
            'ning': (46, 3, 'e'),
            'ting': (48, 3, 'e'),
            # 'ssed': (49, 2, None),  # masked by 28
            # 'lled': (53, 2, None),  # masked by 12.1
            'zing': (54.1, 3, 'e'),
            'sing': (54, 3, 'e'),
            'lves': (60.1, 3, 'f'),
            'aped': (61.3, 1, None),
            'uded': (61.2, 1, None),
            'oded': (61.1, 1, None),
            # 'ated': (61, 1, None),  # masked by 22.1
            'ones': (63.6, 1, None),
            'izes': (63.5, 1, None),
            'ures': (63.4, 1, None),
            'ines': (63.3, 1, None),
            'ides': (63.2, 1, None),
            'ited': (22.7, 2, None),
            'oked': (31.1, 1, None),
            'aked': (31.1, 1, None),
            'iked': (31.1, 1, None),
            'uked': (31.1, 1, None),
            'amed': (31, 1, None),
            'imed': (31, 1, None),
            'does': (31.2, 2, None),
        },
        3: {
            'ces': (2, 1, None),
            'sis': (4, 0, None),
            'tis': (5, 0, None),
            'eed': (7, 0, None),
            'ued': (8, 1, None),
            'ues': (9, 1, None),
            'ees': (10, 1, None),
            'ses': (11, 1, None),
            'led': (12, 2, None),
            'ned': (13, 1, None),
            'ved': (17, 1, None),
            'ced': (18, 1, None),
            'red': (20, 1, None),
            'ted': (22, 2, None),
            'sed': (29, 1, None),
            'bed': (36, 2, None),
            'ged': (43, 1, None),
            'les': (50, 1, None),
            'tes': (51, 1, None),
            'zed': (52, 1, None),
            'ied': (56, 3, 'y'),
            'ies': (59, 3, 'y'),
            'ves': (60, 1, None),
            'pes': (63.8, 1, None),
            'mes': (63.7, 1, None),
            'ges': (63.1, 1, None),
            'ous': (65, 0, None),
            'ums': (66, 0, None),
            'oed': (31.3, 1, None),
            'oes': (31.2, 1, None),
            'kes': (63.1, 1, None),
            'des': (63.10, 1, None),
            'res': (63.9, 1, None),
        },
        2: {
            'cs': (3, 0, None),
            'ss': (6, 0, None),
            'es': (63, 2, None),
            'is': (64, 2, 'e'),
            'us': (67, 0, None),
        },
    }

    _rules = {
        'standard': _standard_rule_table,
        'Adams': _adams_rule_table,
        'Perl': _perl_rule_table,
    }

    def stem(
        self,
        word,
        max_word_length=20,
        max_acro_length=8,
        return_rule_no=False,
        var='standard',
    ):
        """Return UEA-Lite stem.

        Parameters
        ----------
        word : str
            The word to stem
        max_word_length : int
            The maximum word length allowed
        max_acro_length : int
            The maximum acronym length allowed
        return_rule_no : bool
            If True, returns the stem along with rule number
        var : str
            Variant rules to use:

                - ``Adams`` to use Jason Adams' rules
                - ``Perl`` to use the original Perl rules

        Returns
        -------
        str or (str, int)
            Word stem

        Examples
        --------
        >>> uealite('readings')
        'read'
        >>> uealite('insulted')
        'insult'
        >>> uealite('cussed')
        'cuss'
        >>> uealite('fancies')
        'fancy'
        >>> uealite('eroded')
        'erode'

        """

        def _stem_with_duplicate_character_check(word, del_len):
            if word[-1] == 's':
                del_len += 1
            stemmed_word = word[:-del_len]
            if re_match(r'.*(\w)\1$', stemmed_word):
                stemmed_word = stemmed_word[:-1]
            return stemmed_word

        def _stem(word):
            stemmed_word = word
            rule_no = 0

            if not word:
                return word, 0
            if word in self._problem_words or (
                word == 'menses' and var == 'Adams'
            ):
                return word, 90
            if max_word_length and len(word) > max_word_length:
                return word, 95

            if "'" in word:
                if word[-2:] in {"'s", "'S"}:
                    stemmed_word = word[:-2]
                if word[-1:] == "'":
                    stemmed_word = word[:-1]
                stemmed_word = stemmed_word.replace("n't", 'not')
                stemmed_word = stemmed_word.replace("'ve", 'have')
                stemmed_word = stemmed_word.replace("'re", 'are')
                stemmed_word = stemmed_word.replace("'m", 'am')
                return stemmed_word, 94

            if word.isdigit():
                return word, 90.3
            else:
                hyphen = word.find('-')
                if len(word) > hyphen > 0:
                    if (
                        word[:hyphen].isalpha()
                        and word[hyphen + 1 :].isalpha()
                    ):
                        return word, 90.2
                    else:
                        return word, 90.1
                elif '_' in word:
                    return word, 90
                elif word[-1] == 's' and word[:-1].isupper():
                    if var == 'Adams' and len(word) - 1 > max_acro_length:
                        return word, 96
                    return word[:-1], 91.1
                elif word.isupper():
                    if var == 'Adams' and len(word) > max_acro_length:
                        return word, 96
                    return word, 91
                elif re_match(r'^.*[A-Z].*[A-Z].*$', word):
                    return word, 92
                elif word[0].isupper():
                    return word, 93
                elif var == 'Adams' and re_match(
                    r'^[a-z](|[rl])(ing|ed)$', word
                ):
                    return word, 97

            for n in range(7, 1, -1):
                if word[-n:] in self._rules[var][n]:
                    rule_no, del_len, add_str = self._rules[var][n][word[-n:]]
                    if del_len:
                        stemmed_word = word[:-del_len]
                    else:
                        stemmed_word = word
                    if add_str:
                        stemmed_word += add_str
                    break

            if not rule_no:
                if re_match(r'.*\w\wings?$', word):  # rule 58
                    stemmed_word = _stem_with_duplicate_character_check(
                        word, 3
                    )
                    rule_no = 58
                elif re_match(r'.*\w\weds?$', word):  # rule 62
                    stemmed_word = _stem_with_duplicate_character_check(
                        word, 2
                    )
                    rule_no = 62
                elif word[-1] == 's':  # rule 68
                    stemmed_word = word[:-1]
                    rule_no = 68

            return stemmed_word, rule_no

        stem, rule_no = _stem(word)
        if return_rule_no:
            return stem, rule_no
        return stem


def uealite(
    word,
    max_word_length=20,
    max_acro_length=8,
    return_rule_no=False,
    var='standard',
):
    """Return UEA-Lite stem.

    This is a wrapper for :py:meth:`UEALite.stem`.

    Parameters
    ----------
    word : str
        The word to stem
    max_word_length : int
        The maximum word length allowed
    max_acro_length : int
        The maximum acronym length allowed
    return_rule_no : bool
        If True, returns the stem along with rule number
    var : str
        Variant rules to use:

            - ``Adams`` to use Jason Adams' rules
            - ``Perl`` to use the original Perl rules

    Returns
    -------
    str or (str, int)
        Word stem

    Examples
    --------
    >>> uealite('readings')
    'read'
    >>> uealite('insulted')
    'insult'
    >>> uealite('cussed')
    'cuss'
    >>> uealite('fancies')
    'fancy'
    >>> uealite('eroded')
    'erode'

    """
    return UEALite().stem(
        word, max_word_length, max_acro_length, return_rule_no, var
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
