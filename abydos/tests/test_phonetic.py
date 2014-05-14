# -*- coding: utf-8 -*-

import unittest
from abydos.phonetic import *

class DoubleMetaphoneTestCase(unittest.TestCase):
    """These test cases are copied verbatim from
    https://github.com/oubiwann/metaphone/blob/master/metaphone/tests/test_metaphone.py
    """
    def test_single_result(self):
        result = double_metaphone(u"aubrey")
        self.assertEquals(result, ('APR', ''))
        
    def test_double_result(self):
        result = double_metaphone(u"richard")
        self.assertEquals(result, ('RXRT', 'RKRT'))

    def test_general_word_list(self):
        result = double_metaphone('Jose')
        self.assertEquals(result, ('JS', 'HS'))
        result = double_metaphone('cambrillo')
        self.assertEquals(result, ('KMPRL', 'KMPR'))
        result = double_metaphone('otto')
        self.assertEquals(result, ('AT', ''))
        result = double_metaphone('aubrey')
        self.assertEquals(result, ('APR', ''))
        result = double_metaphone('maurice')
        self.assertEquals(result, ('MRS', ''))
        result = double_metaphone('auto')
        self.assertEquals(result, ('AT', ''))
        result = double_metaphone('maisey')
        self.assertEquals(result, ('MS', ''))
        result = double_metaphone('catherine')
        self.assertEquals(result, ('K0RN', 'KTRN'))
        result = double_metaphone('geoff')
        self.assertEquals(result, ('JF', 'KF'))
        result = double_metaphone('Chile')
        self.assertEquals(result, ('XL', ''))
        result = double_metaphone('katherine')
        self.assertEquals(result, ('K0RN', 'KTRN'))
        result = double_metaphone('steven')
        self.assertEquals(result, ('STFN', ''))
        result = double_metaphone('zhang')
        self.assertEquals(result, ('JNK', ''))
        result = double_metaphone('bob')
        self.assertEquals(result, ('PP', ''))
        result = double_metaphone('ray')
        self.assertEquals(result, ('R', ''))
        result = double_metaphone('Tux')
        self.assertEquals(result, ('TKS', ''))
        result = double_metaphone('bryan')
        self.assertEquals(result, ('PRN', ''))
        result = double_metaphone('bryce')
        self.assertEquals(result, ('PRS', ''))
        result = double_metaphone('Rapelje')
        self.assertEquals(result, ('RPL', ''))
        result = double_metaphone('richard')
        self.assertEquals(result, ('RXRT', 'RKRT'))
        result = double_metaphone('solilijs')
        self.assertEquals(result, ('SLLS', ''))
        result = double_metaphone('Dallas')
        self.assertEquals(result, ('TLS', ''))
        result = double_metaphone('Schwein')
        self.assertEquals(result, ('XN', 'XFN'))
        result = double_metaphone('dave')
        self.assertEquals(result, ('TF', ''))
        result = double_metaphone('eric')
        self.assertEquals(result, ('ARK', ''))
        result = double_metaphone('Parachute')
        self.assertEquals(result, ('PRKT', ''))
        result = double_metaphone('brian')
        self.assertEquals(result, ('PRN', ''))
        result = double_metaphone('randy')
        self.assertEquals(result, ('RNT', ''))
        result = double_metaphone('Through')
        self.assertEquals(result, ('0R', 'TR'))
        result = double_metaphone('Nowhere')
        self.assertEquals(result, ('NR', ''))
        result = double_metaphone('heidi')
        self.assertEquals(result, ('HT', ''))
        result = double_metaphone('Arnow')
        self.assertEquals(result, ('ARN', 'ARNF'))
        result = double_metaphone('Thumbail')
        self.assertEquals(result, ('0MPL', 'TMPL'))

    def test_homophones(self):
        self.assertEqual(
            double_metaphone(u"tolled"),
            double_metaphone(u"told"))
        self.assertEqual(
            double_metaphone(u"katherine"),
            double_metaphone(u"catherine"))
        self.assertEqual(
            double_metaphone(u"brian"),
            double_metaphone(u"bryan"))

    def test_similar_names(self):
        result = double_metaphone("Bartoš")
        self.assertEquals(result, ('PRTS', ''))
        result = double_metaphone(u"Bartosz")
        self.assertEquals(result, ('PRTS', 'PRTX'))
        result = double_metaphone(u"Bartosch")
        self.assertEquals(result, ('PRTX', ''))
        result = double_metaphone(u"Bartos")
        self.assertEquals(result, ('PRTS', ''))

        result = set(double_metaphone(u"Jablonski")).intersection(
            double_metaphone(u"Yablonsky"))
        self.assertEquals(list(result), ['APLNSK'])
        result = set(double_metaphone(u"Smith")).intersection(
            double_metaphone(u"Schmidt"))
        self.assertEquals(list(result), ['XMT'])

    def test_non_english_unicode(self):
        result = double_metaphone("andestādītu")
        self.assertEquals(result, ('ANTSTTT', ''))

    def test_c_cedilla(self):
        result = double_metaphone("français")
        self.assertEquals(result, ('FRNS', 'FRNSS'))
        result = double_metaphone("garçon")
        self.assertEquals(result, ('KRSN', ''))
        result = double_metaphone("leçon")
        self.assertEquals(result, ('LSN', ''))

    def test_various_german(self):
        result = double_metaphone("ach")
        self.assertEquals(result, ("AX", "AK"))
        result = double_metaphone("bacher")
        self.assertEquals(result, ("PKR", ""))
        result = double_metaphone("macher")
        self.assertEquals(result, ("MKR", ""))

    def test_various_italian(self):
        result = double_metaphone("bacci")
        self.assertEquals(result, ("PX", ""))
        result = double_metaphone("bertucci")
        self.assertEquals(result, ("PRTX", ""))
        result = double_metaphone("bellocchio")
        self.assertEquals(result, ("PLX", ""))
        result = double_metaphone("bacchus")
        self.assertEquals(result, ("PKS", ""))
        result = double_metaphone("focaccia")
        self.assertEquals(result, ("FKX", ""))
        result = double_metaphone("chianti")
        self.assertEquals(result, ("KNT", ""))
        result = double_metaphone("tagliaro")
        self.assertEquals(result, ("TKLR", "TLR"))
        result = double_metaphone("biaggi")
        self.assertEquals(result, ("PJ", "PK"))

    def test_various_spanish(self):
        result = double_metaphone("bajador")
        self.assertEquals(result, ("PJTR", "PHTR"))
        result = double_metaphone("cabrillo")
        self.assertEquals(result, ("KPRL", "KPR"))
        result = double_metaphone("gallegos")
        self.assertEquals(result, ("KLKS", "KKS"))
        result = double_metaphone("San Jacinto")
        self.assertEquals(result, ("SNHSNT", ""))

    def test_various_french(self):
        result = double_metaphone("rogier")
        self.assertEquals(result, ("RJ", "RKR"))
        result = double_metaphone("breaux")
        self.assertEquals(result, ("PR", ""))

    def test_various_slavic(self):
        result = double_metaphone("Wewski")
        self.assertEquals(result, ("ASK", "FFSK"))

    def test_various_chinese(self):
        result = double_metaphone("zhao")
        self.assertEquals(result, ("J", ""))

    def test_dutch_origin(self):
        result = double_metaphone("school")
        self.assertEquals(result, ("SKL", ""))
        result = double_metaphone("schooner")
        self.assertEquals(result, ("SKNR", ""))
        result = double_metaphone("schermerhorn")
        self.assertEquals(result, ("XRMRRN", "SKRMRRN"))
        result = double_metaphone("schenker")
        self.assertEquals(result, ("XNKR", "SKNKR"))

    def test_ch_words(self):
        result = double_metaphone("Charac")
        self.assertEquals(result, ("KRK", ""))
        result = double_metaphone("Charis")
        self.assertEquals(result, ("KRS", ""))
        result = double_metaphone("chord")
        self.assertEquals(result, ("KRT", ""))
        result = double_metaphone("Chym")
        self.assertEquals(result, ("KM", ""))
        result = double_metaphone("Chia")
        self.assertEquals(result, ("K", ""))
        result = double_metaphone("chem")
        self.assertEquals(result, ("KM", ""))
        result = double_metaphone("chore")
        self.assertEquals(result, ("XR", ""))
        result = double_metaphone("orchestra")
        self.assertEquals(result, ("ARKSTR", ""))
        result = double_metaphone("architect")
        self.assertEquals(result, ("ARKTKT", ""))
        result = double_metaphone("orchid")
        self.assertEquals(result, ("ARKT", ""))

    def test_cc_words(self):
        result = double_metaphone("accident")
        self.assertEquals(result, ("AKSTNT", ""))
        result = double_metaphone("accede")
        self.assertEquals(result, ("AKST", ""))
        result = double_metaphone("succeed")
        self.assertEquals(result, ("SKST", ""))

    def test_mc_words(self):
        result = double_metaphone("mac caffrey")
        self.assertEquals(result, ("MKFR", ""))
        result = double_metaphone("mac gregor")
        self.assertEquals(result, ("MKRKR", ""))
        result = double_metaphone("mc crae")
        self.assertEquals(result, ("MKR", ""))
        result = double_metaphone("mcclain")
        self.assertEquals(result, ("MKLN", ""))

    def test_gh_words(self):
        result = double_metaphone("laugh")
        self.assertEquals(result, ("LF", ""))
        result = double_metaphone("cough")
        self.assertEquals(result, ("KF", ""))
        result = double_metaphone("rough")
        self.assertEquals(result, ("RF", ""))

    def test_g3_words(self):
        result = double_metaphone("gya")
        self.assertEquals(result, ("K", "J"))
        result = double_metaphone("ges")
        self.assertEquals(result, ("KS", "JS"))
        result = double_metaphone("gep")
        self.assertEquals(result, ("KP", "JP"))
        result = double_metaphone("geb")
        self.assertEquals(result, ("KP", "JP"))
        result = double_metaphone("gel")
        self.assertEquals(result, ("KL", "JL"))
        result = double_metaphone("gey")
        self.assertEquals(result, ("K", "J"))
        result = double_metaphone("gib")
        self.assertEquals(result, ("KP", "JP"))
        result = double_metaphone("gil")
        self.assertEquals(result, ("KL", "JL"))
        result = double_metaphone("gin")
        self.assertEquals(result, ("KN", "JN"))
        result = double_metaphone("gie")
        self.assertEquals(result, ("K", "J"))
        result = double_metaphone("gei")
        self.assertEquals(result, ("K", "J"))
        result = double_metaphone("ger")
        self.assertEquals(result, ("KR", "JR"))
        result = double_metaphone("danger")
        self.assertEquals(result, ("TNJR", "TNKR"))
        result = double_metaphone("manager")
        self.assertEquals(result, ("MNKR", "MNJR"))
        result = double_metaphone("dowager")
        self.assertEquals(result, ("TKR", "TJR"))

    def test_pb_words(self):
        result = double_metaphone("Campbell")
        self.assertEquals(result, ("KMPL", ""))
        result = double_metaphone("raspberry")
        self.assertEquals(result, ("RSPR", ""))

    def test_th_words(self):
        result = double_metaphone("Thomas")
        self.assertEquals(result, ("TMS", ""))
        result = double_metaphone("Thames")
        self.assertEquals(result, ("TMS", ""))

if __name__ == '__main__':
    unittest.main()
