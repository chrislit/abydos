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

"""abydos.phonetic._phonet.

phonet algorithm (a.k.a. Hannoveraner Phonetik), intended chiefly for German
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter
from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['Phonet', 'phonet']


class Phonet(_Phonetic):
    """Phonet code.

    phonet ("Hannoveraner Phonetik") was developed by Jörg Michael and
    documented in :cite:`Michael:1999`.

    This is a port of Jesper Zedlitz's code, which is licensed LGPL
    :cite:`Zedlitz:2015`.

    That is, in turn, based on Michael's C code, which is also licensed LGPL
    :cite:`Michael:2007`.
    """

    _rules_no_lang = (  # separator chars
        # fmt: off
        '´', ' ', ' ',
        '"', ' ', ' ',
        '`$', '', '',
        '\'', ' ', ' ',
        ',', ',', ',',
        ';', ',', ',',
        '-', ' ', ' ',
        ' ', ' ', ' ',
        '.', '.', '.',
        ':', '.', '.',
        # German umlauts
        'Ä', 'AE', 'AE',
        'Ö', 'OE', 'OE',
        'Ü', 'UE', 'UE',
        'ß', 'S', 'S',
        # international umlauts
        'À', 'A', 'A',
        'Á', 'A', 'A',
        'Â', 'A', 'A',
        'Ã', 'A', 'A',
        'Å', 'A', 'A',
        'Æ', 'AE', 'AE',
        'Ç', 'C', 'C',
        'Ð', 'DJ', 'DJ',
        'È', 'E', 'E',
        'É', 'E', 'E',
        'Ê', 'E', 'E',
        'Ë', 'E', 'E',
        'Ì', 'I', 'I',
        'Í', 'I', 'I',
        'Î', 'I', 'I',
        'Ï', 'I', 'I',
        'Ñ', 'NH', 'NH',
        'Ò', 'O', 'O',
        'Ó', 'O', 'O',
        'Ô', 'O', 'O',
        'Õ', 'O', 'O',
        'Œ', 'OE', 'OE',
        'Ø', 'OE', 'OE',
        'Š', 'SH', 'SH',
        'Þ', 'TH', 'TH',
        'Ù', 'U', 'U',
        'Ú', 'U', 'U',
        'Û', 'U', 'U',
        'Ý', 'Y', 'Y',
        'Ÿ', 'Y', 'Y',
        # 'normal' letters (A-Z)
        'MC^', 'MAC', 'MAC',
        'MC^', 'MAC', 'MAC',
        'M´^', 'MAC', 'MAC',
        'M\'^', 'MAC', 'MAC',
        'O´^', 'O', 'O',
        'O\'^', 'O', 'O',
        'VAN DEN ^', 'VANDEN', 'VANDEN',
        None, None, None
        # fmt: on
    )

    _rules_german = (  # separator chars
        # fmt: off
        '´', ' ', ' ',
        '"', ' ', ' ',
        '`$', '', '',
        '\'', ' ', ' ',
        ',', ' ', ' ',
        ';', ' ', ' ',
        '-', ' ', ' ',
        ' ', ' ', ' ',
        '.', '.', '.',
        ':', '.', '.',
        # German umlauts
        'ÄE', 'E', 'E',
        'ÄU<', 'EU', 'EU',
        'ÄV(AEOU)-<', 'EW', None,
        'Ä$', 'Ä', None,
        'Ä<', None, 'E',
        'Ä', 'E', None,
        'ÖE', 'Ö', 'Ö',
        'ÖU', 'Ö', 'Ö',
        'ÖVER--<', 'ÖW', None,
        'ÖV(AOU)-', 'ÖW', None,
        'ÜBEL(GNRW)-^^', 'ÜBL ', 'IBL ',
        'ÜBER^^', 'ÜBA', 'IBA',
        'ÜE', 'Ü', 'I',
        'ÜVER--<', 'ÜW', None,
        'ÜV(AOU)-', 'ÜW', None,
        'Ü', None, 'I',
        'ßCH<', None, 'Z',
        'ß<', 'S', 'Z',
        # international umlauts
        'À<', 'A', 'A',
        'Á<', 'A', 'A',
        'Â<', 'A', 'A',
        'Ã<', 'A', 'A',
        'Å<', 'A', 'A',
        'ÆER-', 'E', 'E',
        'ÆU<', 'EU', 'EU',
        'ÆV(AEOU)-<', 'EW', None,
        'Æ$', 'Ä', None,
        'Æ<', None, 'E',
        'Æ', 'E', None,
        'Ç', 'Z', 'Z',
        'ÐÐ-', '', '',
        'Ð', 'DI', 'TI',
        'È<', 'E', 'E',
        'É<', 'E', 'E',
        'Ê<', 'E', 'E',
        'Ë', 'E', 'E',
        'Ì<', 'I', 'I',
        'Í<', 'I', 'I',
        'Î<', 'I', 'I',
        'Ï', 'I', 'I',
        'ÑÑ-', '', '',
        'Ñ', 'NI', 'NI',
        'Ò<', 'O', 'U',
        'Ó<', 'O', 'U',
        'Ô<', 'O', 'U',
        'Õ<', 'O', 'U',
        'Œ<', 'Ö', 'Ö',
        'Ø(IJY)-<', 'E', 'E',
        'Ø<', 'Ö', 'Ö',
        'Š', 'SH', 'Z',
        'Þ', 'T', 'T',
        'Ù<', 'U', 'U',
        'Ú<', 'U', 'U',
        'Û<', 'U', 'U',
        'Ý<', 'I', 'I',
        'Ÿ<', 'I', 'I',
        # 'normal' letters (A-Z)
        'ABELLE$', 'ABL', 'ABL',
        'ABELL$', 'ABL', 'ABL',
        'ABIENNE$', 'ABIN', 'ABIN',
        'ACHME---^', 'ACH', 'AK',
        'ACEY$', 'AZI', 'AZI',
        'ADV', 'ATW', None,
        'AEGL-', 'EK', None,
        'AEU<', 'EU', 'EU',
        'AE2', 'E', 'E',
        'AFTRAUBEN------', 'AFT ', 'AFT ',
        'AGL-1', 'AK', None,
        'AGNI-^', 'AKN', 'AKN',
        'AGNIE-', 'ANI', 'ANI',
        'AGN(AEOU)-$', 'ANI', 'ANI',
        'AH(AIOÖUÜY)-', 'AH', None,
        'AIA2', 'AIA', 'AIA',
        'AIE$', 'E', 'E',
        'AILL(EOU)-', 'ALI', 'ALI',
        'AINE$', 'EN', 'EN',
        'AIRE$', 'ER', 'ER',
        'AIR-', 'E', 'E',
        'AISE$', 'ES', 'EZ',
        'AISSANCE$', 'ESANS', 'EZANZ',
        'AISSE$', 'ES', 'EZ',
        'AIX$', 'EX', 'EX',
        'AJ(AÄEÈÉÊIOÖUÜ)--', 'A', 'A',
        'AKTIE', 'AXIE', 'AXIE',
        'AKTUEL', 'AKTUEL', None,
        'ALOI^', 'ALOI', 'ALUI',  # Don't merge these rules
        'ALOY^', 'ALOI', 'ALUI',  # needed by 'check_rules'
        'AMATEU(RS)-', 'AMATÖ', 'ANATÖ',
        'ANCH(OEI)-', 'ANSH', 'ANZ',
        'ANDERGEGANG----', 'ANDA GE', 'ANTA KE',
        'ANDERGEHE----', 'ANDA ', 'ANTA ',
        'ANDERGESETZ----', 'ANDA GE', 'ANTA KE',
        'ANDERGING----', 'ANDA ', 'ANTA ',
        'ANDERSETZ(ET)-----', 'ANDA ', 'ANTA ',
        'ANDERZUGEHE----', 'ANDA ZU ', 'ANTA ZU ',
        'ANDERZUSETZE-----', 'ANDA ZU ', 'ANTA ZU ',
        'ANER(BKO)---^^', 'AN', None,
        'ANHAND---^$', 'AN H', 'AN ',
        'ANH(AÄEIOÖUÜY)--^^', 'AN', None,
        'ANIELLE$', 'ANIEL', 'ANIL',
        'ANIEL', 'ANIEL', None,
        'ANSTELLE----^$', 'AN ST', 'AN ZT',
        'ANTI^^', 'ANTI', 'ANTI',
        'ANVER^^', 'ANFA', 'ANFA',
        'ATIA$', 'ATIA', 'ATIA',
        'ATIA(NS)--', 'ATI', 'ATI',
        'ATI(AÄOÖUÜ)-', 'AZI', 'AZI',
        'AUAU--', '', '',
        'AUERE$', 'AUERE', None,
        'AUERE(NS)-$', 'AUERE', None,
        'AUERE(AIOUY)--', 'AUER', None,
        'AUER(AÄIOÖUÜY)-', 'AUER', None,
        'AUER<', 'AUA', 'AUA',
        'AUF^^', 'AUF', 'AUF',
        'AULT$', 'O', 'U',
        'AUR(BCDFGKLMNQSTVWZ)-', 'AUA', 'AUA',
        'AUR$', 'AUA', 'AUA',
        'AUSSE$', 'OS', 'UZ',
        'AUS(ST)-^', 'AUS', 'AUS',
        'AUS^^', 'AUS', 'AUS',
        'AUTOFAHR----', 'AUTO ', 'AUTU ',
        'AUTO^^', 'AUTO', 'AUTU',
        'AUX(IY)-', 'AUX', 'AUX',
        'AUX', 'O', 'U',
        'AU', 'AU', 'AU',
        'AVER--<', 'AW', None,
        'AVIER$', 'AWIE', 'AFIE',
        'AV(EÈÉÊI)-^', 'AW', None,
        'AV(AOU)-', 'AW', None,
        'AYRE$', 'EIRE', 'EIRE',
        'AYRE(NS)-$', 'EIRE', 'EIRE',
        'AYRE(AIOUY)--', 'EIR', 'EIR',
        'AYR(AÄIOÖUÜY)-', 'EIR', 'EIR',
        'AYR<', 'EIA', 'EIA',
        'AYER--<', 'EI', 'EI',
        'AY(AÄEIOÖUÜY)--', 'A', 'A',
        'AË', 'E', 'E',
        'A(IJY)<', 'EI', 'EI',
        'BABY^$', 'BEBI', 'BEBI',
        'BAB(IY)^', 'BEBI', 'BEBI',
        'BEAU^$', 'BO', None,
        'BEA(BCMNRU)-^', 'BEA', 'BEA',
        'BEAT(AEIMORU)-^', 'BEAT', 'BEAT',
        'BEE$', 'BI', 'BI',
        'BEIGE^$', 'BESH', 'BEZ',
        'BENOIT--', 'BENO', 'BENU',
        'BER(DT)-', 'BER', None,
        'BERN(DT)-', 'BERN', None,
        'BE(LMNRST)-^', 'BE', 'BE',
        'BETTE$', 'BET', 'BET',
        'BEVOR^$', 'BEFOR', None,
        'BIC$', 'BIZ', 'BIZ',
        'BOWL(EI)-', 'BOL', 'BUL',
        'BP(AÄEÈÉÊIÌÍÎOÖRUÜY)-', 'B', 'B',
        'BRINGEND-----^', 'BRI', 'BRI',
        'BRINGEND-----', ' BRI', ' BRI',
        'BROW(NS)-', 'BRAU', 'BRAU',
        'BUDGET7', 'BÜGE', 'BIKE',
        'BUFFET7', 'BÜFE', 'BIFE',
        'BYLLE$', 'BILE', 'BILE',
        'BYLL$', 'BIL', 'BIL',
        'BYPA--^', 'BEI', 'BEI',
        'BYTE<', 'BEIT', 'BEIT',
        'BY9^', 'BÜ', None,
        'B(SßZ)$', 'BS', None,
        'CACH(EI)-^', 'KESH', 'KEZ',
        'CAE--', 'Z', 'Z',
        'CA(IY)$', 'ZEI', 'ZEI',
        'CE(EIJUY)--', 'Z', 'Z',
        'CENT<', 'ZENT', 'ZENT',
        'CERST(EI)----^', 'KE', 'KE',
        'CER$', 'ZA', 'ZA',
        'CE3', 'ZE', 'ZE',
        'CH\'S$', 'X', 'X',
        'CH´S$', 'X', 'X',
        'CHAO(ST)-', 'KAO', 'KAU',
        'CHAMPIO-^', 'SHEMPI', 'ZENBI',
        'CHAR(AI)-^', 'KAR', 'KAR',
        'CHAU(CDFSVWXZ)-', 'SHO', 'ZU',
        'CHÄ(CF)-', 'SHE', 'ZE',
        'CHE(CF)-', 'SHE', 'ZE',
        'CHEM-^', 'KE', 'KE',  # or: 'CHE', 'KE'
        'CHEQUE<', 'SHEK', 'ZEK',
        'CHI(CFGPVW)-', 'SHI', 'ZI',
        'CH(AEUY)-<^', 'SH', 'Z',
        'CHK-', '', '',
        'CHO(CKPS)-^', 'SHO', 'ZU',
        'CHRIS-', 'KRI', None,
        'CHRO-', 'KR', None,
        'CH(LOR)-<^', 'K', 'K',
        'CHST-', 'X', 'X',
        'CH(SßXZ)3', 'X', 'X',
        'CHTNI-3', 'CHN', 'KN',
        'CH^', 'K', 'K',  # or: 'CH', 'K'
        'CH', 'CH', 'K',
        'CIC$', 'ZIZ', 'ZIZ',
        'CIENCEFICT----', 'EIENS ', 'EIENZ ',
        'CIENCE$', 'EIENS', 'EIENZ',
        'CIER$', 'ZIE', 'ZIE',
        'CYB-^', 'ZEI', 'ZEI',
        'CY9^', 'ZÜ', 'ZI',
        'C(IJY)-<3', 'Z', 'Z',
        'CLOWN-', 'KLAU', 'KLAU',
        'CCH', 'Z', 'Z',
        'CCE-', 'X', 'X',
        'C(CK)-', '', '',
        'CLAUDET---', 'KLO', 'KLU',
        'CLAUDINE^$', 'KLODIN', 'KLUTIN',
        'COACH', 'KOSH', 'KUZ',
        'COLE$', 'KOL', 'KUL',
        'COUCH', 'KAUSH', 'KAUZ',
        'COW', 'KAU', 'KAU',
        'CQUES$', 'K', 'K',
        'CQUE', 'K', 'K',
        'CRASH--9', 'KRE', 'KRE',
        'CREAT-^', 'KREA', 'KREA',
        'CST', 'XT', 'XT',
        'CS<^', 'Z', 'Z',
        'C(SßX)', 'X', 'X',
        'CT\'S$', 'X', 'X',
        'CT(SßXZ)', 'X', 'X',
        'CZ<', 'Z', 'Z',
        'C(ÈÉÊÌÍÎÝ)3', 'Z', 'Z',
        'C.^', 'C.', 'C.',
        'CÄ-', 'Z', 'Z',
        'CÜ$', 'ZÜ', 'ZI',
        'C\'S$', 'X', 'X',
        'C<', 'K', 'K',
        'DAHER^$', 'DAHER', None,
        'DARAUFFOLGE-----', 'DARAUF ', 'TARAUF ',
        'DAVO(NR)-^$', 'DAFO', 'TAFU',
        'DD(SZ)--<', '', '',
        'DD9', 'D', None,
        'DEPOT7', 'DEPO', 'TEBU',
        'DESIGN', 'DISEIN', 'TIZEIN',
        'DE(LMNRST)-3^', 'DE', 'TE',
        'DETTE$', 'DET', 'TET',
        'DH$', 'T', None,
        'DIC$', 'DIZ', 'TIZ',
        'DIDR-^', 'DIT', None,
        'DIEDR-^', 'DIT', None,
        'DJ(AEIOU)-^', 'I', 'I',
        'DMITR-^', 'DIMIT', 'TINIT',
        'DRY9^', 'DRÜ', None,
        'DT-', '', '',
        'DUIS-^', 'DÜ', 'TI',
        'DURCH^^', 'DURCH', 'TURK',
        'DVA$', 'TWA', None,
        'DY9^', 'DÜ', None,
        'DYS$', 'DIS', None,
        'DS(CH)--<', 'T', 'T',
        'DST', 'ZT', 'ZT',
        'DZS(CH)--', 'T', 'T',
        'D(SßZ)', 'Z', 'Z',
        'D(AÄEIOÖRUÜY)-', 'D', None,
        'D(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'D', None,
        'D\'H^', 'D', 'T',
        'D´H^', 'D', 'T',
        'D`H^', 'D', 'T',
        'D\'S3$', 'Z', 'Z',
        'D´S3$', 'Z', 'Z',
        'D^', 'D', None,
        'D', 'T', 'T',
        'EAULT$', 'O', 'U',
        'EAUX$', 'O', 'U',
        'EAU', 'O', 'U',
        'EAV', 'IW', 'IF',
        'EAS3$', 'EAS', None,
        'EA(AÄEIOÖÜY)-3', 'EA', 'EA',
        'EA3$', 'EA', 'EA',
        'EA3', 'I', 'I',
        'EBENSO^$', 'EBNSO', 'EBNZU',
        'EBENSO^^', 'EBNSO ', 'EBNZU ',
        'EBEN^^', 'EBN', 'EBN',
        'EE9', 'E', 'E',
        'EGL-1', 'EK', None,
        'EHE(IUY)--1', 'EH', None,
        'EHUNG---1', 'E', None,
        'EH(AÄIOÖUÜY)-1', 'EH', None,
        'EIEI--', '', '',
        'EIERE^$', 'EIERE', None,
        'EIERE$', 'EIERE', None,
        'EIERE(NS)-$', 'EIERE', None,
        'EIERE(AIOUY)--', 'EIER', None,
        'EIER(AÄIOÖUÜY)-', 'EIER', None,
        'EIER<', 'EIA', None,
        'EIGL-1', 'EIK', None,
        'EIGH$', 'EI', 'EI',
        'EIH--', 'E', 'E',
        'EILLE$', 'EI', 'EI',
        'EIR(BCDFGKLMNQSTVWZ)-', 'EIA', 'EIA',
        'EIR$', 'EIA', 'EIA',
        'EITRAUBEN------', 'EIT ', 'EIT ',
        'EI', 'EI', 'EI',
        'EJ$', 'EI', 'EI',
        'ELIZ^', 'ELIS', None,
        'ELZ^', 'ELS', None,
        'EL-^', 'E', 'E',
        'ELANG----1', 'E', 'E',
        'EL(DKL)--1', 'E', 'E',
        'EL(MNT)--1$', 'E', 'E',
        'ELYNE$', 'ELINE', 'ELINE',
        'ELYN$', 'ELIN', 'ELIN',
        'EL(AÄEÈÉÊIÌÍÎOÖUÜY)-1', 'EL', 'EL',
        'EL-1', 'L', 'L',
        'EM-^', None, 'E',
        'EM(DFKMPQT)--1', None, 'E',
        'EM(AÄEÈÉÊIÌÍÎOÖUÜY)--1', None, 'E',
        'EM-1', None, 'N',
        'ENGAG-^', 'ANGA', 'ANKA',
        'EN-^', 'E', 'E',
        'ENTUEL', 'ENTUEL', None,
        'EN(CDGKQSTZ)--1', 'E', 'E',
        'EN(AÄEÈÉÊIÌÍÎNOÖUÜY)-1', 'EN', 'EN',
        'EN-1', '', '',
        'ERH(AÄEIOÖUÜ)-^', 'ERH', 'ER',
        'ER-^', 'E', 'E',
        'ERREGEND-----', ' ER', ' ER',
        'ERT1$', 'AT', None,
        'ER(DGLKMNRQTZß)-1', 'ER', None,
        'ER(AÄEÈÉÊIÌÍÎOÖUÜY)-1', 'ER', 'A',
        'ER1$', 'A', 'A',
        'ER<1', 'A', 'A',
        'ETAT7', 'ETA', 'ETA',
        'ETI(AÄOÖÜU)-', 'EZI', 'EZI',
        'EUERE$', 'EUERE', None,
        'EUERE(NS)-$', 'EUERE', None,
        'EUERE(AIOUY)--', 'EUER', None,
        'EUER(AÄIOÖUÜY)-', 'EUER', None,
        'EUER<', 'EUA', None,
        'EUEU--', '', '',
        'EUILLE$', 'Ö', 'Ö',
        'EUR$', 'ÖR', 'ÖR',
        'EUX', 'Ö', 'Ö',
        'EUSZ$', 'EUS', None,
        'EUTZ$', 'EUS', None,
        'EUYS$', 'EUS', 'EUZ',
        'EUZ$', 'EUS', None,
        'EU', 'EU', 'EU',
        'EVER--<1', 'EW', None,
        'EV(ÄOÖUÜ)-1', 'EW', None,
        'EYER<', 'EIA', 'EIA',
        'EY<', 'EI', 'EI',
        'FACETTE', 'FASET', 'FAZET',
        'FANS--^$', 'FE', 'FE',
        'FAN-^$', 'FE', 'FE',
        'FAULT-', 'FOL', 'FUL',
        'FEE(DL)-', 'FI', 'FI',
        'FEHLER', 'FELA', 'FELA',
        'FE(LMNRST)-3^', 'FE', 'FE',
        'FOERDERN---^', 'FÖRD', 'FÖRT',
        'FOERDERN---', ' FÖRD', ' FÖRT',
        'FOND7', 'FON', 'FUN',
        'FRAIN$', 'FRA', 'FRA',
        'FRISEU(RS)-', 'FRISÖ', 'FRIZÖ',
        'FY9^', 'FÜ', None,
        'FÖRDERN---^', 'FÖRD', 'FÖRT',
        'FÖRDERN---', ' FÖRD', ' FÖRT',
        'GAGS^$', 'GEX', 'KEX',
        'GAG^$', 'GEK', 'KEK',
        'GD', 'KT', 'KT',
        'GEGEN^^', 'GEGN', 'KEKN',
        'GEGENGEKOM-----', 'GEGN ', 'KEKN ',
        'GEGENGESET-----', 'GEGN ', 'KEKN ',
        'GEGENKOMME-----', 'GEGN ', 'KEKN ',
        'GEGENZUKOM---', 'GEGN ZU ', 'KEKN ZU ',
        'GENDETWAS-----$', 'GENT ', 'KENT ',
        'GENRE', 'IORE', 'IURE',
        'GE(LMNRST)-3^', 'GE', 'KE',
        'GER(DKT)-', 'GER', None,
        'GETTE$', 'GET', 'KET',
        'GGF.', 'GF.', None,
        'GG-', '', '',
        'GH', 'G', None,
        'GI(AOU)-^', 'I', 'I',
        'GION-3', 'KIO', 'KIU',
        'G(CK)-', '', '',
        'GJ(AEIOU)-^', 'I', 'I',
        'GMBH^$', 'GMBH', 'GMBH',
        'GNAC$', 'NIAK', 'NIAK',
        'GNON$', 'NION', 'NIUN',
        'GN$', 'N', 'N',
        'GONCAL-^', 'GONZA', 'KUNZA',
        'GRY9^', 'GRÜ', None,
        'G(SßXZ)-<', 'K', 'K',
        'GUCK-', 'KU', 'KU',
        'GUISEP-^', 'IUSE', 'IUZE',
        'GUI-^', 'G', 'K',
        'GUTAUSSEH------^', 'GUT ', 'KUT ',
        'GUTGEHEND------^', 'GUT ', 'KUT ',
        'GY9^', 'GÜ', None,
        'G(AÄEILOÖRUÜY)-', 'G', None,
        'G(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'G', None,
        'G\'S$', 'X', 'X',
        'G´S$', 'X', 'X',
        'G^', 'G', None,
        'G', 'K', 'K',
        'HA(HIUY)--1', 'H', None,
        'HANDVOL---^', 'HANT ', 'ANT ',
        'HANNOVE-^', 'HANOF', None,
        'HAVEN7$', 'HAFN', None,
        'HEAD-', 'HE', 'E',
        'HELIEGEN------', 'E ', 'E ',
        'HESTEHEN------', 'E ', 'E ',
        'HE(LMNRST)-3^', 'HE', 'E',
        'HE(LMN)-1', 'E', 'E',
        'HEUR1$', 'ÖR', 'ÖR',
        'HE(HIUY)--1', 'H', None,
        'HIH(AÄEIOÖUÜY)-1', 'IH', None,
        'HLH(AÄEIOÖUÜY)-1', 'LH', None,
        'HMH(AÄEIOÖUÜY)-1', 'MH', None,
        'HNH(AÄEIOÖUÜY)-1', 'NH', None,
        'HOBBY9^', 'HOBI', None,
        'HOCHBEGAB-----^', 'HOCH ', 'UK ',
        'HOCHTALEN-----^', 'HOCH ', 'UK ',
        'HOCHZUFRI-----^', 'HOCH ', 'UK ',
        'HO(HIY)--1', 'H', None,
        'HRH(AÄEIOÖUÜY)-1', 'RH', None,
        'HUH(AÄEIOÖUÜY)-1', 'UH', None,
        'HUIS^^', 'HÜS', 'IZ',
        'HUIS$', 'ÜS', 'IZ',
        'HUI--1', 'H', None,
        'HYGIEN^', 'HÜKIEN', None,
        'HY9^', 'HÜ', None,
        'HY(BDGMNPST)-', 'Ü', None,
        'H.^', None, 'H.',
        'HÄU--1', 'H', None,
        'H^', 'H', '',
        'H', '', '',
        'ICHELL---', 'ISH', 'IZ',
        'ICHI$', 'ISHI', 'IZI',
        'IEC$', 'IZ', 'IZ',
        'IEDENSTELLE------', 'IDN ', 'ITN ',
        'IEI-3', '', '',
        'IELL3', 'IEL', 'IEL',
        'IENNE$', 'IN', 'IN',
        'IERRE$', 'IER', 'IER',
        'IERZULAN---', 'IR ZU ', 'IR ZU ',
        'IETTE$', 'IT', 'IT',
        'IEU', 'IÖ', 'IÖ',
        'IE<4', 'I', 'I',
        'IGL-1', 'IK', None,
        'IGHT3$', 'EIT', 'EIT',
        'IGNI(EO)-', 'INI', 'INI',
        'IGN(AEOU)-$', 'INI', 'INI',
        'IHER(DGLKRT)--1', 'IHE', None,
        'IHE(IUY)--', 'IH', None,
        'IH(AIOÖUÜY)-', 'IH', None,
        'IJ(AOU)-', 'I', 'I',
        'IJ$', 'I', 'I',
        'IJ<', 'EI', 'EI',
        'IKOLE$', 'IKOL', 'IKUL',
        'ILLAN(STZ)--4', 'ILIA', 'ILIA',
        'ILLAR(DT)--4', 'ILIA', 'ILIA',
        'IMSTAN----^', 'IM ', 'IN ',
        'INDELERREGE------', 'INDL ', 'INTL ',
        'INFRAGE-----^$', 'IN ', 'IN ',
        'INTERN(AOU)-^', 'INTAN', 'INTAN',
        'INVER-', 'INWE', 'INFE',
        'ITI(AÄIOÖUÜ)-', 'IZI', 'IZI',
        'IUSZ$', 'IUS', None,
        'IUTZ$', 'IUS', None,
        'IUZ$', 'IUS', None,
        'IVER--<', 'IW', None,
        'IVIER$', 'IWIE', 'IFIE',
        'IV(ÄOÖUÜ)-', 'IW', None,
        'IV<3', 'IW', None,
        'IY2', 'I', None,
        'I(ÈÉÊ)<4', 'I', 'I',
        'JAVIE---<^', 'ZA', 'ZA',
        'JEANS^$', 'JINS', 'INZ',
        'JEANNE^$', 'IAN', 'IAN',
        'JEAN-^', 'IA', 'IA',
        'JER-^', 'IE', 'IE',
        'JE(LMNST)-', 'IE', 'IE',
        'JI^', 'JI', None,
        'JOR(GK)^$', 'IÖRK', 'IÖRK',
        'J', 'I', 'I',
        'KC(ÄEIJ)-', 'X', 'X',
        'KD', 'KT', None,
        'KE(LMNRST)-3^', 'KE', 'KE',
        'KG(AÄEILOÖRUÜY)-', 'K', None,
        'KH<^', 'K', 'K',
        'KIC$', 'KIZ', 'KIZ',
        'KLE(LMNRST)-3^', 'KLE', 'KLE',
        'KOTELE-^', 'KOTL', 'KUTL',
        'KREAT-^', 'KREA', 'KREA',
        'KRÜS(TZ)--^', 'KRI', None,
        'KRYS(TZ)--^', 'KRI', None,
        'KRY9^', 'KRÜ', None,
        'KSCH---', 'K', 'K',
        'KSH--', 'K', 'K',
        'K(SßXZ)7', 'X', 'X',  # implies 'KST' -> 'XT'
        'KT\'S$', 'X', 'X',
        'KTI(AIOU)-3', 'XI', 'XI',
        'KT(SßXZ)', 'X', 'X',
        'KY9^', 'KÜ', None,
        'K\'S$', 'X', 'X',
        'K´S$', 'X', 'X',
        'LANGES$', ' LANGES', ' LANKEZ',
        'LANGE$', ' LANGE', ' LANKE',
        'LANG$', ' LANK', ' LANK',
        'LARVE-', 'LARF', 'LARF',
        'LD(SßZ)$', 'LS', 'LZ',
        'LD\'S$', 'LS', 'LZ',
        'LD´S$', 'LS', 'LZ',
        'LEAND-^', 'LEAN', 'LEAN',
        'LEERSTEHE-----^', 'LER ', 'LER ',
        'LEICHBLEIB-----', 'LEICH ', 'LEIK ',
        'LEICHLAUTE-----', 'LEICH ', 'LEIK ',
        'LEIDERREGE------', 'LEIT ', 'LEIT ',
        'LEIDGEPR----^', 'LEIT ', 'LEIT ',
        'LEINSTEHE-----', 'LEIN ', 'LEIN ',
        'LEL-', 'LE', 'LE',
        'LE(MNRST)-3^', 'LE', 'LE',
        'LETTE$', 'LET', 'LET',
        'LFGNAG-', 'LFGAN', 'LFKAN',
        'LICHERWEIS----', 'LICHA ', 'LIKA ',
        'LIC$', 'LIZ', 'LIZ',
        'LIVE^$', 'LEIF', 'LEIF',
        'LT(SßZ)$', 'LS', 'LZ',
        'LT\'S$', 'LS', 'LZ',
        'LT´S$', 'LS', 'LZ',
        'LUI(GS)--', 'LU', 'LU',
        'LV(AIO)-', 'LW', None,
        'LY9^', 'LÜ', None,
        'LSTS$', 'LS', 'LZ',
        'LZ(BDFGKLMNPQRSTVWX)-', 'LS', None,
        'L(SßZ)$', 'LS', None,
        'MAIR-<', 'MEI', 'NEI',
        'MANAG-', 'MENE', 'NENE',
        'MANUEL', 'MANUEL', None,
        'MASSEU(RS)-', 'MASÖ', 'NAZÖ',
        'MATCH', 'MESH', 'NEZ',
        'MAURICE', 'MORIS', 'NURIZ',
        'MBH^$', 'MBH', 'MBH',
        'MB(ßZ)$', 'MS', None,
        'MB(SßTZ)-', 'M', 'N',
        'MCG9^', 'MAK', 'NAK',
        'MC9^', 'MAK', 'NAK',
        'MEMOIR-^', 'MEMOA', 'NENUA',
        'MERHAVEN$', 'MAHAFN', None,
        'ME(LMNRST)-3^', 'ME', 'NE',
        'MEN(STZ)--3', 'ME', None,
        'MEN$', 'MEN', None,
        'MIGUEL-', 'MIGE', 'NIKE',
        'MIKE^$', 'MEIK', 'NEIK',
        'MITHILFE----^$', 'MIT H', 'NIT ',
        'MN$', 'M', None,
        'MN', 'N', 'N',
        'MPJUTE-', 'MPUT', 'NBUT',
        'MP(ßZ)$', 'MS', None,
        'MP(SßTZ)-', 'M', 'N',
        'MP(BDJLMNPQVW)-', 'MB', 'NB',
        'MY9^', 'MÜ', None,
        'M(ßZ)$', 'MS', None,
        'M´G7^', 'MAK', 'NAK',
        'M\'G7^', 'MAK', 'NAK',
        'M´^', 'MAK', 'NAK',
        'M\'^', 'MAK', 'NAK',
        'M', None, 'N',
        'NACH^^', 'NACH', 'NAK',
        'NADINE', 'NADIN', 'NATIN',
        'NAIV--', 'NA', 'NA',
        'NAISE$', 'NESE', 'NEZE',
        'NAUGENOMM------', 'NAU ', 'NAU ',
        'NAUSOGUT$', 'NAUSO GUT', 'NAUZU KUT',
        'NCH$', 'NSH', 'NZ',
        'NCOISE$', 'SOA', 'ZUA',
        'NCOIS$', 'SOA', 'ZUA',
        'NDAR$', 'NDA', 'NTA',
        'NDERINGEN------', 'NDE ', 'NTE ',
        'NDRO(CDKTZ)-', 'NTRO', None,
        'ND(BFGJLMNPQVW)-', 'NT', None,
        'ND(SßZ)$', 'NS', 'NZ',
        'ND\'S$', 'NS', 'NZ',
        'ND´S$', 'NS', 'NZ',
        'NEBEN^^', 'NEBN', 'NEBN',
        'NENGELERN------', 'NEN ', 'NEN ',
        'NENLERN(ET)---', 'NEN LE', 'NEN LE',
        'NENZULERNE---', 'NEN ZU LE', 'NEN ZU LE',
        'NE(LMNRST)-3^', 'NE', 'NE',
        'NEN-3', 'NE', 'NE',
        'NETTE$', 'NET', 'NET',
        'NGU^^', 'NU', 'NU',
        'NG(BDFJLMNPQRTVW)-', 'NK', 'NK',
        'NH(AUO)-$', 'NI', 'NI',
        'NICHTSAHNEN-----', 'NIX ', 'NIX ',
        'NICHTSSAGE----', 'NIX ', 'NIX ',
        'NICHTS^^', 'NIX', 'NIX',
        'NICHT^^', 'NICHT', 'NIKT',
        'NINE$', 'NIN', 'NIN',
        'NON^^', 'NON', 'NUN',
        'NOTLEIDE-----^', 'NOT ', 'NUT ',
        'NOT^^', 'NOT', 'NUT',
        'NTI(AIOU)-3', 'NZI', 'NZI',
        'NTIEL--3', 'NZI', 'NZI',
        'NT(SßZ)$', 'NS', 'NZ',
        'NT\'S$', 'NS', 'NZ',
        'NT´S$', 'NS', 'NZ',
        'NYLON', 'NEILON', 'NEILUN',
        'NY9^', 'NÜ', None,
        'NSTZUNEH---', 'NST ZU ', 'NZT ZU ',
        'NSZ-', 'NS', None,
        'NSTS$', 'NS', 'NZ',
        'NZ(BDFGKLMNPQRSTVWX)-', 'NS', None,
        'N(SßZ)$', 'NS', None,
        'OBERE-', 'OBER', None,
        'OBER^^', 'OBA', 'UBA',
        'OEU2', 'Ö', 'Ö',
        'OE<2', 'Ö', 'Ö',
        'OGL-', 'OK', None,
        'OGNIE-', 'ONI', 'UNI',
        'OGN(AEOU)-$', 'ONI', 'UNI',
        'OH(AIOÖUÜY)-', 'OH', None,
        'OIE$', 'Ö', 'Ö',
        'OIRE$', 'OA', 'UA',
        'OIR$', 'OA', 'UA',
        'OIX', 'OA', 'UA',
        'OI<3', 'EU', 'EU',
        'OKAY^$', 'OKE', 'UKE',
        'OLYN$', 'OLIN', 'ULIN',
        'OO(DLMZ)-', 'U', None,
        'OO$', 'U', None,
        'OO-', '', '',
        'ORGINAL-----', 'ORI', 'URI',
        'OTI(AÄOÖUÜ)-', 'OZI', 'UZI',
        'OUI^', 'WI', 'FI',
        'OUILLE$', 'ULIE', 'ULIE',
        'OU(DT)-^', 'AU', 'AU',
        'OUSE$', 'AUS', 'AUZ',
        'OUT-', 'AU', 'AU',
        'OU', 'U', 'U',
        'O(FV)$', 'AU', 'AU',  # due to 'OW$' -> 'AU'
        'OVER--<', 'OW', None,
        'OV(AOU)-', 'OW', None,
        'OW$', 'AU', 'AU',
        'OWS$', 'OS', 'UZ',
        'OJ(AÄEIOÖUÜ)--', 'O', 'U',
        'OYER', 'OIA', None,
        'OY(AÄEIOÖUÜ)--', 'O', 'U',
        'O(JY)<', 'EU', 'EU',
        'OZ$', 'OS', None,
        'O´^', 'O', 'U',
        'O\'^', 'O', 'U',
        'O', None, 'U',
        'PATIEN--^', 'PAZI', 'PAZI',
        'PENSIO-^', 'PANSI', 'PANZI',
        'PE(LMNRST)-3^', 'PE', 'PE',
        'PFER-^', 'FE', 'FE',
        'P(FH)<', 'F', 'F',
        'PIC^$', 'PIK', 'PIK',
        'PIC$', 'PIZ', 'PIZ',
        'PIPELINE', 'PEIBLEIN', 'PEIBLEIN',
        'POLYP-', 'POLÜ', None,
        'POLY^^', 'POLI', 'PULI',
        'PORTRAIT7', 'PORTRE', 'PURTRE',
        'POWER7', 'PAUA', 'PAUA',
        'PP(FH)--<', 'B', 'B',
        'PP-', '', '',
        'PRODUZ-^', 'PRODU', 'BRUTU',
        'PRODUZI--', ' PRODU', ' BRUTU',
        'PRIX^$', 'PRI', 'PRI',
        'PS-^^', 'P', None,
        'P(SßZ)^', None, 'Z',
        'P(SßZ)$', 'BS', None,
        'PT-^', '', '',
        'PTI(AÄOÖUÜ)-3', 'BZI', 'BZI',
        'PY9^', 'PÜ', None,
        'P(AÄEIOÖRUÜY)-', 'P', 'P',
        'P(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'P', None,
        'P.^', None, 'P.',
        'P^', 'P', None,
        'P', 'B', 'B',
        'QI-', 'Z', 'Z',
        'QUARANT--', 'KARA', 'KARA',
        'QUE(LMNRST)-3', 'KWE', 'KFE',
        'QUE$', 'K', 'K',
        'QUI(NS)$', 'KI', 'KI',
        'QUIZ7', 'KWIS', None,
        'Q(UV)7', 'KW', 'KF',
        'Q<', 'K', 'K',
        'RADFAHR----', 'RAT ', 'RAT ',
        'RAEFTEZEHRE-----', 'REFTE ', 'REFTE ',
        'RCH', 'RCH', 'RK',
        'REA(DU)---3^', 'R', None,
        'REBSERZEUG------', 'REBS ', 'REBZ ',
        'RECHERCH^', 'RESHASH', 'REZAZ',
        'RECYCL--', 'RIZEI', 'RIZEI',
        'RE(ALST)-3^', 'RE', None,
        'REE$', 'RI', 'RI',
        'RER$', 'RA', 'RA',
        'RE(MNR)-4', 'RE', 'RE',
        'RETTE$', 'RET', 'RET',
        'REUZ$', 'REUZ', None,
        'REW$', 'RU', 'RU',
        'RH<^', 'R', 'R',
        'RJA(MN)--', 'RI', 'RI',
        'ROWD-^', 'RAU', 'RAU',
        'RTEMONNAIE-', 'RTMON', 'RTNUN',
        'RTI(AÄOÖUÜ)-3', 'RZI', 'RZI',
        'RTIEL--3', 'RZI', 'RZI',
        'RV(AEOU)-3', 'RW', None,
        'RY(KN)-$', 'RI', 'RI',
        'RY9^', 'RÜ', None,
        'RÄFTEZEHRE-----', 'REFTE ', 'REFTE ',
        'SAISO-^', 'SES', 'ZEZ',
        'SAFE^$', 'SEIF', 'ZEIF',
        'SAUCE-^', 'SOS', 'ZUZ',
        'SCHLAGGEBEN-----<', 'SHLAK ', 'ZLAK ',
        'SCHSCH---7', '', '',
        'SCHTSCH', 'SH', 'Z',
        'SC(HZ)<', 'SH', 'Z',
        'SC', 'SK', 'ZK',
        'SELBSTST--7^^', 'SELB', 'ZELB',
        'SELBST7^^', 'SELBST', 'ZELBZT',
        'SERVICE7^', 'SÖRWIS', 'ZÖRFIZ',
        'SERVI-^', 'SERW', None,
        'SE(LMNRST)-3^', 'SE', 'ZE',
        'SETTE$', 'SET', 'ZET',
        'SHP-^', 'S', 'Z',
        'SHST', 'SHT', 'ZT',
        'SHTSH', 'SH', 'Z',
        'SHT', 'ST', 'Z',
        'SHY9^', 'SHÜ', None,
        'SH^^', 'SH', None,
        'SH3', 'SH', 'Z',
        'SICHERGEGAN-----^', 'SICHA ', 'ZIKA ',
        'SICHERGEHE----^', 'SICHA ', 'ZIKA ',
        'SICHERGESTEL------^', 'SICHA ', 'ZIKA ',
        'SICHERSTELL-----^', 'SICHA ', 'ZIKA ',
        'SICHERZU(GS)--^', 'SICHA ZU ', 'ZIKA ZU ',
        'SIEGLI-^', 'SIKL', 'ZIKL',
        'SIGLI-^', 'SIKL', 'ZIKL',
        'SIGHT', 'SEIT', 'ZEIT',
        'SIGN', 'SEIN', 'ZEIN',
        'SKI(NPZ)-', 'SKI', 'ZKI',
        'SKI<^', 'SHI', 'ZI',
        'SODASS^$', 'SO DAS', 'ZU TAZ',
        'SODAß^$', 'SO DAS', 'ZU TAZ',
        'SOGENAN--^', 'SO GEN', 'ZU KEN',
        'SOUND-', 'SAUN', 'ZAUN',
        'STAATS^^', 'STAZ', 'ZTAZ',
        'STADT^^', 'STAT', 'ZTAT',
        'STANDE$', ' STANDE', ' ZTANTE',
        'START^^', 'START', 'ZTART',
        'STAURANT7', 'STORAN', 'ZTURAN',
        'STEAK-', 'STE', 'ZTE',
        'STEPHEN-^$', 'STEW', None,
        'STERN', 'STERN', None,
        'STRAF^^', 'STRAF', 'ZTRAF',
        'ST\'S$', 'Z', 'Z',
        'ST´S$', 'Z', 'Z',
        'STST--', '', '',
        'STS(ACEÈÉÊHIÌÍÎOUÄÜÖ)--', 'ST', 'ZT',
        'ST(SZ)', 'Z', 'Z',
        'SPAREN---^', 'SPA', 'ZPA',
        'SPAREND----', ' SPA', ' ZPA',
        'S(PTW)-^^', 'S', None,
        'SP', 'SP', None,
        'STYN(AE)-$', 'STIN', 'ZTIN',
        'ST', 'ST', 'ZT',
        'SUITE<', 'SIUT', 'ZIUT',
        'SUKE--$', 'S', 'Z',
        'SURF(EI)-', 'SÖRF', 'ZÖRF',
        'SV(AEÈÉÊIÌÍÎOU)-<^', 'SW', None,
        'SYB(IY)--^', 'SIB', None,
        'SYL(KVW)--^', 'SI', None,
        'SY9^', 'SÜ', None,
        'SZE(NPT)-^', 'ZE', 'ZE',
        'SZI(ELN)-^', 'ZI', 'ZI',
        'SZCZ<', 'SH', 'Z',
        'SZT<', 'ST', 'ZT',
        'SZ<3', 'SH', 'Z',
        'SÜL(KVW)--^', 'SI', None,
        'S', None, 'Z',
        'TCH', 'SH', 'Z',
        'TD(AÄEIOÖRUÜY)-', 'T', None,
        'TD(ÀÁÂÃÅÈÉÊËÌÍÎÏÒÓÔÕØÙÚÛÝŸ)-', 'T', None,
        'TEAT-^', 'TEA', 'TEA',
        'TERRAI7^', 'TERA', 'TERA',
        'TE(LMNRST)-3^', 'TE', 'TE',
        'TH<', 'T', 'T',
        'TICHT-', 'TIK', 'TIK',
        'TICH$', 'TIK', 'TIK',
        'TIC$', 'TIZ', 'TIZ',
        'TIGGESTELL-------', 'TIK ', 'TIK ',
        'TIGSTELL-----', 'TIK ', 'TIK ',
        'TOAS-^', 'TO', 'TU',
        'TOILET-', 'TOLE', 'TULE',
        'TOIN-', 'TOA', 'TUA',
        'TRAECHTI-^', 'TRECHT', 'TREKT',
        'TRAECHTIG--', ' TRECHT', ' TREKT',
        'TRAINI-', 'TREN', 'TREN',
        'TRÄCHTI-^', 'TRECHT', 'TREKT',
        'TRÄCHTIG--', ' TRECHT', ' TREKT',
        'TSCH', 'SH', 'Z',
        'TSH', 'SH', 'Z',
        'TST', 'ZT', 'ZT',
        'T(Sß)', 'Z', 'Z',
        'TT(SZ)--<', '', '',
        'TT9', 'T', 'T',
        'TV^$', 'TV', 'TV',
        'TX(AEIOU)-3', 'SH', 'Z',
        'TY9^', 'TÜ', None,
        'TZ-', '', '',
        'T\'S3$', 'Z', 'Z',
        'T´S3$', 'Z', 'Z',
        'UEBEL(GNRW)-^^', 'ÜBL ', 'IBL ',
        'UEBER^^', 'ÜBA', 'IBA',
        'UE2', 'Ü', 'I',
        'UGL-', 'UK', None,
        'UH(AOÖUÜY)-', 'UH', None,
        'UIE$', 'Ü', 'I',
        'UM^^', 'UM', 'UN',
        'UNTERE--3', 'UNTE', 'UNTE',
        'UNTER^^', 'UNTA', 'UNTA',
        'UNVER^^', 'UNFA', 'UNFA',
        'UN^^', 'UN', 'UN',
        'UTI(AÄOÖUÜ)-', 'UZI', 'UZI',
        'UVE-4', 'UW', None,
        'UY2', 'UI', None,
        'UZZ', 'AS', 'AZ',
        'VACL-^', 'WAZ', 'FAZ',
        'VAC$', 'WAZ', 'FAZ',
        'VAN DEN ^', 'FANDN', 'FANTN',
        'VANES-^', 'WANE', None,
        'VATRO-', 'WATR', None,
        'VA(DHJNT)--^', 'F', None,
        'VEDD-^', 'FE', 'FE',
        'VE(BEHIU)--^', 'F', None,
        'VEL(BDLMNT)-^', 'FEL', None,
        'VENTZ-^', 'FEN', None,
        'VEN(NRSZ)-^', 'FEN', None,
        'VER(AB)-^$', 'WER', None,
        'VERBAL^$', 'WERBAL', None,
        'VERBAL(EINS)-^', 'WERBAL', None,
        'VERTEBR--', 'WERTE', None,
        'VEREIN-----', 'F', None,
        'VEREN(AEIOU)-^', 'WEREN', None,
        'VERIFI', 'WERIFI', None,
        'VERON(AEIOU)-^', 'WERON', None,
        'VERSEN^', 'FERSN', 'FAZN',
        'VERSIERT--^', 'WERSI', None,
        'VERSIO--^', 'WERS', None,
        'VERSUS', 'WERSUS', None,
        'VERTI(GK)-', 'WERTI', None,
        'VER^^', 'FER', 'FA',
        'VERSPRECHE-------', ' FER', ' FA',
        'VER$', 'WA', None,
        'VER', 'FA', 'FA',
        'VET(HT)-^', 'FET', 'FET',
        'VETTE$', 'WET', 'FET',
        'VE^', 'WE', None,
        'VIC$', 'WIZ', 'FIZ',
        'VIELSAGE----', 'FIL ', 'FIL ',
        'VIEL', 'FIL', 'FIL',
        'VIEW', 'WIU', 'FIU',
        'VILL(AE)-', 'WIL', None,
        'VIS(ACEIKUVWZ)-<^', 'WIS', None,
        'VI(ELS)--^', 'F', None,
        'VILLON--', 'WILI', 'FILI',
        'VIZE^^', 'FIZE', 'FIZE',
        'VLIE--^', 'FL', None,
        'VL(AEIOU)--', 'W', None,
        'VOKA-^', 'WOK', None,
        'VOL(ATUVW)--^', 'WO', None,
        'VOR^^', 'FOR', 'FUR',
        'VR(AEIOU)--', 'W', None,
        'VV9', 'W', None,
        'VY9^', 'WÜ', 'FI',
        'V(ÜY)-', 'W', None,
        'V(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'W', None,
        'V(AEIJLRU)-<', 'W', None,
        'V.^', 'V.', None,
        'V<', 'F', 'F',
        'WEITERENTWI-----^', 'WEITA ', 'FEITA ',
        'WEITREICH-----^', 'WEIT ', 'FEIT ',
        'WEITVER^', 'WEIT FER', 'FEIT FA',
        'WE(LMNRST)-3^', 'WE', 'FE',
        'WER(DST)-', 'WER', None,
        'WIC$', 'WIZ', 'FIZ',
        'WIEDERU--', 'WIDE', 'FITE',
        'WIEDER^$', 'WIDA', 'FITA',
        'WIEDER^^', 'WIDA ', 'FITA ',
        'WIEVIEL', 'WI FIL', 'FI FIL',
        'WISUEL', 'WISUEL', None,
        'WR-^', 'W', None,
        'WY9^', 'WÜ', 'FI',
        'W(BDFGJKLMNPQRSTZ)-', 'F', None,
        'W$', 'F', None,
        'W', None, 'F',
        'X<^', 'Z', 'Z',
        'XHAVEN$', 'XAFN', None,
        'X(CSZ)', 'X', 'X',
        'XTS(CH)--', 'XT', 'XT',
        'XT(SZ)', 'Z', 'Z',
        'YE(LMNRST)-3^', 'IE', 'IE',
        'YE-3', 'I', 'I',
        'YOR(GK)^$', 'IÖRK', 'IÖRK',
        'Y(AOU)-<7', 'I', 'I',
        'Y(BKLMNPRSTX)-1', 'Ü', None,
        'YVES^$', 'IF', 'IF',
        'YVONNE^$', 'IWON', 'IFUN',
        'Y.^', 'Y.', None,
        'Y', 'I', 'I',
        'ZC(AOU)-', 'SK', 'ZK',
        'ZE(LMNRST)-3^', 'ZE', 'ZE',
        'ZIEJ$', 'ZI', 'ZI',
        'ZIGERJA(HR)-3', 'ZIGA IA', 'ZIKA IA',
        'ZL(AEIOU)-', 'SL', None,
        'ZS(CHT)--', '', '',
        'ZS', 'SH', 'Z',
        'ZUERST', 'ZUERST', 'ZUERST',
        'ZUGRUNDE^$', 'ZU GRUNDE', 'ZU KRUNTE',
        'ZUGRUNDE', 'ZU GRUNDE ', 'ZU KRUNTE ',
        'ZUGUNSTEN', 'ZU GUNSTN', 'ZU KUNZTN',
        'ZUHAUSE-', 'ZU HAUS', 'ZU AUZ',
        'ZULASTEN^$', 'ZU LASTN', 'ZU LAZTN',
        'ZURUECK^^', 'ZURÜK', 'ZURIK',
        'ZURZEIT', 'ZUR ZEIT', 'ZUR ZEIT',
        'ZURÜCK^^', 'ZURÜK', 'ZURIK',
        'ZUSTANDE', 'ZU STANDE', 'ZU ZTANTE',
        'ZUTAGE', 'ZU TAGE', 'ZU TAKE',
        'ZUVER^^', 'ZUFA', 'ZUFA',
        'ZUVIEL', 'ZU FIL', 'ZU FIL',
        'ZUWENIG', 'ZU WENIK', 'ZU FENIK',
        'ZY9^', 'ZÜ', None,
        'ZYK3$', 'ZIK', None,
        'Z(VW)7^', 'SW', None,
        None, None, None
        # fmt: on
    )

    _upper_trans = dict(
        zip(
            (
                ord(_)
                for _ in 'abcdefghijklmnopqrstuvwxyzàáâãåäæ'
                + 'çðèéêëìíîïñòóôõöøœšßþùúûüýÿ'
            ),
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÅÄÆ'
            + 'ÇÐÈÉÊËÌÍÎÏÑÒÓÔÕÖØŒŠßÞÙÚÛÜÝŸ',
        )
    )

    def encode(self, word, mode=1, lang='de'):
        """Return the phonet code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        mode : int
            The ponet variant to employ (1 or 2)
        lang : str
            ``de`` (default) for German, ``none`` for no language

        Returns
        -------
        str
            The phonet value

        Examples
        --------
        >>> pe = Phonet()
        >>> pe.encode('Christopher')
        'KRISTOFA'
        >>> pe.encode('Niall')
        'NIAL'
        >>> pe.encode('Smith')
        'SMIT'
        >>> pe.encode('Schmidt')
        'SHMIT'

        >>> pe.encode('Christopher', mode=2)
        'KRIZTUFA'
        >>> pe.encode('Niall', mode=2)
        'NIAL'
        >>> pe.encode('Smith', mode=2)
        'ZNIT'
        >>> pe.encode('Schmidt', mode=2)
        'ZNIT'

        >>> pe.encode('Christopher', lang='none')
        'CHRISTOPHER'
        >>> pe.encode('Niall', lang='none')
        'NIAL'
        >>> pe.encode('Smith', lang='none')
        'SMITH'
        >>> pe.encode('Schmidt', lang='none')
        'SCHMIDT'

        """
        phonet_hash = Counter()
        alpha_pos = Counter()

        phonet_hash_1 = Counter()
        phonet_hash_2 = Counter()

        def _initialize_phonet(lang):
            """Initialize phonet variables.

            Parameters
            ----------
            lang : str
                Language to use for rules

            """
            if lang == 'none':
                _phonet_rules = self._rules_no_lang
            else:
                _phonet_rules = self._rules_german

            phonet_hash[''] = -1

            # German and international umlauts
            for j in {
                'À',
                'Á',
                'Â',
                'Ã',
                'Ä',
                'Å',
                'Æ',
                'Ç',
                'È',
                'É',
                'Ê',
                'Ë',
                'Ì',
                'Í',
                'Î',
                'Ï',
                'Ð',
                'Ñ',
                'Ò',
                'Ó',
                'Ô',
                'Õ',
                'Ö',
                'Ø',
                'Ù',
                'Ú',
                'Û',
                'Ü',
                'Ý',
                'Þ',
                'ß',
                'Œ',
                'Š',
                'Ÿ',
            }:
                alpha_pos[j] = 1
                phonet_hash[j] = -1

            # "normal" letters ('A'-'Z')
            for i, j in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                alpha_pos[j] = i + 2
                phonet_hash[j] = -1

            for i in range(26):
                for j in range(28):
                    phonet_hash_1[i, j] = -1
                    phonet_hash_2[i, j] = -1

            # for each phonetc rule
            for i in range(len(_phonet_rules)):
                rule = _phonet_rules[i]

                if rule and i % 3 == 0:
                    # calculate first hash value
                    k = _phonet_rules[i][0]

                    if phonet_hash[k] < 0 and (
                        _phonet_rules[i + 1] or _phonet_rules[i + 2]
                    ):
                        phonet_hash[k] = i

                    # calculate second hash values
                    if k and alpha_pos[k] >= 2:
                        k = alpha_pos[k]

                        j = k - 2
                        rule = rule[1:]

                        if not rule:
                            rule = ' '
                        elif rule[0] == '(':
                            rule = rule[1:]
                        else:
                            rule = rule[0]

                        while rule and (rule[0] != ')'):
                            k = alpha_pos[rule[0]]

                            if k > 0:
                                # add hash value for this letter
                                if phonet_hash_1[j, k] < 0:
                                    phonet_hash_1[j, k] = i
                                    phonet_hash_2[j, k] = i

                                if phonet_hash_2[j, k] >= (i - 30):
                                    phonet_hash_2[j, k] = i
                                else:
                                    k = -1

                            if k <= 0:
                                # add hash value for all letters
                                if phonet_hash_1[j, 0] < 0:
                                    phonet_hash_1[j, 0] = i

                                phonet_hash_2[j, 0] = i

                            rule = rule[1:]

        def _phonet(term, mode, lang):
            """Return the phonet coded form of a term.

            Parameters
            ----------
            term : str
                Term to transform
            mode : int
                The ponet variant to employ (1 or 2)
            lang : str
                ``de`` (default) for German, ``none`` for no language

            Returns
            -------
            str
                The phonet value

            """
            if lang == 'none':
                _phonet_rules = self._rules_no_lang
            else:
                _phonet_rules = self._rules_german

            char0 = ''
            dest = term

            if not term:
                return ''

            term_length = len(term)

            # convert input string to upper-case
            src = term.translate(self._upper_trans)

            # check "src"
            i = 0
            j = 0
            zeta = 0

            while i < len(src):
                char = src[i]

                pos = alpha_pos[char]

                if pos >= 2:
                    xpos = pos - 2

                    if i + 1 == len(src):
                        pos = alpha_pos['']
                    else:
                        pos = alpha_pos[src[i + 1]]

                    start1 = phonet_hash_1[xpos, pos]
                    start2 = phonet_hash_1[xpos, 0]
                    end1 = phonet_hash_2[xpos, pos]
                    end2 = phonet_hash_2[xpos, 0]

                    # preserve rule priorities
                    if (start2 >= 0) and ((start1 < 0) or (start2 < start1)):
                        pos = start1
                        start1 = start2
                        start2 = pos
                        pos = end1
                        end1 = end2
                        end2 = pos

                    if (end1 >= start2) and (start2 >= 0):
                        if end2 > end1:
                            end1 = end2

                        start2 = -1
                        end2 = -1
                else:
                    pos = phonet_hash[char]
                    start1 = pos
                    end1 = 10000
                    start2 = -1
                    end2 = -1

                pos = start1
                zeta0 = 0

                if pos >= 0:
                    # check rules for this char
                    while (_phonet_rules[pos] is None) or (
                        _phonet_rules[pos][0] == char
                    ):
                        if pos > end1:
                            if start2 > 0:
                                pos = start2
                                start1 = start2
                                start2 = -1
                                end1 = end2
                                end2 = -1
                                continue

                            break

                        if (_phonet_rules[pos] is None) or (
                            _phonet_rules[pos + mode] is None
                        ):
                            # no conversion rule available
                            pos += 3
                            continue

                        # check whole string
                        matches = 1  # number of matching letters
                        priority = 5  # default priority
                        rule = _phonet_rules[pos]
                        rule = rule[1:]

                        while (
                            rule
                            and (len(src) > (i + matches))
                            and (src[i + matches] == rule[0])
                            and not rule[0].isdigit()
                            and (rule not in '(-<^$')
                        ):
                            matches += 1
                            rule = rule[1:]

                        if rule and (rule[0] == '('):
                            # check an array of letters
                            if (
                                (len(src) > (i + matches))
                                and src[i + matches].isalpha()
                                and (src[i + matches] in rule[1:])
                            ):
                                matches += 1

                                while rule and rule[0] != ')':
                                    rule = rule[1:]

                                # if rule[0] == ')':
                                rule = rule[1:]

                        if rule:
                            priority0 = ord(rule[0])
                        else:
                            priority0 = 0

                        matches0 = matches

                        while rule and rule[0] == '-' and matches > 1:
                            matches -= 1
                            rule = rule[1:]

                        if rule and rule[0] == '<':
                            rule = rule[1:]

                        if rule and rule[0].isdigit():
                            # read priority
                            priority = int(rule[0])
                            rule = rule[1:]

                        if rule and rule[0:2] == '^^':
                            rule = rule[1:]

                        if (
                            not rule
                            or (
                                (rule[0] == '^')
                                and ((i == 0) or not src[i - 1].isalpha())
                                and (
                                    (rule[1:2] != '$')
                                    or (
                                        not (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ].isalpha()
                                        )
                                        and (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ]
                                            != '.'
                                        )
                                    )
                                )
                            )
                            or (
                                (rule[0] == '$')
                                and (i > 0)
                                and src[i - 1].isalpha()
                                and (
                                    (
                                        not src[
                                            i + matches0 : i + matches0 + 1
                                        ].isalpha()
                                    )
                                    and (
                                        src[i + matches0 : i + matches0 + 1]
                                        != '.'
                                    )
                                )
                            )
                        ):
                            # look for continuation, if:
                            # matches > 1 und NO '-' in first string */
                            pos0 = -1

                            start3 = 0
                            start4 = 0
                            end3 = 0
                            end4 = 0

                            if (
                                (matches > 1)
                                and src[i + matches : i + matches + 1]
                                and (priority0 != ord('-'))
                            ):
                                char0 = src[i + matches - 1]
                                pos0 = alpha_pos[char0]

                                if pos0 >= 2 and src[i + matches]:
                                    xpos = pos0 - 2
                                    pos0 = alpha_pos[src[i + matches]]
                                    start3 = phonet_hash_1[xpos, pos0]
                                    start4 = phonet_hash_1[xpos, 0]
                                    end3 = phonet_hash_2[xpos, pos0]
                                    end4 = phonet_hash_2[xpos, 0]

                                    # preserve rule priorities
                                    if (start4 >= 0) and (
                                        (start3 < 0) or (start4 < start3)
                                    ):
                                        pos0 = start3
                                        start3 = start4
                                        start4 = pos0
                                        pos0 = end3
                                        end3 = end4
                                        end4 = pos0

                                    if (end3 >= start4) and (start4 >= 0):
                                        if end4 > end3:
                                            end3 = end4

                                        start4 = -1
                                        end4 = -1
                                else:
                                    pos0 = phonet_hash[char0]
                                    start3 = pos0
                                    end3 = 10000
                                    start4 = -1
                                    end4 = -1

                                pos0 = start3

                            # check continuation rules for src[i+matches]
                            if pos0 >= 0:
                                while (_phonet_rules[pos0] is None) or (
                                    _phonet_rules[pos0][0] == char0
                                ):
                                    if pos0 > end3:
                                        if start4 > 0:
                                            pos0 = start4
                                            start3 = start4
                                            start4 = -1
                                            end3 = end4
                                            end4 = -1
                                            continue

                                        priority0 = -1

                                        # important
                                        break

                                    if (_phonet_rules[pos0] is None) or (
                                        _phonet_rules[pos0 + mode] is None
                                    ):
                                        # no conversion rule available
                                        pos0 += 3
                                        continue

                                    # check whole string
                                    matches0 = matches
                                    priority0 = 5
                                    rule = _phonet_rules[pos0]
                                    rule = rule[1:]

                                    while (
                                        rule
                                        and (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ]
                                            == rule[0]
                                        )
                                        and (
                                            not rule[0].isdigit()
                                            or (rule in '(-<^$')
                                        )
                                    ):
                                        matches0 += 1
                                        rule = rule[1:]

                                    if rule and rule[0] == '(':
                                        # check an array of letters
                                        if src[
                                            i + matches0 : i + matches0 + 1
                                        ].isalpha() and (
                                            src[i + matches0] in rule[1:]
                                        ):
                                            matches0 += 1

                                            while rule and rule[0] != ')':
                                                rule = rule[1:]

                                            # if rule[0] == ')':
                                            rule = rule[1:]

                                    while rule and rule[0] == '-':
                                        # "matches0" is NOT decremented
                                        # because of
                                        #    "if (matches0 == matches)"
                                        rule = rule[1:]

                                    if rule and rule[0] == '<':
                                        rule = rule[1:]

                                    if rule and rule[0].isdigit():
                                        priority0 = int(rule[0])
                                        rule = rule[1:]

                                    if (
                                        not rule
                                        or
                                        # rule == '^' is not possible here
                                        (
                                            (rule[0] == '$')
                                            and not src[
                                                i + matches0 : i + matches0 + 1
                                            ].isalpha()
                                            and (
                                                src[
                                                    i
                                                    + matches0 : i
                                                    + matches0
                                                    + 1
                                                ]
                                                != '.'
                                            )
                                        )
                                    ):
                                        if matches0 == matches:
                                            # this is only a partial string
                                            pos0 += 3
                                            continue

                                        if priority0 < priority:
                                            # priority is too low
                                            pos0 += 3
                                            continue

                                        # continuation rule found
                                        break

                                    pos0 += 3

                                # end of "while"
                                if (priority0 >= priority) and (
                                    (_phonet_rules[pos0] is not None)
                                    and (_phonet_rules[pos0][0] == char0)
                                ):

                                    pos += 3
                                    continue

                            # replace string
                            if _phonet_rules[pos] and (
                                '<' in _phonet_rules[pos][1:]
                            ):
                                priority0 = 1
                            else:
                                priority0 = 0

                            rule = _phonet_rules[pos + mode]

                            if (priority0 == 1) and (zeta == 0):
                                # rule with '<' is applied
                                if (
                                    (j > 0)
                                    and rule
                                    and (
                                        (dest[j - 1] == char)
                                        or (dest[j - 1] == rule[0])
                                    )
                                ):
                                    j -= 1

                                zeta0 = 1
                                zeta += 1
                                matches0 = 0

                                while rule and src[i + matches0]:
                                    src = (
                                        src[0 : i + matches0]
                                        + rule[0]
                                        + src[i + matches0 + 1 :]
                                    )
                                    matches0 += 1
                                    rule = rule[1:]

                                if matches0 < matches:
                                    src = (
                                        src[0 : i + matches0]
                                        + src[i + matches :]
                                    )

                                char = src[i]
                            else:
                                i = i + matches - 1
                                zeta = 0

                                while len(rule) > 1:
                                    if (j == 0) or (dest[j - 1] != rule[0]):
                                        dest = (
                                            dest[0:j]
                                            + rule[0]
                                            + dest[min(len(dest), j + 1) :]
                                        )
                                        j += 1

                                    rule = rule[1:]

                                # new "current char"
                                if not rule:
                                    rule = ''
                                    char = ''
                                else:
                                    char = rule[0]

                                if (
                                    _phonet_rules[pos]
                                    and '^^' in _phonet_rules[pos][1:]
                                ):
                                    if char:
                                        dest = (
                                            dest[0:j]
                                            + char
                                            + dest[min(len(dest), j + 1) :]
                                        )
                                        j += 1

                                    src = src[i + 1 :]
                                    i = 0
                                    zeta0 = 1

                            break

                        pos += 3

                        if pos > end1 and start2 > 0:
                            pos = start2
                            start1 = start2
                            end1 = end2
                            start2 = -1
                            end2 = -1

                if zeta0 == 0:
                    if char and ((j == 0) or (dest[j - 1] != char)):
                        # delete multiple letters only
                        dest = (
                            dest[0:j] + char + dest[min(j + 1, term_length) :]
                        )
                        j += 1

                    i += 1
                    zeta = 0

            dest = dest[0:j]

            return dest

        _initialize_phonet(lang)

        word = unicode_normalize('NFKC', text_type(word))
        return _phonet(word, mode, lang)


def phonet(word, mode=1, lang='de'):
    """Return the phonet code for a word.

    This is a wrapper for :py:meth:`Phonet.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    mode : int
        The ponet variant to employ (1 or 2)
    lang : str
        ``de`` (default) for German, ``none`` for no language

    Returns
    -------
    str
        The phonet value

    Examples
    --------
    >>> phonet('Christopher')
    'KRISTOFA'
    >>> phonet('Niall')
    'NIAL'
    >>> phonet('Smith')
    'SMIT'
    >>> phonet('Schmidt')
    'SHMIT'

    >>> phonet('Christopher', mode=2)
    'KRIZTUFA'
    >>> phonet('Niall', mode=2)
    'NIAL'
    >>> phonet('Smith', mode=2)
    'ZNIT'
    >>> phonet('Schmidt', mode=2)
    'ZNIT'

    >>> phonet('Christopher', lang='none')
    'CHRISTOPHER'
    >>> phonet('Niall', lang='none')
    'NIAL'
    >>> phonet('Smith', lang='none')
    'SMITH'
    >>> phonet('Schmidt', lang='none')
    'SCHMIDT'

    """
    return Phonet().encode(word, mode, lang)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
