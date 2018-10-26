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

"""abydos.tests.phonetic.test_phonetic_bmpm.

This module contains unit tests for abydos.phonetic._bmpm
"""

from __future__ import unicode_literals

import codecs
import unittest

from abydos.phonetic import bmpm

# noinspection PyProtectedMember
from abydos.phonetic._bmdata import (
    L_ANY,
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
    L_POLISH,
    L_PORTUGUESE,
    L_ROMANIAN,
    L_SPANISH,
    L_TURKISH,
)

# noinspection PyProtectedMember
from abydos.phonetic._bmpm import (
    _bm_apply_rule_if_compat,
    _bm_expand_alternates,
    _bm_language,
    _bm_normalize_lang_attrs,
    _bm_phonetic_number,
    _bm_remove_dupes,
)


from six import text_type

from .. import ALLOW_RANDOM, _corpus_file, _one_in


class BeiderMorseTestCases(unittest.TestCase):
    """Test BMPM functions.

    test cases for abydos.phonetic._bmpm.bmpm, ._phonetic_number,
    ._bm_apply_rule_if_compat, ._bm_language, ._bm_expand_alternates,
    ._bm_remove_dupes, ._bm_normalize_lang_attrs
    """

    def test_bmpm(self):
        """Test abydos.phonetic._bmpm.bmpm.

        Most test cases from:
        http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/bm/

        As a rule, the test cases are copied from the above code, but the
        resultant values are not. This is largely because this Python port
        follows the PHP reference implementation much more closely than the
        Java port in Apache Commons Codec does. As a result, these tests have
        been conformed to the output produced by the PHP implementation,
        particularly in terms of formatting and ordering.
        """
        # base cases
        self.assertEqual(bmpm(''), '')

        for langs in ('', 1, 'spanish', 'english,italian', 3):
            for name_mode in ('gen', 'ash', 'sep'):
                for match_mode in ('approx', 'exact'):
                    for concat in (False, True):
                        if isinstance(langs, text_type) and (
                            (name_mode == 'ash' and 'italian' in langs)
                            or (name_mode == 'sep' and 'english' in langs)
                        ):
                            self.assertRaises(
                                ValueError,
                                bmpm,
                                '',
                                langs,
                                name_mode,
                                match_mode,
                                concat,
                            )
                        else:
                            self.assertEqual(
                                bmpm('', langs, name_mode, match_mode, concat),
                                '',
                            )

        # testSolrGENERIC
        # concat is true, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'gen', 'exact', True),
            'angelo anxelo anhelo anjelo anZelo andZelo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'gen', 'exact', True),
            'angelo anxelo anhelo anjelo anZelo andZelo dangelo'
            + ' danxelo danhelo danjelo danZelo dandZelo',
        )
        self.assertEqual(
            bmpm('Angelo', 'italian,greek,spanish', 'gen', 'exact', True),
            'angelo anxelo andZelo',
        )
        self.assertEqual(bmpm('1234', '', 'gen', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'gen', 'exact', False),
            'angelo anxelo anhelo anjelo anZelo andZelo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'gen', 'exact', False),
            'angelo anxelo anhelo anjelo anZelo andZelo dangelo'
            + ' danxelo danhelo danjelo danZelo dandZelo',
        )
        self.assertEqual(
            bmpm('Angelo', 'italian,greek,spanish', 'gen', 'exact', False),
            'angelo anxelo andZelo',
        )
        self.assertEqual(bmpm('1234', '', 'gen', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'gen', 'approx', True),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'gen', 'approx', True),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo dangilo dangYlo dagilo dongilo'
            + ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo'
            + ' danilo donilo daniilo doniilo danzilo donzilo',
        )
        self.assertEqual(
            bmpm('Angelo', 'italian,greek,spanish', 'gen', 'approx', True),
            'angilo ongilo anxilo onxilo anzilo onzilo',
        )
        self.assertEqual(bmpm('1234', '', 'gen', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'gen', 'approx', False),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'gen', 'approx', False),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo dangilo dangYlo dagilo dongilo'
            + ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo'
            + ' danilo donilo daniilo doniilo danzilo donzilo',
        )
        self.assertEqual(
            bmpm('Angelo', 'italian,greek,spanish', 'gen', 'approx', False),
            'angilo ongilo anxilo onxilo anzilo onzilo',
        )
        self.assertEqual(bmpm('1234', '', 'gen', 'approx', False), '')

        # testSolrASHKENAZI
        # concat is true, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'ash', 'exact', True),
            'angelo andZelo anhelo anxelo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'ash', 'exact', True),
            'dangelo dandZelo danhelo danxelo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'ash',
            'exact',
            True,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'ash', 'exact', True, True
            ),
            'anxelo angelo',
        )
        self.assertEqual(bmpm('1234', '', 'ash', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'ash', 'exact', False),
            'angelo andZelo anhelo anxelo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'ash', 'exact', False),
            'dangelo dandZelo danhelo danxelo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'ash',
            'exact',
            False,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'ash', 'exact', False, True
            ),
            'anxelo angelo',
        )
        self.assertEqual(bmpm('1234', '', 'ash', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'ash', 'approx', True),
            'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo'
            + ' onzilo anilo onilo anxilo onxilo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'ash', 'approx', True),
            'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo'
            + ' danzilo donzilo danilo donilo danxilo donxilo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'ash',
            'approx',
            True,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'ash', 'approx', True, True
            ),
            'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' + ' ongilo',
        )
        self.assertEqual(bmpm('1234', '', 'ash', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'ash', 'approx', False),
            'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo'
            + ' onzilo anilo onilo anxilo onxilo',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'ash', 'approx', False),
            'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo'
            + ' danzilo donzilo danilo donilo danxilo donxilo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'ash',
            'approx',
            False,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'ash', 'approx', False, True
            ),
            'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' + ' ongilo',
        )
        self.assertEqual(bmpm('1234', '', 'ash', 'approx', False), '')

        # testSolrSEPHARDIC
        # concat is true, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'sep', 'exact', True), 'anZelo andZelo anxelo'
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'sep', 'exact', True),
            'anZelo andZelo anxelo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'sep',
            'exact',
            True,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'sep', 'exact', True, True
            ),
            'andZelo anxelo',
        )
        self.assertEqual(bmpm('1234', '', 'sep', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(
            bmpm('Angelo', '', 'sep', 'exact', False), 'anZelo andZelo anxelo'
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'sep', 'exact', False),
            'anZelo andZelo anxelo',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'sep',
            'exact',
            False,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'sep', 'exact', False, True
            ),
            'andZelo anxelo',
        )
        self.assertEqual(bmpm('1234', '', 'sep', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'sep', 'approx', True),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'sep', 'approx', True),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'sep',
            'approx',
            True,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'sep', 'approx', True, True
            ),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(bmpm('1234', '', 'sep', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(
            bmpm('Angelo', '', 'sep', 'approx', False),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            bmpm('D\'Angelo', '', 'sep', 'approx', False),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertRaises(
            ValueError,
            bmpm,
            'Angelo',
            'italian,greek,spanish',
            'sep',
            'approx',
            False,
        )
        self.assertEqual(
            bmpm(
                'Angelo', 'italian,greek,spanish', 'sep', 'approx', False, True
            ),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(bmpm('1234', '', 'sep', 'approx', False), '')

        # testCompatibilityWithOriginalVersion
        self.assertEqual(
            bmpm('abram', '', 'gen', 'approx', False),
            'abram abrom avram avrom obram obrom ovram ovrom'
            + ' Ybram Ybrom abran abron obran obron',
        )
        self.assertEqual(
            bmpm('Bendzin', '', 'gen', 'approx', False),
            'binzn bindzn vindzn bintsn vintsn',
        )
        self.assertEqual(
            bmpm('abram', '', 'ash', 'approx', False),
            'abram abrom avram avrom obram obrom ovram ovrom'
            + ' Ybram Ybrom ombram ombrom imbram imbrom',
        )
        self.assertEqual(
            bmpm('Halpern', '', 'ash', 'approx', False),
            'alpirn alpYrn olpirn olpYrn Ylpirn YlpYrn xalpirn' + ' xolpirn',
        )

        # PhoneticEngineTest
        self.assertEqual(
            bmpm('Renault', '', 'gen', 'approx', True),
            'rinolt rino rinDlt rinalt rinult rinD rina rinu',
        )
        self.assertEqual(
            bmpm('Renault', '', 'ash', 'approx', True),
            'rinDlt rinalt rinult rYnDlt rYnalt rYnult rinolt',
        )
        self.assertEqual(bmpm('Renault', '', 'sep', 'approx', True), 'rinDlt')
        self.assertEqual(
            bmpm('SntJohn-Smith', '', 'gen', 'exact', True), 'sntjonsmit'
        )
        self.assertEqual(
            bmpm('d\'ortley', '', 'gen', 'exact', True),
            'ortlaj ortlej dortlaj dortlej',
        )
        self.assertEqual(
            bmpm('van helsing', '', 'gen', 'exact', False),
            'helSink helsink helzink xelsink elSink elsink'
            + ' vanhelsink vanhelzink vanjelsink fanhelsink'
            + ' fanhelzink banhelsink',
        )

    def test_bmpm_misc(self):
        """Test abydos.phonetic._bmpm.bmpm (miscellaneous tests).

        The purpose of this test set is to achieve higher code coverage
        and to hit some of the test cases noted in the BMPM reference code.
        """
        # test of Ashkenazi with discardable prefix
        self.assertEqual(bmpm('bar Hayim', name_mode='ash'), 'Dm xDm')

        # tests of concat behavior
        self.assertEqual(
            bmpm('Rodham Clinton', concat=False),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )
        self.assertEqual(
            bmpm('Rodham Clinton', concat=True),
            'rodamklinton rodomklinton rodamklnton rodomklnton'
            + ' rodamklintun rodomklintun rodamklntun rodomklntun'
            + ' rodamtzlinton rodomtzlinton rodamtzlnton'
            + ' rodomtzlnton rodamtzlintun rodomtzlintun'
            + ' rodamtzlntun rodomtzlntun rodamzlinton'
            + ' rodomzlinton rodamzlnton rodomzlnton rodanklinton'
            + ' rodonklinton rodanklnton rodonklnton'
            + ' rodxamklinton rodxomklinton rodxamklnton'
            + ' rodxomklnton rodxanklinton rodxonklinton'
            + ' rodxanklnton rodxonklnton rudamklinton'
            + ' rudomklinton rudamklnton rudomklnton rudamklintun'
            + ' rudomklintun rudamklntun rudomklntun'
            + ' rudamtzlinton rudomtzlinton rudamtzlnton'
            + ' rudomtzlnton rudamtzlintun rudomtzlintun'
            + ' rudamtzlntun rudomtzlntun',
        )

        # tests of name_mode values
        self.assertEqual(bmpm('bar Hayim', name_mode='ash'), 'Dm xDm')
        self.assertEqual(bmpm('bar Hayim', name_mode='ashkenazi'), 'Dm xDm')
        self.assertEqual(bmpm('bar Hayim', name_mode='Ashkenazi'), 'Dm xDm')
        self.assertEqual(
            bmpm('bar Hayim', name_mode='gen', concat=True),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            bmpm('bar Hayim', name_mode='general', concat=True),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            bmpm('bar Hayim', name_mode='Mizrahi', concat=True),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            bmpm('bar Hayim', name_mode='mizrahi', concat=True),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            bmpm('bar Hayim', name_mode='miz', concat=True),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )

        # test that out-of-range language_arg results in L_ANY
        self.assertEqual(
            bmpm('Rodham Clinton', language_arg=2 ** 32),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )
        self.assertEqual(
            bmpm('Rodham Clinton', language_arg=-4),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )

        # etc. (for code coverage)
        self.assertEqual(bmpm('van Damme', name_mode='sep'), 'dami mi dam m')

    def test_bmpm_nachnamen(self):
        """Test abydos.phonetic._bmpm.bmpm (Nachnamen set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(
            _corpus_file('nachnamen.bm.csv'), encoding='utf-8'
        ) as nachnamen_testset:
            next(nachnamen_testset)
            for nn_line in nachnamen_testset:
                nn_line = nn_line.strip().split(',')
                # This test set is very large (~10000 entries)
                # so let's just randomly select about 20 for testing
                if nn_line[0] != '#' and _one_in(500):
                    self.assertEqual(
                        bmpm(nn_line[0], language_arg='german'), nn_line[1]
                    )
                    self.assertEqual(bmpm(nn_line[0]), nn_line[2])

    def test_bmpm_nachnamen_cc(self):
        """Test abydos.phonetic._bmpm.bmpm (Nachnamen, corner cases)."""
        with codecs.open(
            _corpus_file('nachnamen.bm.cc.csv'), encoding='utf-8'
        ) as nachnamen_testset:
            next(nachnamen_testset)
            for nn_line in nachnamen_testset:
                nn_line = nn_line.strip().split(',')
                # This test set is very large (~10000 entries)
                # so let's just randomly select about 20 for testing
                if nn_line[0] != '#':
                    self.assertEqual(
                        bmpm(nn_line[0], language_arg='german'), nn_line[1]
                    )
                    self.assertEqual(bmpm(nn_line[0]), nn_line[2])

    def test_bmpm_uscensus2000(self):
        """Test abydos.phonetic._bmpm.bmpm (US Census 2000 set)."""
        if not ALLOW_RANDOM:
            return
        with open(_corpus_file('uscensus2000.bm.csv')) as uscensus_ts:
            next(uscensus_ts)
            for cen_line in uscensus_ts:
                cen_line = cen_line.strip().split(',')
                # This test set is very large (~150000 entries)
                # so let's just randomly select about 20 for testing
                if cen_line[0] != '#' and _one_in(7500):
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='gen'
                        ),
                        cen_line[1],
                    )
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='ash'
                        ),
                        cen_line[2],
                    )
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='sep'
                        ),
                        cen_line[3],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='gen'),
                        cen_line[4],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='ash'),
                        cen_line[5],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='sep'),
                        cen_line[6],
                    )

    def test_bmpm_uscensus2000_cc(self):
        """Test abydos.phonetic._bmpm.bmpm (US Census 2000, corner cases)."""
        with open(_corpus_file('uscensus2000.bm.cc.csv')) as uscensus_ts:
            next(uscensus_ts)
            for cen_line in uscensus_ts:
                cen_line = cen_line.strip().split(',')
                # This test set is very large (~150000 entries)
                # so let's just randomly select about 20 for testing
                if cen_line[0] != '#' and _one_in(10):
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='gen'
                        ),
                        cen_line[1],
                    )
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='ash'
                        ),
                        cen_line[2],
                    )
                    self.assertEqual(
                        bmpm(
                            cen_line[0], match_mode='approx', name_mode='sep'
                        ),
                        cen_line[3],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='gen'),
                        cen_line[4],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='ash'),
                        cen_line[5],
                    )
                    self.assertEqual(
                        bmpm(cen_line[0], match_mode='exact', name_mode='sep'),
                        cen_line[6],
                    )

    def test_bm_phonetic_number(self):
        """Test abydos.phonetic._bmpm._bm_phonetic_number."""
        self.assertEqual(_bm_phonetic_number(''), '')
        self.assertEqual(_bm_phonetic_number('abcd'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[123]'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[123'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd['), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[[[123]]]'), 'abcd')

    def test_bm_apply_rule_if_compat(self):
        """Test abydos.phonetic._bmpm._bm_apply_rule_if_compat."""
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def', 4), 'abcdef')
        self.assertEqual(
            _bm_apply_rule_if_compat('abc', 'def[6]', 4), 'abcdef[4]'
        )
        self.assertEqual(
            _bm_apply_rule_if_compat('abc', 'def[4]', 4), 'abcdef[4]'
        )
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[0]', 4), None)
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[8]', 4), None)
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def', 1), 'abcdef')
        self.assertEqual(
            _bm_apply_rule_if_compat('abc', 'def[4]', 1), 'abcdef[4]'
        )

    def test_bm_language(self):
        """Test abydos.phonetic._bmpm._bm_language.

        Most test cases from:
        http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/bm/LanguageGuessingTest.java?view=markup
        """
        self.assertEqual(_bm_language('Renault', 'gen'), L_FRENCH)
        self.assertEqual(_bm_language('Mickiewicz', 'gen'), L_POLISH)
        self.assertEqual(
            _bm_language('Thompson', 'gen') & L_ENGLISH, L_ENGLISH
        )
        self.assertEqual(_bm_language('Nuñez', 'gen'), L_SPANISH)
        self.assertEqual(_bm_language('Carvalho', 'gen'), L_PORTUGUESE)
        self.assertEqual(_bm_language('Čapek', 'gen'), L_CZECH | L_LATVIAN)
        self.assertEqual(_bm_language('Sjneijder', 'gen'), L_DUTCH)
        self.assertEqual(_bm_language('Klausewitz', 'gen'), L_GERMAN)
        self.assertEqual(_bm_language('Küçük', 'gen'), L_TURKISH)
        self.assertEqual(_bm_language('Giacometti', 'gen'), L_ITALIAN)
        self.assertEqual(_bm_language('Nagy', 'gen'), L_HUNGARIAN)
        self.assertEqual(_bm_language('Ceauşescu', 'gen'), L_ROMANIAN)
        self.assertEqual(_bm_language('Angelopoulos', 'gen'), L_GREEKLATIN)
        self.assertEqual(_bm_language('Αγγελόπουλος', 'gen'), L_GREEK)
        self.assertEqual(_bm_language('Пушкин', 'gen'), L_CYRILLIC)
        self.assertEqual(_bm_language('כהן', 'gen'), L_HEBREW)
        self.assertEqual(_bm_language('ácz', 'gen'), L_ANY)
        self.assertEqual(_bm_language('átz', 'gen'), L_ANY)

    def test_bm_expand_alternates(self):
        """Test abydos.phonetic._bmpm._bm_expand_alternates."""
        self.assertEqual(_bm_expand_alternates(''), '')
        self.assertEqual(_bm_expand_alternates('aa'), 'aa')
        self.assertEqual(_bm_expand_alternates('aa|bb'), 'aa|bb')
        self.assertEqual(_bm_expand_alternates('aa|aa'), 'aa|aa')

        self.assertEqual(_bm_expand_alternates('(aa)(bb)'), 'aabb')
        self.assertEqual(_bm_expand_alternates('(aa)(bb[0])'), '')
        self.assertEqual(_bm_expand_alternates('(aa)(bb[4])'), 'aabb[4]')
        self.assertEqual(_bm_expand_alternates('(aa[0])(bb)'), '')
        self.assertEqual(_bm_expand_alternates('(aa[4])(bb)'), 'aabb[4]')

        self.assertEqual(
            _bm_expand_alternates('(a|b|c)(a|b|c)'),
            'aa|ab|ac|ba|bb|bc|ca|cb|cc',
        )
        self.assertEqual(
            _bm_expand_alternates('(a[1]|b[2])(c|d)'),
            'ac[1]|ad[1]|bc[2]|bd[2]',
        )
        self.assertEqual(
            _bm_expand_alternates('(a[1]|b[2])(c[4]|d)'), 'ad[1]|bd[2]'
        )

    def test_bm_remove_dupes(self):
        """Test abydos.phonetic._bmpm._bm_remove_dupes."""
        self.assertEqual(_bm_remove_dupes(''), '')
        self.assertEqual(_bm_remove_dupes('aa'), 'aa')
        self.assertEqual(_bm_remove_dupes('aa|bb'), 'aa|bb')
        self.assertEqual(_bm_remove_dupes('aa|aa'), 'aa')
        self.assertEqual(_bm_remove_dupes('aa|aa|aa|bb|aa'), 'aa|bb')
        self.assertEqual(_bm_remove_dupes('bb|aa|bb|aa|bb'), 'bb|aa')

    def test_bm_normalize_lang_attrs(self):
        """Test abydos.phonetic._bmpm._bm_normalize_language_attributes."""
        self.assertEqual(_bm_normalize_lang_attrs('', False), '')
        self.assertEqual(_bm_normalize_lang_attrs('', True), '')

        self.assertRaises(ValueError, _bm_normalize_lang_attrs, 'a[1', False)
        self.assertRaises(ValueError, _bm_normalize_lang_attrs, 'a[1', True)

        self.assertEqual(_bm_normalize_lang_attrs('abc', False), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[0]', False), '[0]')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2]', False), 'abc[2]')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][4]', False), '[0]')
        self.assertEqual(
            _bm_normalize_lang_attrs('abc[2][6]', False), 'abc[2]'
        )
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[4]', False), '[0]')
        self.assertEqual(
            _bm_normalize_lang_attrs('ab[2]c[6]', False), 'abc[2]'
        )

        self.assertEqual(_bm_normalize_lang_attrs('abc', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[0]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][4]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][6]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[4]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[6]', True), 'abc')


if __name__ == '__main__':
    unittest.main()
