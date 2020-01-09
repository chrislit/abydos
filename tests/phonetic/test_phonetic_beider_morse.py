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

"""abydos.tests.phonetic.test_phonetic_beider_morse.

This module contains unit tests for abydos.phonetic.BeiderMorse
"""

import codecs
import unittest

from abydos.phonetic import BeiderMorse, bmpm

# noinspection PyProtectedMember
from abydos.phonetic._beider_morse_data import (
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

from six import text_type

from .. import ALLOW_RANDOM, _corpus_file, _one_in


class BeiderMorseTestCases(unittest.TestCase):
    """Test BeiderMorse functions.

    test cases for abydos.phonetic.BeiderMorse
    """

    pa = BeiderMorse()

    def test_beider_morse_encode(self):
        """Test abydos.phonetic.BeiderMorse.

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
        self.assertEqual(BeiderMorse().encode(''), '')

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
                                BeiderMorse,
                                langs,
                                name_mode,
                                match_mode,
                                concat,
                            )
                        else:
                            self.assertEqual(
                                BeiderMorse(
                                    langs, name_mode, match_mode, concat
                                ).encode(''),
                                '',
                            )

        # testSolrGENERIC
        # concat is true, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', True).encode('Angelo'),
            'angelo anxelo anhelo anjelo anZelo andZelo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', True).encode("D'Angelo"),
            'angelo anxelo anhelo anjelo anZelo andZelo dangelo'
            + ' danxelo danhelo danjelo danZelo dandZelo',
        )
        self.assertEqual(
            BeiderMorse('italian,greek,spanish', 'gen', 'exact', True).encode(
                'Angelo'
            ),
            'angelo anxelo andZelo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', True).encode('1234'), ''
        )

        # concat is false, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', False).encode('Angelo'),
            'angelo anxelo anhelo anjelo anZelo andZelo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', False).encode("D'Angelo"),
            'angelo anxelo anhelo anjelo anZelo andZelo dangelo'
            + ' danxelo danhelo danjelo danZelo dandZelo',
        )
        self.assertEqual(
            BeiderMorse('italian,greek,spanish', 'gen', 'exact', False).encode(
                'Angelo'
            ),
            'angelo anxelo andZelo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', False).encode('1234'), ''
        )

        # concat is true, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', True).encode('Angelo'),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', True).encode("D'Angelo"),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo dangilo dangYlo dagilo dongilo'
            + ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo'
            + ' danilo donilo daniilo doniilo danzilo donzilo',
        )
        self.assertEqual(
            BeiderMorse('italian,greek,spanish', 'gen', 'approx', True).encode(
                'Angelo'
            ),
            'angilo ongilo anxilo onxilo anzilo onzilo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', True).encode('1234'), ''
        )

        # concat is false, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', False).encode('Angelo'),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', False).encode("D'Angelo"),
            'angilo angYlo agilo ongilo ongYlo ogilo Yngilo'
            + ' YngYlo anxilo onxilo anilo onilo aniilo oniilo'
            + ' anzilo onzilo dangilo dangYlo dagilo dongilo'
            + ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo'
            + ' danilo donilo daniilo doniilo danzilo donzilo',
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'gen', 'approx', False
            ).encode('Angelo'),
            'angilo ongilo anxilo onxilo anzilo onzilo',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', False).encode('1234'), ''
        )

        # testSolrASHKENAZI
        # concat is true, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', True).encode('Angelo'),
            'angelo andZelo anhelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', True).encode("D'Angelo"),
            'dangelo dandZelo danhelo danxelo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'ash',
            'exact',
            True,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'ash', 'exact', True, True
            ).encode('Angelo'),
            'anxelo angelo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', True).encode('1234'), ''
        )

        # concat is false, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', False).encode('Angelo'),
            'angelo andZelo anhelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', False).encode("D'Angelo"),
            'dangelo dandZelo danhelo danxelo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'ash',
            'exact',
            False,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'ash', 'exact', False, True
            ).encode('Angelo'),
            'anxelo angelo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'exact', False).encode('1234'), ''
        )

        # concat is true, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', True).encode('Angelo'),
            'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo'
            + ' onzilo anilo onilo anxilo onxilo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', True).encode("D'Angelo"),
            'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo'
            + ' danzilo donzilo danilo donilo danxilo donxilo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'ash',
            'approx',
            True,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'ash', 'approx', True, True
            ).encode('Angelo'),
            'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' + ' ongilo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', True).encode('1234'), ''
        )

        # concat is false, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', False).encode('Angelo'),
            'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo'
            + ' onzilo anilo onilo anxilo onxilo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', False).encode("D'Angelo"),
            'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo'
            + ' danzilo donzilo danilo donilo danxilo donxilo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'ash',
            'approx',
            False,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'ash', 'approx', False, True
            ).encode('Angelo'),
            'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' + ' ongilo',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', False).encode('1234'), ''
        )

        # testSolrSEPHARDIC
        # concat is true, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', True).encode('Angelo'),
            'anZelo andZelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', True).encode("D'Angelo"),
            'anZelo andZelo anxelo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'sep',
            'exact',
            True,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'sep', 'exact', True, True
            ).encode('Angelo'),
            'andZelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', True).encode('1234'), ''
        )

        # concat is false, ruleType is EXACT
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', False).encode('Angelo'),
            'anZelo andZelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', False).encode("D'Angelo"),
            'anZelo andZelo anxelo',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'sep',
            'exact',
            False,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'sep', 'exact', False, True
            ).encode('Angelo'),
            'andZelo anxelo',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'exact', False).encode('1234'), ''
        )

        # concat is true, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', True).encode('Angelo'),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', True).encode("D'Angelo"),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'sep',
            'approx',
            True,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'sep', 'approx', True, True
            ).encode('Angelo'),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', True).encode('1234'), ''
        )

        # concat is false, ruleType is APPROX
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', False).encode('Angelo'),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', False).encode("D'Angelo"),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertRaises(
            ValueError,
            BeiderMorse,
            'italian,greek,spanish',
            'sep',
            'approx',
            False,
        )
        self.assertEqual(
            BeiderMorse(
                'italian,greek,spanish', 'sep', 'approx', False, True
            ).encode('Angelo'),
            'anzila anzilu nzila nzilu anhila anhilu nhila nhilu',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', False).encode('1234'), ''
        )

        # testCompatibilityWithOriginalVersion
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', False).encode('abram'),
            'abram abrom avram avrom obram obrom ovram ovrom'
            + ' Ybram Ybrom abran abron obran obron',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', False).encode('Bendzin'),
            'binzn bindzn vindzn bintsn vintsn',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', False).encode('abram'),
            'abram abrom avram avrom obram obrom ovram ovrom'
            + ' Ybram Ybrom ombram ombrom imbram imbrom',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', False).encode('Halpern'),
            'alpirn alpYrn olpirn olpYrn Ylpirn YlpYrn xalpirn' + ' xolpirn',
        )

        # PhoneticEngineTest
        self.assertEqual(
            BeiderMorse('', 'gen', 'approx', True).encode('Renault'),
            'rinolt rino rinDlt rinalt rinult rinD rina rinu',
        )
        self.assertEqual(
            BeiderMorse('', 'ash', 'approx', True).encode('Renault'),
            'rinDlt rinalt rinult rYnDlt rYnalt rYnult rinolt',
        )
        self.assertEqual(
            BeiderMorse('', 'sep', 'approx', True).encode('Renault'), 'rinDlt'
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', True).encode('SntJohn-Smith'),
            'sntjonsmit',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', True).encode("d'ortley"),
            'ortlaj ortlej dortlaj dortlej',
        )
        self.assertEqual(
            BeiderMorse('', 'gen', 'exact', False).encode('van helsing'),
            'helSink helsink helzink xelsink elSink elsink'
            + ' vanhelsink vanhelzink vanjelsink fanhelsink'
            + ' fanhelzink banhelsink',
        )

        # Test wrapper
        self.assertEqual(
            bmpm('Angelo', '', 'gen', 'exact', True),
            'angelo anxelo anhelo anjelo anZelo andZelo',
        )

    def test_beider_morse_encode_misc(self):
        """Test abydos.phonetic.BeiderMorse (miscellaneous tests).

        The purpose of this test set is to achieve higher code coverage
        and to hit some of the test cases noted in the BMPM reference code.
        """
        # test of Ashkenazi with discardable prefix
        self.assertEqual(
            BeiderMorse(name_mode='ash').encode('bar Hayim'), 'Dm xDm'
        )

        # tests of concat behavior
        self.assertEqual(
            BeiderMorse(concat=False).encode('Rodham Clinton'),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )
        self.assertEqual(
            BeiderMorse(concat=True).encode('Rodham Clinton'),
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
        self.assertEqual(
            BeiderMorse(name_mode='ash').encode('bar Hayim'), 'Dm xDm'
        )
        self.assertEqual(
            BeiderMorse(name_mode='ashkenazi').encode('bar Hayim'), 'Dm xDm'
        )
        self.assertEqual(
            BeiderMorse(name_mode='Ashkenazi').encode('bar Hayim'), 'Dm xDm'
        )
        self.assertEqual(
            BeiderMorse(name_mode='gen', concat=True).encode('bar Hayim'),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            BeiderMorse(name_mode='general', concat=True).encode('bar Hayim'),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            BeiderMorse(name_mode='Mizrahi', concat=True).encode('bar Hayim'),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            BeiderMorse(name_mode='mizrahi', concat=True).encode('bar Hayim'),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )
        self.assertEqual(
            BeiderMorse(name_mode='miz', concat=True).encode('bar Hayim'),
            'barDm borDm bYrDm varDm vorDm barDn borDn barxDm'
            + ' borxDm varxDm vorxDm barxDn borxDn',
        )

        # test that out-of-range language_arg results in L_ANY
        self.assertEqual(
            BeiderMorse(language_arg=2 ** 32).encode('Rodham Clinton'),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )
        self.assertEqual(
            BeiderMorse(language_arg=-4).encode('Rodham Clinton'),
            'rodam rodom rYdam rYdom rodan rodon rodxam rodxom'
            + ' rodxan rodxon rudam rudom klinton klnton klintun'
            + ' klntun tzlinton tzlnton tzlintun tzlntun zlinton'
            + ' zlnton',
        )

        # etc. (for code coverage)
        self.assertEqual(
            BeiderMorse(name_mode='sep').encode('van Damme'), 'dami mi dam m'
        )

    def test_beider_morse_encode_nachnamen(self):
        """Test abydos.phonetic.BeiderMorse (Nachnamen set)."""
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
                        BeiderMorse(language_arg='german').encode(nn_line[0]),
                        nn_line[1],
                    )
                    self.assertEqual(
                        BeiderMorse().encode(nn_line[0]), nn_line[2]
                    )

    def test_beider_morse_encode_nachnamen_cc(self):
        """Test abydos.phonetic.BeiderMorse (Nachnamen, corner cases)."""
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
                        BeiderMorse(language_arg='german').encode(nn_line[0]),
                        nn_line[1],
                    )
                    self.assertEqual(
                        BeiderMorse().encode(nn_line[0]), nn_line[2]
                    )

    def test_beider_morse_encode_uscensus2000(self):
        """Test abydos.phonetic.BeiderMorse (US Census 2000 set)."""
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
                        BeiderMorse(
                            match_mode='approx', name_mode='gen'
                        ).encode(cen_line[0]),
                        cen_line[1],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='approx', name_mode='ash'
                        ).encode(cen_line[0]),
                        cen_line[2],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='approx', name_mode='sep'
                        ).encode(cen_line[0]),
                        cen_line[3],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='gen'
                        ).encode(cen_line[0]),
                        cen_line[4],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='ash'
                        ).encode(cen_line[0]),
                        cen_line[5],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='sep'
                        ).encode(cen_line[0]),
                        cen_line[6],
                    )

    def test_beider_morse_encode_uscensus2000_cc(self):
        """Test abydos.phonetic.BeiderMorse (US Census 2000, corner cases)."""
        with open(_corpus_file('uscensus2000.bm.cc.csv')) as uscensus_ts:
            next(uscensus_ts)
            for cen_line in uscensus_ts:
                cen_line = cen_line.strip().split(',')
                # This test set is very large (~150000 entries)
                # so let's just randomly select about 20 for testing
                if cen_line[0] != '#' and _one_in(10):
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='approx', name_mode='gen'
                        ).encode(cen_line[0]),
                        cen_line[1],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='approx', name_mode='ash'
                        ).encode(cen_line[0]),
                        cen_line[2],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='approx', name_mode='sep'
                        ).encode(cen_line[0]),
                        cen_line[3],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='gen'
                        ).encode(cen_line[0]),
                        cen_line[4],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='ash'
                        ).encode(cen_line[0]),
                        cen_line[5],
                    )
                    self.assertEqual(
                        BeiderMorse(
                            match_mode='exact', name_mode='sep'
                        ).encode(cen_line[0]),
                        cen_line[6],
                    )

    def test_beider_morse_phonetic_number(self):
        """Test abydos.phonetic.BeiderMorse._phonetic_number."""
        self.assertEqual(self.pa._phonetic_number(''), '')  # noqa: SF01
        self.assertEqual(
            self.pa._phonetic_number('abcd'), 'abcd'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._phonetic_number('abcd[123]'), 'abcd'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._phonetic_number('abcd[123'), 'abcd'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._phonetic_number('abcd['), 'abcd'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._phonetic_number('abcd[[[123]]]'), 'abcd'  # noqa: SF01
        )

    def test_beider_morse_apply_rule_if_compat(self):
        """Test abydos.phonetic.BeiderMorse._apply_rule_if_compat."""
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def', 4),  # noqa: SF01
            'abcdef',
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def[6]', 4),  # noqa: SF01
            'abcdef[4]',
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def[4]', 4),  # noqa: SF01
            'abcdef[4]',
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def[0]', 4),  # noqa: SF01
            None,
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def[8]', 4),  # noqa: SF01
            None,
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def', 1),  # noqa: SF01
            'abcdef',
        )
        self.assertEqual(
            self.pa._apply_rule_if_compat('abc', 'def[4]', 1),  # noqa: SF01
            'abcdef[4]',
        )

    def test_beider_morse_language(self):
        """Test abydos.phonetic.BeiderMorse._language.

        Most test cases from:
        http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/bm/LanguageGuessingTest.java?view=markup
        """
        self.assertEqual(
            self.pa._language('Renault', 'gen'), L_FRENCH  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Mickiewicz', 'gen'), L_POLISH  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Thompson', 'gen') & L_ENGLISH,  # noqa: SF01
            L_ENGLISH,
        )
        self.assertEqual(
            self.pa._language('Nuñez', 'gen'), L_SPANISH  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Carvalho', 'gen'), L_PORTUGUESE  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Čapek', 'gen'),  # noqa: SF01
            L_CZECH | L_LATVIAN,
        )
        self.assertEqual(
            self.pa._language('Sjneijder', 'gen'), L_DUTCH  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Klausewitz', 'gen'), L_GERMAN  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Küçük', 'gen'), L_TURKISH  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Giacometti', 'gen'), L_ITALIAN  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Nagy', 'gen'), L_HUNGARIAN  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Ceauşescu', 'gen'), L_ROMANIAN  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Angelopoulos', 'gen'),  # noqa: SF01
            L_GREEKLATIN,
        )
        self.assertEqual(
            self.pa._language('Αγγελόπουλος', 'gen'), L_GREEK  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('Пушкин', 'gen'), L_CYRILLIC  # noqa: SF01
        )
        self.assertEqual(
            self.pa._language('כהן', 'gen'), L_HEBREW  # noqa: SF01
        )
        self.assertEqual(self.pa._language('ácz', 'gen'), L_ANY)  # noqa: SF01
        self.assertEqual(self.pa._language('átz', 'gen'), L_ANY)  # noqa: SF01

    def test_beider_morse_expand_alternates(self):
        """Test abydos.phonetic.BeiderMorse._expand_alternates."""
        self.assertEqual(self.pa._expand_alternates(''), '')  # noqa: SF01
        self.assertEqual(self.pa._expand_alternates('aa'), 'aa')  # noqa: SF01
        self.assertEqual(
            self.pa._expand_alternates('aa|bb'), 'aa|bb'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._expand_alternates('aa|aa'), 'aa|aa'  # noqa: SF01
        )

        self.assertEqual(
            self.pa._expand_alternates('(aa)(bb)'), 'aabb'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._expand_alternates('(aa)(bb[0])'), ''  # noqa: SF01
        )
        self.assertEqual(
            self.pa._expand_alternates('(aa)(bb[4])'), 'aabb[4]'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._expand_alternates('(aa[0])(bb)'), ''  # noqa: SF01
        )
        self.assertEqual(
            self.pa._expand_alternates('(aa[4])(bb)'), 'aabb[4]'  # noqa: SF01
        )

        self.assertEqual(
            self.pa._expand_alternates('(a|b|c)(a|b|c)'),  # noqa: SF01
            'aa|ab|ac|ba|bb|bc|ca|cb|cc',
        )
        self.assertEqual(
            self.pa._expand_alternates('(a[1]|b[2])(c|d)'),  # noqa: SF01
            'ac[1]|ad[1]|bc[2]|bd[2]',
        )
        self.assertEqual(
            self.pa._expand_alternates('(a[1]|b[2])(c[4]|d)'),  # noqa: SF01
            'ad[1]|bd[2]',
        )

    def test_beider_morse_remove_dupes(self):
        """Test abydos.phonetic.BeiderMorse._remove_dupes."""
        self.assertEqual(self.pa._remove_dupes(''), '')  # noqa: SF01
        self.assertEqual(self.pa._remove_dupes('aa'), 'aa')  # noqa: SF01
        self.assertEqual(self.pa._remove_dupes('aa|bb'), 'aa|bb')  # noqa: SF01
        self.assertEqual(self.pa._remove_dupes('aa|aa'), 'aa')  # noqa: SF01
        self.assertEqual(
            self.pa._remove_dupes('aa|aa|aa|bb|aa'), 'aa|bb'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._remove_dupes('bb|aa|bb|aa|bb'), 'bb|aa'  # noqa: SF01
        )

    def test_beider_morse_normalize_lang_attrs(self):
        """Test abydos.phonetic.BeiderMorse._normalize_language_attributes."""
        self.assertEqual(
            self.pa._normalize_lang_attrs('', False), ''  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('', True), ''  # noqa: SF01
        )

        self.assertRaises(
            ValueError,
            self.pa._normalize_lang_attrs,  # noqa: SF01
            'a[1',
            False,
        )
        self.assertRaises(
            ValueError,
            self.pa._normalize_lang_attrs,  # noqa: SF01
            'a[1',
            True,
        )

        self.assertEqual(
            self.pa._normalize_lang_attrs('abc', False), 'abc'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[0]', False), '[0]'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2]', False),  # noqa: SF01
            'abc[2]',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2][4]', False),  # noqa: SF01
            '[0]',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2][6]', False),  # noqa: SF01
            'abc[2]',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('ab[2]c[4]', False),  # noqa: SF01
            '[0]',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('ab[2]c[6]', False),  # noqa: SF01
            'abc[2]',
        )

        self.assertEqual(
            self.pa._normalize_lang_attrs('abc', True), 'abc'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[0]', True), 'abc'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2]', True), 'abc'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2][4]', True),  # noqa: SF01
            'abc',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('abc[2][6]', True),  # noqa: SF01
            'abc',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('ab[2]c[4]', True),  # noqa: SF01
            'abc',
        )
        self.assertEqual(
            self.pa._normalize_lang_attrs('ab[2]c[6]', True),  # noqa: SF01
            'abc',
        )

        self.assertEqual(
            self.pa._language_index_from_code(0, 'gen'), L_ANY  # noqa: SF01
        )


if __name__ == '__main__':
    unittest.main()
