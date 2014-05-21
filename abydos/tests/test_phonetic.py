# -*- coding: utf-8 -*-
"""abydos.tests.test_phonetic

This module contains unit tests for abydos.phonetic

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

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
import unittest
from abydos.phonetic import russell_index, russell_index_num_to_alpha, \
    russell_index_alpha, soundex, dm_soundex, koelner_phonetik, \
    koelner_phonetik_num_to_alpha, koelner_phonetik_alpha, nysiis, mra, \
    metaphone, double_metaphone, caverphone, alpha_sis

class russell_index_test_cases(unittest.TestCase):
    def test_russel_index(self):
        self.assertEquals(russell_index(''), None)
        self.assertEquals(russell_index('Hoppa'), 12)
        self.assertEquals(russell_index('Hopley'), 125)
        self.assertEquals(russell_index('Highfield'), 1254)
        self.assertEquals(russell_index('Wright'), 814)
        self.assertEquals(russell_index('Carter'), 31848)
        self.assertEquals(russell_index('Hopf'), 12)
        self.assertEquals(russell_index('Hay'), 1)
        self.assertEquals(russell_index('Haas'), 1)
        self.assertEquals(russell_index('Meyers'), 618)
        self.assertEquals(russell_index('Myers'), 618)
        self.assertEquals(russell_index('Meyer'), 618)
        self.assertEquals(russell_index('Myer'), 618)
        self.assertEquals(russell_index('Mack'), 613)
        self.assertEquals(russell_index('Knack'), 3713)

    def test_russel_index_num_to_alpha(self):
        self.assertEquals(russell_index_num_to_alpha(0), None)
        self.assertEquals(russell_index_num_to_alpha(''), None)
        self.assertEquals(russell_index_num_to_alpha(123456789), 'ABCDLMNR')
        self.assertEquals(russell_index_num_to_alpha('0123456789'), 'ABCDLMNR')

    def test_russel_index_alpha(self):
        self.assertEquals(russell_index_alpha(''), None)
        self.assertEquals(russell_index_alpha('Hoppa'), 'AB')
        self.assertEquals(russell_index_alpha('Hopley'), 'ABL')
        self.assertEquals(russell_index_alpha('Highfield'), 'ABLD')
        self.assertEquals(russell_index_alpha('Wright'), 'RAD')
        self.assertEquals(russell_index_alpha('Carter'), 'CARDR')
        self.assertEquals(russell_index_alpha('Hopf'), 'AB')
        self.assertEquals(russell_index_alpha('Hay'), 'A')
        self.assertEquals(russell_index_alpha('Haas'), 'A')
        self.assertEquals(russell_index_alpha('Meyers'), 'MAR')
        self.assertEquals(russell_index_alpha('Myers'), 'MAR')
        self.assertEquals(russell_index_alpha('Meyer'), 'MAR')
        self.assertEquals(russell_index_alpha('Myer'), 'MAR')
        self.assertEquals(russell_index_alpha('Mack'), 'MAC')
        self.assertEquals(russell_index_alpha('Knack'), 'CNAC')


class soundex_test_cases(unittest.TestCase):
    def test_soundex(self):
        self.assertEquals(soundex(''), '0000')

        # https://archive.org/stream/accessingindivid00moor#page/14/mode/2up
        self.assertEquals(soundex('Euler'), 'E460')
        self.assertEquals(soundex('Gauss'), 'G200')
        self.assertEquals(soundex('Hilbert'), 'H416')
        self.assertEquals(soundex('Knuth'), 'K530')
        self.assertEquals(soundex('Lloyd'), 'L300')
        self.assertEquals(soundex('Lukasieicz'), 'L222')
        self.assertEquals(soundex('Ellery'), 'E460')
        self.assertEquals(soundex('Ghosh'), 'G200')
        self.assertEquals(soundex('Heilbronn'), 'H416')
        self.assertEquals(soundex('Kant'), 'K530')
        self.assertEquals(soundex('Ladd'), 'L300')
        self.assertEquals(soundex('Lissajous'), 'L222')
        self.assertEquals(soundex('Rogers'), 'R262')
        self.assertEquals(soundex('Rodgers'), 'R326')
        self.assertNotEquals(soundex('Rogers'), soundex('Rodgers'))
        self.assertNotEquals(soundex('Sinclair'), soundex('St. Clair'))
        self.assertNotEquals(soundex('Tchebysheff'), soundex('Chebyshev'))

        # http://creativyst.com/Doc/Articles/SoundEx1/SoundEx1.htm#Related
        self.assertEquals(soundex('Htacky'), 'H320')
        self.assertEquals(soundex('Atacky'), 'A320')
        self.assertEquals(soundex('Schmit'), 'S530')
        self.assertEquals(soundex('Schneider'), 'S536')
        self.assertEquals(soundex('Pfister'), 'P236')
        self.assertEquals(soundex('Ashcroft'), 'A261')
        self.assertEquals(soundex('Asicroft'), 'A226')

        # https://en.wikipedia.org/wiki/Soundex
        self.assertEquals(soundex('Robert'), 'R163')
        self.assertEquals(soundex('Rupert'), 'R163')
        self.assertEquals(soundex('Rubin'), 'R150')
        self.assertEquals(soundex('Tymczak'), 'T522')

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEquals(soundex('Peters'), 'P362')
        self.assertEquals(soundex('Peterson'), 'P362')
        self.assertEquals(soundex('Moskowitz'), 'M232')
        self.assertEquals(soundex('Moskovitz'), 'M213')
        self.assertEquals(soundex('Auerbach'), 'A612')
        self.assertEquals(soundex('Uhrbach'), 'U612')
        self.assertEquals(soundex('Jackson'), 'J250')
        self.assertEquals(soundex('Jackson-Jackson'), 'J252')

        # maxlength tests
        self.assertEquals(soundex('Lincoln', 10), 'L524500000')
        self.assertEquals(soundex('Lincoln', 5), 'L5245')
        self.assertEquals(soundex('Christopher', 6), 'C62316')

        # reverse tests
        self.assertEquals(soundex('Rubin', reverse=True), 'N160')
        self.assertEquals(soundex('Llyod', reverse=True), 'D400')
        self.assertEquals(soundex('Lincoln', reverse=True), 'N425')
        self.assertEquals(soundex('Knuth', reverse=True), 'H352')

    def test_soundex_caversham_testset(self):
        # caversham.otago.ac.nz/files/variantNames.csv
        self.assertEquals(soundex('abernathy'), 'A165')
        self.assertEquals(soundex('abernethie'), 'A165')
        self.assertEquals(soundex('abernethy'), 'A165')
        self.assertEquals(soundex('ailen'), 'A450')
        self.assertEquals(soundex('aldridge'), 'A436')
        self.assertEquals(soundex('allan'), 'A450')
        self.assertEquals(soundex('allen'), 'A450')
        self.assertEquals(soundex('andersen'), 'A536')
        self.assertEquals(soundex('anderson'), 'A536')
        self.assertEquals(soundex('andorson'), 'A536')
        self.assertEquals(soundex('applegart'), 'A142')
        self.assertEquals(soundex('applegarth'), 'A142')
        self.assertEquals(soundex('arnal'), 'A654')
        self.assertEquals(soundex('arnel'), 'A654')
        self.assertEquals(soundex('bail'), 'B400')
        self.assertEquals(soundex('bailer'), 'B460')
        self.assertEquals(soundex('bailey'), 'B400')
        self.assertEquals(soundex('bain'), 'B500')
        self.assertEquals(soundex('baley'), 'B400')
        self.assertEquals(soundex('ball'), 'B400')
        self.assertEquals(soundex('barclay'), 'B624')
        self.assertEquals(soundex('barkla'), 'B624')
        self.assertEquals(soundex('barlthrop'), 'B643')
        self.assertEquals(soundex('barltrop'), 'B643')
        self.assertEquals(soundex('barnett'), 'B653')
        self.assertEquals(soundex('barratt'), 'B630')
        self.assertEquals(soundex('barrett'), 'B630')
        self.assertEquals(soundex('barrie'), 'B600')
        self.assertEquals(soundex('barwick'), 'B620')
        self.assertEquals(soundex('baylee'), 'B400')
        self.assertEquals(soundex('bell'), 'B400')
        self.assertEquals(soundex('bellet'), 'B430')
        self.assertEquals(soundex('bellett'), 'B430')
        self.assertEquals(soundex('bennet'), 'B530')
        self.assertEquals(soundex('bennett'), 'B530')
        self.assertEquals(soundex('bennie'), 'B500')
        self.assertEquals(soundex('bernie'), 'B650')
        self.assertEquals(soundex('berry'), 'B600')
        self.assertEquals(soundex('berwick'), 'B620')
        self.assertEquals(soundex('beven'), 'B150')
        self.assertEquals(soundex('bevin'), 'B150')
        self.assertEquals(soundex('binnie'), 'B500')
        self.assertEquals(soundex('birrell'), 'B640')
        self.assertEquals(soundex('black'), 'B420')
        self.assertEquals(soundex('blake'), 'B420')
        self.assertEquals(soundex('blakeley'), 'B424')
        self.assertEquals(soundex('blakely'), 'B424')
        self.assertEquals(soundex('bouchor'), 'B260')
        self.assertEquals(soundex('boutcher'), 'B326')
        self.assertEquals(soundex('brand'), 'B653')
        self.assertEquals(soundex('brandt'), 'B653')
        self.assertEquals(soundex('brock'), 'B620')
        self.assertEquals(soundex('brockie'), 'B620')
        self.assertEquals(soundex('brook'), 'B620')
        self.assertEquals(soundex('brooke'), 'B620')
        self.assertEquals(soundex('brown'), 'B650')
        self.assertEquals(soundex('browne'), 'B650')
        self.assertEquals(soundex('bruten'), 'B635')
        self.assertEquals(soundex('bruton'), 'B635')
        self.assertEquals(soundex('bulger'), 'B426')
        self.assertEquals(soundex('bull'), 'B400')
        self.assertEquals(soundex('burger'), 'B626')
        self.assertEquals(soundex('burgess'), 'B622')
        self.assertEquals(soundex('burnett'), 'B653')
        self.assertEquals(soundex('buttermore'), 'B365')
        self.assertEquals(soundex('buttimore'), 'B356')
        self.assertEquals(soundex('calder'), 'C436')
        self.assertEquals(soundex('caley'), 'C400')
        self.assertEquals(soundex('callaghan'), 'C425')
        self.assertEquals(soundex('callander'), 'C453')
        self.assertEquals(soundex('callender'), 'C453')
        self.assertEquals(soundex('callighan'), 'C425')
        self.assertEquals(soundex('carder'), 'C636')
        self.assertEquals(soundex('carley'), 'C640')
        self.assertEquals(soundex('carruthers'), 'C636')
        self.assertEquals(soundex('carside'), 'C623')
        self.assertEquals(soundex('caruthers'), 'C636')
        self.assertEquals(soundex('case'), 'C200')
        self.assertEquals(soundex('casey'), 'C200')
        self.assertEquals(soundex('cassells'), 'C242')
        self.assertEquals(soundex('cassels'), 'C242')
        self.assertEquals(soundex('cassidy'), 'C230')
        self.assertEquals(soundex('chaplain'), 'C145')
        self.assertEquals(soundex('chaplin'), 'C145')
        self.assertEquals(soundex('chrisp'), 'C621')
        self.assertEquals(soundex('chronican'), 'C652')
        self.assertEquals(soundex('chronichan'), 'C652')
        self.assertEquals(soundex('clark'), 'C462')
        self.assertEquals(soundex('clarke'), 'C462')
        self.assertEquals(soundex('clent'), 'C453')
        self.assertEquals(soundex('clint'), 'C453')
        self.assertEquals(soundex('coates'), 'C320')
        self.assertEquals(soundex('coats'), 'C320')
        self.assertEquals(soundex('conheady'), 'C530')
        self.assertEquals(soundex('connell'), 'C540')
        self.assertEquals(soundex('connolly'), 'C540')
        self.assertEquals(soundex('conolly'), 'C540')
        self.assertEquals(soundex('cook'), 'C200')
        self.assertEquals(soundex('cooke'), 'C200')
        self.assertEquals(soundex('corcoran'), 'C626')
        self.assertEquals(soundex('corkran'), 'C626')
        self.assertEquals(soundex('cornell'), 'C654')
        self.assertEquals(soundex('cosegrove'), 'C226')
        self.assertEquals(soundex('cosgrove'), 'C261')
        self.assertEquals(soundex('coulter'), 'C436')
        self.assertEquals(soundex('coupar'), 'C160')
        self.assertEquals(soundex('couper'), 'C160')
        self.assertEquals(soundex('courter'), 'C636')
        self.assertEquals(soundex('craig'), 'C620')
        self.assertEquals(soundex('craik'), 'C620')
        self.assertEquals(soundex('crammond'), 'C655')
        self.assertEquals(soundex('cramond'), 'C655')
        self.assertEquals(soundex('crawford'), 'C616')
        self.assertEquals(soundex('crawfurd'), 'C616')
        self.assertEquals(soundex('cress'), 'C620')
        self.assertEquals(soundex('crisp'), 'C621')
        self.assertEquals(soundex('crosbie'), 'C621')
        self.assertEquals(soundex('crosby'), 'C621')
        self.assertEquals(soundex('crossan'), 'C625')
        self.assertEquals(soundex('crossian'), 'C625')
        self.assertEquals(soundex('cruse'), 'C620')
        self.assertEquals(soundex('cubbins'), 'C152')
        self.assertEquals(soundex('culsey'), 'C420')
        self.assertEquals(soundex('cunhingham'), 'C552')
        self.assertEquals(soundex('cunningham'), 'C552')
        self.assertEquals(soundex('curran'), 'C650')
        self.assertEquals(soundex('curren'), 'C650')
        self.assertEquals(soundex('cursey'), 'C620')
        self.assertEquals(soundex('daly'), 'D400')
        self.assertEquals(soundex('davany'), 'D150')
        self.assertEquals(soundex('daveis'), 'D120')
        self.assertEquals(soundex('davies'), 'D120')
        self.assertEquals(soundex('davis'), 'D120')
        self.assertEquals(soundex('davys'), 'D120')
        self.assertEquals(soundex('delaney'), 'D450')
        self.assertEquals(soundex('delany'), 'D450')
        self.assertEquals(soundex('delargey'), 'D462')
        self.assertEquals(soundex('delargy'), 'D462')
        self.assertEquals(soundex('dely'), 'D400')
        self.assertEquals(soundex('denfold'), 'D514')
        self.assertEquals(soundex('denford'), 'D516')
        self.assertEquals(soundex('devaney'), 'D150')
        self.assertEquals(soundex('dickison'), 'D225')
        self.assertEquals(soundex('dickson'), 'D250')
        self.assertEquals(soundex('dillan'), 'D450')
        self.assertEquals(soundex('dillon'), 'D450')
        self.assertEquals(soundex('dockworth'), 'D263')
        self.assertEquals(soundex('dodd'), 'D300')
        self.assertEquals(soundex('donne'), 'D500')
        self.assertEquals(soundex('dougal'), 'D240')
        self.assertEquals(soundex('dougall'), 'D240')
        self.assertEquals(soundex('douglas'), 'D242')
        self.assertEquals(soundex('douglass'), 'D242')
        self.assertEquals(soundex('dreaver'), 'D616')
        self.assertEquals(soundex('dreavor'), 'D616')
        self.assertEquals(soundex('droaver'), 'D616')
        self.assertEquals(soundex('duckworth'), 'D263')
        self.assertEquals(soundex('dunn'), 'D500')
        self.assertEquals(soundex('dunne'), 'D500')
        self.assertEquals(soundex('eagan'), 'E250')
        self.assertEquals(soundex('eagar'), 'E260')
        self.assertEquals(soundex('eager'), 'E260')
        self.assertEquals(soundex('easson'), 'E250')
        self.assertEquals(soundex('egan'), 'E250')
        self.assertEquals(soundex('eldridge'), 'E436')
        self.assertEquals(soundex('elliis'), 'E420')
        self.assertEquals(soundex('ellis'), 'E420')
        self.assertEquals(soundex('emerson'), 'E562')
        self.assertEquals(soundex('emmerson'), 'E562')
        self.assertEquals(soundex('essson'), 'E250')
        self.assertEquals(soundex('fahey'), 'F000')
        self.assertEquals(soundex('fahy'), 'F000')
        self.assertEquals(soundex('fail'), 'F400')
        self.assertEquals(soundex('fairbairn'), 'F616')
        self.assertEquals(soundex('fairburn'), 'F616')
        self.assertEquals(soundex('faithful'), 'F314')
        self.assertEquals(soundex('faithfull'), 'F314')
        self.assertEquals(soundex('fall'), 'F400')
        self.assertEquals(soundex('farminger'), 'F655')
        self.assertEquals(soundex('farry'), 'F600')
        self.assertEquals(soundex('feil'), 'F400')
        self.assertEquals(soundex('fell'), 'F400')
        self.assertEquals(soundex('fennessey'), 'F520')
        self.assertEquals(soundex('fennessy'), 'F520')
        self.assertEquals(soundex('ferry'), 'F600')
        self.assertEquals(soundex('fiddes'), 'F320')
        self.assertEquals(soundex('fiddis'), 'F320')
        self.assertEquals(soundex('fielden'), 'F435')
        self.assertEquals(soundex('fielder'), 'F436')
        self.assertEquals(soundex('findlay'), 'F534')
        self.assertEquals(soundex('findley'), 'F534')
        self.assertEquals(soundex('fitzpatric'), 'F321')
        self.assertEquals(soundex('fitzpatrick'), 'F321')
        self.assertEquals(soundex('fraer'), 'F660')
        self.assertEquals(soundex('fraher'), 'F660')
        self.assertEquals(soundex('fullarton'), 'F463')
        self.assertEquals(soundex('fullerton'), 'F463')
        self.assertEquals(soundex('furminger'), 'F655')
        self.assertEquals(soundex('gailichan'), 'G425')
        self.assertEquals(soundex('galbraith'), 'G416')
        self.assertEquals(soundex('gallanders'), 'G453')
        self.assertEquals(soundex('gallaway'), 'G400')
        self.assertEquals(soundex('gallbraith'), 'G416')
        self.assertEquals(soundex('gallichan'), 'G425')
        self.assertEquals(soundex('galloway'), 'G400')
        self.assertEquals(soundex('garcho'), 'G620')
        self.assertEquals(soundex('garchow'), 'G620')
        self.assertEquals(soundex('garret'), 'G630')
        self.assertEquals(soundex('garrett'), 'G630')
        self.assertEquals(soundex('garside'), 'G623')
        self.assertEquals(soundex('geddes'), 'G320')
        self.assertEquals(soundex('geddis'), 'G320')
        self.assertEquals(soundex('george'), 'G620')
        self.assertEquals(soundex('georgeison'), 'G622')
        self.assertEquals(soundex('georgeson'), 'G622')
        self.assertEquals(soundex('gillanders'), 'G453')
        self.assertEquals(soundex('gillespie'), 'G421')
        self.assertEquals(soundex('gillispie'), 'G421')
        self.assertEquals(soundex('gilmore'), 'G456')
        self.assertEquals(soundex('gilmour'), 'G456')
        self.assertEquals(soundex('glendining'), 'G453')
        self.assertEquals(soundex('glendinnin'), 'G453')
        self.assertEquals(soundex('glendinning'), 'G453')
        self.assertEquals(soundex('gorge'), 'G620')
        self.assertEquals(soundex('graig'), 'G620')
        self.assertEquals(soundex('gray'), 'G600')
        self.assertEquals(soundex('greeves'), 'G612')
        self.assertEquals(soundex('greig'), 'G620')
        self.assertEquals(soundex('greves'), 'G612')
        self.assertEquals(soundex('grey'), 'G600')
        self.assertEquals(soundex('griffiths'), 'G613')
        self.assertEquals(soundex('griffths'), 'G613')
        self.assertEquals(soundex('grig'), 'G620')
        self.assertEquals(soundex('grigg'), 'G620')
        self.assertEquals(soundex('gubbins'), 'G152')
        self.assertEquals(soundex('gulbins'), 'G415')
        self.assertEquals(soundex('haddon'), 'H350')
        self.assertEquals(soundex('hal'), 'H400')
        self.assertEquals(soundex('hall'), 'H400')
        self.assertEquals(soundex('hanley'), 'H540')
        self.assertEquals(soundex('hanly'), 'H540')
        self.assertEquals(soundex('hannagan'), 'H525')
        self.assertEquals(soundex('hannan'), 'H550')
        self.assertEquals(soundex('hannigan'), 'H525')
        self.assertEquals(soundex('hanon'), 'H550')
        self.assertEquals(soundex('harman'), 'H655')
        self.assertEquals(soundex('hart'), 'H630')
        self.assertEquals(soundex('harty'), 'H630')
        self.assertEquals(soundex('hatton'), 'H350')
        self.assertEquals(soundex('hayden'), 'H350')
        self.assertEquals(soundex('hay'), 'H000')
        self.assertEquals(soundex('healey'), 'H400')
        self.assertEquals(soundex('healy'), 'H400')
        self.assertEquals(soundex('helleyer'), 'H460')
        self.assertEquals(soundex('hellyer'), 'H460')
        self.assertEquals(soundex('henaghan'), 'H525')
        self.assertEquals(soundex('heneghan'), 'H525')
        self.assertEquals(soundex('herman'), 'H655')
        self.assertEquals(soundex('hey'), 'H000')
        self.assertEquals(soundex('hill'), 'H400')
        self.assertEquals(soundex('hinde'), 'H530')
        self.assertEquals(soundex('hobcraft'), 'H126')
        self.assertEquals(soundex('hobcroft'), 'H126')
        self.assertEquals(soundex('hocking'), 'H252')
        self.assertEquals(soundex('hoeking'), 'H252')
        self.assertEquals(soundex('holander'), 'H453')
        self.assertEquals(soundex('holdgate'), 'H432')
        self.assertEquals(soundex('holgate'), 'H423')
        self.assertEquals(soundex('hollander'), 'H453')
        self.assertEquals(soundex('home'), 'H500')
        self.assertEquals(soundex('horne'), 'H650')
        self.assertEquals(soundex('horn'), 'H650')
        self.assertEquals(soundex('howarth'), 'H630')
        self.assertEquals(soundex('howe'), 'H000')
        self.assertEquals(soundex('howie'), 'H000')
        self.assertEquals(soundex('howorth'), 'H630')
        self.assertEquals(soundex('hoy'), 'H000')
        self.assertEquals(soundex('huddlestone'), 'H342')
        self.assertEquals(soundex('huddleston'), 'H342')
        self.assertEquals(soundex('hugget'), 'H230')
        self.assertEquals(soundex('huggett'), 'H230')
        self.assertEquals(soundex('hume'), 'H500')
        self.assertEquals(soundex('hunt'), 'H530')
        self.assertEquals(soundex('hurt'), 'H630')
        self.assertEquals(soundex('hutcheson'), 'H322')
        self.assertEquals(soundex('hutchison'), 'H322')
        self.assertEquals(soundex('hutt'), 'H300')
        self.assertEquals(soundex('hutton'), 'H350')
        self.assertEquals(soundex('jacobsen'), 'J212')
        self.assertEquals(soundex('jacobs'), 'J212')
        self.assertEquals(soundex('jacobson'), 'J212')
        self.assertEquals(soundex('jaicobs'), 'J212')
        self.assertEquals(soundex('jamieson'), 'J525')
        self.assertEquals(soundex('jamison'), 'J525')
        self.assertEquals(soundex('jansen'), 'J525')
        self.assertEquals(soundex('janson'), 'J525')
        self.assertEquals(soundex('jardine'), 'J635')
        self.assertEquals(soundex('jeannings'), 'J552')
        self.assertEquals(soundex('jeffery'), 'J160')
        self.assertEquals(soundex('jeffrey'), 'J160')
        self.assertEquals(soundex('jelly'), 'J400')
        self.assertEquals(soundex('jennings'), 'J552')
        self.assertEquals(soundex('johns'), 'J520')
        self.assertEquals(soundex('johnstone'), 'J523')
        self.assertEquals(soundex('johnston'), 'J523')
        self.assertEquals(soundex('jolly'), 'J400')
        self.assertEquals(soundex('jones'), 'J520')
        self.assertEquals(soundex('jurdine'), 'J635')
        self.assertEquals(soundex('kean'), 'K500')
        self.assertEquals(soundex('keen'), 'K500')
        self.assertEquals(soundex('keennelly'), 'K540')
        self.assertEquals(soundex('kellan'), 'K450')
        self.assertEquals(soundex('kennard'), 'K563')
        self.assertEquals(soundex('kennealy'), 'K540')
        self.assertEquals(soundex('kennedy'), 'K530')
        self.assertEquals(soundex('kenn'), 'K500')
        self.assertEquals(soundex('killin'), 'K450')
        self.assertEquals(soundex('kirkaldie'), 'K624')
        self.assertEquals(soundex('kirkcaldie'), 'K624')
        self.assertEquals(soundex('kirke'), 'K620')
        self.assertEquals(soundex('kirk'), 'K620')
        self.assertEquals(soundex('kitchen'), 'K325')
        self.assertEquals(soundex('kitchin'), 'K325')
        self.assertEquals(soundex('krause'), 'K620')
        self.assertEquals(soundex('kraus'), 'K620')
        self.assertEquals(soundex('langham'), 'L525')
        self.assertEquals(soundex('lanham'), 'L550')
        self.assertEquals(soundex('larson'), 'L625')
        self.assertEquals(soundex('laughlin'), 'L245')
        self.assertEquals(soundex('laurie'), 'L600')
        self.assertEquals(soundex('lawrie'), 'L600')
        self.assertEquals(soundex('lawson'), 'L250')
        self.assertEquals(soundex('leary'), 'L600')
        self.assertEquals(soundex('leech'), 'L200')
        self.assertEquals(soundex('leery'), 'L600')
        self.assertEquals(soundex('leitch'), 'L320')
        self.assertEquals(soundex('lemin'), 'L550')
        self.assertEquals(soundex('lemon'), 'L550')
        self.assertEquals(soundex('lenihan'), 'L550')
        self.assertEquals(soundex('lennon'), 'L550')
        self.assertEquals(soundex('leyden'), 'L350')
        self.assertEquals(soundex('leydon'), 'L350')
        self.assertEquals(soundex('lister'), 'L236')
        self.assertEquals(soundex('list'), 'L230')
        self.assertEquals(soundex('livingstone'), 'L152')
        self.assertEquals(soundex('livingston'), 'L152')
        self.assertEquals(soundex('lochhead'), 'L230')
        self.assertEquals(soundex('lockhead'), 'L230')
        self.assertEquals(soundex('loughlin'), 'L245')
        self.assertEquals(soundex('macallum'), 'M245')
        self.assertEquals(soundex('macaskill'), 'M224')
        self.assertEquals(soundex('macaulay'), 'M240')
        self.assertEquals(soundex('macauley'), 'M240')
        self.assertEquals(soundex('macbeath'), 'M213')
        self.assertEquals(soundex('macdonald'), 'M235')
        self.assertEquals(soundex('maceewan'), 'M250')
        self.assertEquals(soundex('macewan'), 'M250')
        self.assertEquals(soundex('macfarlane'), 'M216')
        self.assertEquals(soundex('macintosh'), 'M253')
        self.assertEquals(soundex('mackechnie'), 'M225')
        self.assertEquals(soundex('mackenzie'), 'M252')
        self.assertEquals(soundex('mackersey'), 'M262')
        self.assertEquals(soundex('mackersy'), 'M262')
        self.assertEquals(soundex('maclean'), 'M245')
        self.assertEquals(soundex('macnee'), 'M250')
        self.assertEquals(soundex('macpherson'), 'M216')
        self.assertEquals(soundex('main'), 'M500')
        self.assertEquals(soundex('maley'), 'M400')
        self.assertEquals(soundex('malladew'), 'M430')
        self.assertEquals(soundex('maloney'), 'M450')
        self.assertEquals(soundex('mann'), 'M500')
        self.assertEquals(soundex('marchant'), 'M625')
        self.assertEquals(soundex('marett'), 'M630')
        self.assertEquals(soundex('marrett'), 'M630')
        self.assertEquals(soundex('mason'), 'M250')
        self.assertEquals(soundex('matheson'), 'M325')
        self.assertEquals(soundex('mathieson'), 'M325')
        self.assertEquals(soundex('mattingle'), 'M352')
        self.assertEquals(soundex('mattingly'), 'M352')
        self.assertEquals(soundex('mawson'), 'M250')
        self.assertEquals(soundex('mcaulay'), 'M240')
        self.assertEquals(soundex('mcauley'), 'M240')
        self.assertEquals(soundex('mcauliffe'), 'M241')
        self.assertEquals(soundex('mcauliff'), 'M241')
        self.assertEquals(soundex('mcbeath'), 'M213')
        self.assertEquals(soundex('mccallum'), 'M245')
        self.assertEquals(soundex('mccarthy'), 'M263')
        self.assertEquals(soundex('mccarty'), 'M263')
        self.assertEquals(soundex('mccaskill'), 'M224')
        self.assertEquals(soundex('mccay'), 'M200')
        self.assertEquals(soundex('mcclintock'), 'M245')
        self.assertEquals(soundex('mccluskey'), 'M242')
        self.assertEquals(soundex('mcclusky'), 'M242')
        self.assertEquals(soundex('mccormack'), 'M265')
        self.assertEquals(soundex('mccormacl'), 'M265')
        self.assertEquals(soundex('mccrorie'), 'M266')
        self.assertEquals(soundex('mccrory'), 'M266')
        self.assertEquals(soundex('mccrossan'), 'M262')
        self.assertEquals(soundex('mccrossin'), 'M262')
        self.assertEquals(soundex('mcdermott'), 'M236')
        self.assertEquals(soundex('mcdiarmid'), 'M236')
        self.assertEquals(soundex('mcdonald'), 'M235')
        self.assertEquals(soundex('mcdonell'), 'M235')
        self.assertEquals(soundex('mcdonnell'), 'M235')
        self.assertEquals(soundex('mcdowall'), 'M234')
        self.assertEquals(soundex('mcdowell'), 'M234')
        self.assertEquals(soundex('mcewan'), 'M250')
        self.assertEquals(soundex('mcewen'), 'M250')
        self.assertEquals(soundex('mcfarlane'), 'M216')
        self.assertEquals(soundex('mcfaull'), 'M214')
        self.assertEquals(soundex('mcgill'), 'M240')
        self.assertEquals(soundex('mciintyre'), 'M253')
        self.assertEquals(soundex('mcintosh'), 'M253')
        self.assertEquals(soundex('mcintyre'), 'M253')
        self.assertEquals(soundex('mciver'), 'M216')
        self.assertEquals(soundex('mcivor'), 'M216')
        self.assertEquals(soundex('mckay'), 'M200')
        self.assertEquals(soundex('mckechnie'), 'M225')
        self.assertEquals(soundex('mckecknie'), 'M225')
        self.assertEquals(soundex('mckellar'), 'M246')
        self.assertEquals(soundex('mckenzie'), 'M252')
        self.assertEquals(soundex('mcketterick'), 'M236')
        self.assertEquals(soundex('mckey'), 'M200')
        self.assertEquals(soundex('mckinlay'), 'M254')
        self.assertEquals(soundex('mckinley'), 'M254')
        self.assertEquals(soundex('mckitterick'), 'M236')
        self.assertEquals(soundex('mclachlan'), 'M242')
        self.assertEquals(soundex('mclauchlan'), 'M242')
        self.assertEquals(soundex('mclauchlin'), 'M242')
        self.assertEquals(soundex('mclaughlan'), 'M242')
        self.assertEquals(soundex('mclaughlin'), 'M242')
        self.assertEquals(soundex('mclean'), 'M245')
        self.assertEquals(soundex('mcledd'), 'M243')
        self.assertEquals(soundex('mcledowne'), 'M243')
        self.assertEquals(soundex('mcledowney'), 'M243')
        self.assertEquals(soundex('mclellan'), 'M244')
        self.assertEquals(soundex('mcleod'), 'M243')
        self.assertEquals(soundex('mclintock'), 'M245')
        self.assertEquals(soundex('mcloud'), 'M243')
        self.assertEquals(soundex('mcloughlin'), 'M242')
        self.assertEquals(soundex('mcmillan'), 'M254')
        self.assertEquals(soundex('mcmullan'), 'M254')
        self.assertEquals(soundex('mcmullen'), 'M254')
        self.assertEquals(soundex('mcnair'), 'M256')
        self.assertEquals(soundex('mcnalty'), 'M254')
        self.assertEquals(soundex('mcnatty'), 'M253')
        self.assertEquals(soundex('mcnee'), 'M250')
        self.assertEquals(soundex('mcneill'), 'M254')
        self.assertEquals(soundex('mcneil'), 'M254')
        self.assertEquals(soundex('mcnicoll'), 'M252')
        self.assertEquals(soundex('mcnicol'), 'M252')
        self.assertEquals(soundex('mcnie'), 'M250')
        self.assertEquals(soundex('mcphail'), 'M214')
        self.assertEquals(soundex('mcphee'), 'M210')
        self.assertEquals(soundex('mcpherson'), 'M216')
        self.assertEquals(soundex('mcsweeney'), 'M250')
        self.assertEquals(soundex('mcsweeny'), 'M250')
        self.assertEquals(soundex('mctague'), 'M232')
        self.assertEquals(soundex('mctigue'), 'M232')
        self.assertEquals(soundex('mcvicar'), 'M212')
        self.assertEquals(soundex('mcvickar'), 'M212')
        self.assertEquals(soundex('mcvie'), 'M210')
        self.assertEquals(soundex('meade'), 'M300')
        self.assertEquals(soundex('mead'), 'M300')
        self.assertEquals(soundex('meder'), 'M360')
        self.assertEquals(soundex('meekin'), 'M250')
        self.assertEquals(soundex('meighan'), 'M250')
        self.assertEquals(soundex('melladew'), 'M430')
        self.assertEquals(soundex('merchant'), 'M625')
        self.assertEquals(soundex('metcalfe'), 'M324')
        self.assertEquals(soundex('metcalf'), 'M324')
        self.assertEquals(soundex('millar'), 'M460')
        self.assertEquals(soundex('millea'), 'M400')
        self.assertEquals(soundex('miller'), 'M460')
        self.assertEquals(soundex('millie'), 'M400')
        self.assertEquals(soundex('moffat'), 'M130')
        self.assertEquals(soundex('moffitt'), 'M130')
        self.assertEquals(soundex('moirison'), 'M625')
        self.assertEquals(soundex('mokenzie'), 'M252')
        self.assertEquals(soundex('moloney'), 'M450')
        self.assertEquals(soundex('molonoy'), 'M450')
        self.assertEquals(soundex('monaghan'), 'M525')
        self.assertEquals(soundex('monagon'), 'M525')
        self.assertEquals(soundex('moodie'), 'M300')
        self.assertEquals(soundex('moody'), 'M300')
        self.assertEquals(soundex('morell'), 'M640')
        self.assertEquals(soundex('morice'), 'M620')
        self.assertEquals(soundex('morrell'), 'M640')
        self.assertEquals(soundex('morrisey'), 'M620')
        self.assertEquals(soundex('morris'), 'M620')
        self.assertEquals(soundex('morrison'), 'M625')
        self.assertEquals(soundex('morrissey'), 'M620')
        self.assertEquals(soundex('muiorhead'), 'M630')
        self.assertEquals(soundex('muirhead'), 'M630')
        self.assertEquals(soundex('mulch'), 'M420')
        self.assertEquals(soundex('mulholland'), 'M445')
        self.assertEquals(soundex('mullay'), 'M400')
        self.assertEquals(soundex('mullholland'), 'M445')
        self.assertEquals(soundex('mulloy'), 'M400')
        self.assertEquals(soundex('mulqueen'), 'M425')
        self.assertEquals(soundex('mulquin'), 'M425')
        self.assertEquals(soundex('murdoch'), 'M632')
        self.assertEquals(soundex('murdock'), 'M632')
        self.assertEquals(soundex('mutch'), 'M320')
        self.assertEquals(soundex('naughton'), 'N235')
        self.assertEquals(soundex('naumann'), 'N550')
        self.assertEquals(soundex('neason'), 'N250')
        self.assertEquals(soundex('nelsion'), 'N425')
        self.assertEquals(soundex('nelson'), 'N425')
        self.assertEquals(soundex('nesbitt'), 'N213')
        self.assertEquals(soundex('neumann'), 'N550')
        self.assertEquals(soundex('newall'), 'N400')
        self.assertEquals(soundex('newell'), 'N400')
        self.assertEquals(soundex('newlands'), 'N453')
        self.assertEquals(soundex('neylan'), 'N450')
        self.assertEquals(soundex('neylon'), 'N450')
        self.assertEquals(soundex('nichol'), 'N240')
        self.assertEquals(soundex('nicoll'), 'N240')
        self.assertEquals(soundex('nicol'), 'N240')
        self.assertEquals(soundex('nisbet'), 'N213')
        self.assertEquals(soundex('norton'), 'N635')
        self.assertEquals(soundex('nowlands'), 'N453')
        self.assertEquals(soundex('o\'brian'), 'O165')
        self.assertEquals(soundex('o\'brien'), 'O165')
        self.assertEquals(soundex('ockwell'), 'O240')
        self.assertEquals(soundex('o\'connell'), 'O254')
        self.assertEquals(soundex('o\'connor'), 'O256')
        self.assertEquals(soundex('ocwell'), 'O240')
        self.assertEquals(soundex('odham'), 'O350')
        self.assertEquals(soundex('ogilvie'), 'O241')
        self.assertEquals(soundex('ogivie'), 'O210')
        self.assertEquals(soundex('o\'keefe'), 'O210')
        self.assertEquals(soundex('o\'keeffe'), 'O210')
        self.assertEquals(soundex('oldham'), 'O435')
        self.assertEquals(soundex('olsen'), 'O425')
        self.assertEquals(soundex('olsien'), 'O425')
        self.assertEquals(soundex('osmand'), 'O255')
        self.assertEquals(soundex('osmond'), 'O255')
        self.assertEquals(soundex('page'), 'P200')
        self.assertEquals(soundex('paine'), 'P500')
        self.assertEquals(soundex('pascoe'), 'P200')
        self.assertEquals(soundex('pasco'), 'P200')
        self.assertEquals(soundex('paterson'), 'P362')
        self.assertEquals(soundex('patrick'), 'P362')
        self.assertEquals(soundex('patterson'), 'P362')
        self.assertEquals(soundex('pattison'), 'P325')
        self.assertEquals(soundex('pattrick'), 'P362')
        self.assertEquals(soundex('payne'), 'P500')
        self.assertEquals(soundex('peace'), 'P200')
        self.assertEquals(soundex('pearce'), 'P620')
        self.assertEquals(soundex('peebles'), 'P142')
        self.assertEquals(soundex('pegg'), 'P200')
        self.assertEquals(soundex('peoples'), 'P142')
        self.assertEquals(soundex('pepperell'), 'P164')
        self.assertEquals(soundex('pepperill'), 'P164')
        self.assertEquals(soundex('perry'), 'P600')
        self.assertEquals(soundex('petersen'), 'P362')
        self.assertEquals(soundex('peterson'), 'P362')
        self.assertEquals(soundex('phimester'), 'P523')
        self.assertEquals(soundex('phimister'), 'P523')
        self.assertEquals(soundex('picket'), 'P230')
        self.assertEquals(soundex('pickett'), 'P230')
        self.assertEquals(soundex('pickles'), 'P242')
        self.assertEquals(soundex('picklis'), 'P242')
        self.assertEquals(soundex('pollock'), 'P420')
        self.assertEquals(soundex('polloek'), 'P420')
        self.assertEquals(soundex('polwarth'), 'P463')
        self.assertEquals(soundex('polworth'), 'P463')
        self.assertEquals(soundex('popperell'), 'P164')
        self.assertEquals(soundex('powell'), 'P400')
        self.assertEquals(soundex('power'), 'P600')
        self.assertEquals(soundex('preston'), 'P623')
        self.assertEquals(soundex('priston'), 'P623')
        self.assertEquals(soundex('procter'), 'P623')
        self.assertEquals(soundex('proctor'), 'P623')
        self.assertEquals(soundex('pullar'), 'P460')
        self.assertEquals(soundex('puller'), 'P460')
        self.assertEquals(soundex('purches'), 'P622')
        self.assertEquals(soundex('rae'), 'R000')
        self.assertEquals(soundex('ramsay'), 'R520')
        self.assertEquals(soundex('ramsey'), 'R520')
        self.assertEquals(soundex('ray'), 'R000')
        self.assertEquals(soundex('redder'), 'R360')
        self.assertEquals(soundex('reed'), 'R300')
        self.assertEquals(soundex('reider'), 'R360')
        self.assertEquals(soundex('reidle'), 'R340')
        self.assertEquals(soundex('reid'), 'R300')
        self.assertEquals(soundex('rendel'), 'R534')
        self.assertEquals(soundex('render'), 'R536')
        self.assertEquals(soundex('renfree'), 'R516')
        self.assertEquals(soundex('renfrew'), 'R516')
        self.assertEquals(soundex('riddoch'), 'R320')
        self.assertEquals(soundex('riddock'), 'R320')
        self.assertEquals(soundex('riedle'), 'R340')
        self.assertEquals(soundex('riley'), 'R400')
        self.assertEquals(soundex('rilly'), 'R400')
        self.assertEquals(soundex('robertsan'), 'R163')
        self.assertEquals(soundex('robertson'), 'R163')
        self.assertEquals(soundex('rodgerson'), 'R326')
        self.assertEquals(soundex('rodgers'), 'R326')
        self.assertEquals(soundex('rogerson'), 'R262')
        self.assertEquals(soundex('rogers'), 'R262')
        self.assertEquals(soundex('rorley'), 'R640')
        self.assertEquals(soundex('rosenbrock'), 'R251')
        self.assertEquals(soundex('rosenbrook'), 'R251')
        self.assertEquals(soundex('rose'), 'R200')
        self.assertEquals(soundex('ross'), 'R200')
        self.assertEquals(soundex('routledge'), 'R343')
        self.assertEquals(soundex('routlege'), 'R342')
        self.assertEquals(soundex('rowley'), 'R400')
        self.assertEquals(soundex('russell'), 'R240')
        self.assertEquals(soundex('sanders'), 'S536')
        self.assertEquals(soundex('sandes'), 'S532')
        self.assertEquals(soundex('sandrey'), 'S536')
        self.assertEquals(soundex('sandry'), 'S536')
        self.assertEquals(soundex('saunders'), 'S536')
        self.assertEquals(soundex('saxton'), 'S235')
        self.assertEquals(soundex('scaife'), 'S100')
        self.assertEquals(soundex('scanlan'), 'S545')
        self.assertEquals(soundex('scanlon'), 'S545')
        self.assertEquals(soundex('scarfe'), 'S610')
        self.assertEquals(soundex('scoffeld'), 'S143')
        self.assertEquals(soundex('scofield'), 'S143')
        self.assertEquals(soundex('seamer'), 'S560')
        self.assertEquals(soundex('sellar'), 'S460')
        self.assertEquals(soundex('seller'), 'S460')
        self.assertEquals(soundex('sexton'), 'S235')
        self.assertEquals(soundex('seymour'), 'S560')
        self.assertEquals(soundex('sharpe'), 'S610')
        self.assertEquals(soundex('sharp'), 'S610')
        self.assertEquals(soundex('shaw'), 'S000')
        self.assertEquals(soundex('shea'), 'S000')
        self.assertEquals(soundex('shephard'), 'S163')
        self.assertEquals(soundex('shepherd'), 'S163')
        self.assertEquals(soundex('sheppard'), 'S163')
        self.assertEquals(soundex('shepperd'), 'S163')
        self.assertEquals(soundex('sheriff'), 'S610')
        self.assertEquals(soundex('sherriff'), 'S610')
        self.assertEquals(soundex('sidey'), 'S300')
        self.assertEquals(soundex('sidoy'), 'S300')
        self.assertEquals(soundex('silvertsen'), 'S416')
        self.assertEquals(soundex('sincock'), 'S522')
        self.assertEquals(soundex('sincok'), 'S522')
        self.assertEquals(soundex('sivertsen'), 'S163')
        self.assertEquals(soundex('skeene'), 'S500')
        self.assertEquals(soundex('skene'), 'S500')
        self.assertEquals(soundex('slowley'), 'S440')
        self.assertEquals(soundex('slowly'), 'S440')
        self.assertEquals(soundex('smith'), 'S530')
        self.assertEquals(soundex('smythe'), 'S530')
        self.assertEquals(soundex('smyth'), 'S530')
        self.assertEquals(soundex('spencer'), 'S152')
        self.assertEquals(soundex('spence'), 'S152')
        self.assertEquals(soundex('steadman'), 'S335')
        self.assertEquals(soundex('stedman'), 'S335')
        self.assertEquals(soundex('stenhouse'), 'S352')
        self.assertEquals(soundex('stennouse'), 'S352')
        self.assertEquals(soundex('stephenson'), 'S315')
        self.assertEquals(soundex('stevenson'), 'S315')
        self.assertEquals(soundex('stichmann'), 'S325')
        self.assertEquals(soundex('stickman'), 'S325')
        self.assertEquals(soundex('stock'), 'S320')
        self.assertEquals(soundex('stook'), 'S320')
        self.assertEquals(soundex('strang'), 'S365')
        self.assertEquals(soundex('strong'), 'S365')
        self.assertEquals(soundex('summerell'), 'S564')
        self.assertEquals(soundex('taverner'), 'T165')
        self.assertEquals(soundex('tillie'), 'T400')
        self.assertEquals(soundex('tiverner'), 'T165')
        self.assertEquals(soundex('todd'), 'T300')
        self.assertEquals(soundex('tonar'), 'T560')
        self.assertEquals(soundex('toner'), 'T560')
        self.assertEquals(soundex('tonner'), 'T560')
        self.assertEquals(soundex('tonnor'), 'T560')
        self.assertEquals(soundex('townsend'), 'T525')
        self.assertEquals(soundex('townshend'), 'T525')
        self.assertEquals(soundex('treeweek'), 'T620')
        self.assertEquals(soundex('tregoning'), 'T625')
        self.assertEquals(soundex('tregonning'), 'T625')
        self.assertEquals(soundex('trevena'), 'T615')
        self.assertEquals(soundex('trevenna'), 'T615')
        self.assertEquals(soundex('trewick'), 'T620')
        self.assertEquals(soundex('turley'), 'T640')
        self.assertEquals(soundex('vial'), 'V400')
        self.assertEquals(soundex('vintinner'), 'V535')
        self.assertEquals(soundex('vintinuer'), 'V535')
        self.assertEquals(soundex('wackeldine'), 'W243')
        self.assertEquals(soundex('wackildene'), 'W243')
        self.assertEquals(soundex('wackilden'), 'W243')
        self.assertEquals(soundex('waghornee'), 'W265')
        self.assertEquals(soundex('waghorne'), 'W265')
        self.assertEquals(soundex('wallace'), 'W420')
        self.assertEquals(soundex('wallin'), 'W450')
        self.assertEquals(soundex('walquest'), 'W422')
        self.assertEquals(soundex('walquist'), 'W422')
        self.assertEquals(soundex('walsh'), 'W420')
        self.assertEquals(soundex('warreil'), 'W640')
        self.assertEquals(soundex('warrell'), 'W640')
        self.assertEquals(soundex('watsan'), 'W325')
        self.assertEquals(soundex('watson'), 'W325')
        self.assertEquals(soundex('welbourn'), 'W416')
        self.assertEquals(soundex('weldon'), 'W435')
        self.assertEquals(soundex('wellbourn'), 'W416')
        self.assertEquals(soundex('wells'), 'W420')
        self.assertEquals(soundex('welsh'), 'W420')
        self.assertEquals(soundex('wheelan'), 'W450')
        self.assertEquals(soundex('wheeler'), 'W460')
        self.assertEquals(soundex('whelan'), 'W450')
        self.assertEquals(soundex('white'), 'W300')
        self.assertEquals(soundex('whyte'), 'W300')
        self.assertEquals(soundex('wilden'), 'W435')
        self.assertEquals(soundex('wildey'), 'W430')
        self.assertEquals(soundex('wildoy'), 'W430')
        self.assertEquals(soundex('willis'), 'W420')
        self.assertEquals(soundex('willon'), 'W450')
        self.assertEquals(soundex('willson'), 'W425')
        self.assertEquals(soundex('wills'), 'W420')
        self.assertEquals(soundex('wilson'), 'W425')
        self.assertEquals(soundex('wilton'), 'W435')
        self.assertEquals(soundex('winders'), 'W536')
        self.assertEquals(soundex('windus'), 'W532')
        self.assertEquals(soundex('wine'), 'W500')
        self.assertEquals(soundex('winn'), 'W500')
        self.assertEquals(soundex('wooton'), 'W350')
        self.assertEquals(soundex('wootten'), 'W350')
        self.assertEquals(soundex('wootton'), 'W350')
        self.assertEquals(soundex('wraight'), 'W623')
        self.assertEquals(soundex('wright'), 'W623')

    def test_soundex_special(self):
        self.assertEquals(soundex('Ashcroft', var='special'), 'A226')
        self.assertEquals(soundex('Asicroft', var='special'), 'A226')
        self.assertEquals(soundex('AsWcroft', var='special'), 'A226')
        self.assertEquals(soundex('Rupert', var='special'), 'R163')
        self.assertEquals(soundex('Rubin', var='special'), 'R150')

    def test_dm_soundex(self):
        # D-M tests
        self.assertEquals(soundex('', var='dm'), set(['000000']))
        self.assertEquals(dm_soundex(''), set(['000000']))

        # http://www.avotaynu.com/soundex.htm
        self.assertEquals(soundex('Augsburg', var='dm'), set(['054795']))
        self.assertEquals(dm_soundex('Augsburg'), set(['054795']))
        self.assertEquals(soundex('Breuer', var='dm'), set(['791900']))
        self.assertEquals(dm_soundex('Breuer'), set(['791900']))
        self.assertEquals(soundex('Halberstadt', var='dm'),
                          set(['587943', '587433']))
        self.assertEquals(dm_soundex('Halberstadt'), set(['587943', '587433']))
        self.assertEquals(soundex('Mannheim', var='dm'), set(['665600']))
        self.assertEquals(dm_soundex('Mannheim'), set(['665600']))
        self.assertEquals(soundex('Chernowitz', var='dm'),
                          set(['496740', '596740']))
        self.assertEquals(dm_soundex('Chernowitz'), set(['496740', '596740']))
        self.assertEquals(soundex('Cherkassy', var='dm'),
                          set(['495400', '595400']))
        self.assertEquals(dm_soundex('Cherkassy'), set(['495400', '595400']))
        self.assertEquals(soundex('Kleinman', var='dm'), set(['586660']))
        self.assertEquals(dm_soundex('Kleinman'), set(['586660']))
        self.assertEquals(soundex('Berlin', var='dm'), set(['798600']))
        self.assertEquals(dm_soundex('Berlin'), set(['798600']))

        self.assertEquals(soundex('Ceniow', var='dm'),
                          set(['467000', '567000']))
        self.assertEquals(dm_soundex('Ceniow'), set(['467000', '567000']))
        self.assertEquals(soundex('Tsenyuv', var='dm'), set(['467000']))
        self.assertEquals(dm_soundex('Tsenyuv'), set(['467000']))
        self.assertEquals(soundex('Holubica', var='dm'),
                          set(['587400', '587500']))
        self.assertEquals(dm_soundex('Holubica'), set(['587400', '587500']))
        self.assertEquals(soundex('Golubitsa', var='dm'), set(['587400']))
        self.assertEquals(dm_soundex('Golubitsa'), set(['587400']))
        self.assertEquals(soundex('Przemysl', var='dm'),
                          set(['746480', '794648']))
        self.assertEquals(dm_soundex('Przemysl'), set(['746480', '794648']))
        self.assertEquals(soundex('Pshemeshil', var='dm'), set(['746480']))
        self.assertEquals(dm_soundex('Pshemeshil'), set(['746480']))
        self.assertEquals(soundex('Rosochowaciec', var='dm'),
                          set(['944744', '945744', '944755', '944754', '944745',
                               '945745', '945754', '945755']))
        self.assertEquals(dm_soundex('Rosochowaciec'),
                          set(['944744', '945744', '944755', '944754', '944745',
                               '945745', '945754', '945755']))
        self.assertEquals(soundex('Rosokhovatsets', var='dm'), set(['945744']))
        self.assertEquals(dm_soundex('Rosokhovatsets'), set(['945744']))

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEquals(soundex('Peters', var='dm'),
                          set(['739400', '734000']))
        self.assertEquals(dm_soundex('Peters'), set(['739400', '734000']))
        self.assertEquals(soundex('Peterson', var='dm'),
                          set(['739460', '734600']))
        self.assertEquals(dm_soundex('Peterson'), set(['739460', '734600']))
        self.assertEquals(soundex('Moskowitz', var='dm'), set(['645740']))
        self.assertEquals(dm_soundex('Moskowitz'), set(['645740']))
        self.assertEquals(soundex('Moskovitz', var='dm'), set(['645740']))
        self.assertEquals(dm_soundex('Moskovitz'), set(['645740']))
        self.assertEquals(soundex('Auerbach', var='dm'),
                          set(['097500', '097400']))
        self.assertEquals(dm_soundex('Auerbach'), set(['097500', '097400']))
        self.assertEquals(soundex('Uhrbach', var='dm'),
                          set(['097500', '097400']))
        self.assertEquals(dm_soundex('Uhrbach'), set(['097500', '097400']))
        self.assertEquals(soundex('Jackson', var='dm'),
                          set(['154600', '454600', '145460', '445460']))
        self.assertEquals(dm_soundex('Jackson'),
                          set(['154600', '454600', '145460', '445460']))
        self.assertEquals(soundex('Jackson-Jackson', var='dm'),
                          set(['154654', '454654', '145465', '445465', '154645',
                               '454645', '145464', '445464', '154644',
                               '454644']))
        self.assertEquals(dm_soundex('Jackson-Jackson'),
                          set(['154654', '454654', '145465', '445465', '154645',
                               '454645', '145464', '445464', '154644',
                               '454644']))

        # http://www.jewishgen.org/infofiles/soundex.html
        self.assertEquals(soundex('OHRBACH', var='dm'),
                          set(['097500', '097400']))
        self.assertEquals(dm_soundex('OHRBACH'), set(['097500', '097400']))
        self.assertEquals(soundex('LIPSHITZ', var='dm'), set(['874400']))
        self.assertEquals(dm_soundex('LIPSHITZ'), set(['874400']))
        self.assertEquals(soundex('LIPPSZYC', var='dm'),
                          set(['874400', '874500']))
        self.assertEquals(dm_soundex('LIPPSZYC'), set(['874400', '874500']))
        self.assertEquals(soundex('LEWINSKY', var='dm'), set(['876450']))
        self.assertEquals(dm_soundex('LEWINSKY'), set(['876450']))
        self.assertEquals(soundex('LEVINSKI', var='dm'), set(['876450']))
        self.assertEquals(dm_soundex('LEVINSKI'), set(['876450']))
        self.assertEquals(soundex('SZLAMAWICZ', var='dm'), set(['486740']))
        self.assertEquals(dm_soundex('SZLAMAWICZ'), set(['486740']))
        self.assertEquals(soundex('SHLAMOVITZ', var='dm'), set(['486740']))
        self.assertEquals(dm_soundex('SHLAMOVITZ'), set(['486740']))

        # http://community.actian.com/wiki/OME_soundex_dm()
        self.assertEquals(soundex('Schwarzenegger', var='dm'),
                          set(['479465', '474659']))
        self.assertEquals(dm_soundex('Schwarzenegger'),
                          set(['479465', '474659']))
        self.assertEquals(soundex('Shwarzenegger', var='dm'),
                          set(['479465', '474659']))
        self.assertEquals(dm_soundex('Shwarzenegger'),
                          set(['479465', '474659']))
        self.assertEquals(soundex('Schwartsenegger', var='dm'),
                          set(['479465']))
        self.assertEquals(dm_soundex('Schwartsenegger'), set(['479465']))


class koelner_phonetik_test_cases(unittest.TestCase):
    def test_koelner_phonetik(self):
        self.assertEquals(koelner_phonetik(''), '')

        # https://de.wikipedia.org/wiki/K%C3%B6lner_Phonetik
        self.assertEquals(koelner_phonetik('Müller-Lüdenscheidt'), '65752682')
        self.assertEquals(koelner_phonetik('Wikipedia'), '3412')
        self.assertEquals(koelner_phonetik('Breschnew'), '17863')

        # http://search.cpan.org/~maros/Text-Phonetic/lib/Text/Phonetic/Koeln.pm
        self.assertEquals(koelner_phonetik('Müller'), '657')
        self.assertEquals(koelner_phonetik('schmidt'), '862')
        self.assertEquals(koelner_phonetik('schneider'), '8627')
        self.assertEquals(koelner_phonetik('fischer'), '387')
        self.assertEquals(koelner_phonetik('weber'), '317')
        self.assertEquals(koelner_phonetik('meyer'), '67')
        self.assertEquals(koelner_phonetik('wagner'), '3467')
        self.assertEquals(koelner_phonetik('schulz'), '858')
        self.assertEquals(koelner_phonetik('becker'), '147')
        self.assertEquals(koelner_phonetik('hoffmann'), '0366')
        self.assertEquals(koelner_phonetik('schäfer'), '837')
        self.assertEquals(koelner_phonetik('cater'), '427')
        self.assertEquals(koelner_phonetik('axel'), '0485')

    def test_koelner_phonetic_num_to_alpha(self):
        self.assertEquals(koelner_phonetik_num_to_alpha('0123456789'),
                          'APTFKLNRS')

    def test_koelner_phonetik_alpha(self):
        self.assertEquals(koelner_phonetik_alpha('Müller-Lüdenscheidt'),
                          'NLRLTNST')
        self.assertEquals(koelner_phonetik_alpha('Wikipedia'), 'FKPT')
        self.assertEquals(koelner_phonetik_alpha('Breschnew'), 'PRSNF')
        self.assertEquals(koelner_phonetik_alpha('Müller'), 'NLR')
        self.assertEquals(koelner_phonetik_alpha('schmidt'), 'SNT')
        self.assertEquals(koelner_phonetik_alpha('schneider'), 'SNTR')
        self.assertEquals(koelner_phonetik_alpha('fischer'), 'FSR')
        self.assertEquals(koelner_phonetik_alpha('weber'), 'FPR')
        self.assertEquals(koelner_phonetik_alpha('meyer'), 'NR')
        self.assertEquals(koelner_phonetik_alpha('wagner'), 'FKNR')
        self.assertEquals(koelner_phonetik_alpha('schulz'), 'SLS')
        self.assertEquals(koelner_phonetik_alpha('becker'), 'PKR')
        self.assertEquals(koelner_phonetik_alpha('hoffmann'), 'AFNN')
        self.assertEquals(koelner_phonetik_alpha('schäfer'), 'SFR')
        self.assertEquals(koelner_phonetik_alpha('cater'), 'KTR')
        self.assertEquals(koelner_phonetik_alpha('axel'), 'AKSL')


class nysiis_test_cases(unittest.TestCase):
    def test_nysiis(self):
        # http://coryodaniel.com/index.php/2009/12/30/ruby-nysiis-implementation/
        self.assertEquals(nysiis('O\'Daniel'), 'ODANAL')
        self.assertEquals(nysiis('O\'Donnel'), 'ODANAL')
        self.assertEquals(nysiis('Cory'), 'CARY')
        self.assertEquals(nysiis('Corey'), 'CARY')
        self.assertEquals(nysiis('Kory'), 'CARY')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEquals(nysiis('Diggell'), 'DAGAL')
        self.assertEquals(nysiis('Dougal'), 'DAGAL')
        self.assertEquals(nysiis('Doughill'), 'DAGAL')
        self.assertEquals(nysiis('Dougill'), 'DAGAL')
        self.assertEquals(nysiis('Dowgill'), 'DAGAL')
        self.assertEquals(nysiis('Dugall'), 'DAGAL')
        self.assertEquals(nysiis('Dugall'), 'DAGAL')
        self.assertEquals(nysiis('Glinde'), 'GLAND')
        self.assertEquals(nysiis('Plumridge', maxlength=20), 'PLANRADG')
        self.assertEquals(nysiis('Chinnick'), 'CANAC')
        self.assertEquals(nysiis('Chinnock'), 'CANAC')
        self.assertEquals(nysiis('Chinnock'), 'CANAC')
        self.assertEquals(nysiis('Chomicki'), 'CANAC')
        self.assertEquals(nysiis('Chomicz'), 'CANAC')
        self.assertEquals(nysiis('Schimek'), 'SANAC')
        self.assertEquals(nysiis('Shimuk'), 'SANAC')
        self.assertEquals(nysiis('Simak'), 'SANAC')
        self.assertEquals(nysiis('Simek'), 'SANAC')
        self.assertEquals(nysiis('Simic'), 'SANAC')
        self.assertEquals(nysiis('Sinnock'), 'SANAC')
        self.assertEquals(nysiis('Sinnocke'), 'SANAC')
        self.assertEquals(nysiis('Sunnex'), 'SANAX')
        self.assertEquals(nysiis('Sunnucks'), 'SANAC')
        self.assertEquals(nysiis('Sunock'), 'SANAC')
        self.assertEquals(nysiis('Webberley', maxlength=20), 'WABARLY')
        self.assertEquals(nysiis('Wibberley', maxlength=20), 'WABARLY')


class mra_test_cases(unittest.TestCase):
    def test_mra(self):
        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEquals(mra('Byrne'), 'BYRN')
        self.assertEquals(mra('Boern'), 'BRN')
        self.assertEquals(mra('Smith'), 'SMTH')
        self.assertEquals(mra('Smyth'), 'SMYTH')
        self.assertEquals(mra('Catherine'), 'CTHRN')
        self.assertEquals(mra('Kathryn'), 'KTHRYN')


class metaphone_test_cases(unittest.TestCase):
    def test_metaphone(self):
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEquals(metaphone('Fishpool', 4), 'FXPL')
        self.assertEquals(metaphone('Fishpoole', 4), 'FXPL')
        self.assertEquals(metaphone('Gellately', 4), 'JLTL')
        self.assertEquals(metaphone('Gelletly', 4), 'JLTL')
        self.assertEquals(metaphone('Lowers', 4), 'LWRS')
        self.assertEquals(metaphone('Lowerson', 4), 'LWRS')
        self.assertEquals(metaphone('Mallabar', 4), 'MLBR')
        self.assertEquals(metaphone('Melbert', 4), 'MLBR')
        self.assertEquals(metaphone('Melbourn', 4), 'MLBR')
        self.assertEquals(metaphone('Melbourne', 4), 'MLBR')
        self.assertEquals(metaphone('Melburg', 4), 'MLBR')
        self.assertEquals(metaphone('Melbury', 4), 'MLBR')
        self.assertEquals(metaphone('Milberry', 4), 'MLBR')
        self.assertEquals(metaphone('Milborn', 4), 'MLBR')
        self.assertEquals(metaphone('Milbourn', 4), 'MLBR')
        self.assertEquals(metaphone('Milbourne', 4), 'MLBR')
        self.assertEquals(metaphone('Milburn', 4), 'MLBR')
        self.assertEquals(metaphone('Milburne', 4), 'MLBR')
        self.assertEquals(metaphone('Millberg', 4), 'MLBR')
        self.assertEquals(metaphone('Mulberry', 4), 'MLBR')
        self.assertEquals(metaphone('Mulbery', 4), 'MLBR')
        self.assertEquals(metaphone('Mulbry', 4), 'MLBR')
        self.assertEquals(metaphone('Saipy', 4), 'SP')
        self.assertEquals(metaphone('Sapey', 4), 'SP')
        self.assertEquals(metaphone('Sapp', 4), 'SP')
        self.assertEquals(metaphone('Sappy', 4), 'SP')
        self.assertEquals(metaphone('Sepey', 4), 'SP')
        self.assertEquals(metaphone('Seppey', 4), 'SP')
        self.assertEquals(metaphone('Sopp', 4), 'SP')
        self.assertEquals(metaphone('Zoppie', 4), 'SP')
        self.assertEquals(metaphone('Zoppo', 4), 'SP')
        self.assertEquals(metaphone('Zupa', 4), 'SP')
        self.assertEquals(metaphone('Zupo', 4), 'SP')
        self.assertEquals(metaphone('Zuppa', 4), 'SP')

    def test_metaphone_caversham_testset(self):
        # caversham.otago.ac.nz/files/variantNames.csv
        self.assertEquals(metaphone('abernathy'), 'ABRN0')
        self.assertEquals(metaphone('abernethie'), 'ABRN0')
        self.assertEquals(metaphone('abernethy'), 'ABRN0')
        self.assertEquals(metaphone('ailen'), 'ALN')
        self.assertEquals(metaphone('aldridge'), 'ALTRJ')
        self.assertEquals(metaphone('allan'), 'ALN')
        self.assertEquals(metaphone('allen'), 'ALN')
        self.assertEquals(metaphone('andersen'), 'ANTRSN')
        self.assertEquals(metaphone('anderson'), 'ANTRSN')
        self.assertEquals(metaphone('andorson'), 'ANTRSN')
        self.assertEquals(metaphone('applegart'), 'APLKRT')
        self.assertEquals(metaphone('applegarth'), 'APLKR0')
        self.assertEquals(metaphone('arnal'), 'ARNL')
        self.assertEquals(metaphone('arnel'), 'ARNL')
        self.assertEquals(metaphone('bail'), 'BL')
        self.assertEquals(metaphone('bailer'), 'BLR')
        self.assertEquals(metaphone('bailey'), 'BL')
        self.assertEquals(metaphone('bain'), 'BN')
        self.assertEquals(metaphone('baley'), 'BL')
        self.assertEquals(metaphone('ball'), 'BL')
        self.assertEquals(metaphone('barclay'), 'BRKL')
        self.assertEquals(metaphone('barkla'), 'BRKL')
        self.assertEquals(metaphone('barlthrop'), 'BRL0RP')
        self.assertEquals(metaphone('barltrop'), 'BRLTRP')
        self.assertEquals(metaphone('barnett'), 'BRNT')
        self.assertEquals(metaphone('barratt'), 'BRT')
        self.assertEquals(metaphone('barrett'), 'BRT')
        self.assertEquals(metaphone('barrie'), 'BR')
        self.assertEquals(metaphone('barwick'), 'BRWK')
        self.assertEquals(metaphone('baylee'), 'BL')
        self.assertEquals(metaphone('bell'), 'BL')
        self.assertEquals(metaphone('bellet'), 'BLT')
        self.assertEquals(metaphone('bellett'), 'BLT')
        self.assertEquals(metaphone('bennet'), 'BNT')
        self.assertEquals(metaphone('bennett'), 'BNT')
        self.assertEquals(metaphone('bennie'), 'BN')
        self.assertEquals(metaphone('bernie'), 'BRN')
        self.assertEquals(metaphone('berry'), 'BR')
        self.assertEquals(metaphone('berwick'), 'BRWK')
        self.assertEquals(metaphone('beven'), 'BFN')
        self.assertEquals(metaphone('bevin'), 'BFN')
        self.assertEquals(metaphone('binnie'), 'BN')
        self.assertEquals(metaphone('birrell'), 'BRL')
        self.assertEquals(metaphone('black'), 'BLK')
        self.assertEquals(metaphone('blake'), 'BLK')
        self.assertEquals(metaphone('blakeley'), 'BLKL')
        self.assertEquals(metaphone('blakely'), 'BLKL')
        self.assertEquals(metaphone('bouchor'), 'BXR')
        self.assertEquals(metaphone('boutcher'), 'BXR')
        self.assertEquals(metaphone('brand'), 'BRNT')
        self.assertEquals(metaphone('brandt'), 'BRNTT')
        self.assertEquals(metaphone('brock'), 'BRK')
        self.assertEquals(metaphone('brockie'), 'BRK')
        self.assertEquals(metaphone('brook'), 'BRK')
        self.assertEquals(metaphone('brooke'), 'BRK')
        self.assertEquals(metaphone('brown'), 'BRN')
        self.assertEquals(metaphone('browne'), 'BRN')
        self.assertEquals(metaphone('bruten'), 'BRTN')
        self.assertEquals(metaphone('bruton'), 'BRTN')
        self.assertEquals(metaphone('bulger'), 'BLJR')
        self.assertEquals(metaphone('bull'), 'BL')
        self.assertEquals(metaphone('burger'), 'BRJR')
        self.assertEquals(metaphone('burgess'), 'BRJS')
        self.assertEquals(metaphone('burnett'), 'BRNT')
        self.assertEquals(metaphone('buttermore'), 'BTRMR')
        self.assertEquals(metaphone('buttimore'), 'BTMR')
        self.assertEquals(metaphone('calder'), 'KLTR')
        self.assertEquals(metaphone('caley'), 'KL')
        self.assertEquals(metaphone('callaghan'), 'KLN')
        self.assertEquals(metaphone('callander'), 'KLNTR')
        self.assertEquals(metaphone('callender'), 'KLNTR')
        self.assertEquals(metaphone('callighan'), 'KLN')
        self.assertEquals(metaphone('carder'), 'KRTR')
        self.assertEquals(metaphone('carley'), 'KRL')
        self.assertEquals(metaphone('carruthers'), 'KR0RS')
        self.assertEquals(metaphone('carside'), 'KRST')
        self.assertEquals(metaphone('caruthers'), 'KR0RS')
        self.assertEquals(metaphone('case'), 'KS')
        self.assertEquals(metaphone('casey'), 'KS')
        self.assertEquals(metaphone('cassells'), 'KSLS')
        self.assertEquals(metaphone('cassels'), 'KSLS')
        self.assertEquals(metaphone('cassidy'), 'KST')
        self.assertEquals(metaphone('chaplain'), 'XPLN')
        self.assertEquals(metaphone('chaplin'), 'XPLN')
        self.assertEquals(metaphone('chrisp'), 'KRSP')
        self.assertEquals(metaphone('chronican'), 'KRNKN')
        self.assertEquals(metaphone('chronichan'), 'KRNXN')
        self.assertEquals(metaphone('clarke'), 'KLRK')
        self.assertEquals(metaphone('clark'), 'KLRK')
        self.assertEquals(metaphone('clent'), 'KLNT')
        self.assertEquals(metaphone('clint'), 'KLNT')
        self.assertEquals(metaphone('coates'), 'KTS')
        self.assertEquals(metaphone('coats'), 'KTS')
        self.assertEquals(metaphone('conheady'), 'KNHT')
        self.assertEquals(metaphone('connell'), 'KNL')
        self.assertEquals(metaphone('connolly'), 'KNL')
        self.assertEquals(metaphone('conolly'), 'KNL')
        self.assertEquals(metaphone('cooke'), 'KK')
        self.assertEquals(metaphone('cook'), 'KK')
        self.assertEquals(metaphone('corcoran'), 'KRKRN')
        self.assertEquals(metaphone('corkran'), 'KRKRN')
        self.assertEquals(metaphone('cornell'), 'KRNL')
        self.assertEquals(metaphone('cosegrove'), 'KSKRF')
        self.assertEquals(metaphone('cosgrove'), 'KSKRF')
        self.assertEquals(metaphone('coulter'), 'KLTR')
        self.assertEquals(metaphone('coupar'), 'KPR')
        self.assertEquals(metaphone('couper'), 'KPR')
        self.assertEquals(metaphone('courter'), 'KRTR')
        self.assertEquals(metaphone('craig'), 'KRK')
        self.assertEquals(metaphone('craik'), 'KRK')
        self.assertEquals(metaphone('crammond'), 'KRMNT')
        self.assertEquals(metaphone('cramond'), 'KRMNT')
        self.assertEquals(metaphone('crawford'), 'KRFRT')
        self.assertEquals(metaphone('crawfurd'), 'KRFRT')
        self.assertEquals(metaphone('cress'), 'KRS')
        self.assertEquals(metaphone('crisp'), 'KRSP')
        self.assertEquals(metaphone('crosbie'), 'KRSB')
        self.assertEquals(metaphone('crosby'), 'KRSB')
        self.assertEquals(metaphone('crossan'), 'KRSN')
        self.assertEquals(metaphone('crossian'), 'KRSN')
        self.assertEquals(metaphone('cruse'), 'KRS')
        self.assertEquals(metaphone('cubbins'), 'KBNS')
        self.assertEquals(metaphone('culsey'), 'KLS')
        self.assertEquals(metaphone('cunhingham'), 'KNHNM')
        self.assertEquals(metaphone('cunningham'), 'KNNM')
        self.assertEquals(metaphone('curran'), 'KRN')
        self.assertEquals(metaphone('curren'), 'KRN')
        self.assertEquals(metaphone('cursey'), 'KRS')
        self.assertEquals(metaphone('daly'), 'TL')
        self.assertEquals(metaphone('davany'), 'TFN')
        self.assertEquals(metaphone('daveis'), 'TFS')
        self.assertEquals(metaphone('davies'), 'TFS')
        self.assertEquals(metaphone('davis'), 'TFS')
        self.assertEquals(metaphone('davys'), 'TFS')
        self.assertEquals(metaphone('delaney'), 'TLN')
        self.assertEquals(metaphone('delany'), 'TLN')
        self.assertEquals(metaphone('delargey'), 'TLRJ')
        self.assertEquals(metaphone('delargy'), 'TLRJ')
        self.assertEquals(metaphone('dely'), 'TL')
        self.assertEquals(metaphone('denfold'), 'TNFLT')
        self.assertEquals(metaphone('denford'), 'TNFRT')
        self.assertEquals(metaphone('devaney'), 'TFN')
        self.assertEquals(metaphone('dickison'), 'TKSN')
        self.assertEquals(metaphone('dickson'), 'TKSN')
        self.assertEquals(metaphone('dillan'), 'TLN')
        self.assertEquals(metaphone('dillon'), 'TLN')
        self.assertEquals(metaphone('dockworth'), 'TKWR0')
        self.assertEquals(metaphone('dodd'), 'TT')
        self.assertEquals(metaphone('donne'), 'TN')
        self.assertEquals(metaphone('dougall'), 'TKL')
        self.assertEquals(metaphone('dougal'), 'TKL')
        self.assertEquals(metaphone('douglass'), 'TKLS')
        self.assertEquals(metaphone('douglas'), 'TKLS')
        self.assertEquals(metaphone('dreaver'), 'TRFR')
        self.assertEquals(metaphone('dreavor'), 'TRFR')
        self.assertEquals(metaphone('droaver'), 'TRFR')
        self.assertEquals(metaphone('duckworth'), 'TKWR0')
        self.assertEquals(metaphone('dunne'), 'TN')
        self.assertEquals(metaphone('dunn'), 'TN')
        self.assertEquals(metaphone('eagan'), 'EKN')
        self.assertEquals(metaphone('eagar'), 'EKR')
        self.assertEquals(metaphone('eager'), 'EJR')
        self.assertEquals(metaphone('easson'), 'ESN')
        self.assertEquals(metaphone('egan'), 'EKN')
        self.assertEquals(metaphone('eldridge'), 'ELTRJ')
        self.assertEquals(metaphone('elliis'), 'ELS')
        self.assertEquals(metaphone('ellis'), 'ELS')
        self.assertEquals(metaphone('emerson'), 'EMRSN')
        self.assertEquals(metaphone('emmerson'), 'EMRSN')
        self.assertEquals(metaphone('essson'), 'ESN')
        self.assertEquals(metaphone('fahey'), 'FH')
        self.assertEquals(metaphone('fahy'), 'F')
        self.assertEquals(metaphone('fail'), 'FL')
        self.assertEquals(metaphone('fairbairn'), 'FRBRN')
        self.assertEquals(metaphone('fairburn'), 'FRBRN')
        self.assertEquals(metaphone('faithful'), 'F0FL')
        self.assertEquals(metaphone('faithfull'), 'F0FL')
        self.assertEquals(metaphone('fall'), 'FL')
        self.assertEquals(metaphone('farminger'), 'FRMNJR')
        self.assertEquals(metaphone('farry'), 'FR')
        self.assertEquals(metaphone('feil'), 'FL')
        self.assertEquals(metaphone('fell'), 'FL')
        self.assertEquals(metaphone('fennessey'), 'FNS')
        self.assertEquals(metaphone('fennessy'), 'FNS')
        self.assertEquals(metaphone('ferry'), 'FR')
        self.assertEquals(metaphone('fiddes'), 'FTS')
        self.assertEquals(metaphone('fiddis'), 'FTS')
        self.assertEquals(metaphone('fielden'), 'FLTN')
        self.assertEquals(metaphone('fielder'), 'FLTR')
        self.assertEquals(metaphone('findlay'), 'FNTL')
        self.assertEquals(metaphone('findley'), 'FNTL')
        self.assertEquals(metaphone('fitzpatric'), 'FTSPTRK')
        self.assertEquals(metaphone('fitzpatrick'), 'FTSPTRK')
        self.assertEquals(metaphone('fraer'), 'FRR')
        self.assertEquals(metaphone('fraher'), 'FRHR')
        self.assertEquals(metaphone('fullarton'), 'FLRTN')
        self.assertEquals(metaphone('fullerton'), 'FLRTN')
        self.assertEquals(metaphone('furminger'), 'FRMNJR')
        self.assertEquals(metaphone('gailichan'), 'KLXN')
        self.assertEquals(metaphone('galbraith'), 'KLBR0')
        self.assertEquals(metaphone('gallanders'), 'KLNTRS')
        self.assertEquals(metaphone('gallaway'), 'KLW')
        self.assertEquals(metaphone('gallbraith'), 'KLBR0')
        self.assertEquals(metaphone('gallichan'), 'KLXN')
        self.assertEquals(metaphone('galloway'), 'KLW')
        self.assertEquals(metaphone('garcho'), 'KRX')
        self.assertEquals(metaphone('garchow'), 'KRX')
        self.assertEquals(metaphone('garret'), 'KRT')
        self.assertEquals(metaphone('garrett'), 'KRT')
        self.assertEquals(metaphone('garside'), 'KRST')
        self.assertEquals(metaphone('geddes'), 'JTS')
        self.assertEquals(metaphone('geddis'), 'JTS')
        self.assertEquals(metaphone('georgeison'), 'JRJSN')
        self.assertEquals(metaphone('george'), 'JRJ')
        self.assertEquals(metaphone('georgeson'), 'JRJSN')
        self.assertEquals(metaphone('gillanders'), 'JLNTRS')
        self.assertEquals(metaphone('gillespie'), 'JLSP')
        self.assertEquals(metaphone('gillispie'), 'JLSP')
        self.assertEquals(metaphone('gilmore'), 'JLMR')
        self.assertEquals(metaphone('gilmour'), 'JLMR')
        self.assertEquals(metaphone('glendining'), 'KLNTNNK')
        self.assertEquals(metaphone('glendinning'), 'KLNTNNK')
        self.assertEquals(metaphone('glendinnin'), 'KLNTNN')
        self.assertEquals(metaphone('gorge'), 'KRJ')
        self.assertEquals(metaphone('graig'), 'KRK')
        self.assertEquals(metaphone('gray'), 'KR')
        self.assertEquals(metaphone('greeves'), 'KRFS')
        self.assertEquals(metaphone('greig'), 'KRK')
        self.assertEquals(metaphone('greves'), 'KRFS')
        self.assertEquals(metaphone('grey'), 'KR')
        self.assertEquals(metaphone('griffiths'), 'KRF0S')
        self.assertEquals(metaphone('griffths'), 'KRF0S')
        self.assertEquals(metaphone('grigg'), 'KRK')
        self.assertEquals(metaphone('grig'), 'KRK')
        self.assertEquals(metaphone('gubbins'), 'KBNS')
        self.assertEquals(metaphone('gulbins'), 'KLBNS')
        self.assertEquals(metaphone('haddon'), 'HTN')
        self.assertEquals(metaphone('hal'), 'HL')
        self.assertEquals(metaphone('hall'), 'HL')
        self.assertEquals(metaphone('hanley'), 'HNL')
        self.assertEquals(metaphone('hanly'), 'HNL')
        self.assertEquals(metaphone('hannagan'), 'HNKN')
        self.assertEquals(metaphone('hannan'), 'HNN')
        self.assertEquals(metaphone('hannigan'), 'HNKN')
        self.assertEquals(metaphone('hanon'), 'HNN')
        self.assertEquals(metaphone('harman'), 'HRMN')
        self.assertEquals(metaphone('hart'), 'HRT')
        self.assertEquals(metaphone('harty'), 'HRT')
        self.assertEquals(metaphone('hatton'), 'HTN')
        self.assertEquals(metaphone('hayden'), 'HTN')
        self.assertEquals(metaphone('hay'), 'H')
        self.assertEquals(metaphone('healey'), 'HL')
        self.assertEquals(metaphone('healy'), 'HL')
        self.assertEquals(metaphone('helleyer'), 'HLYR')
        self.assertEquals(metaphone('hellyer'), 'HLYR')
        self.assertEquals(metaphone('henaghan'), 'HNN')
        self.assertEquals(metaphone('heneghan'), 'HNN')
        self.assertEquals(metaphone('herman'), 'HRMN')
        self.assertEquals(metaphone('hey'), 'H')
        self.assertEquals(metaphone('hill'), 'HL')
        self.assertEquals(metaphone('hinde'), 'HNT')
        self.assertEquals(metaphone('hobcraft'), 'HBKRFT')
        self.assertEquals(metaphone('hobcroft'), 'HBKRFT')
        self.assertEquals(metaphone('hocking'), 'HKNK')
        self.assertEquals(metaphone('hoeking'), 'HKNK')
        self.assertEquals(metaphone('holander'), 'HLNTR')
        self.assertEquals(metaphone('holdgate'), 'HLTKT')
        self.assertEquals(metaphone('holgate'), 'HLKT')
        self.assertEquals(metaphone('hollander'), 'HLNTR')
        self.assertEquals(metaphone('home'), 'HM')
        self.assertEquals(metaphone('horne'), 'HRN')
        self.assertEquals(metaphone('horn'), 'HRN')
        self.assertEquals(metaphone('howarth'), 'HWR0')
        self.assertEquals(metaphone('howe'), 'HW')
        self.assertEquals(metaphone('howie'), 'HW')
        self.assertEquals(metaphone('howorth'), 'HWR0')
        self.assertEquals(metaphone('hoy'), 'H')
        self.assertEquals(metaphone('huddlestone'), 'HTLSTN')
        self.assertEquals(metaphone('huddleston'), 'HTLSTN')
        self.assertEquals(metaphone('hugget'), 'HKT')
        self.assertEquals(metaphone('huggett'), 'HKT')
        self.assertEquals(metaphone('hume'), 'HM')
        self.assertEquals(metaphone('hunt'), 'HNT')
        self.assertEquals(metaphone('hurt'), 'HRT')
        self.assertEquals(metaphone('hutcheson'), 'HXSN')
        self.assertEquals(metaphone('hutchison'), 'HXSN')
        self.assertEquals(metaphone('hutt'), 'HT')
        self.assertEquals(metaphone('hutton'), 'HTN')
        self.assertEquals(metaphone('jacobsen'), 'JKBSN')
        self.assertEquals(metaphone('jacobs'), 'JKBS')
        self.assertEquals(metaphone('jacobson'), 'JKBSN')
        self.assertEquals(metaphone('jaicobs'), 'JKBS')
        self.assertEquals(metaphone('jamieson'), 'JMSN')
        self.assertEquals(metaphone('jamison'), 'JMSN')
        self.assertEquals(metaphone('jansen'), 'JNSN')
        self.assertEquals(metaphone('janson'), 'JNSN')
        self.assertEquals(metaphone('jardine'), 'JRTN')
        self.assertEquals(metaphone('jeannings'), 'JNNKS')
        self.assertEquals(metaphone('jeffery'), 'JFR')
        self.assertEquals(metaphone('jeffrey'), 'JFR')
        self.assertEquals(metaphone('jelly'), 'JL')
        self.assertEquals(metaphone('jennings'), 'JNNKS')
        self.assertEquals(metaphone('johns'), 'JNS')
        self.assertEquals(metaphone('johnstone'), 'JNSTN')
        self.assertEquals(metaphone('johnston'), 'JNSTN')
        self.assertEquals(metaphone('jolly'), 'JL')
        self.assertEquals(metaphone('jones'), 'JNS')
        self.assertEquals(metaphone('jurdine'), 'JRTN')
        self.assertEquals(metaphone('kean'), 'KN')
        self.assertEquals(metaphone('keen'), 'KN')
        self.assertEquals(metaphone('keennelly'), 'KNL')
        self.assertEquals(metaphone('kellan'), 'KLN')
        self.assertEquals(metaphone('kennard'), 'KNRT')
        self.assertEquals(metaphone('kennealy'), 'KNL')
        self.assertEquals(metaphone('kennedy'), 'KNT')
        self.assertEquals(metaphone('kenn'), 'KN')
        self.assertEquals(metaphone('killin'), 'KLN')
        self.assertEquals(metaphone('kirkaldie'), 'KRKLT')
        self.assertEquals(metaphone('kirkcaldie'), 'KRKKLT')
        self.assertEquals(metaphone('kirke'), 'KRK')
        self.assertEquals(metaphone('kirk'), 'KRK')
        self.assertEquals(metaphone('kitchen'), 'KXN')
        self.assertEquals(metaphone('kitchin'), 'KXN')
        self.assertEquals(metaphone('krause'), 'KRS')
        self.assertEquals(metaphone('kraus'), 'KRS')
        self.assertEquals(metaphone('langham'), 'LNM')
        self.assertEquals(metaphone('lanham'), 'LNHM')
        self.assertEquals(metaphone('larson'), 'LRSN')
        self.assertEquals(metaphone('laughlin'), 'LKLN')
        self.assertEquals(metaphone('laurie'), 'LR')
        self.assertEquals(metaphone('lawrie'), 'LR')
        self.assertEquals(metaphone('lawson'), 'LSN')
        self.assertEquals(metaphone('leary'), 'LR')
        self.assertEquals(metaphone('leech'), 'LX')
        self.assertEquals(metaphone('leery'), 'LR')
        self.assertEquals(metaphone('leitch'), 'LX')
        self.assertEquals(metaphone('lemin'), 'LMN')
        self.assertEquals(metaphone('lemon'), 'LMN')
        self.assertEquals(metaphone('lenihan'), 'LNHN')
        self.assertEquals(metaphone('lennon'), 'LNN')
        self.assertEquals(metaphone('leyden'), 'LTN')
        self.assertEquals(metaphone('leydon'), 'LTN')
        self.assertEquals(metaphone('lister'), 'LSTR')
        self.assertEquals(metaphone('list'), 'LST')
        self.assertEquals(metaphone('livingstone'), 'LFNKSTN')
        self.assertEquals(metaphone('livingston'), 'LFNKSTN')
        self.assertEquals(metaphone('lochhead'), 'LXT')
        self.assertEquals(metaphone('lockhead'), 'LKHT')
        self.assertEquals(metaphone('loughlin'), 'LKLN')
        self.assertEquals(metaphone('macallum'), 'MKLM')
        self.assertEquals(metaphone('macaskill'), 'MKSKL')
        self.assertEquals(metaphone('macaulay'), 'MKL')
        self.assertEquals(metaphone('macauley'), 'MKL')
        self.assertEquals(metaphone('macbeath'), 'MKB0')
        self.assertEquals(metaphone('macdonald'), 'MKTNLT')
        self.assertEquals(metaphone('maceewan'), 'MSWN')
        self.assertEquals(metaphone('macewan'), 'MSWN')
        self.assertEquals(metaphone('macfarlane'), 'MKFRLN')
        self.assertEquals(metaphone('macintosh'), 'MSNTX')
        self.assertEquals(metaphone('mackechnie'), 'MKXN')
        self.assertEquals(metaphone('mackenzie'), 'MKNS')
        self.assertEquals(metaphone('mackersey'), 'MKRS')
        self.assertEquals(metaphone('mackersy'), 'MKRS')
        self.assertEquals(metaphone('maclean'), 'MKLN')
        self.assertEquals(metaphone('macnee'), 'MKN')
        self.assertEquals(metaphone('macpherson'), 'MKFRSN')
        self.assertEquals(metaphone('main'), 'MN')
        self.assertEquals(metaphone('maley'), 'ML')
        self.assertEquals(metaphone('malladew'), 'MLT')
        self.assertEquals(metaphone('maloney'), 'MLN')
        self.assertEquals(metaphone('mann'), 'MN')
        self.assertEquals(metaphone('marchant'), 'MRXNT')
        self.assertEquals(metaphone('marett'), 'MRT')
        self.assertEquals(metaphone('marrett'), 'MRT')
        self.assertEquals(metaphone('mason'), 'MSN')
        self.assertEquals(metaphone('matheson'), 'M0SN')
        self.assertEquals(metaphone('mathieson'), 'M0SN')
        self.assertEquals(metaphone('mattingle'), 'MTNKL')
        self.assertEquals(metaphone('mattingly'), 'MTNKL')
        self.assertEquals(metaphone('mawson'), 'MSN')
        self.assertEquals(metaphone('mcaulay'), 'MKL')
        self.assertEquals(metaphone('mcauley'), 'MKL')
        self.assertEquals(metaphone('mcauliffe'), 'MKLF')
        self.assertEquals(metaphone('mcauliff'), 'MKLF')
        self.assertEquals(metaphone('mcbeath'), 'MKB0')
        self.assertEquals(metaphone('mccallum'), 'MKLM')
        self.assertEquals(metaphone('mccarthy'), 'MKR0')
        self.assertEquals(metaphone('mccarty'), 'MKRT')
        self.assertEquals(metaphone('mccaskill'), 'MKSKL')
        self.assertEquals(metaphone('mccay'), 'MK')
        self.assertEquals(metaphone('mcclintock'), 'MKLNTK')
        self.assertEquals(metaphone('mccluskey'), 'MKLSK')
        self.assertEquals(metaphone('mcclusky'), 'MKLSK')
        self.assertEquals(metaphone('mccormack'), 'MKRMK')
        self.assertEquals(metaphone('mccormacl'), 'MKRMKL')
        self.assertEquals(metaphone('mccrorie'), 'MKRR')
        self.assertEquals(metaphone('mccrory'), 'MKRR')
        self.assertEquals(metaphone('mccrossan'), 'MKRSN')
        self.assertEquals(metaphone('mccrossin'), 'MKRSN')
        self.assertEquals(metaphone('mcdermott'), 'MKTRMT')
        self.assertEquals(metaphone('mcdiarmid'), 'MKTRMT')
        self.assertEquals(metaphone('mcdonald'), 'MKTNLT')
        self.assertEquals(metaphone('mcdonell'), 'MKTNL')
        self.assertEquals(metaphone('mcdonnell'), 'MKTNL')
        self.assertEquals(metaphone('mcdowall'), 'MKTWL')
        self.assertEquals(metaphone('mcdowell'), 'MKTWL')
        self.assertEquals(metaphone('mcewan'), 'MSWN')
        self.assertEquals(metaphone('mcewen'), 'MSWN')
        self.assertEquals(metaphone('mcfarlane'), 'MKFRLN')
        self.assertEquals(metaphone('mcfaull'), 'MKFL')
        self.assertEquals(metaphone('mcgill'), 'MKJL')
        self.assertEquals(metaphone('mciintyre'), 'MSNTR')
        self.assertEquals(metaphone('mcintosh'), 'MSNTX')
        self.assertEquals(metaphone('mcintyre'), 'MSNTR')
        self.assertEquals(metaphone('mciver'), 'MSFR')
        self.assertEquals(metaphone('mcivor'), 'MSFR')
        self.assertEquals(metaphone('mckay'), 'MK')
        self.assertEquals(metaphone('mckechnie'), 'MKXN')
        self.assertEquals(metaphone('mckecknie'), 'MKKN')
        self.assertEquals(metaphone('mckellar'), 'MKLR')
        self.assertEquals(metaphone('mckenzie'), 'MKNS')
        self.assertEquals(metaphone('mcketterick'), 'MKTRK')
        self.assertEquals(metaphone('mckey'), 'MK')
        self.assertEquals(metaphone('mckinlay'), 'MKNL')
        self.assertEquals(metaphone('mckinley'), 'MKNL')
        self.assertEquals(metaphone('mckitterick'), 'MKTRK')
        self.assertEquals(metaphone('mclachlan'), 'MKLXLN')
        self.assertEquals(metaphone('mclauchlan'), 'MKLXLN')
        self.assertEquals(metaphone('mclauchlin'), 'MKLXLN')
        self.assertEquals(metaphone('mclaughlan'), 'MKLKLN')
        self.assertEquals(metaphone('mclaughlin'), 'MKLKLN')
        self.assertEquals(metaphone('mclean'), 'MKLN')
        self.assertEquals(metaphone('mcledd'), 'MKLT')
        self.assertEquals(metaphone('mcledowne'), 'MKLTN')
        self.assertEquals(metaphone('mcledowney'), 'MKLTN')
        self.assertEquals(metaphone('mclellan'), 'MKLLN')
        self.assertEquals(metaphone('mcleod'), 'MKLT')
        self.assertEquals(metaphone('mclintock'), 'MKLNTK')
        self.assertEquals(metaphone('mcloud'), 'MKLT')
        self.assertEquals(metaphone('mcloughlin'), 'MKLKLN')
        self.assertEquals(metaphone('mcmillan'), 'MKMLN')
        self.assertEquals(metaphone('mcmullan'), 'MKMLN')
        self.assertEquals(metaphone('mcmullen'), 'MKMLN')
        self.assertEquals(metaphone('mcnair'), 'MKNR')
        self.assertEquals(metaphone('mcnalty'), 'MKNLT')
        self.assertEquals(metaphone('mcnatty'), 'MKNT')
        self.assertEquals(metaphone('mcnee'), 'MKN')
        self.assertEquals(metaphone('mcneill'), 'MKNL')
        self.assertEquals(metaphone('mcneil'), 'MKNL')
        self.assertEquals(metaphone('mcnicoll'), 'MKNKL')
        self.assertEquals(metaphone('mcnicol'), 'MKNKL')
        self.assertEquals(metaphone('mcnie'), 'MKN')
        self.assertEquals(metaphone('mcphail'), 'MKFL')
        self.assertEquals(metaphone('mcphee'), 'MKF')
        self.assertEquals(metaphone('mcpherson'), 'MKFRSN')
        self.assertEquals(metaphone('mcsweeney'), 'MKSWN')
        self.assertEquals(metaphone('mcsweeny'), 'MKSWN')
        self.assertEquals(metaphone('mctague'), 'MKTK')
        self.assertEquals(metaphone('mctigue'), 'MKTK')
        self.assertEquals(metaphone('mcvicar'), 'MKFKR')
        self.assertEquals(metaphone('mcvickar'), 'MKFKR')
        self.assertEquals(metaphone('mcvie'), 'MKF')
        self.assertEquals(metaphone('meade'), 'MT')
        self.assertEquals(metaphone('mead'), 'MT')
        self.assertEquals(metaphone('meder'), 'MTR')
        self.assertEquals(metaphone('meekin'), 'MKN')
        self.assertEquals(metaphone('meighan'), 'MN')
        self.assertEquals(metaphone('melladew'), 'MLT')
        self.assertEquals(metaphone('merchant'), 'MRXNT')
        self.assertEquals(metaphone('metcalfe'), 'MTKLF')
        self.assertEquals(metaphone('metcalf'), 'MTKLF')
        self.assertEquals(metaphone('millar'), 'MLR')
        self.assertEquals(metaphone('millea'), 'ML')
        self.assertEquals(metaphone('miller'), 'MLR')
        self.assertEquals(metaphone('millie'), 'ML')
        self.assertEquals(metaphone('moffat'), 'MFT')
        self.assertEquals(metaphone('moffitt'), 'MFT')
        self.assertEquals(metaphone('moirison'), 'MRSN')
        self.assertEquals(metaphone('mokenzie'), 'MKNS')
        self.assertEquals(metaphone('moloney'), 'MLN')
        self.assertEquals(metaphone('molonoy'), 'MLN')
        self.assertEquals(metaphone('monaghan'), 'MNN')
        self.assertEquals(metaphone('monagon'), 'MNKN')
        self.assertEquals(metaphone('moodie'), 'MT')
        self.assertEquals(metaphone('moody'), 'MT')
        self.assertEquals(metaphone('morell'), 'MRL')
        self.assertEquals(metaphone('morice'), 'MRS')
        self.assertEquals(metaphone('morrell'), 'MRL')
        self.assertEquals(metaphone('morrisey'), 'MRS')
        self.assertEquals(metaphone('morris'), 'MRS')
        self.assertEquals(metaphone('morrison'), 'MRSN')
        self.assertEquals(metaphone('morrissey'), 'MRS')
        self.assertEquals(metaphone('muiorhead'), 'MRHT')
        self.assertEquals(metaphone('muirhead'), 'MRHT')
        self.assertEquals(metaphone('mulch'), 'MLX')
        self.assertEquals(metaphone('mulholland'), 'MLHLNT')
        self.assertEquals(metaphone('mullay'), 'ML')
        self.assertEquals(metaphone('mullholland'), 'MLHLNT')
        self.assertEquals(metaphone('mulloy'), 'ML')
        self.assertEquals(metaphone('mulqueen'), 'MLKN')
        self.assertEquals(metaphone('mulquin'), 'MLKN')
        self.assertEquals(metaphone('murdoch'), 'MRTX')
        self.assertEquals(metaphone('murdock'), 'MRTK')
        self.assertEquals(metaphone('mutch'), 'MX')
        self.assertEquals(metaphone('naughton'), 'NKTN')
        self.assertEquals(metaphone('naumann'), 'NMN')
        self.assertEquals(metaphone('neason'), 'NSN')
        self.assertEquals(metaphone('nelsion'), 'NLXN')
        self.assertEquals(metaphone('nelson'), 'NLSN')
        self.assertEquals(metaphone('nesbitt'), 'NSBT')
        self.assertEquals(metaphone('neumann'), 'NMN')
        self.assertEquals(metaphone('newall'), 'NWL')
        self.assertEquals(metaphone('newell'), 'NWL')
        self.assertEquals(metaphone('newlands'), 'NLNTS')
        self.assertEquals(metaphone('neylan'), 'NLN')
        self.assertEquals(metaphone('neylon'), 'NLN')
        self.assertEquals(metaphone('nichol'), 'NXL')
        self.assertEquals(metaphone('nicoll'), 'NKL')
        self.assertEquals(metaphone('nicol'), 'NKL')
        self.assertEquals(metaphone('nisbet'), 'NSBT')
        self.assertEquals(metaphone('norton'), 'NRTN')
        self.assertEquals(metaphone('nowlands'), 'NLNTS')
        self.assertEquals(metaphone('o\'brian'), 'OBRN')
        self.assertEquals(metaphone('o\'brien'), 'OBRN')
        self.assertEquals(metaphone('ockwell'), 'OKWL')
        self.assertEquals(metaphone('o\'connell'), 'OKNL')
        self.assertEquals(metaphone('o\'connor'), 'OKNR')
        self.assertEquals(metaphone('ocwell'), 'OKWL')
        self.assertEquals(metaphone('odham'), 'OTHM')
        self.assertEquals(metaphone('ogilvie'), 'OJLF')
        self.assertEquals(metaphone('ogivie'), 'OJF')
        self.assertEquals(metaphone('o\'keefe'), 'OKF')
        self.assertEquals(metaphone('o\'keeffe'), 'OKF')
        self.assertEquals(metaphone('oldham'), 'OLTHM')
        self.assertEquals(metaphone('olsen'), 'OLSN')
        self.assertEquals(metaphone('olsien'), 'OLSN')
        self.assertEquals(metaphone('osmand'), 'OSMNT')
        self.assertEquals(metaphone('osmond'), 'OSMNT')
        self.assertEquals(metaphone('page'), 'PJ')
        self.assertEquals(metaphone('paine'), 'PN')
        self.assertEquals(metaphone('pascoe'), 'PSK')
        self.assertEquals(metaphone('pasco'), 'PSK')
        self.assertEquals(metaphone('paterson'), 'PTRSN')
        self.assertEquals(metaphone('patrick'), 'PTRK')
        self.assertEquals(metaphone('patterson'), 'PTRSN')
        self.assertEquals(metaphone('pattison'), 'PTSN')
        self.assertEquals(metaphone('pattrick'), 'PTRK')
        self.assertEquals(metaphone('payne'), 'PN')
        self.assertEquals(metaphone('peace'), 'PS')
        self.assertEquals(metaphone('pearce'), 'PRS')
        self.assertEquals(metaphone('peebles'), 'PBLS')
        self.assertEquals(metaphone('pegg'), 'PK')
        self.assertEquals(metaphone('peoples'), 'PPLS')
        self.assertEquals(metaphone('pepperell'), 'PPRL')
        self.assertEquals(metaphone('pepperill'), 'PPRL')
        self.assertEquals(metaphone('perry'), 'PR')
        self.assertEquals(metaphone('petersen'), 'PTRSN')
        self.assertEquals(metaphone('peterson'), 'PTRSN')
        self.assertEquals(metaphone('phimester'), 'FMSTR')
        self.assertEquals(metaphone('phimister'), 'FMSTR')
        self.assertEquals(metaphone('picket'), 'PKT')
        self.assertEquals(metaphone('pickett'), 'PKT')
        self.assertEquals(metaphone('pickles'), 'PKLS')
        self.assertEquals(metaphone('picklis'), 'PKLS')
        self.assertEquals(metaphone('pollock'), 'PLK')
        self.assertEquals(metaphone('polloek'), 'PLK')
        self.assertEquals(metaphone('polwarth'), 'PLWR0')
        self.assertEquals(metaphone('polworth'), 'PLWR0')
        self.assertEquals(metaphone('popperell'), 'PPRL')
        self.assertEquals(metaphone('powell'), 'PWL')
        self.assertEquals(metaphone('power'), 'PWR')
        self.assertEquals(metaphone('preston'), 'PRSTN')
        self.assertEquals(metaphone('priston'), 'PRSTN')
        self.assertEquals(metaphone('procter'), 'PRKTR')
        self.assertEquals(metaphone('proctor'), 'PRKTR')
        self.assertEquals(metaphone('pullar'), 'PLR')
        self.assertEquals(metaphone('puller'), 'PLR')
        self.assertEquals(metaphone('purches'), 'PRXS')
        self.assertEquals(metaphone('rae'), 'R')
        self.assertEquals(metaphone('ramsay'), 'RMS')
        self.assertEquals(metaphone('ramsey'), 'RMS')
        self.assertEquals(metaphone('ray'), 'R')
        self.assertEquals(metaphone('redder'), 'RTR')
        self.assertEquals(metaphone('reed'), 'RT')
        self.assertEquals(metaphone('reider'), 'RTR')
        self.assertEquals(metaphone('reidle'), 'RTL')
        self.assertEquals(metaphone('reid'), 'RT')
        self.assertEquals(metaphone('rendel'), 'RNTL')
        self.assertEquals(metaphone('render'), 'RNTR')
        self.assertEquals(metaphone('renfree'), 'RNFR')
        self.assertEquals(metaphone('renfrew'), 'RNFR')
        self.assertEquals(metaphone('riddoch'), 'RTX')
        self.assertEquals(metaphone('riddock'), 'RTK')
        self.assertEquals(metaphone('riedle'), 'RTL')
        self.assertEquals(metaphone('riley'), 'RL')
        self.assertEquals(metaphone('rilly'), 'RL')
        self.assertEquals(metaphone('robertsan'), 'RBRTSN')
        self.assertEquals(metaphone('robertson'), 'RBRTSN')
        self.assertEquals(metaphone('rodgerson'), 'RJRSN')
        self.assertEquals(metaphone('rodgers'), 'RJRS')
        self.assertEquals(metaphone('rogerson'), 'RJRSN')
        self.assertEquals(metaphone('rogers'), 'RJRS')
        self.assertEquals(metaphone('rorley'), 'RRL')
        self.assertEquals(metaphone('rosenbrock'), 'RSNBRK')
        self.assertEquals(metaphone('rosenbrook'), 'RSNBRK')
        self.assertEquals(metaphone('rose'), 'RS')
        self.assertEquals(metaphone('ross'), 'RS')
        self.assertEquals(metaphone('routledge'), 'RTLJ')
        self.assertEquals(metaphone('routlege'), 'RTLJ')
        self.assertEquals(metaphone('rowley'), 'RL')
        self.assertEquals(metaphone('russell'), 'RSL')
        self.assertEquals(metaphone('sanders'), 'SNTRS')
        self.assertEquals(metaphone('sandes'), 'SNTS')
        self.assertEquals(metaphone('sandrey'), 'SNTR')
        self.assertEquals(metaphone('sandry'), 'SNTR')
        self.assertEquals(metaphone('saunders'), 'SNTRS')
        self.assertEquals(metaphone('saxton'), 'SKSTN')
        self.assertEquals(metaphone('scaife'), 'SKF')
        self.assertEquals(metaphone('scanlan'), 'SKNLN')
        self.assertEquals(metaphone('scanlon'), 'SKNLN')
        self.assertEquals(metaphone('scarfe'), 'SKRF')
        self.assertEquals(metaphone('scoffeld'), 'SKFLT')
        self.assertEquals(metaphone('scofield'), 'SKFLT')
        self.assertEquals(metaphone('seamer'), 'SMR')
        self.assertEquals(metaphone('sellar'), 'SLR')
        self.assertEquals(metaphone('seller'), 'SLR')
        self.assertEquals(metaphone('sexton'), 'SKSTN')
        self.assertEquals(metaphone('seymour'), 'SMR')
        self.assertEquals(metaphone('sharpe'), 'XRP')
        self.assertEquals(metaphone('sharp'), 'XRP')
        self.assertEquals(metaphone('shaw'), 'X')
        self.assertEquals(metaphone('shea'), 'X')
        self.assertEquals(metaphone('shephard'), 'XFRT')
        self.assertEquals(metaphone('shepherd'), 'XFRT')
        self.assertEquals(metaphone('sheppard'), 'XPRT')
        self.assertEquals(metaphone('shepperd'), 'XPRT')
        self.assertEquals(metaphone('sheriff'), 'XRF')
        self.assertEquals(metaphone('sherriff'), 'XRF')
        self.assertEquals(metaphone('sidey'), 'ST')
        self.assertEquals(metaphone('sidoy'), 'ST')
        self.assertEquals(metaphone('silvertsen'), 'SLFRTSN')
        self.assertEquals(metaphone('sincock'), 'SNKK')
        self.assertEquals(metaphone('sincok'), 'SNKK')
        self.assertEquals(metaphone('sivertsen'), 'SFRTSN')
        self.assertEquals(metaphone('skeene'), 'SKN')
        self.assertEquals(metaphone('skene'), 'SKN')
        self.assertEquals(metaphone('slowley'), 'SLL')
        self.assertEquals(metaphone('slowly'), 'SLL')
        self.assertEquals(metaphone('smith'), 'SM0')
        self.assertEquals(metaphone('smythe'), 'SM0')
        self.assertEquals(metaphone('smyth'), 'SM0')
        self.assertEquals(metaphone('spencer'), 'SPNSR')
        self.assertEquals(metaphone('spence'), 'SPNS')
        self.assertEquals(metaphone('steadman'), 'STTMN')
        self.assertEquals(metaphone('stedman'), 'STTMN')
        self.assertEquals(metaphone('stenhouse'), 'STNHS')
        self.assertEquals(metaphone('stennouse'), 'STNS')
        self.assertEquals(metaphone('stephenson'), 'STFNSN')
        self.assertEquals(metaphone('stevenson'), 'STFNSN')
        self.assertEquals(metaphone('stichmann'), 'STXMN')
        self.assertEquals(metaphone('stickman'), 'STKMN')
        self.assertEquals(metaphone('stock'), 'STK')
        self.assertEquals(metaphone('stook'), 'STK')
        self.assertEquals(metaphone('strang'), 'STRNK')
        self.assertEquals(metaphone('strong'), 'STRNK')
        self.assertEquals(metaphone('summerell'), 'SMRL')
        self.assertEquals(metaphone('taverner'), 'TFRNR')
        self.assertEquals(metaphone('tillie'), 'TL')
        self.assertEquals(metaphone('tiverner'), 'TFRNR')
        self.assertEquals(metaphone('todd'), 'TT')
        self.assertEquals(metaphone('tonar'), 'TNR')
        self.assertEquals(metaphone('toner'), 'TNR')
        self.assertEquals(metaphone('tonner'), 'TNR')
        self.assertEquals(metaphone('tonnor'), 'TNR')
        self.assertEquals(metaphone('townsend'), 'TNSNT')
        self.assertEquals(metaphone('townshend'), 'TNXNT')
        self.assertEquals(metaphone('treeweek'), 'TRWK')
        self.assertEquals(metaphone('tregoning'), 'TRKNNK')
        self.assertEquals(metaphone('tregonning'), 'TRKNNK')
        self.assertEquals(metaphone('trevena'), 'TRFN')
        self.assertEquals(metaphone('trevenna'), 'TRFN')
        self.assertEquals(metaphone('trewick'), 'TRWK')
        self.assertEquals(metaphone('turley'), 'TRL')
        self.assertEquals(metaphone('vial'), 'FL')
        self.assertEquals(metaphone('vintinner'), 'FNTNR')
        self.assertEquals(metaphone('vintinuer'), 'FNTNR')
        self.assertEquals(metaphone('wackeldine'), 'WKLTN')
        self.assertEquals(metaphone('wackildene'), 'WKLTN')
        self.assertEquals(metaphone('wackilden'), 'WKLTN')
        self.assertEquals(metaphone('waghornee'), 'WRN')
        self.assertEquals(metaphone('waghorne'), 'WRN')
        self.assertEquals(metaphone('wallace'), 'WLS')
        self.assertEquals(metaphone('wallin'), 'WLN')
        self.assertEquals(metaphone('walquest'), 'WLKST')
        self.assertEquals(metaphone('walquist'), 'WLKST')
        self.assertEquals(metaphone('walsh'), 'WLX')
        self.assertEquals(metaphone('warreil'), 'WRL')
        self.assertEquals(metaphone('warrell'), 'WRL')
        self.assertEquals(metaphone('watsan'), 'WTSN')
        self.assertEquals(metaphone('watson'), 'WTSN')
        self.assertEquals(metaphone('welbourn'), 'WLBRN')
        self.assertEquals(metaphone('weldon'), 'WLTN')
        self.assertEquals(metaphone('wellbourn'), 'WLBRN')
        self.assertEquals(metaphone('wells'), 'WLS')
        self.assertEquals(metaphone('welsh'), 'WLX')
        self.assertEquals(metaphone('wheelan'), 'WLN')
        self.assertEquals(metaphone('wheeler'), 'WLR')
        self.assertEquals(metaphone('whelan'), 'WLN')
        self.assertEquals(metaphone('white'), 'WT')
        self.assertEquals(metaphone('whyte'), 'T')
        self.assertEquals(metaphone('wilden'), 'WLTN')
        self.assertEquals(metaphone('wildey'), 'WLT')
        self.assertEquals(metaphone('wildoy'), 'WLT')
        self.assertEquals(metaphone('willis'), 'WLS')
        self.assertEquals(metaphone('willon'), 'WLN')
        self.assertEquals(metaphone('willson'), 'WLSN')
        self.assertEquals(metaphone('wills'), 'WLS')
        self.assertEquals(metaphone('wilson'), 'WLSN')
        self.assertEquals(metaphone('wilton'), 'WLTN')
        self.assertEquals(metaphone('winders'), 'WNTRS')
        self.assertEquals(metaphone('windus'), 'WNTS')
        self.assertEquals(metaphone('wine'), 'WN')
        self.assertEquals(metaphone('winn'), 'WN')
        self.assertEquals(metaphone('wooton'), 'WTN')
        self.assertEquals(metaphone('wootten'), 'WTN')
        self.assertEquals(metaphone('wootton'), 'WTN')
        self.assertEquals(metaphone('wraight'), 'RKT')
        self.assertEquals(metaphone('wright'), 'RKT')


class double_metaphone_test_cases(unittest.TestCase):
    """These test cases are copied from two sources:
    https://github.com/oubiwann/metaphone/blob/master/metaphone/tests/test_metaphone.py
    and
    http://swoodbridge.com/DoubleMetaPhone/surnames.txt

    All tests other than test_surnames and test_surnames4 come from
    the former and are under the following license:

        Copyright (c) 2007 Andrew Collins, Chris Leong
        Copyright (c) 2009 Matthew Somerville
        Copyright (c) 2010 Maximillian Dornseif, Richard Barran
        Copyright (c) 2012 Duncan McGreggor
        All rights reserved.

         * Redistribution and use in source and binary forms, with or without
            modification, are permitted provided that the following conditions
            are met:

         * Redistributions of source code must retain the above copyright
             notice, this list of conditions and the following disclaimer.

         * Redistributions in binary form must reproduce the above copyright
            notice, this list of conditions and the following disclaimer in
            the documentation and/or other materials provided with the
            distribution.

        Neither the name "Metaphone" nor the names of its contributors may be
        used to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
        A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
        HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
        SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
        LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
        THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    test_surname and test_surname4 come from a set of tests for a PHP port
    of Double Metaphone that is Copyright 2001, Stephen Woodbridge and
    identified as 'freely distributable'
    """
    def test_double_metaphone_single_result(self):
        self.assertEquals(double_metaphone(u"aubrey"), ('APR', ''))

    def test_double_metaphone_double_result(self):
        self.assertEquals(double_metaphone(u"richard"), ('RXRT', 'RKRT'))

    def test_double_metaphone_general_word_list(self):
        self.assertEquals(double_metaphone('Jose'), ('HS', ''))
        self.assertEquals(double_metaphone('cambrillo'), ('KMPRL', 'KMPR'))
        self.assertEquals(double_metaphone('otto'), ('AT', ''))
        self.assertEquals(double_metaphone('aubrey'), ('APR', ''))
        self.assertEquals(double_metaphone('maurice'), ('MRS', ''))
        self.assertEquals(double_metaphone('auto'), ('AT', ''))
        self.assertEquals(double_metaphone('maisey'), ('MS', ''))
        self.assertEquals(double_metaphone('catherine'), ('K0RN', 'KTRN'))
        self.assertEquals(double_metaphone('geoff'), ('JF', 'KF'))
        self.assertEquals(double_metaphone('Chile'), ('XL', ''))
        self.assertEquals(double_metaphone('katherine'), ('K0RN', 'KTRN'))
        self.assertEquals(double_metaphone('steven'), ('STFN', ''))
        self.assertEquals(double_metaphone('zhang'), ('JNK', ''))
        self.assertEquals(double_metaphone('bob'), ('PP', ''))
        self.assertEquals(double_metaphone('ray'), ('R', ''))
        self.assertEquals(double_metaphone('Tux'), ('TKS', ''))
        self.assertEquals(double_metaphone('bryan'), ('PRN', ''))
        self.assertEquals(double_metaphone('bryce'), ('PRS', ''))
        self.assertEquals(double_metaphone('Rapelje'), ('RPL', ''))
        self.assertEquals(double_metaphone('richard'), ('RXRT', 'RKRT'))
        self.assertEquals(double_metaphone('solilijs'), ('SLLS', ''))
        self.assertEquals(double_metaphone('Dallas'), ('TLS', ''))
        self.assertEquals(double_metaphone('Schwein'), ('XN', 'XFN'))
        self.assertEquals(double_metaphone('dave'), ('TF', ''))
        self.assertEquals(double_metaphone('eric'), ('ARK', ''))
        self.assertEquals(double_metaphone('Parachute'), ('PRKT', ''))
        self.assertEquals(double_metaphone('brian'), ('PRN', ''))
        self.assertEquals(double_metaphone('randy'), ('RNT', ''))
        self.assertEquals(double_metaphone('Through'), ('0R', 'TR'))
        self.assertEquals(double_metaphone('Nowhere'), ('NR', ''))
        self.assertEquals(double_metaphone('heidi'), ('HT', ''))
        self.assertEquals(double_metaphone('Arnow'), ('ARN', 'ARNF'))
        self.assertEquals(double_metaphone('Thumbail'), ('0MPL', 'TMPL'))

    def test_double_metaphone_homophones(self):
        self.assertEqual(double_metaphone(u"tolled"), double_metaphone(u"told"))
        self.assertEqual(double_metaphone(u"katherine"),
                         double_metaphone(u"catherine"))
        self.assertEqual(double_metaphone(u"brian"), double_metaphone(u"bryan"))

    def test_double_metaphone_similar_names(self):
        self.assertEquals(double_metaphone("Bartoš"), ('PRT', ''))
        self.assertEquals(double_metaphone(u"Bartosz"), ('PRTS', 'PRTX'))
        self.assertEquals(double_metaphone(u"Bartosch"), ('PRTX', ''))
        self.assertEquals(double_metaphone(u"Bartos"), ('PRTS', ''))
        self.assertEquals(list(set(double_metaphone(u"Jablonski"))\
                               .intersection(double_metaphone(u"Yablonsky"))),\
                          ['APLNSK'])
        self.assertEquals(list(set(double_metaphone(u"Smith"))\
                               .intersection(double_metaphone(u"Schmidt"))),\
                          ['XMT'])

    def test_double_metaphone_non_english_unicode(self):
        self.assertEquals(double_metaphone("andestādītu"), ('ANTSTTT', ''))

    def test_double_metaphone_c_cedilla(self):
        self.assertEquals(double_metaphone("français"), ('FRNS', 'FRNSS'))
        self.assertEquals(double_metaphone("garçon"), ('KRSN', ''))
        self.assertEquals(double_metaphone("leçon"), ('LSN', ''))

    def test_double_metaphone_german(self):
        self.assertEquals(double_metaphone("ach"), ("AK", ""))
        self.assertEquals(double_metaphone("bacher"), ("PKR", ""))
        self.assertEquals(double_metaphone("macher"), ("MKR", ""))

    def test_double_metaphone_italian(self):
        self.assertEquals(double_metaphone("bacci"), ("PX", ""))
        self.assertEquals(double_metaphone("bertucci"), ("PRTX", ""))
        self.assertEquals(double_metaphone("bellocchio"), ("PLX", ""))
        self.assertEquals(double_metaphone("bacchus"), ("PKS", ""))
        self.assertEquals(double_metaphone("focaccia"), ("FKX", ""))
        self.assertEquals(double_metaphone("chianti"), ("KNT", ""))
        self.assertEquals(double_metaphone("tagliaro"), ("TKLR", "TLR"))
        self.assertEquals(double_metaphone("biaggi"), ("PJ", "PK"))

    def test_double_metaphone_spanish(self):
        self.assertEquals(double_metaphone("bajador"), ("PJTR", "PHTR"))
        self.assertEquals(double_metaphone("cabrillo"), ("KPRL", "KPR"))
        self.assertEquals(double_metaphone("gallegos"), ("KLKS", "KKS"))
        self.assertEquals(double_metaphone("San Jacinto"), ("SNHSNT", ""))

    def test_double_metaphone_french(self):
        self.assertEquals(double_metaphone("rogier"), ("RJ", "RJR"))
        self.assertEquals(double_metaphone("breaux"), ("PR", ""))

    def test_double_metaphone_slavic(self):
        self.assertEquals(double_metaphone("Wewski"), ("ASK", "FFSK"))

    def test_double_metaphone_chinese(self):
        self.assertEquals(double_metaphone("zhao"), ("J", ""))

    def test_double_metaphone_dutch_origin(self):
        self.assertEquals(double_metaphone("school"), ("SKL", ""))
        self.assertEquals(double_metaphone("schooner"), ("SKNR", ""))
        self.assertEquals(double_metaphone("schermerhorn"),
                          ("XRMRRN", "SKRMRRN"))
        self.assertEquals(double_metaphone("schenker"), ("XNKR", "SKNKR"))

    def test_double_metaphone_ch_words(self):
        self.assertEquals(double_metaphone("Charac"), ("KRK", ""))
        self.assertEquals(double_metaphone("Charis"), ("KRS", ""))
        self.assertEquals(double_metaphone("chord"), ("KRT", ""))
        self.assertEquals(double_metaphone("Chym"), ("KM", ""))
        self.assertEquals(double_metaphone("Chia"), ("K", ""))
        self.assertEquals(double_metaphone("chem"), ("KM", ""))
        self.assertEquals(double_metaphone("chore"), ("XR", ""))
        self.assertEquals(double_metaphone("orchestra"), ("ARKSTR", ""))
        self.assertEquals(double_metaphone("architect"), ("ARKTKT", ""))
        self.assertEquals(double_metaphone("orchid"), ("ARKT", ""))

    def test_double_metaphone_cc_words(self):
        self.assertEquals(double_metaphone("accident"), ("AKSTNT", ""))
        self.assertEquals(double_metaphone("accede"), ("AKST", ""))
        self.assertEquals(double_metaphone("succeed"), ("SKST", ""))

    def test_double_metaphone_mc_words(self):
        self.assertEquals(double_metaphone("mac caffrey"), ("MKFR", ""))
        self.assertEquals(double_metaphone("mac gregor"), ("MKRKR", ""))
        self.assertEquals(double_metaphone("mc crae"), ("MKR", ""))
        self.assertEquals(double_metaphone("mcclain"), ("MKLN", ""))

    def test_double_metaphone_gh_words(self):
        self.assertEquals(double_metaphone("laugh"), ("LF", ""))
        self.assertEquals(double_metaphone("cough"), ("KF", ""))
        self.assertEquals(double_metaphone("rough"), ("RF", ""))

    def test_double_metaphone_g3_words(self):
        self.assertEquals(double_metaphone("gya"), ("K", "J"))
        self.assertEquals(double_metaphone("ges"), ("KS", "JS"))
        self.assertEquals(double_metaphone("gep"), ("KP", "JP"))
        self.assertEquals(double_metaphone("geb"), ("KP", "JP"))
        self.assertEquals(double_metaphone("gel"), ("KL", "JL"))
        self.assertEquals(double_metaphone("gey"), ("K", "J"))
        self.assertEquals(double_metaphone("gib"), ("KP", "JP"))
        self.assertEquals(double_metaphone("gil"), ("KL", "JL"))
        self.assertEquals(double_metaphone("gin"), ("KN", "JN"))
        self.assertEquals(double_metaphone("gie"), ("K", "J"))
        self.assertEquals(double_metaphone("gei"), ("K", "J"))
        self.assertEquals(double_metaphone("ger"), ("KR", "JR"))
        self.assertEquals(double_metaphone("danger"), ("TNJR", "TNKR"))
        self.assertEquals(double_metaphone("manager"), ("MNKR", "MNJR"))
        self.assertEquals(double_metaphone("dowager"), ("TKR", "TJR"))

    def test_double_metaphone_pb_words(self):
        self.assertEquals(double_metaphone("Campbell"), ("KMPL", ""))
        self.assertEquals(double_metaphone("raspberry"), ("RSPR", ""))

    def test_double_metaphone_th_words(self):
        self.assertEquals(double_metaphone("Thomas"), ("TMS", ""))
        self.assertEquals(double_metaphone("Thames"), ("TMS", ""))

    def test_double_metaphone_surnames(self):
        self.assertEquals(double_metaphone(''), ('', ''))
        self.assertEquals(double_metaphone('ALLERTON'), ('ALRTN', ''))
        self.assertEquals(double_metaphone('Acton'), ('AKTN', ''))
        self.assertEquals(double_metaphone('Adams'), ('ATMS', ''))
        self.assertEquals(double_metaphone('Aggar'), ('AKR', ''))
        self.assertEquals(double_metaphone('Ahl'), ('AL', ''))
        self.assertEquals(double_metaphone('Aiken'), ('AKN', ''))
        self.assertEquals(double_metaphone('Alan'), ('ALN', ''))
        self.assertEquals(double_metaphone('Alcock'), ('ALKK', ''))
        self.assertEquals(double_metaphone('Alden'), ('ALTN', ''))
        self.assertEquals(double_metaphone('Aldham'), ('ALTM', ''))
        self.assertEquals(double_metaphone('Allen'), ('ALN', ''))
        self.assertEquals(double_metaphone('Allerton'), ('ALRTN', ''))
        self.assertEquals(double_metaphone('Alsop'), ('ALSP', ''))
        self.assertEquals(double_metaphone('Alwein'), ('ALN', ''))
        self.assertEquals(double_metaphone('Ambler'), ('AMPLR', ''))
        self.assertEquals(double_metaphone('Andevill'), ('ANTFL', ''))
        self.assertEquals(double_metaphone('Andrews'), ('ANTRS', ''))
        self.assertEquals(double_metaphone('Andreyco'), ('ANTRK', ''))
        self.assertEquals(double_metaphone('Andriesse'), ('ANTRS', ''))
        self.assertEquals(double_metaphone('Angier'), ('ANJ', 'ANJR'))
        self.assertEquals(double_metaphone('Annabel'), ('ANPL', ''))
        self.assertEquals(double_metaphone('Anne'), ('AN', ''))
        self.assertEquals(double_metaphone('Anstye'), ('ANST', ''))
        self.assertEquals(double_metaphone('Appling'), ('APLNK', ''))
        self.assertEquals(double_metaphone('Apuke'), ('APK', ''))
        self.assertEquals(double_metaphone('Arnold'), ('ARNLT', ''))
        self.assertEquals(double_metaphone('Ashby'), ('AXP', ''))
        self.assertEquals(double_metaphone('Astwood'), ('ASTT', ''))
        self.assertEquals(double_metaphone('Atkinson'), ('ATKNSN', ''))
        self.assertEquals(double_metaphone('Audley'), ('ATL', ''))
        self.assertEquals(double_metaphone('Austin'), ('ASTN', ''))
        self.assertEquals(double_metaphone('Avenal'), ('AFNL', ''))
        self.assertEquals(double_metaphone('Ayer'), ('AR', ''))
        self.assertEquals(double_metaphone('Ayot'), ('AT', ''))
        self.assertEquals(double_metaphone('Babbitt'), ('PPT', ''))
        self.assertEquals(double_metaphone('Bachelor'), ('PXLR', 'PKLR'))
        self.assertEquals(double_metaphone('Bachelour'), ('PXLR', 'PKLR'))
        self.assertEquals(double_metaphone('Bailey'), ('PL', ''))
        self.assertEquals(double_metaphone('Baivel'), ('PFL', ''))
        self.assertEquals(double_metaphone('Baker'), ('PKR', ''))
        self.assertEquals(double_metaphone('Baldwin'), ('PLTN', ''))
        self.assertEquals(double_metaphone('Balsley'), ('PLSL', ''))
        self.assertEquals(double_metaphone('Barber'), ('PRPR', ''))
        self.assertEquals(double_metaphone('Barker'), ('PRKR', ''))
        self.assertEquals(double_metaphone('Barlow'), ('PRL', 'PRLF'))
        self.assertEquals(double_metaphone('Barnard'), ('PRNRT', ''))
        self.assertEquals(double_metaphone('Barnes'), ('PRNS', ''))
        self.assertEquals(double_metaphone('Barnsley'), ('PRNSL', ''))
        self.assertEquals(double_metaphone('Barouxis'), ('PRKSS', ''))
        self.assertEquals(double_metaphone('Bartlet'), ('PRTLT', ''))
        self.assertEquals(double_metaphone('Basley'), ('PSL', ''))
        self.assertEquals(double_metaphone('Basset'), ('PST', ''))
        self.assertEquals(double_metaphone('Bassett'), ('PST', ''))
        self.assertEquals(double_metaphone('Batchlor'), ('PXLR', ''))
        self.assertEquals(double_metaphone('Bates'), ('PTS', ''))
        self.assertEquals(double_metaphone('Batson'), ('PTSN', ''))
        self.assertEquals(double_metaphone('Bayes'), ('PS', ''))
        self.assertEquals(double_metaphone('Bayley'), ('PL', ''))
        self.assertEquals(double_metaphone('Beale'), ('PL', ''))
        self.assertEquals(double_metaphone('Beauchamp'), ('PXMP', 'PKMP'))
        self.assertEquals(double_metaphone('Beauclerc'), ('PKLRK', ''))
        self.assertEquals(double_metaphone('Beech'), ('PK', ''))
        self.assertEquals(double_metaphone('Beers'), ('PRS', ''))
        self.assertEquals(double_metaphone('Beke'), ('PK', ''))
        self.assertEquals(double_metaphone('Belcher'), ('PLXR', 'PLKR'))
        self.assertEquals(double_metaphone('Benjamin'), ('PNJMN', ''))
        self.assertEquals(double_metaphone('Benningham'), ('PNNKM', ''))
        self.assertEquals(double_metaphone('Bereford'), ('PRFRT', ''))
        self.assertEquals(double_metaphone('Bergen'), ('PRJN', 'PRKN'))
        self.assertEquals(double_metaphone('Berkeley'), ('PRKL', ''))
        self.assertEquals(double_metaphone('Berry'), ('PR', ''))
        self.assertEquals(double_metaphone('Besse'), ('PS', ''))
        self.assertEquals(double_metaphone('Bessey'), ('PS', ''))
        self.assertEquals(double_metaphone('Bessiles'), ('PSLS', ''))
        self.assertEquals(double_metaphone('Bigelow'), ('PJL', 'PKLF'))
        self.assertEquals(double_metaphone('Bigg'), ('PK', ''))
        self.assertEquals(double_metaphone('Bigod'), ('PKT', ''))
        self.assertEquals(double_metaphone('Billings'), ('PLNKS', ''))
        self.assertEquals(double_metaphone('Bimper'), ('PMPR', ''))
        self.assertEquals(double_metaphone('Binker'), ('PNKR', ''))
        self.assertEquals(double_metaphone('Birdsill'), ('PRTSL', ''))
        self.assertEquals(double_metaphone('Bishop'), ('PXP', ''))
        self.assertEquals(double_metaphone('Black'), ('PLK', ''))
        self.assertEquals(double_metaphone('Blagge'), ('PLK', ''))
        self.assertEquals(double_metaphone('Blake'), ('PLK', ''))
        self.assertEquals(double_metaphone('Blanck'), ('PLNK', ''))
        self.assertEquals(double_metaphone('Bledsoe'), ('PLTS', ''))
        self.assertEquals(double_metaphone('Blennerhasset'), ('PLNRST', ''))
        self.assertEquals(double_metaphone('Blessing'), ('PLSNK', ''))
        self.assertEquals(double_metaphone('Blewett'), ('PLT', ''))
        self.assertEquals(double_metaphone('Bloctgoed'), ('PLKTKT', ''))
        self.assertEquals(double_metaphone('Bloetgoet'), ('PLTKT', ''))
        self.assertEquals(double_metaphone('Bloodgood'), ('PLTKT', ''))
        self.assertEquals(double_metaphone('Blossom'), ('PLSM', ''))
        self.assertEquals(double_metaphone('Blount'), ('PLNT', ''))
        self.assertEquals(double_metaphone('Bodine'), ('PTN', ''))
        self.assertEquals(double_metaphone('Bodman'), ('PTMN', ''))
        self.assertEquals(double_metaphone('BonCoeur'), ('PNKR', ''))
        self.assertEquals(double_metaphone('Bond'), ('PNT', ''))
        self.assertEquals(double_metaphone('Boscawen'), ('PSKN', ''))
        self.assertEquals(double_metaphone('Bosworth'), ('PSR0', 'PSRT'))
        self.assertEquals(double_metaphone('Bouchier'), ('PX', 'PKR'))
        self.assertEquals(double_metaphone('Bowne'), ('PN', ''))
        self.assertEquals(double_metaphone('Bradbury'), ('PRTPR', ''))
        self.assertEquals(double_metaphone('Bradder'), ('PRTR', ''))
        self.assertEquals(double_metaphone('Bradford'), ('PRTFRT', ''))
        self.assertEquals(double_metaphone('Bradstreet'), ('PRTSTRT', ''))
        self.assertEquals(double_metaphone('Braham'), ('PRHM', ''))
        self.assertEquals(double_metaphone('Brailsford'), ('PRLSFRT', ''))
        self.assertEquals(double_metaphone('Brainard'), ('PRNRT', ''))
        self.assertEquals(double_metaphone('Brandish'), ('PRNTX', ''))
        self.assertEquals(double_metaphone('Braun'), ('PRN', ''))
        self.assertEquals(double_metaphone('Brecc'), ('PRK', ''))
        self.assertEquals(double_metaphone('Brent'), ('PRNT', ''))
        self.assertEquals(double_metaphone('Brenton'), ('PRNTN', ''))
        self.assertEquals(double_metaphone('Briggs'), ('PRKS', ''))
        self.assertEquals(double_metaphone('Brigham'), ('PRM', ''))
        self.assertEquals(double_metaphone('Brobst'), ('PRPST', ''))
        self.assertEquals(double_metaphone('Brome'), ('PRM', ''))
        self.assertEquals(double_metaphone('Bronson'), ('PRNSN', ''))
        self.assertEquals(double_metaphone('Brooks'), ('PRKS', ''))
        self.assertEquals(double_metaphone('Brouillard'), ('PRLRT', ''))
        self.assertEquals(double_metaphone('Brown'), ('PRN', ''))
        self.assertEquals(double_metaphone('Browne'), ('PRN', ''))
        self.assertEquals(double_metaphone('Brownell'), ('PRNL', ''))
        self.assertEquals(double_metaphone('Bruley'), ('PRL', ''))
        self.assertEquals(double_metaphone('Bryant'), ('PRNT', ''))
        self.assertEquals(double_metaphone('Brzozowski'), ('PRSSSK', 'PRTSTSFSK'))
        self.assertEquals(double_metaphone('Buide'), ('PT', ''))
        self.assertEquals(double_metaphone('Bulmer'), ('PLMR', ''))
        self.assertEquals(double_metaphone('Bunker'), ('PNKR', ''))
        self.assertEquals(double_metaphone('Burden'), ('PRTN', ''))
        self.assertEquals(double_metaphone('Burge'), ('PRJ', 'PRK'))
        self.assertEquals(double_metaphone('Burgoyne'), ('PRKN', ''))
        self.assertEquals(double_metaphone('Burke'), ('PRK', ''))
        self.assertEquals(double_metaphone('Burnett'), ('PRNT', ''))
        self.assertEquals(double_metaphone('Burpee'), ('PRP', ''))
        self.assertEquals(double_metaphone('Bursley'), ('PRSL', ''))
        self.assertEquals(double_metaphone('Burton'), ('PRTN', ''))
        self.assertEquals(double_metaphone('Bushnell'), ('PXNL', ''))
        self.assertEquals(double_metaphone('Buss'), ('PS', ''))
        self.assertEquals(double_metaphone('Buswell'), ('PSL', ''))
        self.assertEquals(double_metaphone('Butler'), ('PTLR', ''))
        self.assertEquals(double_metaphone('Calkin'), ('KLKN', ''))
        self.assertEquals(double_metaphone('Canada'), ('KNT', ''))
        self.assertEquals(double_metaphone('Canmore'), ('KNMR', ''))
        self.assertEquals(double_metaphone('Canney'), ('KN', ''))
        self.assertEquals(double_metaphone('Capet'), ('KPT', ''))
        self.assertEquals(double_metaphone('Card'), ('KRT', ''))
        self.assertEquals(double_metaphone('Carman'), ('KRMN', ''))
        self.assertEquals(double_metaphone('Carpenter'), ('KRPNTR', ''))
        self.assertEquals(double_metaphone('Cartwright'), ('KRTRT', ''))
        self.assertEquals(double_metaphone('Casey'), ('KS', ''))
        self.assertEquals(double_metaphone('Catterfield'), ('KTRFLT', ''))
        self.assertEquals(double_metaphone('Ceeley'), ('SL', ''))
        self.assertEquals(double_metaphone('Chambers'), ('XMPRS', ''))
        self.assertEquals(double_metaphone('Champion'), ('XMPN', ''))
        self.assertEquals(double_metaphone('Chapman'), ('XPMN', ''))
        self.assertEquals(double_metaphone('Chase'), ('XS', ''))
        self.assertEquals(double_metaphone('Cheney'), ('XN', ''))
        self.assertEquals(double_metaphone('Chetwynd'), ('XTNT', ''))
        self.assertEquals(double_metaphone('Chevalier'), ('XFL', 'XFLR'))
        self.assertEquals(double_metaphone('Chillingsworth'),
                          ('XLNKSR0', 'XLNKSRT'))
        self.assertEquals(double_metaphone('Christie'), ('KRST', ''))
        self.assertEquals(double_metaphone('Chubbuck'), ('XPK', ''))
        self.assertEquals(double_metaphone('Church'), ('XRX', 'XRK'))
        self.assertEquals(double_metaphone('Clark'), ('KLRK', ''))
        self.assertEquals(double_metaphone('Clarke'), ('KLRK', ''))
        self.assertEquals(double_metaphone('Cleare'), ('KLR', ''))
        self.assertEquals(double_metaphone('Clement'), ('KLMNT', ''))
        self.assertEquals(double_metaphone('Clerke'), ('KLRK', ''))
        self.assertEquals(double_metaphone('Clibben'), ('KLPN', ''))
        self.assertEquals(double_metaphone('Clifford'), ('KLFRT', ''))
        self.assertEquals(double_metaphone('Clivedon'), ('KLFTN', ''))
        self.assertEquals(double_metaphone('Close'), ('KLS', ''))
        self.assertEquals(double_metaphone('Clothilde'), ('KL0LT', 'KLTLT'))
        self.assertEquals(double_metaphone('Cobb'), ('KP', ''))
        self.assertEquals(double_metaphone('Coburn'), ('KPRN', ''))
        self.assertEquals(double_metaphone('Coburne'), ('KPRN', ''))
        self.assertEquals(double_metaphone('Cocke'), ('KK', ''))
        self.assertEquals(double_metaphone('Coffin'), ('KFN', ''))
        self.assertEquals(double_metaphone('Coffyn'), ('KFN', ''))
        self.assertEquals(double_metaphone('Colborne'), ('KLPRN', ''))
        self.assertEquals(double_metaphone('Colby'), ('KLP', ''))
        self.assertEquals(double_metaphone('Cole'), ('KL', ''))
        self.assertEquals(double_metaphone('Coleman'), ('KLMN', ''))
        self.assertEquals(double_metaphone('Collier'), ('KL', 'KLR'))
        self.assertEquals(double_metaphone('Compton'), ('KMPTN', ''))
        self.assertEquals(double_metaphone('Cone'), ('KN', ''))
        self.assertEquals(double_metaphone('Cook'), ('KK', ''))
        self.assertEquals(double_metaphone('Cooke'), ('KK', ''))
        self.assertEquals(double_metaphone('Cooper'), ('KPR', ''))
        self.assertEquals(double_metaphone('Copperthwaite'), ('KPR0T', 'KPRTT'))
        self.assertEquals(double_metaphone('Corbet'), ('KRPT', ''))
        self.assertEquals(double_metaphone('Corell'), ('KRL', ''))
        self.assertEquals(double_metaphone('Corey'), ('KR', ''))
        self.assertEquals(double_metaphone('Corlies'), ('KRLS', ''))
        self.assertEquals(double_metaphone('Corneliszen'), ('KRNLSN', 'KRNLXN'))
        self.assertEquals(double_metaphone('Cornelius'), ('KRNLS', ''))
        self.assertEquals(double_metaphone('Cornwallis'), ('KRNLS', ''))
        self.assertEquals(double_metaphone('Cosgrove'), ('KSKRF', ''))
        self.assertEquals(double_metaphone('Count of Brionne'), ('KNTFPRN', ''))
        self.assertEquals(double_metaphone('Covill'), ('KFL', ''))
        self.assertEquals(double_metaphone('Cowperthwaite'), ('KPR0T', 'KPRTT'))
        self.assertEquals(double_metaphone('Cowperwaite'), ('KPRT', ''))
        self.assertEquals(double_metaphone('Crane'), ('KRN', ''))
        self.assertEquals(double_metaphone('Creagmile'), ('KRKML', ''))
        self.assertEquals(double_metaphone('Crew'), ('KR', 'KRF'))
        self.assertEquals(double_metaphone('Crispin'), ('KRSPN', ''))
        self.assertEquals(double_metaphone('Crocker'), ('KRKR', ''))
        self.assertEquals(double_metaphone('Crockett'), ('KRKT', ''))
        self.assertEquals(double_metaphone('Crosby'), ('KRSP', ''))
        self.assertEquals(double_metaphone('Crump'), ('KRMP', ''))
        self.assertEquals(double_metaphone('Cunningham'), ('KNNKM', ''))
        self.assertEquals(double_metaphone('Curtis'), ('KRTS', ''))
        self.assertEquals(double_metaphone('Cutha'), ('K0', 'KT'))
        self.assertEquals(double_metaphone('Cutter'), ('KTR', ''))
        self.assertEquals(double_metaphone('D\'Aubigny'), ('TPN', 'TPKN'))
        self.assertEquals(double_metaphone('DAVIS'), ('TFS', ''))
        self.assertEquals(double_metaphone('Dabinott'), ('TPNT', ''))
        self.assertEquals(double_metaphone('Dacre'), ('TKR', ''))
        self.assertEquals(double_metaphone('Daggett'), ('TKT', ''))
        self.assertEquals(double_metaphone('Danvers'), ('TNFRS', ''))
        self.assertEquals(double_metaphone('Darcy'), ('TRS', ''))
        self.assertEquals(double_metaphone('Davis'), ('TFS', ''))
        self.assertEquals(double_metaphone('Dawn'), ('TN', ''))
        self.assertEquals(double_metaphone('Dawson'), ('TSN', ''))
        self.assertEquals(double_metaphone('Day'), ('T', ''))
        self.assertEquals(double_metaphone('Daye'), ('T', ''))
        self.assertEquals(double_metaphone('DeGrenier'), ('TKRN', 'TKRNR'))
        self.assertEquals(double_metaphone('Dean'), ('TN', ''))
        self.assertEquals(double_metaphone('Deekindaugh'), ('TKNT', ''))
        self.assertEquals(double_metaphone('Dennis'), ('TNS', ''))
        self.assertEquals(double_metaphone('Denny'), ('TN', ''))
        self.assertEquals(double_metaphone('Denton'), ('TNTN', ''))
        self.assertEquals(double_metaphone('Desborough'), ('TSPRF', ''))
        self.assertEquals(double_metaphone('Despenser'), ('TSPNSR', ''))
        self.assertEquals(double_metaphone('Deverill'), ('TFRL', ''))
        self.assertEquals(double_metaphone('Devine'), ('TFN', ''))
        self.assertEquals(double_metaphone('Dexter'), ('TKSTR', ''))
        self.assertEquals(double_metaphone('Dillaway'), ('TL', ''))
        self.assertEquals(double_metaphone('Dimmick'), ('TMK', ''))
        self.assertEquals(double_metaphone('Dinan'), ('TNN', ''))
        self.assertEquals(double_metaphone('Dix'), ('TKS', ''))
        self.assertEquals(double_metaphone('Doggett'), ('TKT', ''))
        self.assertEquals(double_metaphone('Donahue'), ('TNH', ''))
        self.assertEquals(double_metaphone('Dorfman'), ('TRFMN', ''))
        self.assertEquals(double_metaphone('Dorris'), ('TRS', ''))
        self.assertEquals(double_metaphone('Dow'), ('T', 'TF'))
        self.assertEquals(double_metaphone('Downey'), ('TN', ''))
        self.assertEquals(double_metaphone('Downing'), ('TNNK', ''))
        self.assertEquals(double_metaphone('Dowsett'), ('TST', ''))
        self.assertEquals(double_metaphone('Duck?'), ('TK', ''))
        self.assertEquals(double_metaphone('Dudley'), ('TTL', ''))
        self.assertEquals(double_metaphone('Duffy'), ('TF', ''))
        self.assertEquals(double_metaphone('Dunn'), ('TN', ''))
        self.assertEquals(double_metaphone('Dunsterville'), ('TNSTRFL', ''))
        self.assertEquals(double_metaphone('Durrant'), ('TRNT', ''))
        self.assertEquals(double_metaphone('Durrin'), ('TRN', ''))
        self.assertEquals(double_metaphone('Dustin'), ('TSTN', ''))
        self.assertEquals(double_metaphone('Duston'), ('TSTN', ''))
        self.assertEquals(double_metaphone('Eames'), ('AMS', ''))
        self.assertEquals(double_metaphone('Early'), ('ARL', ''))
        self.assertEquals(double_metaphone('Easty'), ('AST', ''))
        self.assertEquals(double_metaphone('Ebbett'), ('APT', ''))
        self.assertEquals(double_metaphone('Eberbach'), ('APRPK', ''))
        self.assertEquals(double_metaphone('Eberhard'), ('APRRT', ''))
        self.assertEquals(double_metaphone('Eddy'), ('AT', ''))
        self.assertEquals(double_metaphone('Edenden'), ('ATNTN', ''))
        self.assertEquals(double_metaphone('Edwards'), ('ATRTS', ''))
        self.assertEquals(double_metaphone('Eglinton'), ('AKLNTN', 'ALNTN'))
        self.assertEquals(double_metaphone('Eliot'), ('ALT', ''))
        self.assertEquals(double_metaphone('Elizabeth'), ('ALSP0', 'ALSPT'))
        self.assertEquals(double_metaphone('Ellis'), ('ALS', ''))
        self.assertEquals(double_metaphone('Ellison'), ('ALSN', ''))
        self.assertEquals(double_metaphone('Ellot'), ('ALT', ''))
        self.assertEquals(double_metaphone('Elny'), ('ALN', ''))
        self.assertEquals(double_metaphone('Elsner'), ('ALSNR', ''))
        self.assertEquals(double_metaphone('Emerson'), ('AMRSN', ''))
        self.assertEquals(double_metaphone('Empson'), ('AMPSN', ''))
        self.assertEquals(double_metaphone('Est'), ('AST', ''))
        self.assertEquals(double_metaphone('Estabrook'), ('ASTPRK', ''))
        self.assertEquals(double_metaphone('Estes'), ('ASTS', ''))
        self.assertEquals(double_metaphone('Estey'), ('AST', ''))
        self.assertEquals(double_metaphone('Evans'), ('AFNS', ''))
        self.assertEquals(double_metaphone('Fallowell'), ('FLL', ''))
        self.assertEquals(double_metaphone('Farnsworth'), ('FRNSR0', 'FRNSRT'))
        self.assertEquals(double_metaphone('Feake'), ('FK', ''))
        self.assertEquals(double_metaphone('Feke'), ('FK', ''))
        self.assertEquals(double_metaphone('Fellows'), ('FLS', ''))
        self.assertEquals(double_metaphone('Fettiplace'), ('FTPLS', ''))
        self.assertEquals(double_metaphone('Finney'), ('FN', ''))
        self.assertEquals(double_metaphone('Fischer'), ('FXR', 'FSKR'))
        self.assertEquals(double_metaphone('Fisher'), ('FXR', ''))
        self.assertEquals(double_metaphone('Fisk'), ('FSK', ''))
        self.assertEquals(double_metaphone('Fiske'), ('FSK', ''))
        self.assertEquals(double_metaphone('Fletcher'), ('FLXR', ''))
        self.assertEquals(double_metaphone('Folger'), ('FLKR', 'FLJR'))
        self.assertEquals(double_metaphone('Foliot'), ('FLT', ''))
        self.assertEquals(double_metaphone('Folyot'), ('FLT', ''))
        self.assertEquals(double_metaphone('Fones'), ('FNS', ''))
        self.assertEquals(double_metaphone('Fordham'), ('FRTM', ''))
        self.assertEquals(double_metaphone('Forstner'), ('FRSTNR', ''))
        self.assertEquals(double_metaphone('Fosten'), ('FSTN', ''))
        self.assertEquals(double_metaphone('Foster'), ('FSTR', ''))
        self.assertEquals(double_metaphone('Foulke'), ('FLK', ''))
        self.assertEquals(double_metaphone('Fowler'), ('FLR', ''))
        self.assertEquals(double_metaphone('Foxwell'), ('FKSL', ''))
        self.assertEquals(double_metaphone('Fraley'), ('FRL', ''))
        self.assertEquals(double_metaphone('Franceys'), ('FRNSS', ''))
        self.assertEquals(double_metaphone('Franke'), ('FRNK', ''))
        self.assertEquals(double_metaphone('Frascella'), ('FRSL', ''))
        self.assertEquals(double_metaphone('Frazer'), ('FRSR', ''))
        self.assertEquals(double_metaphone('Fredd'), ('FRT', ''))
        self.assertEquals(double_metaphone('Freeman'), ('FRMN', ''))
        self.assertEquals(double_metaphone('French'), ('FRNX', 'FRNK'))
        self.assertEquals(double_metaphone('Freville'), ('FRFL', ''))
        self.assertEquals(double_metaphone('Frey'), ('FR', ''))
        self.assertEquals(double_metaphone('Frick'), ('FRK', ''))
        self.assertEquals(double_metaphone('Frier'), ('FR', 'FRR'))
        self.assertEquals(double_metaphone('Froe'), ('FR', ''))
        self.assertEquals(double_metaphone('Frorer'), ('FRRR', ''))
        self.assertEquals(double_metaphone('Frost'), ('FRST', ''))
        self.assertEquals(double_metaphone('Frothingham'), ('FR0NKM', 'FRTNKM'))
        self.assertEquals(double_metaphone('Fry'), ('FR', ''))
        self.assertEquals(double_metaphone('Gaffney'), ('KFN', ''))
        self.assertEquals(double_metaphone('Gage'), ('KJ', 'KK'))
        self.assertEquals(double_metaphone('Gallion'), ('KLN', ''))
        self.assertEquals(double_metaphone('Gallishan'), ('KLXN', ''))
        self.assertEquals(double_metaphone('Gamble'), ('KMPL', ''))
        self.assertEquals(double_metaphone('Garbrand'), ('KRPRNT', ''))
        self.assertEquals(double_metaphone('Gardner'), ('KRTNR', ''))
        self.assertEquals(double_metaphone('Garrett'), ('KRT', ''))
        self.assertEquals(double_metaphone('Gassner'), ('KSNR', ''))
        self.assertEquals(double_metaphone('Gater'), ('KTR', ''))
        self.assertEquals(double_metaphone('Gaunt'), ('KNT', ''))
        self.assertEquals(double_metaphone('Gayer'), ('KR', ''))
        self.assertEquals(double_metaphone('Gerken'), ('KRKN', 'JRKN'))
        self.assertEquals(double_metaphone('Gerritsen'), ('KRTSN', 'JRTSN'))
        self.assertEquals(double_metaphone('Gibbs'), ('KPS', 'JPS'))
        self.assertEquals(double_metaphone('Giffard'), ('JFRT', 'KFRT'))
        self.assertEquals(double_metaphone('Gilbert'), ('KLPRT', 'JLPRT'))
        self.assertEquals(double_metaphone('Gill'), ('KL', 'JL'))
        self.assertEquals(double_metaphone('Gilman'), ('KLMN', 'JLMN'))
        self.assertEquals(double_metaphone('Glass'), ('KLS', ''))
        self.assertEquals(double_metaphone('GoddardGifford'), ('KTRJFRT', ''))
        self.assertEquals(double_metaphone('Godfrey'), ('KTFR', ''))
        self.assertEquals(double_metaphone('Godwin'), ('KTN', ''))
        self.assertEquals(double_metaphone('Goodale'), ('KTL', ''))
        self.assertEquals(double_metaphone('Goodnow'), ('KTN', 'KTNF'))
        self.assertEquals(double_metaphone('Gorham'), ('KRM', ''))
        self.assertEquals(double_metaphone('Goseline'), ('KSLN', ''))
        self.assertEquals(double_metaphone('Gott'), ('KT', ''))
        self.assertEquals(double_metaphone('Gould'), ('KLT', ''))
        self.assertEquals(double_metaphone('Grafton'), ('KRFTN', ''))
        self.assertEquals(double_metaphone('Grant'), ('KRNT', ''))
        self.assertEquals(double_metaphone('Gray'), ('KR', ''))
        self.assertEquals(double_metaphone('Green'), ('KRN', ''))
        self.assertEquals(double_metaphone('Griffin'), ('KRFN', ''))
        self.assertEquals(double_metaphone('Grill'), ('KRL', ''))
        self.assertEquals(double_metaphone('Grim'), ('KRM', ''))
        self.assertEquals(double_metaphone('Grisgonelle'), ('KRSKNL', ''))
        self.assertEquals(double_metaphone('Gross'), ('KRS', ''))
        self.assertEquals(double_metaphone('Guba'), ('KP', ''))
        self.assertEquals(double_metaphone('Gybbes'), ('KPS', 'JPS'))
        self.assertEquals(double_metaphone('Haburne'), ('HPRN', ''))
        self.assertEquals(double_metaphone('Hackburne'), ('HKPRN', ''))
        self.assertEquals(double_metaphone('Haddon?'), ('HTN', ''))
        self.assertEquals(double_metaphone('Haines'), ('HNS', ''))
        self.assertEquals(double_metaphone('Hale'), ('HL', ''))
        self.assertEquals(double_metaphone('Hall'), ('HL', ''))
        self.assertEquals(double_metaphone('Hallet'), ('HLT', ''))
        self.assertEquals(double_metaphone('Hallock'), ('HLK', ''))
        self.assertEquals(double_metaphone('Halstead'), ('HLSTT', ''))
        self.assertEquals(double_metaphone('Hammond'), ('HMNT', ''))
        self.assertEquals(double_metaphone('Hance'), ('HNS', ''))
        self.assertEquals(double_metaphone('Handy'), ('HNT', ''))
        self.assertEquals(double_metaphone('Hanson'), ('HNSN', ''))
        self.assertEquals(double_metaphone('Harasek'), ('HRSK', ''))
        self.assertEquals(double_metaphone('Harcourt'), ('HRKRT', ''))
        self.assertEquals(double_metaphone('Hardy'), ('HRT', ''))
        self.assertEquals(double_metaphone('Harlock'), ('HRLK', ''))
        self.assertEquals(double_metaphone('Harris'), ('HRS', ''))
        self.assertEquals(double_metaphone('Hartley'), ('HRTL', ''))
        self.assertEquals(double_metaphone('Harvey'), ('HRF', ''))
        self.assertEquals(double_metaphone('Harvie'), ('HRF', ''))
        self.assertEquals(double_metaphone('Harwood'), ('HRT', ''))
        self.assertEquals(double_metaphone('Hathaway'), ('H0', 'HT'))
        self.assertEquals(double_metaphone('Haukeness'), ('HKNS', ''))
        self.assertEquals(double_metaphone('Hawkes'), ('HKS', ''))
        self.assertEquals(double_metaphone('Hawkhurst'), ('HKRST', ''))
        self.assertEquals(double_metaphone('Hawkins'), ('HKNS', ''))
        self.assertEquals(double_metaphone('Hawley'), ('HL', ''))
        self.assertEquals(double_metaphone('Heald'), ('HLT', ''))
        self.assertEquals(double_metaphone('Helsdon'), ('HLSTN', ''))
        self.assertEquals(double_metaphone('Hemenway'), ('HMN', ''))
        self.assertEquals(double_metaphone('Hemmenway'), ('HMN', ''))
        self.assertEquals(double_metaphone('Henck'), ('HNK', ''))
        self.assertEquals(double_metaphone('Henderson'), ('HNTRSN', ''))
        self.assertEquals(double_metaphone('Hendricks'), ('HNTRKS', ''))
        self.assertEquals(double_metaphone('Hersey'), ('HRS', ''))
        self.assertEquals(double_metaphone('Hewes'), ('HS', ''))
        self.assertEquals(double_metaphone('Heyman'), ('HMN', ''))
        self.assertEquals(double_metaphone('Hicks'), ('HKS', ''))
        self.assertEquals(double_metaphone('Hidden'), ('HTN', ''))
        self.assertEquals(double_metaphone('Higgs'), ('HKS', ''))
        self.assertEquals(double_metaphone('Hill'), ('HL', ''))
        self.assertEquals(double_metaphone('Hills'), ('HLS', ''))
        self.assertEquals(double_metaphone('Hinckley'), ('HNKL', ''))
        self.assertEquals(double_metaphone('Hipwell'), ('HPL', ''))
        self.assertEquals(double_metaphone('Hobart'), ('HPRT', ''))
        self.assertEquals(double_metaphone('Hoben'), ('HPN', ''))
        self.assertEquals(double_metaphone('Hoffmann'), ('HFMN', ''))
        self.assertEquals(double_metaphone('Hogan'), ('HKN', ''))
        self.assertEquals(double_metaphone('Holmes'), ('HLMS', ''))
        self.assertEquals(double_metaphone('Hoo'), ('H', ''))
        self.assertEquals(double_metaphone('Hooker'), ('HKR', ''))
        self.assertEquals(double_metaphone('Hopcott'), ('HPKT', ''))
        self.assertEquals(double_metaphone('Hopkins'), ('HPKNS', ''))
        self.assertEquals(double_metaphone('Hopkinson'), ('HPKNSN', ''))
        self.assertEquals(double_metaphone('Hornsey'), ('HRNS', ''))
        self.assertEquals(double_metaphone('Houckgeest'), ('HKJST', 'HKKST'))
        self.assertEquals(double_metaphone('Hough'), ('H', ''))
        self.assertEquals(double_metaphone('Houstin'), ('HSTN', ''))
        self.assertEquals(double_metaphone('How'), ('H', 'HF'))
        self.assertEquals(double_metaphone('Howe'), ('H', ''))
        self.assertEquals(double_metaphone('Howland'), ('HLNT', ''))
        self.assertEquals(double_metaphone('Hubner'), ('HPNR', ''))
        self.assertEquals(double_metaphone('Hudnut'), ('HTNT', ''))
        self.assertEquals(double_metaphone('Hughes'), ('HS', ''))
        self.assertEquals(double_metaphone('Hull'), ('HL', ''))
        self.assertEquals(double_metaphone('Hulme'), ('HLM', ''))
        self.assertEquals(double_metaphone('Hume'), ('HM', ''))
        self.assertEquals(double_metaphone('Hundertumark'), ('HNTRTMRK', ''))
        self.assertEquals(double_metaphone('Hundley'), ('HNTL', ''))
        self.assertEquals(double_metaphone('Hungerford'),
                          ('HNKRFRT', 'HNJRFRT'))
        self.assertEquals(double_metaphone('Hunt'), ('HNT', ''))
        self.assertEquals(double_metaphone('Hurst'), ('HRST', ''))
        self.assertEquals(double_metaphone('Husbands'), ('HSPNTS', ''))
        self.assertEquals(double_metaphone('Hussey'), ('HS', ''))
        self.assertEquals(double_metaphone('Husted'), ('HSTT', ''))
        self.assertEquals(double_metaphone('Hutchins'), ('HXNS', ''))
        self.assertEquals(double_metaphone('Hutchinson'), ('HXNSN', ''))
        self.assertEquals(double_metaphone('Huttinger'), ('HTNKR', 'HTNJR'))
        self.assertEquals(double_metaphone('Huybertsen'), ('HPRTSN', ''))
        self.assertEquals(double_metaphone('Iddenden'), ('ATNTN', ''))
        self.assertEquals(double_metaphone('Ingraham'), ('ANKRHM', ''))
        self.assertEquals(double_metaphone('Ives'), ('AFS', ''))
        self.assertEquals(double_metaphone('Jackson'), ('JKSN', 'AKSN'))
        self.assertEquals(double_metaphone('Jacob'), ('JKP', 'AKP'))
        self.assertEquals(double_metaphone('Jans'), ('JNS', 'ANS'))
        self.assertEquals(double_metaphone('Jenkins'), ('JNKNS', 'ANKNS'))
        self.assertEquals(double_metaphone('Jewett'), ('JT', 'AT'))
        self.assertEquals(double_metaphone('Jewitt'), ('JT', 'AT'))
        self.assertEquals(double_metaphone('Johnson'), ('JNSN', 'ANSN'))
        self.assertEquals(double_metaphone('Jones'), ('JNS', 'ANS'))
        self.assertEquals(double_metaphone('Josephine'), ('JSFN', 'HSFN'))
        self.assertEquals(double_metaphone('Judd'), ('JT', 'AT'))
        self.assertEquals(double_metaphone('June'), ('JN', 'AN'))
        self.assertEquals(double_metaphone('Kamarowska'), ('KMRSK', ''))
        self.assertEquals(double_metaphone('Kay'), ('K', ''))
        self.assertEquals(double_metaphone('Kelley'), ('KL', ''))
        self.assertEquals(double_metaphone('Kelly'), ('KL', ''))
        self.assertEquals(double_metaphone('Keymber'), ('KMPR', ''))
        self.assertEquals(double_metaphone('Keynes'), ('KNS', ''))
        self.assertEquals(double_metaphone('Kilham'), ('KLM', ''))
        self.assertEquals(double_metaphone('Kim'), ('KM', ''))
        self.assertEquals(double_metaphone('Kimball'), ('KMPL', ''))
        self.assertEquals(double_metaphone('King'), ('KNK', ''))
        self.assertEquals(double_metaphone('Kinsey'), ('KNS', ''))
        self.assertEquals(double_metaphone('Kirk'), ('KRK', ''))
        self.assertEquals(double_metaphone('Kirton'), ('KRTN', ''))
        self.assertEquals(double_metaphone('Kistler'), ('KSTLR', ''))
        self.assertEquals(double_metaphone('Kitchen'), ('KXN', ''))
        self.assertEquals(double_metaphone('Kitson'), ('KTSN', ''))
        self.assertEquals(double_metaphone('Klett'), ('KLT', ''))
        self.assertEquals(double_metaphone('Kline'), ('KLN', ''))
        self.assertEquals(double_metaphone('Knapp'), ('NP', ''))
        self.assertEquals(double_metaphone('Knight'), ('NT', ''))
        self.assertEquals(double_metaphone('Knote'), ('NT', ''))
        self.assertEquals(double_metaphone('Knott'), ('NT', ''))
        self.assertEquals(double_metaphone('Knox'), ('NKS', ''))
        self.assertEquals(double_metaphone('Koeller'), ('KLR', ''))
        self.assertEquals(double_metaphone('La Pointe'), ('LPNT', ''))
        self.assertEquals(double_metaphone('LaPlante'), ('LPLNT', ''))
        self.assertEquals(double_metaphone('Laimbeer'), ('LMPR', ''))
        self.assertEquals(double_metaphone('Lamb'), ('LMP', ''))
        self.assertEquals(double_metaphone('Lambertson'), ('LMPRTSN', ''))
        self.assertEquals(double_metaphone('Lancto'), ('LNKT', ''))
        self.assertEquals(double_metaphone('Landry'), ('LNTR', ''))
        self.assertEquals(double_metaphone('Lane'), ('LN', ''))
        self.assertEquals(double_metaphone('Langendyck'), ('LNJNTK', 'LNKNTK'))
        self.assertEquals(double_metaphone('Langer'), ('LNKR', 'LNJR'))
        self.assertEquals(double_metaphone('Langford'), ('LNKFRT', ''))
        self.assertEquals(double_metaphone('Lantersee'), ('LNTRS', ''))
        self.assertEquals(double_metaphone('Laquer'), ('LKR', ''))
        self.assertEquals(double_metaphone('Larkin'), ('LRKN', ''))
        self.assertEquals(double_metaphone('Latham'), ('LTM', ''))
        self.assertEquals(double_metaphone('Lathrop'), ('L0RP', 'LTRP'))
        self.assertEquals(double_metaphone('Lauter'), ('LTR', ''))
        self.assertEquals(double_metaphone('Lawrence'), ('LRNS', ''))
        self.assertEquals(double_metaphone('Leach'), ('LK', ''))
        self.assertEquals(double_metaphone('Leager'), ('LKR', 'LJR'))
        self.assertEquals(double_metaphone('Learned'), ('LRNT', ''))
        self.assertEquals(double_metaphone('Leavitt'), ('LFT', ''))
        self.assertEquals(double_metaphone('Lee'), ('L', ''))
        self.assertEquals(double_metaphone('Leete'), ('LT', ''))
        self.assertEquals(double_metaphone('Leggett'), ('LKT', ''))
        self.assertEquals(double_metaphone('Leland'), ('LLNT', ''))
        self.assertEquals(double_metaphone('Leonard'), ('LNRT', ''))
        self.assertEquals(double_metaphone('Lester'), ('LSTR', ''))
        self.assertEquals(double_metaphone('Lestrange'), ('LSTRNJ', 'LSTRNK'))
        self.assertEquals(double_metaphone('Lethem'), ('L0M', 'LTM'))
        self.assertEquals(double_metaphone('Levine'), ('LFN', ''))
        self.assertEquals(double_metaphone('Lewes'), ('LS', ''))
        self.assertEquals(double_metaphone('Lewis'), ('LS', ''))
        self.assertEquals(double_metaphone('Lincoln'), ('LNKLN', ''))
        self.assertEquals(double_metaphone('Lindsey'), ('LNTS', ''))
        self.assertEquals(double_metaphone('Linher'), ('LNR', ''))
        self.assertEquals(double_metaphone('Lippet'), ('LPT', ''))
        self.assertEquals(double_metaphone('Lippincott'), ('LPNKT', ''))
        self.assertEquals(double_metaphone('Lockwood'), ('LKT', ''))
        self.assertEquals(double_metaphone('Loines'), ('LNS', ''))
        self.assertEquals(double_metaphone('Lombard'), ('LMPRT', ''))
        self.assertEquals(double_metaphone('Long'), ('LNK', ''))
        self.assertEquals(double_metaphone('Longespee'), ('LNJSP', 'LNKSP'))
        self.assertEquals(double_metaphone('Look'), ('LK', ''))
        self.assertEquals(double_metaphone('Lounsberry'), ('LNSPR', ''))
        self.assertEquals(double_metaphone('Lounsbury'), ('LNSPR', ''))
        self.assertEquals(double_metaphone('Louthe'), ('L0', 'LT'))
        self.assertEquals(double_metaphone('Loveyne'), ('LFN', ''))
        self.assertEquals(double_metaphone('Lowe'), ('L', ''))
        self.assertEquals(double_metaphone('Ludlam'), ('LTLM', ''))
        self.assertEquals(double_metaphone('Lumbard'), ('LMPRT', ''))
        self.assertEquals(double_metaphone('Lund'), ('LNT', ''))
        self.assertEquals(double_metaphone('Luno'), ('LN', ''))
        self.assertEquals(double_metaphone('Lutz'), ('LTS', ''))
        self.assertEquals(double_metaphone('Lydia'), ('LT', ''))
        self.assertEquals(double_metaphone('Lynne'), ('LN', ''))
        self.assertEquals(double_metaphone('Lyon'), ('LN', ''))
        self.assertEquals(double_metaphone('MacAlpin'), ('MKLPN', ''))
        self.assertEquals(double_metaphone('MacBricc'), ('MKPRK', ''))
        self.assertEquals(double_metaphone('MacCrinan'), ('MKRNN', ''))
        self.assertEquals(double_metaphone('MacKenneth'), ('MKN0', 'MKNT'))
        self.assertEquals(double_metaphone('MacMael nam Bo'), ('MKMLNMP', ''))
        self.assertEquals(double_metaphone('MacMurchada'), ('MKMRXT', 'MKMRKT'))
        self.assertEquals(double_metaphone('Macomber'), ('MKMPR', ''))
        self.assertEquals(double_metaphone('Macy'), ('MS', ''))
        self.assertEquals(double_metaphone('Magnus'), ('MNS', 'MKNS'))
        self.assertEquals(double_metaphone('Mahien'), ('MHN', ''))
        self.assertEquals(double_metaphone('Malmains'), ('MLMNS', ''))
        self.assertEquals(double_metaphone('Malory'), ('MLR', ''))
        self.assertEquals(double_metaphone('Mancinelli'), ('MNSNL', ''))
        self.assertEquals(double_metaphone('Mancini'), ('MNSN', ''))
        self.assertEquals(double_metaphone('Mann'), ('MN', ''))
        self.assertEquals(double_metaphone('Manning'), ('MNNK', ''))
        self.assertEquals(double_metaphone('Manter'), ('MNTR', ''))
        self.assertEquals(double_metaphone('Marion'), ('MRN', ''))
        self.assertEquals(double_metaphone('Marley'), ('MRL', ''))
        self.assertEquals(double_metaphone('Marmion'), ('MRMN', ''))
        self.assertEquals(double_metaphone('Marquart'), ('MRKRT', ''))
        self.assertEquals(double_metaphone('Marsh'), ('MRX', ''))
        self.assertEquals(double_metaphone('Marshal'), ('MRXL', ''))
        self.assertEquals(double_metaphone('Marshall'), ('MRXL', ''))
        self.assertEquals(double_metaphone('Martel'), ('MRTL', ''))
        self.assertEquals(double_metaphone('Martha'), ('MR0', 'MRT'))
        self.assertEquals(double_metaphone('Martin'), ('MRTN', ''))
        self.assertEquals(double_metaphone('Marturano'), ('MRTRN', ''))
        self.assertEquals(double_metaphone('Marvin'), ('MRFN', ''))
        self.assertEquals(double_metaphone('Mary'), ('MR', ''))
        self.assertEquals(double_metaphone('Mason'), ('MSN', ''))
        self.assertEquals(double_metaphone('Maxwell'), ('MKSL', ''))
        self.assertEquals(double_metaphone('Mayhew'), ('MH', 'MHF'))
        self.assertEquals(double_metaphone('McAllaster'), ('MKLSTR', ''))
        self.assertEquals(double_metaphone('McAllister'), ('MKLSTR', ''))
        self.assertEquals(double_metaphone('McConnell'), ('MKNL', ''))
        self.assertEquals(double_metaphone('McFarland'), ('MKFRLNT', ''))
        self.assertEquals(double_metaphone('McIlroy'), ('MSLR', ''))
        self.assertEquals(double_metaphone('McNair'), ('MKNR', ''))
        self.assertEquals(double_metaphone('McNair-Landry'), ('MKNRLNTR', ''))
        self.assertEquals(double_metaphone('McRaven'), ('MKRFN', ''))
        self.assertEquals(double_metaphone('Mead'), ('MT', ''))
        self.assertEquals(double_metaphone('Meade'), ('MT', ''))
        self.assertEquals(double_metaphone('Meck'), ('MK', ''))
        self.assertEquals(double_metaphone('Melton'), ('MLTN', ''))
        self.assertEquals(double_metaphone('Mendenhall'), ('MNTNL', ''))
        self.assertEquals(double_metaphone('Mering'), ('MRNK', ''))
        self.assertEquals(double_metaphone('Merrick'), ('MRK', ''))
        self.assertEquals(double_metaphone('Merry'), ('MR', ''))
        self.assertEquals(double_metaphone('Mighill'), ('ML', ''))
        self.assertEquals(double_metaphone('Miller'), ('MLR', ''))
        self.assertEquals(double_metaphone('Milton'), ('MLTN', ''))
        self.assertEquals(double_metaphone('Mohun'), ('MHN', ''))
        self.assertEquals(double_metaphone('Montague'), ('MNTK', ''))
        self.assertEquals(double_metaphone('Montboucher'), ('MNTPXR', 'MNTPKR'))
        self.assertEquals(double_metaphone('Moore'), ('MR', ''))
        self.assertEquals(double_metaphone('Morrel'), ('MRL', ''))
        self.assertEquals(double_metaphone('Morrill'), ('MRL', ''))
        self.assertEquals(double_metaphone('Morris'), ('MRS', ''))
        self.assertEquals(double_metaphone('Morton'), ('MRTN', ''))
        self.assertEquals(double_metaphone('Moton'), ('MTN', ''))
        self.assertEquals(double_metaphone('Muir'), ('MR', ''))
        self.assertEquals(double_metaphone('Mulferd'), ('MLFRT', ''))
        self.assertEquals(double_metaphone('Mullins'), ('MLNS', ''))
        self.assertEquals(double_metaphone('Mulso'), ('MLS', ''))
        self.assertEquals(double_metaphone('Munger'), ('MNKR', 'MNJR'))
        self.assertEquals(double_metaphone('Munt'), ('MNT', ''))
        self.assertEquals(double_metaphone('Murchad'), ('MRXT', 'MRKT'))
        self.assertEquals(double_metaphone('Murdock'), ('MRTK', ''))
        self.assertEquals(double_metaphone('Murray'), ('MR', ''))
        self.assertEquals(double_metaphone('Muskett'), ('MSKT', ''))
        self.assertEquals(double_metaphone('Myers'), ('MRS', ''))
        self.assertEquals(double_metaphone('Myrick'), ('MRK', ''))
        self.assertEquals(double_metaphone('NORRIS'), ('NRS', ''))
        self.assertEquals(double_metaphone('Nayle'), ('NL', ''))
        self.assertEquals(double_metaphone('Newcomb'), ('NKMP', ''))
        self.assertEquals(double_metaphone('Newcomb(e)'), ('NKMP', ''))
        self.assertEquals(double_metaphone('Newkirk'), ('NKRK', ''))
        self.assertEquals(double_metaphone('Newton'), ('NTN', ''))
        self.assertEquals(double_metaphone('Niles'), ('NLS', ''))
        self.assertEquals(double_metaphone('Noble'), ('NPL', ''))
        self.assertEquals(double_metaphone('Noel'), ('NL', ''))
        self.assertEquals(double_metaphone('Northend'), ('NR0NT', 'NRTNT'))
        self.assertEquals(double_metaphone('Norton'), ('NRTN', ''))
        self.assertEquals(double_metaphone('Nutter'), ('NTR', ''))
        self.assertEquals(double_metaphone('Odding'), ('ATNK', ''))
        self.assertEquals(double_metaphone('Odenbaugh'), ('ATNP', ''))
        self.assertEquals(double_metaphone('Ogborn'), ('AKPRN', ''))
        self.assertEquals(double_metaphone('Oppenheimer'), ('APNMR', ''))
        self.assertEquals(double_metaphone('Otis'), ('ATS', ''))
        self.assertEquals(double_metaphone('Oviatt'), ('AFT', ''))
        self.assertEquals(double_metaphone('PRUST?'), ('PRST', ''))
        self.assertEquals(double_metaphone('Paddock'), ('PTK', ''))
        self.assertEquals(double_metaphone('Page'), ('PJ', 'PK'))
        self.assertEquals(double_metaphone('Paine'), ('PN', ''))
        self.assertEquals(double_metaphone('Paist'), ('PST', ''))
        self.assertEquals(double_metaphone('Palmer'), ('PLMR', ''))
        self.assertEquals(double_metaphone('Park'), ('PRK', ''))
        self.assertEquals(double_metaphone('Parker'), ('PRKR', ''))
        self.assertEquals(double_metaphone('Parkhurst'), ('PRKRST', ''))
        self.assertEquals(double_metaphone('Parrat'), ('PRT', ''))
        self.assertEquals(double_metaphone('Parsons'), ('PRSNS', ''))
        self.assertEquals(double_metaphone('Partridge'), ('PRTRJ', ''))
        self.assertEquals(double_metaphone('Pashley'), ('PXL', ''))
        self.assertEquals(double_metaphone('Pasley'), ('PSL', ''))
        self.assertEquals(double_metaphone('Patrick'), ('PTRK', ''))
        self.assertEquals(double_metaphone('Pattee'), ('PT', ''))
        self.assertEquals(double_metaphone('Patten'), ('PTN', ''))
        self.assertEquals(double_metaphone('Pawley'), ('PL', ''))
        self.assertEquals(double_metaphone('Payne'), ('PN', ''))
        self.assertEquals(double_metaphone('Peabody'), ('PPT', ''))
        self.assertEquals(double_metaphone('Peake'), ('PK', ''))
        self.assertEquals(double_metaphone('Pearson'), ('PRSN', ''))
        self.assertEquals(double_metaphone('Peat'), ('PT', ''))
        self.assertEquals(double_metaphone('Pedersen'), ('PTRSN', ''))
        self.assertEquals(double_metaphone('Percy'), ('PRS', ''))
        self.assertEquals(double_metaphone('Perkins'), ('PRKNS', ''))
        self.assertEquals(double_metaphone('Perrine'), ('PRN', ''))
        self.assertEquals(double_metaphone('Perry'), ('PR', ''))
        self.assertEquals(double_metaphone('Peson'), ('PSN', ''))
        self.assertEquals(double_metaphone('Peterson'), ('PTRSN', ''))
        self.assertEquals(double_metaphone('Peyton'), ('PTN', ''))
        self.assertEquals(double_metaphone('Phinney'), ('FN', ''))
        self.assertEquals(double_metaphone('Pickard'), ('PKRT', ''))
        self.assertEquals(double_metaphone('Pierce'), ('PRS', ''))
        self.assertEquals(double_metaphone('Pierrepont'), ('PRPNT', ''))
        self.assertEquals(double_metaphone('Pike'), ('PK', ''))
        self.assertEquals(double_metaphone('Pinkham'), ('PNKM', ''))
        self.assertEquals(double_metaphone('Pitman'), ('PTMN', ''))
        self.assertEquals(double_metaphone('Pitt'), ('PT', ''))
        self.assertEquals(double_metaphone('Pitts'), ('PTS', ''))
        self.assertEquals(double_metaphone('Plantagenet'),
                          ('PLNTJNT', 'PLNTKNT'))
        self.assertEquals(double_metaphone('Platt'), ('PLT', ''))
        self.assertEquals(double_metaphone('Platts'), ('PLTS', ''))
        self.assertEquals(double_metaphone('Pleis'), ('PLS', ''))
        self.assertEquals(double_metaphone('Pleiss'), ('PLS', ''))
        self.assertEquals(double_metaphone('Plisko'), ('PLSK', ''))
        self.assertEquals(double_metaphone('Pliskovitch'), ('PLSKFX', ''))
        self.assertEquals(double_metaphone('Plum'), ('PLM', ''))
        self.assertEquals(double_metaphone('Plume'), ('PLM', ''))
        self.assertEquals(double_metaphone('Poitou'), ('PT', ''))
        self.assertEquals(double_metaphone('Pomeroy'), ('PMR', ''))
        self.assertEquals(double_metaphone('Poretiers'), ('PRTRS', ''))
        self.assertEquals(double_metaphone('Pote'), ('PT', ''))
        self.assertEquals(double_metaphone('Potter'), ('PTR', ''))
        self.assertEquals(double_metaphone('Potts'), ('PTS', ''))
        self.assertEquals(double_metaphone('Powell'), ('PL', ''))
        self.assertEquals(double_metaphone('Pratt'), ('PRT', ''))
        self.assertEquals(double_metaphone('Presbury'), ('PRSPR', ''))
        self.assertEquals(double_metaphone('Priest'), ('PRST', ''))
        self.assertEquals(double_metaphone('Prindle'), ('PRNTL', ''))
        self.assertEquals(double_metaphone('Prior'), ('PRR', ''))
        self.assertEquals(double_metaphone('Profumo'), ('PRFM', ''))
        self.assertEquals(double_metaphone('Purdy'), ('PRT', ''))
        self.assertEquals(double_metaphone('Purefoy'), ('PRF', ''))
        self.assertEquals(double_metaphone('Pury'), ('PR', ''))
        self.assertEquals(double_metaphone('Quinter'), ('KNTR', ''))
        self.assertEquals(double_metaphone('Rachel'), ('RXL', 'RKL'))
        self.assertEquals(double_metaphone('Rand'), ('RNT', ''))
        self.assertEquals(double_metaphone('Rankin'), ('RNKN', ''))
        self.assertEquals(double_metaphone('Ravenscroft'), ('RFNSKFT', ''))
        self.assertEquals(double_metaphone('Raynsford'), ('RNSFRT', ''))
        self.assertEquals(double_metaphone('Reakirt'), ('RKRT', ''))
        self.assertEquals(double_metaphone('Reaves'), ('RFS', ''))
        self.assertEquals(double_metaphone('Reeves'), ('RFS', ''))
        self.assertEquals(double_metaphone('Reichert'), ('RXRT', 'RKRT'))
        self.assertEquals(double_metaphone('Remmele'), ('RML', ''))
        self.assertEquals(double_metaphone('Reynolds'), ('RNLTS', ''))
        self.assertEquals(double_metaphone('Rhodes'), ('RTS', ''))
        self.assertEquals(double_metaphone('Richards'), ('RXRTS', 'RKRTS'))
        self.assertEquals(double_metaphone('Richardson'), ('RXRTSN', 'RKRTSN'))
        self.assertEquals(double_metaphone('Ring'), ('RNK', ''))
        self.assertEquals(double_metaphone('Roberts'), ('RPRTS', ''))
        self.assertEquals(double_metaphone('Robertson'), ('RPRTSN', ''))
        self.assertEquals(double_metaphone('Robson'), ('RPSN', ''))
        self.assertEquals(double_metaphone('Rodie'), ('RT', ''))
        self.assertEquals(double_metaphone('Rody'), ('RT', ''))
        self.assertEquals(double_metaphone('Rogers'), ('RKRS', 'RJRS'))
        self.assertEquals(double_metaphone('Ross'), ('RS', ''))
        self.assertEquals(double_metaphone('Rosslevin'), ('RSLFN', ''))
        self.assertEquals(double_metaphone('Rowland'), ('RLNT', ''))
        self.assertEquals(double_metaphone('Ruehl'), ('RL', ''))
        self.assertEquals(double_metaphone('Russell'), ('RSL', ''))
        self.assertEquals(double_metaphone('Ruth'), ('R0', 'RT'))
        self.assertEquals(double_metaphone('Ryan'), ('RN', ''))
        self.assertEquals(double_metaphone('Rysse'), ('RS', ''))
        self.assertEquals(double_metaphone('Sadler'), ('STLR', ''))
        self.assertEquals(double_metaphone('Salmon'), ('SLMN', ''))
        self.assertEquals(double_metaphone('Salter'), ('SLTR', ''))
        self.assertEquals(double_metaphone('Salvatore'), ('SLFTR', ''))
        self.assertEquals(double_metaphone('Sanders'), ('SNTRS', ''))
        self.assertEquals(double_metaphone('Sands'), ('SNTS', ''))
        self.assertEquals(double_metaphone('Sanford'), ('SNFRT', ''))
        self.assertEquals(double_metaphone('Sanger'), ('SNKR', 'SNJR'))
        self.assertEquals(double_metaphone('Sargent'), ('SRJNT', 'SRKNT'))
        self.assertEquals(double_metaphone('Saunders'), ('SNTRS', ''))
        self.assertEquals(double_metaphone('Schilling'), ('XLNK', ''))
        self.assertEquals(double_metaphone('Schlegel'), ('XLKL', 'SLKL'))
        self.assertEquals(double_metaphone('Scott'), ('SKT', ''))
        self.assertEquals(double_metaphone('Sears'), ('SRS', ''))
        self.assertEquals(double_metaphone('Segersall'), ('SJRSL', 'SKRSL'))
        self.assertEquals(double_metaphone('Senecal'), ('SNKL', ''))
        self.assertEquals(double_metaphone('Sergeaux'), ('SRJ', 'SRK'))
        self.assertEquals(double_metaphone('Severance'), ('SFRNS', ''))
        self.assertEquals(double_metaphone('Sharp'), ('XRP', ''))
        self.assertEquals(double_metaphone('Sharpe'), ('XRP', ''))
        self.assertEquals(double_metaphone('Sharply'), ('XRPL', ''))
        self.assertEquals(double_metaphone('Shatswell'), ('XTSL', ''))
        self.assertEquals(double_metaphone('Shattack'), ('XTK', ''))
        self.assertEquals(double_metaphone('Shattock'), ('XTK', ''))
        self.assertEquals(double_metaphone('Shattuck'), ('XTK', ''))
        self.assertEquals(double_metaphone('Shaw'), ('X', 'XF'))
        self.assertEquals(double_metaphone('Sheldon'), ('XLTN', ''))
        self.assertEquals(double_metaphone('Sherman'), ('XRMN', ''))
        self.assertEquals(double_metaphone('Shinn'), ('XN', ''))
        self.assertEquals(double_metaphone('Shirford'), ('XRFRT', ''))
        self.assertEquals(double_metaphone('Shirley'), ('XRL', ''))
        self.assertEquals(double_metaphone('Shively'), ('XFL', ''))
        self.assertEquals(double_metaphone('Shoemaker'), ('XMKR', ''))
        self.assertEquals(double_metaphone('Short'), ('XRT', ''))
        self.assertEquals(double_metaphone('Shotwell'), ('XTL', ''))
        self.assertEquals(double_metaphone('Shute'), ('XT', ''))
        self.assertEquals(double_metaphone('Sibley'), ('SPL', ''))
        self.assertEquals(double_metaphone('Silver'), ('SLFR', ''))
        self.assertEquals(double_metaphone('Simes'), ('SMS', ''))
        self.assertEquals(double_metaphone('Sinken'), ('SNKN', ''))
        self.assertEquals(double_metaphone('Sinn'), ('SN', ''))
        self.assertEquals(double_metaphone('Skelton'), ('SKLTN', ''))
        self.assertEquals(double_metaphone('Skiffe'), ('SKF', ''))
        self.assertEquals(double_metaphone('Skotkonung'), ('SKTKNNK', ''))
        self.assertEquals(double_metaphone('Slade'), ('SLT', 'XLT'))
        self.assertEquals(double_metaphone('Slye'), ('SL', 'XL'))
        self.assertEquals(double_metaphone('Smedley'), ('SMTL', 'XMTL'))
        self.assertEquals(double_metaphone('Smith'), ('SM0', 'XMT'))
        self.assertEquals(double_metaphone('Snow'), ('SN', 'XNF'))
        self.assertEquals(double_metaphone('Soole'), ('SL', ''))
        self.assertEquals(double_metaphone('Soule'), ('SL', ''))
        self.assertEquals(double_metaphone('Southworth'), ('S0R0', 'STRT'))
        self.assertEquals(double_metaphone('Sowles'), ('SLS', ''))
        self.assertEquals(double_metaphone('Spalding'), ('SPLTNK', ''))
        self.assertEquals(double_metaphone('Spark'), ('SPRK', ''))
        self.assertEquals(double_metaphone('Spencer'), ('SPNSR', ''))
        self.assertEquals(double_metaphone('Sperry'), ('SPR', ''))
        self.assertEquals(double_metaphone('Spofford'), ('SPFRT', ''))
        self.assertEquals(double_metaphone('Spooner'), ('SPNR', ''))
        self.assertEquals(double_metaphone('Sprague'), ('SPRK', ''))
        self.assertEquals(double_metaphone('Springer'), ('SPRNKR', 'SPRNJR'))
        self.assertEquals(double_metaphone('St. Clair'), ('STKLR', ''))
        self.assertEquals(double_metaphone('St. Claire'), ('STKLR', ''))
        self.assertEquals(double_metaphone('St. Leger'), ('STLJR', 'STLKR'))
        self.assertEquals(double_metaphone('St. Omer'), ('STMR', ''))
        self.assertEquals(double_metaphone('Stafferton'), ('STFRTN', ''))
        self.assertEquals(double_metaphone('Stafford'), ('STFRT', ''))
        self.assertEquals(double_metaphone('Stalham'), ('STLM', ''))
        self.assertEquals(double_metaphone('Stanford'), ('STNFRT', ''))
        self.assertEquals(double_metaphone('Stanton'), ('STNTN', ''))
        self.assertEquals(double_metaphone('Star'), ('STR', ''))
        self.assertEquals(double_metaphone('Starbuck'), ('STRPK', ''))
        self.assertEquals(double_metaphone('Starkey'), ('STRK', ''))
        self.assertEquals(double_metaphone('Starkweather'),
                          ('STRK0R', 'STRKTR'))
        self.assertEquals(double_metaphone('Stearns'), ('STRNS', ''))
        self.assertEquals(double_metaphone('Stebbins'), ('STPNS', ''))
        self.assertEquals(double_metaphone('Steele'), ('STL', ''))
        self.assertEquals(double_metaphone('Stephenson'), ('STFNSN', ''))
        self.assertEquals(double_metaphone('Stevens'), ('STFNS', ''))
        self.assertEquals(double_metaphone('Stoddard'), ('STTRT', ''))
        self.assertEquals(double_metaphone('Stodder'), ('STTR', ''))
        self.assertEquals(double_metaphone('Stone'), ('STN', ''))
        self.assertEquals(double_metaphone('Storey'), ('STR', ''))
        self.assertEquals(double_metaphone('Storrada'), ('STRT', ''))
        self.assertEquals(double_metaphone('Story'), ('STR', ''))
        self.assertEquals(double_metaphone('Stoughton'), ('STFTN', ''))
        self.assertEquals(double_metaphone('Stout'), ('STT', ''))
        self.assertEquals(double_metaphone('Stow'), ('ST', 'STF'))
        self.assertEquals(double_metaphone('Strong'), ('STRNK', ''))
        self.assertEquals(double_metaphone('Strutt'), ('STRT', ''))
        self.assertEquals(double_metaphone('Stryker'), ('STRKR', ''))
        self.assertEquals(double_metaphone('Stuckeley'), ('STKL', ''))
        self.assertEquals(double_metaphone('Sturges'), ('STRJS', 'STRKS'))
        self.assertEquals(double_metaphone('Sturgess'), ('STRJS', 'STRKS'))
        self.assertEquals(double_metaphone('Sturgis'), ('STRJS', 'STRKS'))
        self.assertEquals(double_metaphone('Suevain'), ('SFN', ''))
        self.assertEquals(double_metaphone('Sulyard'), ('SLRT', ''))
        self.assertEquals(double_metaphone('Sutton'), ('STN', ''))
        self.assertEquals(double_metaphone('Swain'), ('SN', 'XN'))
        self.assertEquals(double_metaphone('Swayne'), ('SN', 'XN'))
        self.assertEquals(double_metaphone('Swayze'), ('SS', 'XTS'))
        self.assertEquals(double_metaphone('Swift'), ('SFT', 'XFT'))
        self.assertEquals(double_metaphone('Taber'), ('TPR', ''))
        self.assertEquals(double_metaphone('Talcott'), ('TLKT', ''))
        self.assertEquals(double_metaphone('Tarne'), ('TRN', ''))
        self.assertEquals(double_metaphone('Tatum'), ('TTM', ''))
        self.assertEquals(double_metaphone('Taverner'), ('TFRNR', ''))
        self.assertEquals(double_metaphone('Taylor'), ('TLR', ''))
        self.assertEquals(double_metaphone('Tenney'), ('TN', ''))
        self.assertEquals(double_metaphone('Thayer'), ('0R', 'TR'))
        self.assertEquals(double_metaphone('Thember'), ('0MPR', 'TMPR'))
        self.assertEquals(double_metaphone('Thomas'), ('TMS', ''))
        self.assertEquals(double_metaphone('Thompson'), ('TMPSN', ''))
        self.assertEquals(double_metaphone('Thorne'), ('0RN', 'TRN'))
        self.assertEquals(double_metaphone('Thornycraft'),
                          ('0RNKRFT', 'TRNKRFT'))
        self.assertEquals(double_metaphone('Threlkeld'), ('0RLKLT', 'TRLKLT'))
        self.assertEquals(double_metaphone('Throckmorton'),
                          ('0RKMRTN', 'TRKMRTN'))
        self.assertEquals(double_metaphone('Thwaits'), ('0TS', 'TTS'))
        self.assertEquals(double_metaphone('Tibbetts'), ('TPTS', ''))
        self.assertEquals(double_metaphone('Tidd'), ('TT', ''))
        self.assertEquals(double_metaphone('Tierney'), ('TRN', ''))
        self.assertEquals(double_metaphone('Tilley'), ('TL', ''))
        self.assertEquals(double_metaphone('Tillieres'), ('TLRS', ''))
        self.assertEquals(double_metaphone('Tilly'), ('TL', ''))
        self.assertEquals(double_metaphone('Tisdale'), ('TSTL', ''))
        self.assertEquals(double_metaphone('Titus'), ('TTS', ''))
        self.assertEquals(double_metaphone('Tobey'), ('TP', ''))
        self.assertEquals(double_metaphone('Tooker'), ('TKR', ''))
        self.assertEquals(double_metaphone('Towle'), ('TL', ''))
        self.assertEquals(double_metaphone('Towne'), ('TN', ''))
        self.assertEquals(double_metaphone('Townsend'), ('TNSNT', ''))
        self.assertEquals(double_metaphone('Treadway'), ('TRT', ''))
        self.assertEquals(double_metaphone('Trelawney'), ('TRLN', ''))
        self.assertEquals(double_metaphone('Trinder'), ('TRNTR', ''))
        self.assertEquals(double_metaphone('Tripp'), ('TRP', ''))
        self.assertEquals(double_metaphone('Trippe'), ('TRP', ''))
        self.assertEquals(double_metaphone('Trott'), ('TRT', ''))
        self.assertEquals(double_metaphone('True'), ('TR', ''))
        self.assertEquals(double_metaphone('Trussebut'), ('TRSPT', ''))
        self.assertEquals(double_metaphone('Tucker'), ('TKR', ''))
        self.assertEquals(double_metaphone('Turgeon'), ('TRJN', 'TRKN'))
        self.assertEquals(double_metaphone('Turner'), ('TRNR', ''))
        self.assertEquals(double_metaphone('Tuttle'), ('TTL', ''))
        self.assertEquals(double_metaphone('Tyler'), ('TLR', ''))
        self.assertEquals(double_metaphone('Tylle'), ('TL', ''))
        self.assertEquals(double_metaphone('Tyrrel'), ('TRL', ''))
        self.assertEquals(double_metaphone('Ua Tuathail'), ('AT0L', 'ATTL'))
        self.assertEquals(double_metaphone('Ulrich'), ('ALRX', 'ALRK'))
        self.assertEquals(double_metaphone('Underhill'), ('ANTRL', ''))
        self.assertEquals(double_metaphone('Underwood'), ('ANTRT', ''))
        self.assertEquals(double_metaphone('Unknown'), ('ANKNN', ''))
        self.assertEquals(double_metaphone('Valentine'), ('FLNTN', ''))
        self.assertEquals(double_metaphone('Van Egmond'), ('FNKMNT', ''))
        self.assertEquals(double_metaphone('Van der Beek'), ('FNTRPK', ''))
        self.assertEquals(double_metaphone('Vaughan'), ('FKN', ''))
        self.assertEquals(double_metaphone('Vermenlen'), ('FRMNLN', ''))
        self.assertEquals(double_metaphone('Vincent'), ('FNSNT', ''))
        self.assertEquals(double_metaphone('Volentine'), ('FLNTN', ''))
        self.assertEquals(double_metaphone('Wagner'), ('AKNR', 'FKNR'))
        self.assertEquals(double_metaphone('Waite'), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Walker'), ('ALKR', 'FLKR'))
        self.assertEquals(double_metaphone('Walter'), ('ALTR', 'FLTR'))
        self.assertEquals(double_metaphone('Wandell'), ('ANTL', 'FNTL'))
        self.assertEquals(double_metaphone('Wandesford'),
                          ('ANTSFRT', 'FNTSFRT'))
        self.assertEquals(double_metaphone('Warbleton'), ('ARPLTN', 'FRPLTN'))
        self.assertEquals(double_metaphone('Ward'), ('ART', 'FRT'))
        self.assertEquals(double_metaphone('Warde'), ('ART', 'FRT'))
        self.assertEquals(double_metaphone('Ware'), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wareham'), ('ARHM', 'FRHM'))
        self.assertEquals(double_metaphone('Warner'), ('ARNR', 'FRNR'))
        self.assertEquals(double_metaphone('Warren'), ('ARN', 'FRN'))
        self.assertEquals(double_metaphone('Washburne'), ('AXPRN', 'FXPRN'))
        self.assertEquals(double_metaphone('Waterbury'), ('ATRPR', 'FTRPR'))
        self.assertEquals(double_metaphone('Watson'), ('ATSN', 'FTSN'))
        self.assertEquals(double_metaphone('WatsonEllithorpe'),
                          ('ATSNL0RP', 'FTSNLTRP'))
        self.assertEquals(double_metaphone('Watts'), ('ATS', 'FTS'))
        self.assertEquals(double_metaphone('Wayne'), ('AN', 'FN'))
        self.assertEquals(double_metaphone('Webb'), ('AP', 'FP'))
        self.assertEquals(double_metaphone('Weber'), ('APR', 'FPR'))
        self.assertEquals(double_metaphone('Webster'), ('APSTR', 'FPSTR'))
        self.assertEquals(double_metaphone('Weed'), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Weeks'), ('AKS', 'FKS'))
        self.assertEquals(double_metaphone('Wells'), ('ALS', 'FLS'))
        self.assertEquals(double_metaphone('Wenzell'), ('ANSL', 'FNTSL'))
        self.assertEquals(double_metaphone('West'), ('AST', 'FST'))
        self.assertEquals(double_metaphone('Westbury'), ('ASTPR', 'FSTPR'))
        self.assertEquals(double_metaphone('Whatlocke'), ('ATLK', ''))
        self.assertEquals(double_metaphone('Wheeler'), ('ALR', ''))
        self.assertEquals(double_metaphone('Whiston'), ('ASTN', ''))
        self.assertEquals(double_metaphone('White'), ('AT', ''))
        self.assertEquals(double_metaphone('Whitman'), ('ATMN', ''))
        self.assertEquals(double_metaphone('Whiton'), ('ATN', ''))
        self.assertEquals(double_metaphone('Whitson'), ('ATSN', ''))
        self.assertEquals(double_metaphone('Wickes'), ('AKS', 'FKS'))
        self.assertEquals(double_metaphone('Wilbur'), ('ALPR', 'FLPR'))
        self.assertEquals(double_metaphone('Wilcotes'), ('ALKTS', 'FLKTS'))
        self.assertEquals(double_metaphone('Wilkinson'), ('ALKNSN', 'FLKNSN'))
        self.assertEquals(double_metaphone('Willets'), ('ALTS', 'FLTS'))
        self.assertEquals(double_metaphone('Willett'), ('ALT', 'FLT'))
        self.assertEquals(double_metaphone('Willey'), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Williams'), ('ALMS', 'FLMS'))
        self.assertEquals(double_metaphone('Williston'), ('ALSTN', 'FLSTN'))
        self.assertEquals(double_metaphone('Wilson'), ('ALSN', 'FLSN'))
        self.assertEquals(double_metaphone('Wimes'), ('AMS', 'FMS'))
        self.assertEquals(double_metaphone('Winch'), ('ANX', 'FNK'))
        self.assertEquals(double_metaphone('Winegar'), ('ANKR', 'FNKR'))
        self.assertEquals(double_metaphone('Wing'), ('ANK', 'FNK'))
        self.assertEquals(double_metaphone('Winsley'), ('ANSL', 'FNSL'))
        self.assertEquals(double_metaphone('Winslow'), ('ANSL', 'FNSLF'))
        self.assertEquals(double_metaphone('Winthrop'), ('AN0RP', 'FNTRP'))
        self.assertEquals(double_metaphone('Wise'), ('AS', 'FS'))
        self.assertEquals(double_metaphone('Wood'), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Woodbridge'), ('ATPRJ', 'FTPRJ'))
        self.assertEquals(double_metaphone('Woodward'), ('ATRT', 'FTRT'))
        self.assertEquals(double_metaphone('Wooley'), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Woolley'), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Worth'), ('AR0', 'FRT'))
        self.assertEquals(double_metaphone('Worthen'), ('AR0N', 'FRTN'))
        self.assertEquals(double_metaphone('Worthley'), ('AR0L', 'FRTL'))
        self.assertEquals(double_metaphone('Wright'), ('RT', ''))
        self.assertEquals(double_metaphone('Wyer'), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wyere'), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wynkoop'), ('ANKP', 'FNKP'))
        self.assertEquals(double_metaphone('Yarnall'), ('ARNL', ''))
        self.assertEquals(double_metaphone('Yeoman'), ('AMN', ''))
        self.assertEquals(double_metaphone('Yorke'), ('ARK', ''))
        self.assertEquals(double_metaphone('Young'), ('ANK', ''))
        self.assertEquals(double_metaphone('ab Wennonwen'), ('APNNN', ''))
        self.assertEquals(double_metaphone('ap Llewellyn'), ('APLLN', ''))
        self.assertEquals(double_metaphone('ap Lorwerth'), ('APLRR0', 'APLRRT'))
        self.assertEquals(double_metaphone('d\'Angouleme'), ('TNKLM', ''))
        self.assertEquals(double_metaphone('de Audeham'), ('TTHM', ''))
        self.assertEquals(double_metaphone('de Bavant'), ('TPFNT', ''))
        self.assertEquals(double_metaphone('de Beauchamp'), ('TPXMP', 'TPKMP'))
        self.assertEquals(double_metaphone('de Beaumont'), ('TPMNT', ''))
        self.assertEquals(double_metaphone('de Bolbec'), ('TPLPK', ''))
        self.assertEquals(double_metaphone('de Braiose'), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Braose'), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Briwere'), ('TPRR', ''))
        self.assertEquals(double_metaphone('de Cantelou'), ('TKNTL', ''))
        self.assertEquals(double_metaphone('de Cherelton'),
                          ('TXRLTN', 'TKRLTN'))
        self.assertEquals(double_metaphone('de Cherleton'),
                          ('TXRLTN', 'TKRLTN'))
        self.assertEquals(double_metaphone('de Clare'), ('TKLR', ''))
        self.assertEquals(double_metaphone('de Claremont'), ('TKLRMNT', ''))
        self.assertEquals(double_metaphone('de Clifford'), ('TKLFRT', ''))
        self.assertEquals(double_metaphone('de Colville'), ('TKLFL', ''))
        self.assertEquals(double_metaphone('de Courtenay'), ('TKRTN', ''))
        self.assertEquals(double_metaphone('de Fauconberg'), ('TFKNPRK', ''))
        self.assertEquals(double_metaphone('de Forest'), ('TFRST', ''))
        self.assertEquals(double_metaphone('de Gai'), ('TK', ''))
        self.assertEquals(double_metaphone('de Grey'), ('TKR', ''))
        self.assertEquals(double_metaphone('de Guernons'), ('TKRNNS', ''))
        self.assertEquals(double_metaphone('de Haia'), ('T', ''))
        self.assertEquals(double_metaphone('de Harcourt'), ('TRKRT', ''))
        self.assertEquals(double_metaphone('de Hastings'), ('TSTNKS', ''))
        self.assertEquals(double_metaphone('de Hoke'), ('TK', ''))
        self.assertEquals(double_metaphone('de Hooch'), ('TK', ''))
        self.assertEquals(double_metaphone('de Hugelville'), ('TJLFL', 'TKLFL'))
        self.assertEquals(double_metaphone('de Huntingdon'), ('TNTNKTN', ''))
        self.assertEquals(double_metaphone('de Insula'), ('TNSL', ''))
        self.assertEquals(double_metaphone('de Keynes'), ('TKNS', ''))
        self.assertEquals(double_metaphone('de Lacy'), ('TLS', ''))
        self.assertEquals(double_metaphone('de Lexington'), ('TLKSNKTN', ''))
        self.assertEquals(double_metaphone('de Lusignan'), ('TLSNN', 'TLSKNN'))
        self.assertEquals(double_metaphone('de Manvers'), ('TMNFRS', ''))
        self.assertEquals(double_metaphone('de Montagu'), ('TMNTK', ''))
        self.assertEquals(double_metaphone('de Montault'), ('TMNTLT', ''))
        self.assertEquals(double_metaphone('de Montfort'), ('TMNTFRT', ''))
        self.assertEquals(double_metaphone('de Mortimer'), ('TMRTMR', ''))
        self.assertEquals(double_metaphone('de Morville'), ('TMRFL', ''))
        self.assertEquals(double_metaphone('de Morvois'), ('TMRF', 'TMRFS'))
        self.assertEquals(double_metaphone('de Neufmarche'),
                          ('TNFMRX', 'TNFMRK'))
        self.assertEquals(double_metaphone('de Odingsells'), ('TTNKSLS', ''))
        self.assertEquals(double_metaphone('de Odyngsells'), ('TTNKSLS', ''))
        self.assertEquals(double_metaphone('de Percy'), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Pierrepont'), ('TPRPNT', ''))
        self.assertEquals(double_metaphone('de Plessetis'), ('TPLSTS', ''))
        self.assertEquals(double_metaphone('de Porhoet'), ('TPRT', ''))
        self.assertEquals(double_metaphone('de Prouz'), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Quincy'), ('TKNS', ''))
        self.assertEquals(double_metaphone('de Ripellis'), ('TRPLS', ''))
        self.assertEquals(double_metaphone('de Ros'), ('TRS', ''))
        self.assertEquals(double_metaphone('de Salisbury'), ('TSLSPR', ''))
        self.assertEquals(double_metaphone('de Sanford'), ('TSNFRT', ''))
        self.assertEquals(double_metaphone('de Somery'), ('TSMR', ''))
        self.assertEquals(double_metaphone('de St. Hilary'), ('TSTLR', ''))
        self.assertEquals(double_metaphone('de St. Liz'), ('TSTLS', ''))
        self.assertEquals(double_metaphone('de Sutton'), ('TSTN', ''))
        self.assertEquals(double_metaphone('de Toeni'), ('TTN', ''))
        self.assertEquals(double_metaphone('de Tony'), ('TTN', ''))
        self.assertEquals(double_metaphone('de Umfreville'), ('TMFRFL', ''))
        self.assertEquals(double_metaphone('de Valognes'), ('TFLNS', 'TFLKNS'))
        self.assertEquals(double_metaphone('de Vaux'), ('TF', ''))
        self.assertEquals(double_metaphone('de Vere'), ('TFR', ''))
        self.assertEquals(double_metaphone('de Vermandois'),
                          ('TFRMNT', 'TFRMNTS'))
        self.assertEquals(double_metaphone('de Vernon'), ('TFRNN', ''))
        self.assertEquals(double_metaphone('de Vexin'), ('TFKSN', ''))
        self.assertEquals(double_metaphone('de Vitre'), ('TFTR', ''))
        self.assertEquals(double_metaphone('de Wandesford'), ('TNTSFRT', ''))
        self.assertEquals(double_metaphone('de Warenne'), ('TRN', ''))
        self.assertEquals(double_metaphone('de Westbury'), ('TSTPR', ''))
        self.assertEquals(double_metaphone('di Saluzzo'), ('TSLS', 'TSLTS'))
        self.assertEquals(double_metaphone('fitz Alan'), ('FTSLN', ''))
        self.assertEquals(double_metaphone('fitz Geoffrey'),
                          ('FTSJFR', 'FTSKFR'))
        self.assertEquals(double_metaphone('fitz Herbert'), ('FTSRPRT', ''))
        self.assertEquals(double_metaphone('fitz John'), ('FTSJN', ''))
        self.assertEquals(double_metaphone('fitz Patrick'), ('FTSPTRK', ''))
        self.assertEquals(double_metaphone('fitz Payn'), ('FTSPN', ''))
        self.assertEquals(double_metaphone('fitz Piers'), ('FTSPRS', ''))
        self.assertEquals(double_metaphone('fitz Randolph'), ('FTSRNTLF', ''))
        self.assertEquals(double_metaphone('fitz Richard'),
                          ('FTSRXRT', 'FTSRKRT'))
        self.assertEquals(double_metaphone('fitz Robert'), ('FTSRPRT', ''))
        self.assertEquals(double_metaphone('fitz Roy'), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Scrob'), ('FTSSKP', ''))
        self.assertEquals(double_metaphone('fitz Walter'), ('FTSLTR', ''))
        self.assertEquals(double_metaphone('fitz Warin'), ('FTSRN', ''))
        self.assertEquals(double_metaphone('fitz Williams'), ('FTSLMS', ''))
        self.assertEquals(double_metaphone('la Zouche'), ('LSX', 'LSK'))
        self.assertEquals(double_metaphone('le Botiller'), ('LPTLR', ''))
        self.assertEquals(double_metaphone('le Despenser'), ('LTSPNSR', ''))
        self.assertEquals(double_metaphone('le deSpencer'), ('LTSPNSR', ''))
        self.assertEquals(double_metaphone('of Allendale'), ('AFLNTL', ''))
        self.assertEquals(double_metaphone('of Angouleme'), ('AFNKLM', ''))
        self.assertEquals(double_metaphone('of Anjou'), ('AFNJ', ''))
        self.assertEquals(double_metaphone('of Aquitaine'), ('AFKTN', ''))
        self.assertEquals(double_metaphone('of Aumale'), ('AFML', ''))
        self.assertEquals(double_metaphone('of Bavaria'), ('AFPFR', ''))
        self.assertEquals(double_metaphone('of Boulogne'), ('AFPLN', 'AFPLKN'))
        self.assertEquals(double_metaphone('of Brittany'), ('AFPRTN', ''))
        self.assertEquals(double_metaphone('of Brittary'), ('AFPRTR', ''))
        self.assertEquals(double_metaphone('of Castile'), ('AFKSTL', ''))
        self.assertEquals(double_metaphone('of Chester'), ('AFXSTR', 'AFKSTR'))
        self.assertEquals(double_metaphone('of Clermont'), ('AFKLRMNT', ''))
        self.assertEquals(double_metaphone('of Cologne'), ('AFKLN', 'AFKLKN'))
        self.assertEquals(double_metaphone('of Dinan'), ('AFTNN', ''))
        self.assertEquals(double_metaphone('of Dunbar'), ('AFTNPR', ''))
        self.assertEquals(double_metaphone('of England'), ('AFNKLNT', ''))
        self.assertEquals(double_metaphone('of Essex'), ('AFSKS', ''))
        self.assertEquals(double_metaphone('of Falaise'), ('AFFLS', ''))
        self.assertEquals(double_metaphone('of Flanders'), ('AFFLNTRS', ''))
        self.assertEquals(double_metaphone('of Galloway'), ('AFKL', ''))
        self.assertEquals(double_metaphone('of Germany'), ('AFKRMN', 'AFJRMN'))
        self.assertEquals(double_metaphone('of Gloucester'), ('AFKLSSTR', ''))
        self.assertEquals(double_metaphone('of Heristal'), ('AFRSTL', ''))
        self.assertEquals(double_metaphone('of Hungary'), ('AFNKR', ''))
        self.assertEquals(double_metaphone('of Huntington'), ('AFNTNKTN', ''))
        self.assertEquals(double_metaphone('of Kiev'), ('AFKF', ''))
        self.assertEquals(double_metaphone('of Kuno'), ('AFKN', ''))
        self.assertEquals(double_metaphone('of Landen'), ('AFLNTN', ''))
        self.assertEquals(double_metaphone('of Laon'), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Leinster'), ('AFLNSTR', ''))
        self.assertEquals(double_metaphone('of Lens'), ('AFLNS', ''))
        self.assertEquals(double_metaphone('of Lorraine'), ('AFLRN', ''))
        self.assertEquals(double_metaphone('of Louvain'), ('AFLFN', ''))
        self.assertEquals(double_metaphone('of Mercia'), ('AFMRS', 'AFMRX'))
        self.assertEquals(double_metaphone('of Metz'), ('AFMTS', ''))
        self.assertEquals(double_metaphone('of Meulan'), ('AFMLN', ''))
        self.assertEquals(double_metaphone('of Nass'), ('AFNS', ''))
        self.assertEquals(double_metaphone('of Normandy'), ('AFNRMNT', ''))
        self.assertEquals(double_metaphone('of Ohningen'), ('AFNNJN', 'AFNNKN'))
        self.assertEquals(double_metaphone('of Orleans'), ('AFRLNS', ''))
        self.assertEquals(double_metaphone('of Poitou'), ('AFPT', ''))
        self.assertEquals(double_metaphone('of Polotzk'), ('AFPLTSK', ''))
        self.assertEquals(double_metaphone('of Provence'), ('AFPRFNS', ''))
        self.assertEquals(double_metaphone('of Ringelheim'),
                          ('AFRNJLM', 'AFRNKLM'))
        self.assertEquals(double_metaphone('of Salisbury'), ('AFSLSPR', ''))
        self.assertEquals(double_metaphone('of Saxony'), ('AFSKSN', ''))
        self.assertEquals(double_metaphone('of Scotland'), ('AFSKTLNT', ''))
        self.assertEquals(double_metaphone('of Senlis'), ('AFSNLS', ''))
        self.assertEquals(double_metaphone('of Stafford'), ('AFSTFRT', ''))
        self.assertEquals(double_metaphone('of Swabia'), ('AFSP', ''))
        self.assertEquals(double_metaphone('of Tongres'), ('AFTNKRS', ''))
        self.assertEquals(double_metaphone('of the Tributes'),
                          ('AF0TRPTS', 'AFTTRPTS'))
        self.assertEquals(double_metaphone('unknown'), ('ANKNN', ''))
        self.assertEquals(double_metaphone('van der Gouda'), ('FNTRKT', ''))
        self.assertEquals(double_metaphone('von Adenbaugh'), ('FNTNP', ''))
        self.assertEquals(double_metaphone('ARCHITure'), ('ARKTR', ''))
        self.assertEquals(double_metaphone('Arnoff'), ('ARNF', ''))
        self.assertEquals(double_metaphone('Arnow'), ('ARN', 'ARNF'))
        self.assertEquals(double_metaphone('DANGER'), ('TNJR', 'TNKR'))
        self.assertEquals(double_metaphone('Jankelowicz'), ('JNKLTS', 'ANKLFX'))
        self.assertEquals(double_metaphone('MANGER'), ('MNJR', 'MNKR'))
        self.assertEquals(double_metaphone('McClellan'), ('MKLLN', ''))
        self.assertEquals(double_metaphone('McHugh'), ('MK', ''))
        self.assertEquals(double_metaphone('McLaughlin'), ('MKLFLN', ''))
        self.assertEquals(double_metaphone('ORCHEStra'), ('ARKSTR', ''))
        self.assertEquals(double_metaphone('ORCHID'), ('ARKT', ''))
        self.assertEquals(double_metaphone('Pierce'), ('PRS', ''))
        self.assertEquals(double_metaphone('RANGER'), ('RNJR', 'RNKR'))
        self.assertEquals(double_metaphone('Schlesinger'), ('XLSNKR', 'SLSNJR'))
        self.assertEquals(double_metaphone('Uomo'), ('AM', ''))
        self.assertEquals(double_metaphone('Vasserman'), ('FSRMN', ''))
        self.assertEquals(double_metaphone('Wasserman'), ('ASRMN', 'FSRMN'))
        self.assertEquals(double_metaphone('Womo'), ('AM', 'FM'))
        self.assertEquals(double_metaphone('Yankelovich'), ('ANKLFX', 'ANKLFK'))
        self.assertEquals(double_metaphone('accede'), ('AKST', ''))
        self.assertEquals(double_metaphone('accident'), ('AKSTNT', ''))
        self.assertEquals(double_metaphone('adelsheim'), ('ATLSM', ''))
        self.assertEquals(double_metaphone('aged'), ('AJT', 'AKT'))
        self.assertEquals(double_metaphone('ageless'), ('AJLS', 'AKLS'))
        self.assertEquals(double_metaphone('agency'), ('AJNS', 'AKNS'))
        self.assertEquals(double_metaphone('aghast'), ('AKST', ''))
        self.assertEquals(double_metaphone('agio'), ('AJ', 'AK'))
        self.assertEquals(double_metaphone('agrimony'), ('AKRMN', ''))
        self.assertEquals(double_metaphone('album'), ('ALPM', ''))
        self.assertEquals(double_metaphone('alcmene'), ('ALKMN', ''))
        self.assertEquals(double_metaphone('alehouse'), ('ALHS', ''))
        self.assertEquals(double_metaphone('antique'), ('ANTK', ''))
        self.assertEquals(double_metaphone('artois'), ('ART', 'ARTS'))
        self.assertEquals(double_metaphone('automation'), ('ATMXN', ''))
        self.assertEquals(double_metaphone('bacchus'), ('PKS', ''))
        self.assertEquals(double_metaphone('bacci'), ('PX', ''))
        self.assertEquals(double_metaphone('bajador'), ('PJTR', 'PHTR'))
        self.assertEquals(double_metaphone('bellocchio'), ('PLX', ''))
        self.assertEquals(double_metaphone('bertucci'), ('PRTX', ''))
        self.assertEquals(double_metaphone('biaggi'), ('PJ', 'PK'))
        self.assertEquals(double_metaphone('bough'), ('P', ''))
        self.assertEquals(double_metaphone('breaux'), ('PR', ''))
        self.assertEquals(double_metaphone('broughton'), ('PRTN', ''))
        self.assertEquals(double_metaphone('cabrillo'), ('KPRL', 'KPR'))
        self.assertEquals(double_metaphone('caesar'), ('SSR', ''))
        self.assertEquals(double_metaphone('cagney'), ('KKN', ''))
        self.assertEquals(double_metaphone('campbell'), ('KMPL', ''))
        self.assertEquals(double_metaphone('carlisle'), ('KRLL', ''))
        self.assertEquals(double_metaphone('carlysle'), ('KRLL', ''))
        self.assertEquals(double_metaphone('chemistry'), ('KMSTR', ''))
        self.assertEquals(double_metaphone('chianti'), ('KNT', ''))
        self.assertEquals(double_metaphone('chorus'), ('KRS', ''))
        self.assertEquals(double_metaphone('cough'), ('KF', ''))
        self.assertEquals(double_metaphone('czerny'), ('SRN', 'XRN'))
        self.assertEquals(double_metaphone('deffenbacher'), ('TFNPKR', ''))
        self.assertEquals(double_metaphone('dumb'), ('TM', ''))
        self.assertEquals(double_metaphone('edgar'), ('ATKR', ''))
        self.assertEquals(double_metaphone('edge'), ('AJ', ''))
        self.assertEquals(double_metaphone('filipowicz'), ('FLPTS', 'FLPFX'))
        self.assertEquals(double_metaphone('focaccia'), ('FKX', ''))
        self.assertEquals(double_metaphone('gallegos'), ('KLKS', 'KKS'))
        self.assertEquals(double_metaphone('gambrelli'), ('KMPRL', ''))
        self.assertEquals(double_metaphone('geithain'), ('K0N', 'JTN'))
        self.assertEquals(double_metaphone('ghiradelli'), ('JRTL', ''))
        self.assertEquals(double_metaphone('ghislane'), ('JLN', ''))
        self.assertEquals(double_metaphone('gough'), ('KF', ''))
        self.assertEquals(double_metaphone('hartheim'), ('HR0M', 'HRTM'))
        self.assertEquals(double_metaphone('heimsheim'), ('HMSM', ''))
        self.assertEquals(double_metaphone('hochmeier'), ('HKMR', ''))
        self.assertEquals(double_metaphone('hugh'), ('H', ''))
        self.assertEquals(double_metaphone('hunger'), ('HNKR', 'HNJR'))
        self.assertEquals(double_metaphone('hungry'), ('HNKR', ''))
        self.assertEquals(double_metaphone('island'), ('ALNT', ''))
        self.assertEquals(double_metaphone('isle'), ('AL', ''))
        self.assertEquals(double_metaphone('jose'), ('HS', ''))
        self.assertEquals(double_metaphone('laugh'), ('LF', ''))
        self.assertEquals(double_metaphone('mac caffrey'), ('MKFR', ''))
        self.assertEquals(double_metaphone('mac gregor'), ('MKRKR', ''))
        self.assertEquals(double_metaphone('pegnitz'), ('PNTS', 'PKNTS'))
        self.assertEquals(double_metaphone('piskowitz'), ('PSKTS', 'PSKFX'))
        self.assertEquals(double_metaphone('queen'), ('KN', ''))
        self.assertEquals(double_metaphone('raspberry'), ('RSPR', ''))
        self.assertEquals(double_metaphone('resnais'), ('RSN', 'RSNS'))
        self.assertEquals(double_metaphone('rogier'), ('RJ', 'RJR'))
        self.assertEquals(double_metaphone('rough'), ('RF', ''))
        self.assertEquals(double_metaphone('san jacinto'), ('SNHSNT', ''))
        self.assertEquals(double_metaphone('schenker'), ('XNKR', 'SKNKR'))
        self.assertEquals(double_metaphone('schermerhorn'),
                          ('XRMRRN', 'SKRMRRN'))
        self.assertEquals(double_metaphone('schmidt'), ('XMT', 'SMT'))
        self.assertEquals(double_metaphone('schneider'), ('XNTR', 'SNTR'))
        self.assertEquals(double_metaphone('school'), ('SKL', ''))
        self.assertEquals(double_metaphone('schooner'), ('SKNR', ''))
        self.assertEquals(double_metaphone('schrozberg'), ('XRSPRK', 'SRSPRK'))
        self.assertEquals(double_metaphone('schulman'), ('XLMN', ''))
        self.assertEquals(double_metaphone('schwabach'), ('XPK', 'XFPK'))
        self.assertEquals(double_metaphone('schwarzach'), ('XRSK', 'XFRTSK'))
        self.assertEquals(double_metaphone('smith'), ('SM0', 'XMT'))
        self.assertEquals(double_metaphone('snider'), ('SNTR', 'XNTR'))
        self.assertEquals(double_metaphone('succeed'), ('SKST', ''))
        self.assertEquals(double_metaphone('sugarcane'), ('XKRKN', 'SKRKN'))
        self.assertEquals(double_metaphone('svobodka'), ('SFPTK', ''))
        self.assertEquals(double_metaphone('tagliaro'), ('TKLR', 'TLR'))
        self.assertEquals(double_metaphone('thames'), ('TMS', ''))
        self.assertEquals(double_metaphone('theilheim'), ('0LM', 'TLM'))
        self.assertEquals(double_metaphone('thomas'), ('TMS', ''))
        self.assertEquals(double_metaphone('thumb'), ('0M', 'TM'))
        self.assertEquals(double_metaphone('tichner'), ('TXNR', 'TKNR'))
        self.assertEquals(double_metaphone('tough'), ('TF', ''))
        self.assertEquals(double_metaphone('umbrella'), ('AMPRL', ''))
        self.assertEquals(double_metaphone('vilshofen'), ('FLXFN', ''))
        self.assertEquals(double_metaphone('von schuller'), ('FNXLR', ''))
        self.assertEquals(double_metaphone('wachtler'), ('AKTLR', 'FKTLR'))
        self.assertEquals(double_metaphone('wechsler'), ('AKSLR', 'FKSLR'))
        self.assertEquals(double_metaphone('weikersheim'), ('AKRSM', 'FKRSM'))
        self.assertEquals(double_metaphone('zhao'), ('J', ''))

    def test_double_metaphone_surnames4(self):
        self.assertEquals(double_metaphone('', 4), ('', ''))
        self.assertEquals(double_metaphone('ALLERTON', 4), ('ALRT', ''))
        self.assertEquals(double_metaphone('Acton', 4), ('AKTN', ''))
        self.assertEquals(double_metaphone('Adams', 4), ('ATMS', ''))
        self.assertEquals(double_metaphone('Aggar', 4), ('AKR', ''))
        self.assertEquals(double_metaphone('Ahl', 4), ('AL', ''))
        self.assertEquals(double_metaphone('Aiken', 4), ('AKN', ''))
        self.assertEquals(double_metaphone('Alan', 4), ('ALN', ''))
        self.assertEquals(double_metaphone('Alcock', 4), ('ALKK', ''))
        self.assertEquals(double_metaphone('Alden', 4), ('ALTN', ''))
        self.assertEquals(double_metaphone('Aldham', 4), ('ALTM', ''))
        self.assertEquals(double_metaphone('Allen', 4), ('ALN', ''))
        self.assertEquals(double_metaphone('Allerton', 4), ('ALRT', ''))
        self.assertEquals(double_metaphone('Alsop', 4), ('ALSP', ''))
        self.assertEquals(double_metaphone('Alwein', 4), ('ALN', ''))
        self.assertEquals(double_metaphone('Ambler', 4), ('AMPL', ''))
        self.assertEquals(double_metaphone('Andevill', 4), ('ANTF', ''))
        self.assertEquals(double_metaphone('Andrews', 4), ('ANTR', ''))
        self.assertEquals(double_metaphone('Andreyco', 4), ('ANTR', ''))
        self.assertEquals(double_metaphone('Andriesse', 4), ('ANTR', ''))
        self.assertEquals(double_metaphone('Angier', 4), ('ANJ', 'ANJR'))
        self.assertEquals(double_metaphone('Annabel', 4), ('ANPL', ''))
        self.assertEquals(double_metaphone('Anne', 4), ('AN', ''))
        self.assertEquals(double_metaphone('Anstye', 4), ('ANST', ''))
        self.assertEquals(double_metaphone('Appling', 4), ('APLN', ''))
        self.assertEquals(double_metaphone('Apuke', 4), ('APK', ''))
        self.assertEquals(double_metaphone('Arnold', 4), ('ARNL', ''))
        self.assertEquals(double_metaphone('Ashby', 4), ('AXP', ''))
        self.assertEquals(double_metaphone('Astwood', 4), ('ASTT', ''))
        self.assertEquals(double_metaphone('Atkinson', 4), ('ATKN', ''))
        self.assertEquals(double_metaphone('Audley', 4), ('ATL', ''))
        self.assertEquals(double_metaphone('Austin', 4), ('ASTN', ''))
        self.assertEquals(double_metaphone('Avenal', 4), ('AFNL', ''))
        self.assertEquals(double_metaphone('Ayer', 4), ('AR', ''))
        self.assertEquals(double_metaphone('Ayot', 4), ('AT', ''))
        self.assertEquals(double_metaphone('Babbitt', 4), ('PPT', ''))
        self.assertEquals(double_metaphone('Bachelor', 4), ('PXLR', 'PKLR'))
        self.assertEquals(double_metaphone('Bachelour', 4), ('PXLR', 'PKLR'))
        self.assertEquals(double_metaphone('Bailey', 4), ('PL', ''))
        self.assertEquals(double_metaphone('Baivel', 4), ('PFL', ''))
        self.assertEquals(double_metaphone('Baker', 4), ('PKR', ''))
        self.assertEquals(double_metaphone('Baldwin', 4), ('PLTN', ''))
        self.assertEquals(double_metaphone('Balsley', 4), ('PLSL', ''))
        self.assertEquals(double_metaphone('Barber', 4), ('PRPR', ''))
        self.assertEquals(double_metaphone('Barker', 4), ('PRKR', ''))
        self.assertEquals(double_metaphone('Barlow', 4), ('PRL', 'PRLF'))
        self.assertEquals(double_metaphone('Barnard', 4), ('PRNR', ''))
        self.assertEquals(double_metaphone('Barnes', 4), ('PRNS', ''))
        self.assertEquals(double_metaphone('Barnsley', 4), ('PRNS', ''))
        self.assertEquals(double_metaphone('Barouxis', 4), ('PRKS', ''))
        self.assertEquals(double_metaphone('Bartlet', 4), ('PRTL', ''))
        self.assertEquals(double_metaphone('Basley', 4), ('PSL', ''))
        self.assertEquals(double_metaphone('Basset', 4), ('PST', ''))
        self.assertEquals(double_metaphone('Bassett', 4), ('PST', ''))
        self.assertEquals(double_metaphone('Batchlor', 4), ('PXLR', ''))
        self.assertEquals(double_metaphone('Bates', 4), ('PTS', ''))
        self.assertEquals(double_metaphone('Batson', 4), ('PTSN', ''))
        self.assertEquals(double_metaphone('Bayes', 4), ('PS', ''))
        self.assertEquals(double_metaphone('Bayley', 4), ('PL', ''))
        self.assertEquals(double_metaphone('Beale', 4), ('PL', ''))
        self.assertEquals(double_metaphone('Beauchamp', 4), ('PXMP', 'PKMP'))
        self.assertEquals(double_metaphone('Beauclerc', 4), ('PKLR', ''))
        self.assertEquals(double_metaphone('Beech', 4), ('PK', ''))
        self.assertEquals(double_metaphone('Beers', 4), ('PRS', ''))
        self.assertEquals(double_metaphone('Beke', 4), ('PK', ''))
        self.assertEquals(double_metaphone('Belcher', 4), ('PLXR', 'PLKR'))
        self.assertEquals(double_metaphone('Benjamin', 4), ('PNJM', ''))
        self.assertEquals(double_metaphone('Benningham', 4), ('PNNK', ''))
        self.assertEquals(double_metaphone('Bereford', 4), ('PRFR', ''))
        self.assertEquals(double_metaphone('Bergen', 4), ('PRJN', 'PRKN'))
        self.assertEquals(double_metaphone('Berkeley', 4), ('PRKL', ''))
        self.assertEquals(double_metaphone('Berry', 4), ('PR', ''))
        self.assertEquals(double_metaphone('Besse', 4), ('PS', ''))
        self.assertEquals(double_metaphone('Bessey', 4), ('PS', ''))
        self.assertEquals(double_metaphone('Bessiles', 4), ('PSLS', ''))
        self.assertEquals(double_metaphone('Bigelow', 4), ('PJL', 'PKLF'))
        self.assertEquals(double_metaphone('Bigg', 4), ('PK', ''))
        self.assertEquals(double_metaphone('Bigod', 4), ('PKT', ''))
        self.assertEquals(double_metaphone('Billings', 4), ('PLNK', ''))
        self.assertEquals(double_metaphone('Bimper', 4), ('PMPR', ''))
        self.assertEquals(double_metaphone('Binker', 4), ('PNKR', ''))
        self.assertEquals(double_metaphone('Birdsill', 4), ('PRTS', ''))
        self.assertEquals(double_metaphone('Bishop', 4), ('PXP', ''))
        self.assertEquals(double_metaphone('Black', 4), ('PLK', ''))
        self.assertEquals(double_metaphone('Blagge', 4), ('PLK', ''))
        self.assertEquals(double_metaphone('Blake', 4), ('PLK', ''))
        self.assertEquals(double_metaphone('Blanck', 4), ('PLNK', ''))
        self.assertEquals(double_metaphone('Bledsoe', 4), ('PLTS', ''))
        self.assertEquals(double_metaphone('Blennerhasset', 4), ('PLNR', ''))
        self.assertEquals(double_metaphone('Blessing', 4), ('PLSN', ''))
        self.assertEquals(double_metaphone('Blewett', 4), ('PLT', ''))
        self.assertEquals(double_metaphone('Bloctgoed', 4), ('PLKT', ''))
        self.assertEquals(double_metaphone('Bloetgoet', 4), ('PLTK', ''))
        self.assertEquals(double_metaphone('Bloodgood', 4), ('PLTK', ''))
        self.assertEquals(double_metaphone('Blossom', 4), ('PLSM', ''))
        self.assertEquals(double_metaphone('Blount', 4), ('PLNT', ''))
        self.assertEquals(double_metaphone('Bodine', 4), ('PTN', ''))
        self.assertEquals(double_metaphone('Bodman', 4), ('PTMN', ''))
        self.assertEquals(double_metaphone('BonCoeur', 4), ('PNKR', ''))
        self.assertEquals(double_metaphone('Bond', 4), ('PNT', ''))
        self.assertEquals(double_metaphone('Boscawen', 4), ('PSKN', ''))
        self.assertEquals(double_metaphone('Bosworth', 4), ('PSR0', 'PSRT'))
        self.assertEquals(double_metaphone('Bouchier', 4), ('PX', 'PKR'))
        self.assertEquals(double_metaphone('Bowne', 4), ('PN', ''))
        self.assertEquals(double_metaphone('Bradbury', 4), ('PRTP', ''))
        self.assertEquals(double_metaphone('Bradder', 4), ('PRTR', ''))
        self.assertEquals(double_metaphone('Bradford', 4), ('PRTF', ''))
        self.assertEquals(double_metaphone('Bradstreet', 4), ('PRTS', ''))
        self.assertEquals(double_metaphone('Braham', 4), ('PRHM', ''))
        self.assertEquals(double_metaphone('Brailsford', 4), ('PRLS', ''))
        self.assertEquals(double_metaphone('Brainard', 4), ('PRNR', ''))
        self.assertEquals(double_metaphone('Brandish', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Braun', 4), ('PRN', ''))
        self.assertEquals(double_metaphone('Brecc', 4), ('PRK', ''))
        self.assertEquals(double_metaphone('Brent', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Brenton', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Briggs', 4), ('PRKS', ''))
        self.assertEquals(double_metaphone('Brigham', 4), ('PRM', ''))
        self.assertEquals(double_metaphone('Brobst', 4), ('PRPS', ''))
        self.assertEquals(double_metaphone('Brome', 4), ('PRM', ''))
        self.assertEquals(double_metaphone('Bronson', 4), ('PRNS', ''))
        self.assertEquals(double_metaphone('Brooks', 4), ('PRKS', ''))
        self.assertEquals(double_metaphone('Brouillard', 4), ('PRLR', ''))
        self.assertEquals(double_metaphone('Brown', 4), ('PRN', ''))
        self.assertEquals(double_metaphone('Browne', 4), ('PRN', ''))
        self.assertEquals(double_metaphone('Brownell', 4), ('PRNL', ''))
        self.assertEquals(double_metaphone('Bruley', 4), ('PRL', ''))
        self.assertEquals(double_metaphone('Bryant', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Brzozowski', 4), ('PRSS', 'PRTS'))
        self.assertEquals(double_metaphone('Buide', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Bulmer', 4), ('PLMR', ''))
        self.assertEquals(double_metaphone('Bunker', 4), ('PNKR', ''))
        self.assertEquals(double_metaphone('Burden', 4), ('PRTN', ''))
        self.assertEquals(double_metaphone('Burge', 4), ('PRJ', 'PRK'))
        self.assertEquals(double_metaphone('Burgoyne', 4), ('PRKN', ''))
        self.assertEquals(double_metaphone('Burke', 4), ('PRK', ''))
        self.assertEquals(double_metaphone('Burnett', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Burpee', 4), ('PRP', ''))
        self.assertEquals(double_metaphone('Bursley', 4), ('PRSL', ''))
        self.assertEquals(double_metaphone('Burton', 4), ('PRTN', ''))
        self.assertEquals(double_metaphone('Bushnell', 4), ('PXNL', ''))
        self.assertEquals(double_metaphone('Buss', 4), ('PS', ''))
        self.assertEquals(double_metaphone('Buswell', 4), ('PSL', ''))
        self.assertEquals(double_metaphone('Butler', 4), ('PTLR', ''))
        self.assertEquals(double_metaphone('Calkin', 4), ('KLKN', ''))
        self.assertEquals(double_metaphone('Canada', 4), ('KNT', ''))
        self.assertEquals(double_metaphone('Canmore', 4), ('KNMR', ''))
        self.assertEquals(double_metaphone('Canney', 4), ('KN', ''))
        self.assertEquals(double_metaphone('Capet', 4), ('KPT', ''))
        self.assertEquals(double_metaphone('Card', 4), ('KRT', ''))
        self.assertEquals(double_metaphone('Carman', 4), ('KRMN', ''))
        self.assertEquals(double_metaphone('Carpenter', 4), ('KRPN', ''))
        self.assertEquals(double_metaphone('Cartwright', 4), ('KRTR', ''))
        self.assertEquals(double_metaphone('Casey', 4), ('KS', ''))
        self.assertEquals(double_metaphone('Catterfield', 4), ('KTRF', ''))
        self.assertEquals(double_metaphone('Ceeley', 4), ('SL', ''))
        self.assertEquals(double_metaphone('Chambers', 4), ('XMPR', ''))
        self.assertEquals(double_metaphone('Champion', 4), ('XMPN', ''))
        self.assertEquals(double_metaphone('Chapman', 4), ('XPMN', ''))
        self.assertEquals(double_metaphone('Chase', 4), ('XS', ''))
        self.assertEquals(double_metaphone('Cheney', 4), ('XN', ''))
        self.assertEquals(double_metaphone('Chetwynd', 4), ('XTNT', ''))
        self.assertEquals(double_metaphone('Chevalier', 4), ('XFL', 'XFLR'))
        self.assertEquals(double_metaphone('Chillingsworth', 4), ('XLNK', ''))
        self.assertEquals(double_metaphone('Christie', 4), ('KRST', ''))
        self.assertEquals(double_metaphone('Chubbuck', 4), ('XPK', ''))
        self.assertEquals(double_metaphone('Church', 4), ('XRX', 'XRK'))
        self.assertEquals(double_metaphone('Clark', 4), ('KLRK', ''))
        self.assertEquals(double_metaphone('Clarke', 4), ('KLRK', ''))
        self.assertEquals(double_metaphone('Cleare', 4), ('KLR', ''))
        self.assertEquals(double_metaphone('Clement', 4), ('KLMN', ''))
        self.assertEquals(double_metaphone('Clerke', 4), ('KLRK', ''))
        self.assertEquals(double_metaphone('Clibben', 4), ('KLPN', ''))
        self.assertEquals(double_metaphone('Clifford', 4), ('KLFR', ''))
        self.assertEquals(double_metaphone('Clivedon', 4), ('KLFT', ''))
        self.assertEquals(double_metaphone('Close', 4), ('KLS', ''))
        self.assertEquals(double_metaphone('Clothilde', 4), ('KL0L', 'KLTL'))
        self.assertEquals(double_metaphone('Cobb', 4), ('KP', ''))
        self.assertEquals(double_metaphone('Coburn', 4), ('KPRN', ''))
        self.assertEquals(double_metaphone('Coburne', 4), ('KPRN', ''))
        self.assertEquals(double_metaphone('Cocke', 4), ('KK', ''))
        self.assertEquals(double_metaphone('Coffin', 4), ('KFN', ''))
        self.assertEquals(double_metaphone('Coffyn', 4), ('KFN', ''))
        self.assertEquals(double_metaphone('Colborne', 4), ('KLPR', ''))
        self.assertEquals(double_metaphone('Colby', 4), ('KLP', ''))
        self.assertEquals(double_metaphone('Cole', 4), ('KL', ''))
        self.assertEquals(double_metaphone('Coleman', 4), ('KLMN', ''))
        self.assertEquals(double_metaphone('Collier', 4), ('KL', 'KLR'))
        self.assertEquals(double_metaphone('Compton', 4), ('KMPT', ''))
        self.assertEquals(double_metaphone('Cone', 4), ('KN', ''))
        self.assertEquals(double_metaphone('Cook', 4), ('KK', ''))
        self.assertEquals(double_metaphone('Cooke', 4), ('KK', ''))
        self.assertEquals(double_metaphone('Cooper', 4), ('KPR', ''))
        self.assertEquals(double_metaphone('Copperthwaite', 4),
                          ('KPR0', 'KPRT'))
        self.assertEquals(double_metaphone('Corbet', 4), ('KRPT', ''))
        self.assertEquals(double_metaphone('Corell', 4), ('KRL', ''))
        self.assertEquals(double_metaphone('Corey', 4), ('KR', ''))
        self.assertEquals(double_metaphone('Corlies', 4), ('KRLS', ''))
        self.assertEquals(double_metaphone('Corneliszen', 4), ('KRNL', ''))
        self.assertEquals(double_metaphone('Cornelius', 4), ('KRNL', ''))
        self.assertEquals(double_metaphone('Cornwallis', 4), ('KRNL', ''))
        self.assertEquals(double_metaphone('Cosgrove', 4), ('KSKR', ''))
        self.assertEquals(double_metaphone('Count of Brionne', 4), ('KNTF', ''))
        self.assertEquals(double_metaphone('Covill', 4), ('KFL', ''))
        self.assertEquals(double_metaphone('Cowperthwaite', 4),
                          ('KPR0', 'KPRT'))
        self.assertEquals(double_metaphone('Cowperwaite', 4), ('KPRT', ''))
        self.assertEquals(double_metaphone('Crane', 4), ('KRN', ''))
        self.assertEquals(double_metaphone('Creagmile', 4), ('KRKM', ''))
        self.assertEquals(double_metaphone('Crew', 4), ('KR', 'KRF'))
        self.assertEquals(double_metaphone('Crispin', 4), ('KRSP', ''))
        self.assertEquals(double_metaphone('Crocker', 4), ('KRKR', ''))
        self.assertEquals(double_metaphone('Crockett', 4), ('KRKT', ''))
        self.assertEquals(double_metaphone('Crosby', 4), ('KRSP', ''))
        self.assertEquals(double_metaphone('Crump', 4), ('KRMP', ''))
        self.assertEquals(double_metaphone('Cunningham', 4), ('KNNK', ''))
        self.assertEquals(double_metaphone('Curtis', 4), ('KRTS', ''))
        self.assertEquals(double_metaphone('Cutha', 4), ('K0', 'KT'))
        self.assertEquals(double_metaphone('Cutter', 4), ('KTR', ''))
        self.assertEquals(double_metaphone('D\'Aubigny', 4), ('TPN', 'TPKN'))
        self.assertEquals(double_metaphone('DAVIS', 4), ('TFS', ''))
        self.assertEquals(double_metaphone('Dabinott', 4), ('TPNT', ''))
        self.assertEquals(double_metaphone('Dacre', 4), ('TKR', ''))
        self.assertEquals(double_metaphone('Daggett', 4), ('TKT', ''))
        self.assertEquals(double_metaphone('Danvers', 4), ('TNFR', ''))
        self.assertEquals(double_metaphone('Darcy', 4), ('TRS', ''))
        self.assertEquals(double_metaphone('Davis', 4), ('TFS', ''))
        self.assertEquals(double_metaphone('Dawn', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Dawson', 4), ('TSN', ''))
        self.assertEquals(double_metaphone('Day', 4), ('T', ''))
        self.assertEquals(double_metaphone('Daye', 4), ('T', ''))
        self.assertEquals(double_metaphone('DeGrenier', 4), ('TKRN', ''))
        self.assertEquals(double_metaphone('Dean', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Deekindaugh', 4), ('TKNT', ''))
        self.assertEquals(double_metaphone('Dennis', 4), ('TNS', ''))
        self.assertEquals(double_metaphone('Denny', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Denton', 4), ('TNTN', ''))
        self.assertEquals(double_metaphone('Desborough', 4), ('TSPR', ''))
        self.assertEquals(double_metaphone('Despenser', 4), ('TSPN', ''))
        self.assertEquals(double_metaphone('Deverill', 4), ('TFRL', ''))
        self.assertEquals(double_metaphone('Devine', 4), ('TFN', ''))
        self.assertEquals(double_metaphone('Dexter', 4), ('TKST', ''))
        self.assertEquals(double_metaphone('Dillaway', 4), ('TL', ''))
        self.assertEquals(double_metaphone('Dimmick', 4), ('TMK', ''))
        self.assertEquals(double_metaphone('Dinan', 4), ('TNN', ''))
        self.assertEquals(double_metaphone('Dix', 4), ('TKS', ''))
        self.assertEquals(double_metaphone('Doggett', 4), ('TKT', ''))
        self.assertEquals(double_metaphone('Donahue', 4), ('TNH', ''))
        self.assertEquals(double_metaphone('Dorfman', 4), ('TRFM', ''))
        self.assertEquals(double_metaphone('Dorris', 4), ('TRS', ''))
        self.assertEquals(double_metaphone('Dow', 4), ('T', 'TF'))
        self.assertEquals(double_metaphone('Downey', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Downing', 4), ('TNNK', ''))
        self.assertEquals(double_metaphone('Dowsett', 4), ('TST', ''))
        self.assertEquals(double_metaphone('Duck?', 4), ('TK', ''))
        self.assertEquals(double_metaphone('Dudley', 4), ('TTL', ''))
        self.assertEquals(double_metaphone('Duffy', 4), ('TF', ''))
        self.assertEquals(double_metaphone('Dunn', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Dunsterville', 4), ('TNST', ''))
        self.assertEquals(double_metaphone('Durrant', 4), ('TRNT', ''))
        self.assertEquals(double_metaphone('Durrin', 4), ('TRN', ''))
        self.assertEquals(double_metaphone('Dustin', 4), ('TSTN', ''))
        self.assertEquals(double_metaphone('Duston', 4), ('TSTN', ''))
        self.assertEquals(double_metaphone('Eames', 4), ('AMS', ''))
        self.assertEquals(double_metaphone('Early', 4), ('ARL', ''))
        self.assertEquals(double_metaphone('Easty', 4), ('AST', ''))
        self.assertEquals(double_metaphone('Ebbett', 4), ('APT', ''))
        self.assertEquals(double_metaphone('Eberbach', 4), ('APRP', ''))
        self.assertEquals(double_metaphone('Eberhard', 4), ('APRR', ''))
        self.assertEquals(double_metaphone('Eddy', 4), ('AT', ''))
        self.assertEquals(double_metaphone('Edenden', 4), ('ATNT', ''))
        self.assertEquals(double_metaphone('Edwards', 4), ('ATRT', ''))
        self.assertEquals(double_metaphone('Eglinton', 4), ('AKLN', 'ALNT'))
        self.assertEquals(double_metaphone('Eliot', 4), ('ALT', ''))
        self.assertEquals(double_metaphone('Elizabeth', 4), ('ALSP', ''))
        self.assertEquals(double_metaphone('Ellis', 4), ('ALS', ''))
        self.assertEquals(double_metaphone('Ellison', 4), ('ALSN', ''))
        self.assertEquals(double_metaphone('Ellot', 4), ('ALT', ''))
        self.assertEquals(double_metaphone('Elny', 4), ('ALN', ''))
        self.assertEquals(double_metaphone('Elsner', 4), ('ALSN', ''))
        self.assertEquals(double_metaphone('Emerson', 4), ('AMRS', ''))
        self.assertEquals(double_metaphone('Empson', 4), ('AMPS', ''))
        self.assertEquals(double_metaphone('Est', 4), ('AST', ''))
        self.assertEquals(double_metaphone('Estabrook', 4), ('ASTP', ''))
        self.assertEquals(double_metaphone('Estes', 4), ('ASTS', ''))
        self.assertEquals(double_metaphone('Estey', 4), ('AST', ''))
        self.assertEquals(double_metaphone('Evans', 4), ('AFNS', ''))
        self.assertEquals(double_metaphone('Fallowell', 4), ('FLL', ''))
        self.assertEquals(double_metaphone('Farnsworth', 4), ('FRNS', ''))
        self.assertEquals(double_metaphone('Feake', 4), ('FK', ''))
        self.assertEquals(double_metaphone('Feke', 4), ('FK', ''))
        self.assertEquals(double_metaphone('Fellows', 4), ('FLS', ''))
        self.assertEquals(double_metaphone('Fettiplace', 4), ('FTPL', ''))
        self.assertEquals(double_metaphone('Finney', 4), ('FN', ''))
        self.assertEquals(double_metaphone('Fischer', 4), ('FXR', 'FSKR'))
        self.assertEquals(double_metaphone('Fisher', 4), ('FXR', ''))
        self.assertEquals(double_metaphone('Fisk', 4), ('FSK', ''))
        self.assertEquals(double_metaphone('Fiske', 4), ('FSK', ''))
        self.assertEquals(double_metaphone('Fletcher', 4), ('FLXR', ''))
        self.assertEquals(double_metaphone('Folger', 4), ('FLKR', 'FLJR'))
        self.assertEquals(double_metaphone('Foliot', 4), ('FLT', ''))
        self.assertEquals(double_metaphone('Folyot', 4), ('FLT', ''))
        self.assertEquals(double_metaphone('Fones', 4), ('FNS', ''))
        self.assertEquals(double_metaphone('Fordham', 4), ('FRTM', ''))
        self.assertEquals(double_metaphone('Forstner', 4), ('FRST', ''))
        self.assertEquals(double_metaphone('Fosten', 4), ('FSTN', ''))
        self.assertEquals(double_metaphone('Foster', 4), ('FSTR', ''))
        self.assertEquals(double_metaphone('Foulke', 4), ('FLK', ''))
        self.assertEquals(double_metaphone('Fowler', 4), ('FLR', ''))
        self.assertEquals(double_metaphone('Foxwell', 4), ('FKSL', ''))
        self.assertEquals(double_metaphone('Fraley', 4), ('FRL', ''))
        self.assertEquals(double_metaphone('Franceys', 4), ('FRNS', ''))
        self.assertEquals(double_metaphone('Franke', 4), ('FRNK', ''))
        self.assertEquals(double_metaphone('Frascella', 4), ('FRSL', ''))
        self.assertEquals(double_metaphone('Frazer', 4), ('FRSR', ''))
        self.assertEquals(double_metaphone('Fredd', 4), ('FRT', ''))
        self.assertEquals(double_metaphone('Freeman', 4), ('FRMN', ''))
        self.assertEquals(double_metaphone('French', 4), ('FRNX', 'FRNK'))
        self.assertEquals(double_metaphone('Freville', 4), ('FRFL', ''))
        self.assertEquals(double_metaphone('Frey', 4), ('FR', ''))
        self.assertEquals(double_metaphone('Frick', 4), ('FRK', ''))
        self.assertEquals(double_metaphone('Frier', 4), ('FR', 'FRR'))
        self.assertEquals(double_metaphone('Froe', 4), ('FR', ''))
        self.assertEquals(double_metaphone('Frorer', 4), ('FRRR', ''))
        self.assertEquals(double_metaphone('Frost', 4), ('FRST', ''))
        self.assertEquals(double_metaphone('Frothingham', 4), ('FR0N', 'FRTN'))
        self.assertEquals(double_metaphone('Fry', 4), ('FR', ''))
        self.assertEquals(double_metaphone('Gaffney', 4), ('KFN', ''))
        self.assertEquals(double_metaphone('Gage', 4), ('KJ', 'KK'))
        self.assertEquals(double_metaphone('Gallion', 4), ('KLN', ''))
        self.assertEquals(double_metaphone('Gallishan', 4), ('KLXN', ''))
        self.assertEquals(double_metaphone('Gamble', 4), ('KMPL', ''))
        self.assertEquals(double_metaphone('Garbrand', 4), ('KRPR', ''))
        self.assertEquals(double_metaphone('Gardner', 4), ('KRTN', ''))
        self.assertEquals(double_metaphone('Garrett', 4), ('KRT', ''))
        self.assertEquals(double_metaphone('Gassner', 4), ('KSNR', ''))
        self.assertEquals(double_metaphone('Gater', 4), ('KTR', ''))
        self.assertEquals(double_metaphone('Gaunt', 4), ('KNT', ''))
        self.assertEquals(double_metaphone('Gayer', 4), ('KR', ''))
        self.assertEquals(double_metaphone('Gerken', 4), ('KRKN', 'JRKN'))
        self.assertEquals(double_metaphone('Gerritsen', 4), ('KRTS', 'JRTS'))
        self.assertEquals(double_metaphone('Gibbs', 4), ('KPS', 'JPS'))
        self.assertEquals(double_metaphone('Giffard', 4), ('JFRT', 'KFRT'))
        self.assertEquals(double_metaphone('Gilbert', 4), ('KLPR', 'JLPR'))
        self.assertEquals(double_metaphone('Gill', 4), ('KL', 'JL'))
        self.assertEquals(double_metaphone('Gilman', 4), ('KLMN', 'JLMN'))
        self.assertEquals(double_metaphone('Glass', 4), ('KLS', ''))
        self.assertEquals(double_metaphone('GoddardGifford', 4), ('KTRJ', ''))
        self.assertEquals(double_metaphone('Godfrey', 4), ('KTFR', ''))
        self.assertEquals(double_metaphone('Godwin', 4), ('KTN', ''))
        self.assertEquals(double_metaphone('Goodale', 4), ('KTL', ''))
        self.assertEquals(double_metaphone('Goodnow', 4), ('KTN', 'KTNF'))
        self.assertEquals(double_metaphone('Gorham', 4), ('KRM', ''))
        self.assertEquals(double_metaphone('Goseline', 4), ('KSLN', ''))
        self.assertEquals(double_metaphone('Gott', 4), ('KT', ''))
        self.assertEquals(double_metaphone('Gould', 4), ('KLT', ''))
        self.assertEquals(double_metaphone('Grafton', 4), ('KRFT', ''))
        self.assertEquals(double_metaphone('Grant', 4), ('KRNT', ''))
        self.assertEquals(double_metaphone('Gray', 4), ('KR', ''))
        self.assertEquals(double_metaphone('Green', 4), ('KRN', ''))
        self.assertEquals(double_metaphone('Griffin', 4), ('KRFN', ''))
        self.assertEquals(double_metaphone('Grill', 4), ('KRL', ''))
        self.assertEquals(double_metaphone('Grim', 4), ('KRM', ''))
        self.assertEquals(double_metaphone('Grisgonelle', 4), ('KRSK', ''))
        self.assertEquals(double_metaphone('Gross', 4), ('KRS', ''))
        self.assertEquals(double_metaphone('Guba', 4), ('KP', ''))
        self.assertEquals(double_metaphone('Gybbes', 4), ('KPS', 'JPS'))
        self.assertEquals(double_metaphone('Haburne', 4), ('HPRN', ''))
        self.assertEquals(double_metaphone('Hackburne', 4), ('HKPR', ''))
        self.assertEquals(double_metaphone('Haddon?', 4), ('HTN', ''))
        self.assertEquals(double_metaphone('Haines', 4), ('HNS', ''))
        self.assertEquals(double_metaphone('Hale', 4), ('HL', ''))
        self.assertEquals(double_metaphone('Hall', 4), ('HL', ''))
        self.assertEquals(double_metaphone('Hallet', 4), ('HLT', ''))
        self.assertEquals(double_metaphone('Hallock', 4), ('HLK', ''))
        self.assertEquals(double_metaphone('Halstead', 4), ('HLST', ''))
        self.assertEquals(double_metaphone('Hammond', 4), ('HMNT', ''))
        self.assertEquals(double_metaphone('Hance', 4), ('HNS', ''))
        self.assertEquals(double_metaphone('Handy', 4), ('HNT', ''))
        self.assertEquals(double_metaphone('Hanson', 4), ('HNSN', ''))
        self.assertEquals(double_metaphone('Harasek', 4), ('HRSK', ''))
        self.assertEquals(double_metaphone('Harcourt', 4), ('HRKR', ''))
        self.assertEquals(double_metaphone('Hardy', 4), ('HRT', ''))
        self.assertEquals(double_metaphone('Harlock', 4), ('HRLK', ''))
        self.assertEquals(double_metaphone('Harris', 4), ('HRS', ''))
        self.assertEquals(double_metaphone('Hartley', 4), ('HRTL', ''))
        self.assertEquals(double_metaphone('Harvey', 4), ('HRF', ''))
        self.assertEquals(double_metaphone('Harvie', 4), ('HRF', ''))
        self.assertEquals(double_metaphone('Harwood', 4), ('HRT', ''))
        self.assertEquals(double_metaphone('Hathaway', 4), ('H0', 'HT'))
        self.assertEquals(double_metaphone('Haukeness', 4), ('HKNS', ''))
        self.assertEquals(double_metaphone('Hawkes', 4), ('HKS', ''))
        self.assertEquals(double_metaphone('Hawkhurst', 4), ('HKRS', ''))
        self.assertEquals(double_metaphone('Hawkins', 4), ('HKNS', ''))
        self.assertEquals(double_metaphone('Hawley', 4), ('HL', ''))
        self.assertEquals(double_metaphone('Heald', 4), ('HLT', ''))
        self.assertEquals(double_metaphone('Helsdon', 4), ('HLST', ''))
        self.assertEquals(double_metaphone('Hemenway', 4), ('HMN', ''))
        self.assertEquals(double_metaphone('Hemmenway', 4), ('HMN', ''))
        self.assertEquals(double_metaphone('Henck', 4), ('HNK', ''))
        self.assertEquals(double_metaphone('Henderson', 4), ('HNTR', ''))
        self.assertEquals(double_metaphone('Hendricks', 4), ('HNTR', ''))
        self.assertEquals(double_metaphone('Hersey', 4), ('HRS', ''))
        self.assertEquals(double_metaphone('Hewes', 4), ('HS', ''))
        self.assertEquals(double_metaphone('Heyman', 4), ('HMN', ''))
        self.assertEquals(double_metaphone('Hicks', 4), ('HKS', ''))
        self.assertEquals(double_metaphone('Hidden', 4), ('HTN', ''))
        self.assertEquals(double_metaphone('Higgs', 4), ('HKS', ''))
        self.assertEquals(double_metaphone('Hill', 4), ('HL', ''))
        self.assertEquals(double_metaphone('Hills', 4), ('HLS', ''))
        self.assertEquals(double_metaphone('Hinckley', 4), ('HNKL', ''))
        self.assertEquals(double_metaphone('Hipwell', 4), ('HPL', ''))
        self.assertEquals(double_metaphone('Hobart', 4), ('HPRT', ''))
        self.assertEquals(double_metaphone('Hoben', 4), ('HPN', ''))
        self.assertEquals(double_metaphone('Hoffmann', 4), ('HFMN', ''))
        self.assertEquals(double_metaphone('Hogan', 4), ('HKN', ''))
        self.assertEquals(double_metaphone('Holmes', 4), ('HLMS', ''))
        self.assertEquals(double_metaphone('Hoo', 4), ('H', ''))
        self.assertEquals(double_metaphone('Hooker', 4), ('HKR', ''))
        self.assertEquals(double_metaphone('Hopcott', 4), ('HPKT', ''))
        self.assertEquals(double_metaphone('Hopkins', 4), ('HPKN', ''))
        self.assertEquals(double_metaphone('Hopkinson', 4), ('HPKN', ''))
        self.assertEquals(double_metaphone('Hornsey', 4), ('HRNS', ''))
        self.assertEquals(double_metaphone('Houckgeest', 4), ('HKJS', 'HKKS'))
        self.assertEquals(double_metaphone('Hough', 4), ('H', ''))
        self.assertEquals(double_metaphone('Houstin', 4), ('HSTN', ''))
        self.assertEquals(double_metaphone('How', 4), ('H', 'HF'))
        self.assertEquals(double_metaphone('Howe', 4), ('H', ''))
        self.assertEquals(double_metaphone('Howland', 4), ('HLNT', ''))
        self.assertEquals(double_metaphone('Hubner', 4), ('HPNR', ''))
        self.assertEquals(double_metaphone('Hudnut', 4), ('HTNT', ''))
        self.assertEquals(double_metaphone('Hughes', 4), ('HS', ''))
        self.assertEquals(double_metaphone('Hull', 4), ('HL', ''))
        self.assertEquals(double_metaphone('Hulme', 4), ('HLM', ''))
        self.assertEquals(double_metaphone('Hume', 4), ('HM', ''))
        self.assertEquals(double_metaphone('Hundertumark', 4), ('HNTR', ''))
        self.assertEquals(double_metaphone('Hundley', 4), ('HNTL', ''))
        self.assertEquals(double_metaphone('Hungerford', 4), ('HNKR', 'HNJR'))
        self.assertEquals(double_metaphone('Hunt', 4), ('HNT', ''))
        self.assertEquals(double_metaphone('Hurst', 4), ('HRST', ''))
        self.assertEquals(double_metaphone('Husbands', 4), ('HSPN', ''))
        self.assertEquals(double_metaphone('Hussey', 4), ('HS', ''))
        self.assertEquals(double_metaphone('Husted', 4), ('HSTT', ''))
        self.assertEquals(double_metaphone('Hutchins', 4), ('HXNS', ''))
        self.assertEquals(double_metaphone('Hutchinson', 4), ('HXNS', ''))
        self.assertEquals(double_metaphone('Huttinger', 4), ('HTNK', 'HTNJ'))
        self.assertEquals(double_metaphone('Huybertsen', 4), ('HPRT', ''))
        self.assertEquals(double_metaphone('Iddenden', 4), ('ATNT', ''))
        self.assertEquals(double_metaphone('Ingraham', 4), ('ANKR', ''))
        self.assertEquals(double_metaphone('Ives', 4), ('AFS', ''))
        self.assertEquals(double_metaphone('Jackson', 4), ('JKSN', 'AKSN'))
        self.assertEquals(double_metaphone('Jacob', 4), ('JKP', 'AKP'))
        self.assertEquals(double_metaphone('Jans', 4), ('JNS', 'ANS'))
        self.assertEquals(double_metaphone('Jenkins', 4), ('JNKN', 'ANKN'))
        self.assertEquals(double_metaphone('Jewett', 4), ('JT', 'AT'))
        self.assertEquals(double_metaphone('Jewitt', 4), ('JT', 'AT'))
        self.assertEquals(double_metaphone('Johnson', 4), ('JNSN', 'ANSN'))
        self.assertEquals(double_metaphone('Jones', 4), ('JNS', 'ANS'))
        self.assertEquals(double_metaphone('Josephine', 4), ('JSFN', 'HSFN'))
        self.assertEquals(double_metaphone('Judd', 4), ('JT', 'AT'))
        self.assertEquals(double_metaphone('June', 4), ('JN', 'AN'))
        self.assertEquals(double_metaphone('Kamarowska', 4), ('KMRS', ''))
        self.assertEquals(double_metaphone('Kay', 4), ('K', ''))
        self.assertEquals(double_metaphone('Kelley', 4), ('KL', ''))
        self.assertEquals(double_metaphone('Kelly', 4), ('KL', ''))
        self.assertEquals(double_metaphone('Keymber', 4), ('KMPR', ''))
        self.assertEquals(double_metaphone('Keynes', 4), ('KNS', ''))
        self.assertEquals(double_metaphone('Kilham', 4), ('KLM', ''))
        self.assertEquals(double_metaphone('Kim', 4), ('KM', ''))
        self.assertEquals(double_metaphone('Kimball', 4), ('KMPL', ''))
        self.assertEquals(double_metaphone('King', 4), ('KNK', ''))
        self.assertEquals(double_metaphone('Kinsey', 4), ('KNS', ''))
        self.assertEquals(double_metaphone('Kirk', 4), ('KRK', ''))
        self.assertEquals(double_metaphone('Kirton', 4), ('KRTN', ''))
        self.assertEquals(double_metaphone('Kistler', 4), ('KSTL', ''))
        self.assertEquals(double_metaphone('Kitchen', 4), ('KXN', ''))
        self.assertEquals(double_metaphone('Kitson', 4), ('KTSN', ''))
        self.assertEquals(double_metaphone('Klett', 4), ('KLT', ''))
        self.assertEquals(double_metaphone('Kline', 4), ('KLN', ''))
        self.assertEquals(double_metaphone('Knapp', 4), ('NP', ''))
        self.assertEquals(double_metaphone('Knight', 4), ('NT', ''))
        self.assertEquals(double_metaphone('Knote', 4), ('NT', ''))
        self.assertEquals(double_metaphone('Knott', 4), ('NT', ''))
        self.assertEquals(double_metaphone('Knox', 4), ('NKS', ''))
        self.assertEquals(double_metaphone('Koeller', 4), ('KLR', ''))
        self.assertEquals(double_metaphone('La Pointe', 4), ('LPNT', ''))
        self.assertEquals(double_metaphone('LaPlante', 4), ('LPLN', ''))
        self.assertEquals(double_metaphone('Laimbeer', 4), ('LMPR', ''))
        self.assertEquals(double_metaphone('Lamb', 4), ('LMP', ''))
        self.assertEquals(double_metaphone('Lambertson', 4), ('LMPR', ''))
        self.assertEquals(double_metaphone('Lancto', 4), ('LNKT', ''))
        self.assertEquals(double_metaphone('Landry', 4), ('LNTR', ''))
        self.assertEquals(double_metaphone('Lane', 4), ('LN', ''))
        self.assertEquals(double_metaphone('Langendyck', 4), ('LNJN', 'LNKN'))
        self.assertEquals(double_metaphone('Langer', 4), ('LNKR', 'LNJR'))
        self.assertEquals(double_metaphone('Langford', 4), ('LNKF', ''))
        self.assertEquals(double_metaphone('Lantersee', 4), ('LNTR', ''))
        self.assertEquals(double_metaphone('Laquer', 4), ('LKR', ''))
        self.assertEquals(double_metaphone('Larkin', 4), ('LRKN', ''))
        self.assertEquals(double_metaphone('Latham', 4), ('LTM', ''))
        self.assertEquals(double_metaphone('Lathrop', 4), ('L0RP', 'LTRP'))
        self.assertEquals(double_metaphone('Lauter', 4), ('LTR', ''))
        self.assertEquals(double_metaphone('Lawrence', 4), ('LRNS', ''))
        self.assertEquals(double_metaphone('Leach', 4), ('LK', ''))
        self.assertEquals(double_metaphone('Leager', 4), ('LKR', 'LJR'))
        self.assertEquals(double_metaphone('Learned', 4), ('LRNT', ''))
        self.assertEquals(double_metaphone('Leavitt', 4), ('LFT', ''))
        self.assertEquals(double_metaphone('Lee', 4), ('L', ''))
        self.assertEquals(double_metaphone('Leete', 4), ('LT', ''))
        self.assertEquals(double_metaphone('Leggett', 4), ('LKT', ''))
        self.assertEquals(double_metaphone('Leland', 4), ('LLNT', ''))
        self.assertEquals(double_metaphone('Leonard', 4), ('LNRT', ''))
        self.assertEquals(double_metaphone('Lester', 4), ('LSTR', ''))
        self.assertEquals(double_metaphone('Lestrange', 4), ('LSTR', ''))
        self.assertEquals(double_metaphone('Lethem', 4), ('L0M', 'LTM'))
        self.assertEquals(double_metaphone('Levine', 4), ('LFN', ''))
        self.assertEquals(double_metaphone('Lewes', 4), ('LS', ''))
        self.assertEquals(double_metaphone('Lewis', 4), ('LS', ''))
        self.assertEquals(double_metaphone('Lincoln', 4), ('LNKL', ''))
        self.assertEquals(double_metaphone('Lindsey', 4), ('LNTS', ''))
        self.assertEquals(double_metaphone('Linher', 4), ('LNR', ''))
        self.assertEquals(double_metaphone('Lippet', 4), ('LPT', ''))
        self.assertEquals(double_metaphone('Lippincott', 4), ('LPNK', ''))
        self.assertEquals(double_metaphone('Lockwood', 4), ('LKT', ''))
        self.assertEquals(double_metaphone('Loines', 4), ('LNS', ''))
        self.assertEquals(double_metaphone('Lombard', 4), ('LMPR', ''))
        self.assertEquals(double_metaphone('Long', 4), ('LNK', ''))
        self.assertEquals(double_metaphone('Longespee', 4), ('LNJS', 'LNKS'))
        self.assertEquals(double_metaphone('Look', 4), ('LK', ''))
        self.assertEquals(double_metaphone('Lounsberry', 4), ('LNSP', ''))
        self.assertEquals(double_metaphone('Lounsbury', 4), ('LNSP', ''))
        self.assertEquals(double_metaphone('Louthe', 4), ('L0', 'LT'))
        self.assertEquals(double_metaphone('Loveyne', 4), ('LFN', ''))
        self.assertEquals(double_metaphone('Lowe', 4), ('L', ''))
        self.assertEquals(double_metaphone('Ludlam', 4), ('LTLM', ''))
        self.assertEquals(double_metaphone('Lumbard', 4), ('LMPR', ''))
        self.assertEquals(double_metaphone('Lund', 4), ('LNT', ''))
        self.assertEquals(double_metaphone('Luno', 4), ('LN', ''))
        self.assertEquals(double_metaphone('Lutz', 4), ('LTS', ''))
        self.assertEquals(double_metaphone('Lydia', 4), ('LT', ''))
        self.assertEquals(double_metaphone('Lynne', 4), ('LN', ''))
        self.assertEquals(double_metaphone('Lyon', 4), ('LN', ''))
        self.assertEquals(double_metaphone('MacAlpin', 4), ('MKLP', ''))
        self.assertEquals(double_metaphone('MacBricc', 4), ('MKPR', ''))
        self.assertEquals(double_metaphone('MacCrinan', 4), ('MKRN', ''))
        self.assertEquals(double_metaphone('MacKenneth', 4), ('MKN0', 'MKNT'))
        self.assertEquals(double_metaphone('MacMael nam Bo', 4), ('MKML', ''))
        self.assertEquals(double_metaphone('MacMurchada', 4), ('MKMR', ''))
        self.assertEquals(double_metaphone('Macomber', 4), ('MKMP', ''))
        self.assertEquals(double_metaphone('Macy', 4), ('MS', ''))
        self.assertEquals(double_metaphone('Magnus', 4), ('MNS', 'MKNS'))
        self.assertEquals(double_metaphone('Mahien', 4), ('MHN', ''))
        self.assertEquals(double_metaphone('Malmains', 4), ('MLMN', ''))
        self.assertEquals(double_metaphone('Malory', 4), ('MLR', ''))
        self.assertEquals(double_metaphone('Mancinelli', 4), ('MNSN', ''))
        self.assertEquals(double_metaphone('Mancini', 4), ('MNSN', ''))
        self.assertEquals(double_metaphone('Mann', 4), ('MN', ''))
        self.assertEquals(double_metaphone('Manning', 4), ('MNNK', ''))
        self.assertEquals(double_metaphone('Manter', 4), ('MNTR', ''))
        self.assertEquals(double_metaphone('Marion', 4), ('MRN', ''))
        self.assertEquals(double_metaphone('Marley', 4), ('MRL', ''))
        self.assertEquals(double_metaphone('Marmion', 4), ('MRMN', ''))
        self.assertEquals(double_metaphone('Marquart', 4), ('MRKR', ''))
        self.assertEquals(double_metaphone('Marsh', 4), ('MRX', ''))
        self.assertEquals(double_metaphone('Marshal', 4), ('MRXL', ''))
        self.assertEquals(double_metaphone('Marshall', 4), ('MRXL', ''))
        self.assertEquals(double_metaphone('Martel', 4), ('MRTL', ''))
        self.assertEquals(double_metaphone('Martha', 4), ('MR0', 'MRT'))
        self.assertEquals(double_metaphone('Martin', 4), ('MRTN', ''))
        self.assertEquals(double_metaphone('Marturano', 4), ('MRTR', ''))
        self.assertEquals(double_metaphone('Marvin', 4), ('MRFN', ''))
        self.assertEquals(double_metaphone('Mary', 4), ('MR', ''))
        self.assertEquals(double_metaphone('Mason', 4), ('MSN', ''))
        self.assertEquals(double_metaphone('Maxwell', 4), ('MKSL', ''))
        self.assertEquals(double_metaphone('Mayhew', 4), ('MH', 'MHF'))
        self.assertEquals(double_metaphone('McAllaster', 4), ('MKLS', ''))
        self.assertEquals(double_metaphone('McAllister', 4), ('MKLS', ''))
        self.assertEquals(double_metaphone('McConnell', 4), ('MKNL', ''))
        self.assertEquals(double_metaphone('McFarland', 4), ('MKFR', ''))
        self.assertEquals(double_metaphone('McIlroy', 4), ('MSLR', ''))
        self.assertEquals(double_metaphone('McNair', 4), ('MKNR', ''))
        self.assertEquals(double_metaphone('McNair-Landry', 4), ('MKNR', ''))
        self.assertEquals(double_metaphone('McRaven', 4), ('MKRF', ''))
        self.assertEquals(double_metaphone('Mead', 4), ('MT', ''))
        self.assertEquals(double_metaphone('Meade', 4), ('MT', ''))
        self.assertEquals(double_metaphone('Meck', 4), ('MK', ''))
        self.assertEquals(double_metaphone('Melton', 4), ('MLTN', ''))
        self.assertEquals(double_metaphone('Mendenhall', 4), ('MNTN', ''))
        self.assertEquals(double_metaphone('Mering', 4), ('MRNK', ''))
        self.assertEquals(double_metaphone('Merrick', 4), ('MRK', ''))
        self.assertEquals(double_metaphone('Merry', 4), ('MR', ''))
        self.assertEquals(double_metaphone('Mighill', 4), ('ML', ''))
        self.assertEquals(double_metaphone('Miller', 4), ('MLR', ''))
        self.assertEquals(double_metaphone('Milton', 4), ('MLTN', ''))
        self.assertEquals(double_metaphone('Mohun', 4), ('MHN', ''))
        self.assertEquals(double_metaphone('Montague', 4), ('MNTK', ''))
        self.assertEquals(double_metaphone('Montboucher', 4), ('MNTP', ''))
        self.assertEquals(double_metaphone('Moore', 4), ('MR', ''))
        self.assertEquals(double_metaphone('Morrel', 4), ('MRL', ''))
        self.assertEquals(double_metaphone('Morrill', 4), ('MRL', ''))
        self.assertEquals(double_metaphone('Morris', 4), ('MRS', ''))
        self.assertEquals(double_metaphone('Morton', 4), ('MRTN', ''))
        self.assertEquals(double_metaphone('Moton', 4), ('MTN', ''))
        self.assertEquals(double_metaphone('Muir', 4), ('MR', ''))
        self.assertEquals(double_metaphone('Mulferd', 4), ('MLFR', ''))
        self.assertEquals(double_metaphone('Mullins', 4), ('MLNS', ''))
        self.assertEquals(double_metaphone('Mulso', 4), ('MLS', ''))
        self.assertEquals(double_metaphone('Munger', 4), ('MNKR', 'MNJR'))
        self.assertEquals(double_metaphone('Munt', 4), ('MNT', ''))
        self.assertEquals(double_metaphone('Murchad', 4), ('MRXT', 'MRKT'))
        self.assertEquals(double_metaphone('Murdock', 4), ('MRTK', ''))
        self.assertEquals(double_metaphone('Murray', 4), ('MR', ''))
        self.assertEquals(double_metaphone('Muskett', 4), ('MSKT', ''))
        self.assertEquals(double_metaphone('Myers', 4), ('MRS', ''))
        self.assertEquals(double_metaphone('Myrick', 4), ('MRK', ''))
        self.assertEquals(double_metaphone('NORRIS', 4), ('NRS', ''))
        self.assertEquals(double_metaphone('Nayle', 4), ('NL', ''))
        self.assertEquals(double_metaphone('Newcomb', 4), ('NKMP', ''))
        self.assertEquals(double_metaphone('Newcomb(e)', 4), ('NKMP', ''))
        self.assertEquals(double_metaphone('Newkirk', 4), ('NKRK', ''))
        self.assertEquals(double_metaphone('Newton', 4), ('NTN', ''))
        self.assertEquals(double_metaphone('Niles', 4), ('NLS', ''))
        self.assertEquals(double_metaphone('Noble', 4), ('NPL', ''))
        self.assertEquals(double_metaphone('Noel', 4), ('NL', ''))
        self.assertEquals(double_metaphone('Northend', 4), ('NR0N', 'NRTN'))
        self.assertEquals(double_metaphone('Norton', 4), ('NRTN', ''))
        self.assertEquals(double_metaphone('Nutter', 4), ('NTR', ''))
        self.assertEquals(double_metaphone('Odding', 4), ('ATNK', ''))
        self.assertEquals(double_metaphone('Odenbaugh', 4), ('ATNP', ''))
        self.assertEquals(double_metaphone('Ogborn', 4), ('AKPR', ''))
        self.assertEquals(double_metaphone('Oppenheimer', 4), ('APNM', ''))
        self.assertEquals(double_metaphone('Otis', 4), ('ATS', ''))
        self.assertEquals(double_metaphone('Oviatt', 4), ('AFT', ''))
        self.assertEquals(double_metaphone('PRUST?', 4), ('PRST', ''))
        self.assertEquals(double_metaphone('Paddock', 4), ('PTK', ''))
        self.assertEquals(double_metaphone('Page', 4), ('PJ', 'PK'))
        self.assertEquals(double_metaphone('Paine', 4), ('PN', ''))
        self.assertEquals(double_metaphone('Paist', 4), ('PST', ''))
        self.assertEquals(double_metaphone('Palmer', 4), ('PLMR', ''))
        self.assertEquals(double_metaphone('Park', 4), ('PRK', ''))
        self.assertEquals(double_metaphone('Parker', 4), ('PRKR', ''))
        self.assertEquals(double_metaphone('Parkhurst', 4), ('PRKR', ''))
        self.assertEquals(double_metaphone('Parrat', 4), ('PRT', ''))
        self.assertEquals(double_metaphone('Parsons', 4), ('PRSN', ''))
        self.assertEquals(double_metaphone('Partridge', 4), ('PRTR', ''))
        self.assertEquals(double_metaphone('Pashley', 4), ('PXL', ''))
        self.assertEquals(double_metaphone('Pasley', 4), ('PSL', ''))
        self.assertEquals(double_metaphone('Patrick', 4), ('PTRK', ''))
        self.assertEquals(double_metaphone('Pattee', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Patten', 4), ('PTN', ''))
        self.assertEquals(double_metaphone('Pawley', 4), ('PL', ''))
        self.assertEquals(double_metaphone('Payne', 4), ('PN', ''))
        self.assertEquals(double_metaphone('Peabody', 4), ('PPT', ''))
        self.assertEquals(double_metaphone('Peake', 4), ('PK', ''))
        self.assertEquals(double_metaphone('Pearson', 4), ('PRSN', ''))
        self.assertEquals(double_metaphone('Peat', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Pedersen', 4), ('PTRS', ''))
        self.assertEquals(double_metaphone('Percy', 4), ('PRS', ''))
        self.assertEquals(double_metaphone('Perkins', 4), ('PRKN', ''))
        self.assertEquals(double_metaphone('Perrine', 4), ('PRN', ''))
        self.assertEquals(double_metaphone('Perry', 4), ('PR', ''))
        self.assertEquals(double_metaphone('Peson', 4), ('PSN', ''))
        self.assertEquals(double_metaphone('Peterson', 4), ('PTRS', ''))
        self.assertEquals(double_metaphone('Peyton', 4), ('PTN', ''))
        self.assertEquals(double_metaphone('Phinney', 4), ('FN', ''))
        self.assertEquals(double_metaphone('Pickard', 4), ('PKRT', ''))
        self.assertEquals(double_metaphone('Pierce', 4), ('PRS', ''))
        self.assertEquals(double_metaphone('Pierrepont', 4), ('PRPN', ''))
        self.assertEquals(double_metaphone('Pike', 4), ('PK', ''))
        self.assertEquals(double_metaphone('Pinkham', 4), ('PNKM', ''))
        self.assertEquals(double_metaphone('Pitman', 4), ('PTMN', ''))
        self.assertEquals(double_metaphone('Pitt', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Pitts', 4), ('PTS', ''))
        self.assertEquals(double_metaphone('Plantagenet', 4), ('PLNT', ''))
        self.assertEquals(double_metaphone('Platt', 4), ('PLT', ''))
        self.assertEquals(double_metaphone('Platts', 4), ('PLTS', ''))
        self.assertEquals(double_metaphone('Pleis', 4), ('PLS', ''))
        self.assertEquals(double_metaphone('Pleiss', 4), ('PLS', ''))
        self.assertEquals(double_metaphone('Plisko', 4), ('PLSK', ''))
        self.assertEquals(double_metaphone('Pliskovitch', 4), ('PLSK', ''))
        self.assertEquals(double_metaphone('Plum', 4), ('PLM', ''))
        self.assertEquals(double_metaphone('Plume', 4), ('PLM', ''))
        self.assertEquals(double_metaphone('Poitou', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Pomeroy', 4), ('PMR', ''))
        self.assertEquals(double_metaphone('Poretiers', 4), ('PRTR', ''))
        self.assertEquals(double_metaphone('Pote', 4), ('PT', ''))
        self.assertEquals(double_metaphone('Potter', 4), ('PTR', ''))
        self.assertEquals(double_metaphone('Potts', 4), ('PTS', ''))
        self.assertEquals(double_metaphone('Powell', 4), ('PL', ''))
        self.assertEquals(double_metaphone('Pratt', 4), ('PRT', ''))
        self.assertEquals(double_metaphone('Presbury', 4), ('PRSP', ''))
        self.assertEquals(double_metaphone('Priest', 4), ('PRST', ''))
        self.assertEquals(double_metaphone('Prindle', 4), ('PRNT', ''))
        self.assertEquals(double_metaphone('Prior', 4), ('PRR', ''))
        self.assertEquals(double_metaphone('Profumo', 4), ('PRFM', ''))
        self.assertEquals(double_metaphone('Purdy', 4), ('PRT', ''))
        self.assertEquals(double_metaphone('Purefoy', 4), ('PRF', ''))
        self.assertEquals(double_metaphone('Pury', 4), ('PR', ''))
        self.assertEquals(double_metaphone('Quinter', 4), ('KNTR', ''))
        self.assertEquals(double_metaphone('Rachel', 4), ('RXL', 'RKL'))
        self.assertEquals(double_metaphone('Rand', 4), ('RNT', ''))
        self.assertEquals(double_metaphone('Rankin', 4), ('RNKN', ''))
        self.assertEquals(double_metaphone('Ravenscroft', 4), ('RFNS', ''))
        self.assertEquals(double_metaphone('Raynsford', 4), ('RNSF', ''))
        self.assertEquals(double_metaphone('Reakirt', 4), ('RKRT', ''))
        self.assertEquals(double_metaphone('Reaves', 4), ('RFS', ''))
        self.assertEquals(double_metaphone('Reeves', 4), ('RFS', ''))
        self.assertEquals(double_metaphone('Reichert', 4), ('RXRT', 'RKRT'))
        self.assertEquals(double_metaphone('Remmele', 4), ('RML', ''))
        self.assertEquals(double_metaphone('Reynolds', 4), ('RNLT', ''))
        self.assertEquals(double_metaphone('Rhodes', 4), ('RTS', ''))
        self.assertEquals(double_metaphone('Richards', 4), ('RXRT', 'RKRT'))
        self.assertEquals(double_metaphone('Richardson', 4), ('RXRT', 'RKRT'))
        self.assertEquals(double_metaphone('Ring', 4), ('RNK', ''))
        self.assertEquals(double_metaphone('Roberts', 4), ('RPRT', ''))
        self.assertEquals(double_metaphone('Robertson', 4), ('RPRT', ''))
        self.assertEquals(double_metaphone('Robson', 4), ('RPSN', ''))
        self.assertEquals(double_metaphone('Rodie', 4), ('RT', ''))
        self.assertEquals(double_metaphone('Rody', 4), ('RT', ''))
        self.assertEquals(double_metaphone('Rogers', 4), ('RKRS', 'RJRS'))
        self.assertEquals(double_metaphone('Ross', 4), ('RS', ''))
        self.assertEquals(double_metaphone('Rosslevin', 4), ('RSLF', ''))
        self.assertEquals(double_metaphone('Rowland', 4), ('RLNT', ''))
        self.assertEquals(double_metaphone('Ruehl', 4), ('RL', ''))
        self.assertEquals(double_metaphone('Russell', 4), ('RSL', ''))
        self.assertEquals(double_metaphone('Ruth', 4), ('R0', 'RT'))
        self.assertEquals(double_metaphone('Ryan', 4), ('RN', ''))
        self.assertEquals(double_metaphone('Rysse', 4), ('RS', ''))
        self.assertEquals(double_metaphone('Sadler', 4), ('STLR', ''))
        self.assertEquals(double_metaphone('Salmon', 4), ('SLMN', ''))
        self.assertEquals(double_metaphone('Salter', 4), ('SLTR', ''))
        self.assertEquals(double_metaphone('Salvatore', 4), ('SLFT', ''))
        self.assertEquals(double_metaphone('Sanders', 4), ('SNTR', ''))
        self.assertEquals(double_metaphone('Sands', 4), ('SNTS', ''))
        self.assertEquals(double_metaphone('Sanford', 4), ('SNFR', ''))
        self.assertEquals(double_metaphone('Sanger', 4), ('SNKR', 'SNJR'))
        self.assertEquals(double_metaphone('Sargent', 4), ('SRJN', 'SRKN'))
        self.assertEquals(double_metaphone('Saunders', 4), ('SNTR', ''))
        self.assertEquals(double_metaphone('Schilling', 4), ('XLNK', ''))
        self.assertEquals(double_metaphone('Schlegel', 4), ('XLKL', 'SLKL'))
        self.assertEquals(double_metaphone('Scott', 4), ('SKT', ''))
        self.assertEquals(double_metaphone('Sears', 4), ('SRS', ''))
        self.assertEquals(double_metaphone('Segersall', 4), ('SJRS', 'SKRS'))
        self.assertEquals(double_metaphone('Senecal', 4), ('SNKL', ''))
        self.assertEquals(double_metaphone('Sergeaux', 4), ('SRJ', 'SRK'))
        self.assertEquals(double_metaphone('Severance', 4), ('SFRN', ''))
        self.assertEquals(double_metaphone('Sharp', 4), ('XRP', ''))
        self.assertEquals(double_metaphone('Sharpe', 4), ('XRP', ''))
        self.assertEquals(double_metaphone('Sharply', 4), ('XRPL', ''))
        self.assertEquals(double_metaphone('Shatswell', 4), ('XTSL', ''))
        self.assertEquals(double_metaphone('Shattack', 4), ('XTK', ''))
        self.assertEquals(double_metaphone('Shattock', 4), ('XTK', ''))
        self.assertEquals(double_metaphone('Shattuck', 4), ('XTK', ''))
        self.assertEquals(double_metaphone('Shaw', 4), ('X', 'XF'))
        self.assertEquals(double_metaphone('Sheldon', 4), ('XLTN', ''))
        self.assertEquals(double_metaphone('Sherman', 4), ('XRMN', ''))
        self.assertEquals(double_metaphone('Shinn', 4), ('XN', ''))
        self.assertEquals(double_metaphone('Shirford', 4), ('XRFR', ''))
        self.assertEquals(double_metaphone('Shirley', 4), ('XRL', ''))
        self.assertEquals(double_metaphone('Shively', 4), ('XFL', ''))
        self.assertEquals(double_metaphone('Shoemaker', 4), ('XMKR', ''))
        self.assertEquals(double_metaphone('Short', 4), ('XRT', ''))
        self.assertEquals(double_metaphone('Shotwell', 4), ('XTL', ''))
        self.assertEquals(double_metaphone('Shute', 4), ('XT', ''))
        self.assertEquals(double_metaphone('Sibley', 4), ('SPL', ''))
        self.assertEquals(double_metaphone('Silver', 4), ('SLFR', ''))
        self.assertEquals(double_metaphone('Simes', 4), ('SMS', ''))
        self.assertEquals(double_metaphone('Sinken', 4), ('SNKN', ''))
        self.assertEquals(double_metaphone('Sinn', 4), ('SN', ''))
        self.assertEquals(double_metaphone('Skelton', 4), ('SKLT', ''))
        self.assertEquals(double_metaphone('Skiffe', 4), ('SKF', ''))
        self.assertEquals(double_metaphone('Skotkonung', 4), ('SKTK', ''))
        self.assertEquals(double_metaphone('Slade', 4), ('SLT', 'XLT'))
        self.assertEquals(double_metaphone('Slye', 4), ('SL', 'XL'))
        self.assertEquals(double_metaphone('Smedley', 4), ('SMTL', 'XMTL'))
        self.assertEquals(double_metaphone('Smith', 4), ('SM0', 'XMT'))
        self.assertEquals(double_metaphone('Snow', 4), ('SN', 'XNF'))
        self.assertEquals(double_metaphone('Soole', 4), ('SL', ''))
        self.assertEquals(double_metaphone('Soule', 4), ('SL', ''))
        self.assertEquals(double_metaphone('Southworth', 4), ('S0R0', 'STRT'))
        self.assertEquals(double_metaphone('Sowles', 4), ('SLS', ''))
        self.assertEquals(double_metaphone('Spalding', 4), ('SPLT', ''))
        self.assertEquals(double_metaphone('Spark', 4), ('SPRK', ''))
        self.assertEquals(double_metaphone('Spencer', 4), ('SPNS', ''))
        self.assertEquals(double_metaphone('Sperry', 4), ('SPR', ''))
        self.assertEquals(double_metaphone('Spofford', 4), ('SPFR', ''))
        self.assertEquals(double_metaphone('Spooner', 4), ('SPNR', ''))
        self.assertEquals(double_metaphone('Sprague', 4), ('SPRK', ''))
        self.assertEquals(double_metaphone('Springer', 4), ('SPRN', ''))
        self.assertEquals(double_metaphone('St. Clair', 4), ('STKL', ''))
        self.assertEquals(double_metaphone('St. Claire', 4), ('STKL', ''))
        self.assertEquals(double_metaphone('St. Leger', 4), ('STLJ', 'STLK'))
        self.assertEquals(double_metaphone('St. Omer', 4), ('STMR', ''))
        self.assertEquals(double_metaphone('Stafferton', 4), ('STFR', ''))
        self.assertEquals(double_metaphone('Stafford', 4), ('STFR', ''))
        self.assertEquals(double_metaphone('Stalham', 4), ('STLM', ''))
        self.assertEquals(double_metaphone('Stanford', 4), ('STNF', ''))
        self.assertEquals(double_metaphone('Stanton', 4), ('STNT', ''))
        self.assertEquals(double_metaphone('Star', 4), ('STR', ''))
        self.assertEquals(double_metaphone('Starbuck', 4), ('STRP', ''))
        self.assertEquals(double_metaphone('Starkey', 4), ('STRK', ''))
        self.assertEquals(double_metaphone('Starkweather', 4), ('STRK', ''))
        self.assertEquals(double_metaphone('Stearns', 4), ('STRN', ''))
        self.assertEquals(double_metaphone('Stebbins', 4), ('STPN', ''))
        self.assertEquals(double_metaphone('Steele', 4), ('STL', ''))
        self.assertEquals(double_metaphone('Stephenson', 4), ('STFN', ''))
        self.assertEquals(double_metaphone('Stevens', 4), ('STFN', ''))
        self.assertEquals(double_metaphone('Stoddard', 4), ('STTR', ''))
        self.assertEquals(double_metaphone('Stodder', 4), ('STTR', ''))
        self.assertEquals(double_metaphone('Stone', 4), ('STN', ''))
        self.assertEquals(double_metaphone('Storey', 4), ('STR', ''))
        self.assertEquals(double_metaphone('Storrada', 4), ('STRT', ''))
        self.assertEquals(double_metaphone('Story', 4), ('STR', ''))
        self.assertEquals(double_metaphone('Stoughton', 4), ('STFT', ''))
        self.assertEquals(double_metaphone('Stout', 4), ('STT', ''))
        self.assertEquals(double_metaphone('Stow', 4), ('ST', 'STF'))
        self.assertEquals(double_metaphone('Strong', 4), ('STRN', ''))
        self.assertEquals(double_metaphone('Strutt', 4), ('STRT', ''))
        self.assertEquals(double_metaphone('Stryker', 4), ('STRK', ''))
        self.assertEquals(double_metaphone('Stuckeley', 4), ('STKL', ''))
        self.assertEquals(double_metaphone('Sturges', 4), ('STRJ', 'STRK'))
        self.assertEquals(double_metaphone('Sturgess', 4), ('STRJ', 'STRK'))
        self.assertEquals(double_metaphone('Sturgis', 4), ('STRJ', 'STRK'))
        self.assertEquals(double_metaphone('Suevain', 4), ('SFN', ''))
        self.assertEquals(double_metaphone('Sulyard', 4), ('SLRT', ''))
        self.assertEquals(double_metaphone('Sutton', 4), ('STN', ''))
        self.assertEquals(double_metaphone('Swain', 4), ('SN', 'XN'))
        self.assertEquals(double_metaphone('Swayne', 4), ('SN', 'XN'))
        self.assertEquals(double_metaphone('Swayze', 4), ('SS', 'XTS'))
        self.assertEquals(double_metaphone('Swift', 4), ('SFT', 'XFT'))
        self.assertEquals(double_metaphone('Taber', 4), ('TPR', ''))
        self.assertEquals(double_metaphone('Talcott', 4), ('TLKT', ''))
        self.assertEquals(double_metaphone('Tarne', 4), ('TRN', ''))
        self.assertEquals(double_metaphone('Tatum', 4), ('TTM', ''))
        self.assertEquals(double_metaphone('Taverner', 4), ('TFRN', ''))
        self.assertEquals(double_metaphone('Taylor', 4), ('TLR', ''))
        self.assertEquals(double_metaphone('Tenney', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Thayer', 4), ('0R', 'TR'))
        self.assertEquals(double_metaphone('Thember', 4), ('0MPR', 'TMPR'))
        self.assertEquals(double_metaphone('Thomas', 4), ('TMS', ''))
        self.assertEquals(double_metaphone('Thompson', 4), ('TMPS', ''))
        self.assertEquals(double_metaphone('Thorne', 4), ('0RN', 'TRN'))
        self.assertEquals(double_metaphone('Thornycraft', 4), ('0RNK', 'TRNK'))
        self.assertEquals(double_metaphone('Threlkeld', 4), ('0RLK', 'TRLK'))
        self.assertEquals(double_metaphone('Throckmorton', 4), ('0RKM', 'TRKM'))
        self.assertEquals(double_metaphone('Thwaits', 4), ('0TS', 'TTS'))
        self.assertEquals(double_metaphone('Tibbetts', 4), ('TPTS', ''))
        self.assertEquals(double_metaphone('Tidd', 4), ('TT', ''))
        self.assertEquals(double_metaphone('Tierney', 4), ('TRN', ''))
        self.assertEquals(double_metaphone('Tilley', 4), ('TL', ''))
        self.assertEquals(double_metaphone('Tillieres', 4), ('TLRS', ''))
        self.assertEquals(double_metaphone('Tilly', 4), ('TL', ''))
        self.assertEquals(double_metaphone('Tisdale', 4), ('TSTL', ''))
        self.assertEquals(double_metaphone('Titus', 4), ('TTS', ''))
        self.assertEquals(double_metaphone('Tobey', 4), ('TP', ''))
        self.assertEquals(double_metaphone('Tooker', 4), ('TKR', ''))
        self.assertEquals(double_metaphone('Towle', 4), ('TL', ''))
        self.assertEquals(double_metaphone('Towne', 4), ('TN', ''))
        self.assertEquals(double_metaphone('Townsend', 4), ('TNSN', ''))
        self.assertEquals(double_metaphone('Treadway', 4), ('TRT', ''))
        self.assertEquals(double_metaphone('Trelawney', 4), ('TRLN', ''))
        self.assertEquals(double_metaphone('Trinder', 4), ('TRNT', ''))
        self.assertEquals(double_metaphone('Tripp', 4), ('TRP', ''))
        self.assertEquals(double_metaphone('Trippe', 4), ('TRP', ''))
        self.assertEquals(double_metaphone('Trott', 4), ('TRT', ''))
        self.assertEquals(double_metaphone('True', 4), ('TR', ''))
        self.assertEquals(double_metaphone('Trussebut', 4), ('TRSP', ''))
        self.assertEquals(double_metaphone('Tucker', 4), ('TKR', ''))
        self.assertEquals(double_metaphone('Turgeon', 4), ('TRJN', 'TRKN'))
        self.assertEquals(double_metaphone('Turner', 4), ('TRNR', ''))
        self.assertEquals(double_metaphone('Tuttle', 4), ('TTL', ''))
        self.assertEquals(double_metaphone('Tyler', 4), ('TLR', ''))
        self.assertEquals(double_metaphone('Tylle', 4), ('TL', ''))
        self.assertEquals(double_metaphone('Tyrrel', 4), ('TRL', ''))
        self.assertEquals(double_metaphone('Ua Tuathail', 4), ('AT0L', 'ATTL'))
        self.assertEquals(double_metaphone('Ulrich', 4), ('ALRX', 'ALRK'))
        self.assertEquals(double_metaphone('Underhill', 4), ('ANTR', ''))
        self.assertEquals(double_metaphone('Underwood', 4), ('ANTR', ''))
        self.assertEquals(double_metaphone('Unknown', 4), ('ANKN', ''))
        self.assertEquals(double_metaphone('Valentine', 4), ('FLNT', ''))
        self.assertEquals(double_metaphone('Van Egmond', 4), ('FNKM', ''))
        self.assertEquals(double_metaphone('Van der Beek', 4), ('FNTR', ''))
        self.assertEquals(double_metaphone('Vaughan', 4), ('FKN', ''))
        self.assertEquals(double_metaphone('Vermenlen', 4), ('FRMN', ''))
        self.assertEquals(double_metaphone('Vincent', 4), ('FNSN', ''))
        self.assertEquals(double_metaphone('Volentine', 4), ('FLNT', ''))
        self.assertEquals(double_metaphone('Wagner', 4), ('AKNR', 'FKNR'))
        self.assertEquals(double_metaphone('Waite', 4), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Walker', 4), ('ALKR', 'FLKR'))
        self.assertEquals(double_metaphone('Walter', 4), ('ALTR', 'FLTR'))
        self.assertEquals(double_metaphone('Wandell', 4), ('ANTL', 'FNTL'))
        self.assertEquals(double_metaphone('Wandesford', 4), ('ANTS', 'FNTS'))
        self.assertEquals(double_metaphone('Warbleton', 4), ('ARPL', 'FRPL'))
        self.assertEquals(double_metaphone('Ward', 4), ('ART', 'FRT'))
        self.assertEquals(double_metaphone('Warde', 4), ('ART', 'FRT'))
        self.assertEquals(double_metaphone('Ware', 4), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wareham', 4), ('ARHM', 'FRHM'))
        self.assertEquals(double_metaphone('Warner', 4), ('ARNR', 'FRNR'))
        self.assertEquals(double_metaphone('Warren', 4), ('ARN', 'FRN'))
        self.assertEquals(double_metaphone('Washburne', 4), ('AXPR', 'FXPR'))
        self.assertEquals(double_metaphone('Waterbury', 4), ('ATRP', 'FTRP'))
        self.assertEquals(double_metaphone('Watson', 4), ('ATSN', 'FTSN'))
        self.assertEquals(double_metaphone('WatsonEllithorpe', 4),
                          ('ATSN', 'FTSN'))
        self.assertEquals(double_metaphone('Watts', 4), ('ATS', 'FTS'))
        self.assertEquals(double_metaphone('Wayne', 4), ('AN', 'FN'))
        self.assertEquals(double_metaphone('Webb', 4), ('AP', 'FP'))
        self.assertEquals(double_metaphone('Weber', 4), ('APR', 'FPR'))
        self.assertEquals(double_metaphone('Webster', 4), ('APST', 'FPST'))
        self.assertEquals(double_metaphone('Weed', 4), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Weeks', 4), ('AKS', 'FKS'))
        self.assertEquals(double_metaphone('Wells', 4), ('ALS', 'FLS'))
        self.assertEquals(double_metaphone('Wenzell', 4), ('ANSL', 'FNTS'))
        self.assertEquals(double_metaphone('West', 4), ('AST', 'FST'))
        self.assertEquals(double_metaphone('Westbury', 4), ('ASTP', 'FSTP'))
        self.assertEquals(double_metaphone('Whatlocke', 4), ('ATLK', ''))
        self.assertEquals(double_metaphone('Wheeler', 4), ('ALR', ''))
        self.assertEquals(double_metaphone('Whiston', 4), ('ASTN', ''))
        self.assertEquals(double_metaphone('White', 4), ('AT', ''))
        self.assertEquals(double_metaphone('Whitman', 4), ('ATMN', ''))
        self.assertEquals(double_metaphone('Whiton', 4), ('ATN', ''))
        self.assertEquals(double_metaphone('Whitson', 4), ('ATSN', ''))
        self.assertEquals(double_metaphone('Wickes', 4), ('AKS', 'FKS'))
        self.assertEquals(double_metaphone('Wilbur', 4), ('ALPR', 'FLPR'))
        self.assertEquals(double_metaphone('Wilcotes', 4), ('ALKT', 'FLKT'))
        self.assertEquals(double_metaphone('Wilkinson', 4), ('ALKN', 'FLKN'))
        self.assertEquals(double_metaphone('Willets', 4), ('ALTS', 'FLTS'))
        self.assertEquals(double_metaphone('Willett', 4), ('ALT', 'FLT'))
        self.assertEquals(double_metaphone('Willey', 4), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Williams', 4), ('ALMS', 'FLMS'))
        self.assertEquals(double_metaphone('Williston', 4), ('ALST', 'FLST'))
        self.assertEquals(double_metaphone('Wilson', 4), ('ALSN', 'FLSN'))
        self.assertEquals(double_metaphone('Wimes', 4), ('AMS', 'FMS'))
        self.assertEquals(double_metaphone('Winch', 4), ('ANX', 'FNK'))
        self.assertEquals(double_metaphone('Winegar', 4), ('ANKR', 'FNKR'))
        self.assertEquals(double_metaphone('Wing', 4), ('ANK', 'FNK'))
        self.assertEquals(double_metaphone('Winsley', 4), ('ANSL', 'FNSL'))
        self.assertEquals(double_metaphone('Winslow', 4), ('ANSL', 'FNSL'))
        self.assertEquals(double_metaphone('Winthrop', 4), ('AN0R', 'FNTR'))
        self.assertEquals(double_metaphone('Wise', 4), ('AS', 'FS'))
        self.assertEquals(double_metaphone('Wood', 4), ('AT', 'FT'))
        self.assertEquals(double_metaphone('Woodbridge', 4), ('ATPR', 'FTPR'))
        self.assertEquals(double_metaphone('Woodward', 4), ('ATRT', 'FTRT'))
        self.assertEquals(double_metaphone('Wooley', 4), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Woolley', 4), ('AL', 'FL'))
        self.assertEquals(double_metaphone('Worth', 4), ('AR0', 'FRT'))
        self.assertEquals(double_metaphone('Worthen', 4), ('AR0N', 'FRTN'))
        self.assertEquals(double_metaphone('Worthley', 4), ('AR0L', 'FRTL'))
        self.assertEquals(double_metaphone('Wright', 4), ('RT', ''))
        self.assertEquals(double_metaphone('Wyer', 4), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wyere', 4), ('AR', 'FR'))
        self.assertEquals(double_metaphone('Wynkoop', 4), ('ANKP', 'FNKP'))
        self.assertEquals(double_metaphone('Yarnall', 4), ('ARNL', ''))
        self.assertEquals(double_metaphone('Yeoman', 4), ('AMN', ''))
        self.assertEquals(double_metaphone('Yorke', 4), ('ARK', ''))
        self.assertEquals(double_metaphone('Young', 4), ('ANK', ''))
        self.assertEquals(double_metaphone('ab Wennonwen', 4), ('APNN', ''))
        self.assertEquals(double_metaphone('ap Llewellyn', 4), ('APLL', ''))
        self.assertEquals(double_metaphone('ap Lorwerth', 4), ('APLR', ''))
        self.assertEquals(double_metaphone('d\'Angouleme', 4), ('TNKL', ''))
        self.assertEquals(double_metaphone('de Audeham', 4), ('TTHM', ''))
        self.assertEquals(double_metaphone('de Bavant', 4), ('TPFN', ''))
        self.assertEquals(double_metaphone('de Beauchamp', 4), ('TPXM', 'TPKM'))
        self.assertEquals(double_metaphone('de Beaumont', 4), ('TPMN', ''))
        self.assertEquals(double_metaphone('de Bolbec', 4), ('TPLP', ''))
        self.assertEquals(double_metaphone('de Braiose', 4), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Braose', 4), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Briwere', 4), ('TPRR', ''))
        self.assertEquals(double_metaphone('de Cantelou', 4), ('TKNT', ''))
        self.assertEquals(double_metaphone('de Cherelton', 4), ('TXRL', 'TKRL'))
        self.assertEquals(double_metaphone('de Cherleton', 4), ('TXRL', 'TKRL'))
        self.assertEquals(double_metaphone('de Clare', 4), ('TKLR', ''))
        self.assertEquals(double_metaphone('de Claremont', 4), ('TKLR', ''))
        self.assertEquals(double_metaphone('de Clifford', 4), ('TKLF', ''))
        self.assertEquals(double_metaphone('de Colville', 4), ('TKLF', ''))
        self.assertEquals(double_metaphone('de Courtenay', 4), ('TKRT', ''))
        self.assertEquals(double_metaphone('de Fauconberg', 4), ('TFKN', ''))
        self.assertEquals(double_metaphone('de Forest', 4), ('TFRS', ''))
        self.assertEquals(double_metaphone('de Gai', 4), ('TK', ''))
        self.assertEquals(double_metaphone('de Grey', 4), ('TKR', ''))
        self.assertEquals(double_metaphone('de Guernons', 4), ('TKRN', ''))
        self.assertEquals(double_metaphone('de Haia', 4), ('T', ''))
        self.assertEquals(double_metaphone('de Harcourt', 4), ('TRKR', ''))
        self.assertEquals(double_metaphone('de Hastings', 4), ('TSTN', ''))
        self.assertEquals(double_metaphone('de Hoke', 4), ('TK', ''))
        self.assertEquals(double_metaphone('de Hooch', 4), ('TK', ''))
        self.assertEquals(double_metaphone('de Hugelville', 4),
                          ('TJLF', 'TKLF'))
        self.assertEquals(double_metaphone('de Huntingdon', 4), ('TNTN', ''))
        self.assertEquals(double_metaphone('de Insula', 4), ('TNSL', ''))
        self.assertEquals(double_metaphone('de Keynes', 4), ('TKNS', ''))
        self.assertEquals(double_metaphone('de Lacy', 4), ('TLS', ''))
        self.assertEquals(double_metaphone('de Lexington', 4), ('TLKS', ''))
        self.assertEquals(double_metaphone('de Lusignan', 4), ('TLSN', 'TLSK'))
        self.assertEquals(double_metaphone('de Manvers', 4), ('TMNF', ''))
        self.assertEquals(double_metaphone('de Montagu', 4), ('TMNT', ''))
        self.assertEquals(double_metaphone('de Montault', 4), ('TMNT', ''))
        self.assertEquals(double_metaphone('de Montfort', 4), ('TMNT', ''))
        self.assertEquals(double_metaphone('de Mortimer', 4), ('TMRT', ''))
        self.assertEquals(double_metaphone('de Morville', 4), ('TMRF', ''))
        self.assertEquals(double_metaphone('de Morvois', 4), ('TMRF', ''))
        self.assertEquals(double_metaphone('de Neufmarche', 4), ('TNFM', ''))
        self.assertEquals(double_metaphone('de Odingsells', 4), ('TTNK', ''))
        self.assertEquals(double_metaphone('de Odyngsells', 4), ('TTNK', ''))
        self.assertEquals(double_metaphone('de Percy', 4), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Pierrepont', 4), ('TPRP', ''))
        self.assertEquals(double_metaphone('de Plessetis', 4), ('TPLS', ''))
        self.assertEquals(double_metaphone('de Porhoet', 4), ('TPRT', ''))
        self.assertEquals(double_metaphone('de Prouz', 4), ('TPRS', ''))
        self.assertEquals(double_metaphone('de Quincy', 4), ('TKNS', ''))
        self.assertEquals(double_metaphone('de Ripellis', 4), ('TRPL', ''))
        self.assertEquals(double_metaphone('de Ros', 4), ('TRS', ''))
        self.assertEquals(double_metaphone('de Salisbury', 4), ('TSLS', ''))
        self.assertEquals(double_metaphone('de Sanford', 4), ('TSNF', ''))
        self.assertEquals(double_metaphone('de Somery', 4), ('TSMR', ''))
        self.assertEquals(double_metaphone('de St. Hilary', 4), ('TSTL', ''))
        self.assertEquals(double_metaphone('de St. Liz', 4), ('TSTL', ''))
        self.assertEquals(double_metaphone('de Sutton', 4), ('TSTN', ''))
        self.assertEquals(double_metaphone('de Toeni', 4), ('TTN', ''))
        self.assertEquals(double_metaphone('de Tony', 4), ('TTN', ''))
        self.assertEquals(double_metaphone('de Umfreville', 4), ('TMFR', ''))
        self.assertEquals(double_metaphone('de Valognes', 4), ('TFLN', 'TFLK'))
        self.assertEquals(double_metaphone('de Vaux', 4), ('TF', ''))
        self.assertEquals(double_metaphone('de Vere', 4), ('TFR', ''))
        self.assertEquals(double_metaphone('de Vermandois', 4), ('TFRM', ''))
        self.assertEquals(double_metaphone('de Vernon', 4), ('TFRN', ''))
        self.assertEquals(double_metaphone('de Vexin', 4), ('TFKS', ''))
        self.assertEquals(double_metaphone('de Vitre', 4), ('TFTR', ''))
        self.assertEquals(double_metaphone('de Wandesford', 4), ('TNTS', ''))
        self.assertEquals(double_metaphone('de Warenne', 4), ('TRN', ''))
        self.assertEquals(double_metaphone('de Westbury', 4), ('TSTP', ''))
        self.assertEquals(double_metaphone('di Saluzzo', 4), ('TSLS', 'TSLT'))
        self.assertEquals(double_metaphone('fitz Alan', 4), ('FTSL', ''))
        self.assertEquals(double_metaphone('fitz Geoffrey', 4),
                          ('FTSJ', 'FTSK'))
        self.assertEquals(double_metaphone('fitz Herbert', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz John', 4), ('FTSJ', ''))
        self.assertEquals(double_metaphone('fitz Patrick', 4), ('FTSP', ''))
        self.assertEquals(double_metaphone('fitz Payn', 4), ('FTSP', ''))
        self.assertEquals(double_metaphone('fitz Piers', 4), ('FTSP', ''))
        self.assertEquals(double_metaphone('fitz Randolph', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Richard', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Robert', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Roy', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Scrob', 4), ('FTSS', ''))
        self.assertEquals(double_metaphone('fitz Walter', 4), ('FTSL', ''))
        self.assertEquals(double_metaphone('fitz Warin', 4), ('FTSR', ''))
        self.assertEquals(double_metaphone('fitz Williams', 4), ('FTSL', ''))
        self.assertEquals(double_metaphone('la Zouche', 4), ('LSX', 'LSK'))
        self.assertEquals(double_metaphone('le Botiller', 4), ('LPTL', ''))
        self.assertEquals(double_metaphone('le Despenser', 4), ('LTSP', ''))
        self.assertEquals(double_metaphone('le deSpencer', 4), ('LTSP', ''))
        self.assertEquals(double_metaphone('of Allendale', 4), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Angouleme', 4), ('AFNK', ''))
        self.assertEquals(double_metaphone('of Anjou', 4), ('AFNJ', ''))
        self.assertEquals(double_metaphone('of Aquitaine', 4), ('AFKT', ''))
        self.assertEquals(double_metaphone('of Aumale', 4), ('AFML', ''))
        self.assertEquals(double_metaphone('of Bavaria', 4), ('AFPF', ''))
        self.assertEquals(double_metaphone('of Boulogne', 4), ('AFPL', ''))
        self.assertEquals(double_metaphone('of Brittany', 4), ('AFPR', ''))
        self.assertEquals(double_metaphone('of Brittary', 4), ('AFPR', ''))
        self.assertEquals(double_metaphone('of Castile', 4), ('AFKS', ''))
        self.assertEquals(double_metaphone('of Chester', 4), ('AFXS', 'AFKS'))
        self.assertEquals(double_metaphone('of Clermont', 4), ('AFKL', ''))
        self.assertEquals(double_metaphone('of Cologne', 4), ('AFKL', ''))
        self.assertEquals(double_metaphone('of Dinan', 4), ('AFTN', ''))
        self.assertEquals(double_metaphone('of Dunbar', 4), ('AFTN', ''))
        self.assertEquals(double_metaphone('of England', 4), ('AFNK', ''))
        self.assertEquals(double_metaphone('of Essex', 4), ('AFSK', ''))
        self.assertEquals(double_metaphone('of Falaise', 4), ('AFFL', ''))
        self.assertEquals(double_metaphone('of Flanders', 4), ('AFFL', ''))
        self.assertEquals(double_metaphone('of Galloway', 4), ('AFKL', ''))
        self.assertEquals(double_metaphone('of Germany', 4), ('AFKR', 'AFJR'))
        self.assertEquals(double_metaphone('of Gloucester', 4), ('AFKL', ''))
        self.assertEquals(double_metaphone('of Heristal', 4), ('AFRS', ''))
        self.assertEquals(double_metaphone('of Hungary', 4), ('AFNK', ''))
        self.assertEquals(double_metaphone('of Huntington', 4), ('AFNT', ''))
        self.assertEquals(double_metaphone('of Kiev', 4), ('AFKF', ''))
        self.assertEquals(double_metaphone('of Kuno', 4), ('AFKN', ''))
        self.assertEquals(double_metaphone('of Landen', 4), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Laon', 4), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Leinster', 4), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Lens', 4), ('AFLN', ''))
        self.assertEquals(double_metaphone('of Lorraine', 4), ('AFLR', ''))
        self.assertEquals(double_metaphone('of Louvain', 4), ('AFLF', ''))
        self.assertEquals(double_metaphone('of Mercia', 4), ('AFMR', ''))
        self.assertEquals(double_metaphone('of Metz', 4), ('AFMT', ''))
        self.assertEquals(double_metaphone('of Meulan', 4), ('AFML', ''))
        self.assertEquals(double_metaphone('of Nass', 4), ('AFNS', ''))
        self.assertEquals(double_metaphone('of Normandy', 4), ('AFNR', ''))
        self.assertEquals(double_metaphone('of Ohningen', 4), ('AFNN', ''))
        self.assertEquals(double_metaphone('of Orleans', 4), ('AFRL', ''))
        self.assertEquals(double_metaphone('of Poitou', 4), ('AFPT', ''))
        self.assertEquals(double_metaphone('of Polotzk', 4), ('AFPL', ''))
        self.assertEquals(double_metaphone('of Provence', 4), ('AFPR', ''))
        self.assertEquals(double_metaphone('of Ringelheim', 4), ('AFRN', ''))
        self.assertEquals(double_metaphone('of Salisbury', 4), ('AFSL', ''))
        self.assertEquals(double_metaphone('of Saxony', 4), ('AFSK', ''))
        self.assertEquals(double_metaphone('of Scotland', 4), ('AFSK', ''))
        self.assertEquals(double_metaphone('of Senlis', 4), ('AFSN', ''))
        self.assertEquals(double_metaphone('of Stafford', 4), ('AFST', ''))
        self.assertEquals(double_metaphone('of Swabia', 4), ('AFSP', ''))
        self.assertEquals(double_metaphone('of Tongres', 4), ('AFTN', ''))
        self.assertEquals(double_metaphone('of the Tributes', 4),
                          ('AF0T', 'AFTT'))
        self.assertEquals(double_metaphone('unknown', 4), ('ANKN', ''))
        self.assertEquals(double_metaphone('van der Gouda', 4), ('FNTR', ''))
        self.assertEquals(double_metaphone('von Adenbaugh', 4), ('FNTN', ''))
        self.assertEquals(double_metaphone('ARCHITure', 4), ('ARKT', ''))
        self.assertEquals(double_metaphone('Arnoff', 4), ('ARNF', ''))
        self.assertEquals(double_metaphone('Arnow', 4), ('ARN', 'ARNF'))
        self.assertEquals(double_metaphone('DANGER', 4), ('TNJR', 'TNKR'))
        self.assertEquals(double_metaphone('Jankelowicz', 4), ('JNKL', 'ANKL'))
        self.assertEquals(double_metaphone('MANGER', 4), ('MNJR', 'MNKR'))
        self.assertEquals(double_metaphone('McClellan', 4), ('MKLL', ''))
        self.assertEquals(double_metaphone('McHugh', 4), ('MK', ''))
        self.assertEquals(double_metaphone('McLaughlin', 4), ('MKLF', ''))
        self.assertEquals(double_metaphone('ORCHEStra', 4), ('ARKS', ''))
        self.assertEquals(double_metaphone('ORCHID', 4), ('ARKT', ''))
        self.assertEquals(double_metaphone('Pierce', 4), ('PRS', ''))
        self.assertEquals(double_metaphone('RANGER', 4), ('RNJR', 'RNKR'))
        self.assertEquals(double_metaphone('Schlesinger', 4), ('XLSN', 'SLSN'))
        self.assertEquals(double_metaphone('Uomo', 4), ('AM', ''))
        self.assertEquals(double_metaphone('Vasserman', 4), ('FSRM', ''))
        self.assertEquals(double_metaphone('Wasserman', 4), ('ASRM', 'FSRM'))
        self.assertEquals(double_metaphone('Womo', 4), ('AM', 'FM'))
        self.assertEquals(double_metaphone('Yankelovich', 4), ('ANKL', ''))
        self.assertEquals(double_metaphone('accede', 4), ('AKST', ''))
        self.assertEquals(double_metaphone('accident', 4), ('AKST', ''))
        self.assertEquals(double_metaphone('adelsheim', 4), ('ATLS', ''))
        self.assertEquals(double_metaphone('aged', 4), ('AJT', 'AKT'))
        self.assertEquals(double_metaphone('ageless', 4), ('AJLS', 'AKLS'))
        self.assertEquals(double_metaphone('agency', 4), ('AJNS', 'AKNS'))
        self.assertEquals(double_metaphone('aghast', 4), ('AKST', ''))
        self.assertEquals(double_metaphone('agio', 4), ('AJ', 'AK'))
        self.assertEquals(double_metaphone('agrimony', 4), ('AKRM', ''))
        self.assertEquals(double_metaphone('album', 4), ('ALPM', ''))
        self.assertEquals(double_metaphone('alcmene', 4), ('ALKM', ''))
        self.assertEquals(double_metaphone('alehouse', 4), ('ALHS', ''))
        self.assertEquals(double_metaphone('antique', 4), ('ANTK', ''))
        self.assertEquals(double_metaphone('artois', 4), ('ART', 'ARTS'))
        self.assertEquals(double_metaphone('automation', 4), ('ATMX', ''))
        self.assertEquals(double_metaphone('bacchus', 4), ('PKS', ''))
        self.assertEquals(double_metaphone('bacci', 4), ('PX', ''))
        self.assertEquals(double_metaphone('bajador', 4), ('PJTR', 'PHTR'))
        self.assertEquals(double_metaphone('bellocchio', 4), ('PLX', ''))
        self.assertEquals(double_metaphone('bertucci', 4), ('PRTX', ''))
        self.assertEquals(double_metaphone('biaggi', 4), ('PJ', 'PK'))
        self.assertEquals(double_metaphone('bough', 4), ('P', ''))
        self.assertEquals(double_metaphone('breaux', 4), ('PR', ''))
        self.assertEquals(double_metaphone('broughton', 4), ('PRTN', ''))
        self.assertEquals(double_metaphone('cabrillo', 4), ('KPRL', 'KPR'))
        self.assertEquals(double_metaphone('caesar', 4), ('SSR', ''))
        self.assertEquals(double_metaphone('cagney', 4), ('KKN', ''))
        self.assertEquals(double_metaphone('campbell', 4), ('KMPL', ''))
        self.assertEquals(double_metaphone('carlisle', 4), ('KRLL', ''))
        self.assertEquals(double_metaphone('carlysle', 4), ('KRLL', ''))
        self.assertEquals(double_metaphone('chemistry', 4), ('KMST', ''))
        self.assertEquals(double_metaphone('chianti', 4), ('KNT', ''))
        self.assertEquals(double_metaphone('chorus', 4), ('KRS', ''))
        self.assertEquals(double_metaphone('cough', 4), ('KF', ''))
        self.assertEquals(double_metaphone('czerny', 4), ('SRN', 'XRN'))
        self.assertEquals(double_metaphone('deffenbacher', 4), ('TFNP', ''))
        self.assertEquals(double_metaphone('dumb', 4), ('TM', ''))
        self.assertEquals(double_metaphone('edgar', 4), ('ATKR', ''))
        self.assertEquals(double_metaphone('edge', 4), ('AJ', ''))
        self.assertEquals(double_metaphone('filipowicz', 4), ('FLPT', 'FLPF'))
        self.assertEquals(double_metaphone('focaccia', 4), ('FKX', ''))
        self.assertEquals(double_metaphone('gallegos', 4), ('KLKS', 'KKS'))
        self.assertEquals(double_metaphone('gambrelli', 4), ('KMPR', ''))
        self.assertEquals(double_metaphone('geithain', 4), ('K0N', 'JTN'))
        self.assertEquals(double_metaphone('ghiradelli', 4), ('JRTL', ''))
        self.assertEquals(double_metaphone('ghislane', 4), ('JLN', ''))
        self.assertEquals(double_metaphone('gough', 4), ('KF', ''))
        self.assertEquals(double_metaphone('hartheim', 4), ('HR0M', 'HRTM'))
        self.assertEquals(double_metaphone('heimsheim', 4), ('HMSM', ''))
        self.assertEquals(double_metaphone('hochmeier', 4), ('HKMR', ''))
        self.assertEquals(double_metaphone('hugh', 4), ('H', ''))
        self.assertEquals(double_metaphone('hunger', 4), ('HNKR', 'HNJR'))
        self.assertEquals(double_metaphone('hungry', 4), ('HNKR', ''))
        self.assertEquals(double_metaphone('island', 4), ('ALNT', ''))
        self.assertEquals(double_metaphone('isle', 4), ('AL', ''))
        self.assertEquals(double_metaphone('jose', 4), ('HS', ''))
        self.assertEquals(double_metaphone('laugh', 4), ('LF', ''))
        self.assertEquals(double_metaphone('mac caffrey', 4), ('MKFR', ''))
        self.assertEquals(double_metaphone('mac gregor', 4), ('MKRK', ''))
        self.assertEquals(double_metaphone('pegnitz', 4), ('PNTS', 'PKNT'))
        self.assertEquals(double_metaphone('piskowitz', 4), ('PSKT', 'PSKF'))
        self.assertEquals(double_metaphone('queen', 4), ('KN', ''))
        self.assertEquals(double_metaphone('raspberry', 4), ('RSPR', ''))
        self.assertEquals(double_metaphone('resnais', 4), ('RSN', 'RSNS'))
        self.assertEquals(double_metaphone('rogier', 4), ('RJ', 'RJR'))
        self.assertEquals(double_metaphone('rough', 4), ('RF', ''))
        self.assertEquals(double_metaphone('san jacinto', 4), ('SNHS', ''))
        self.assertEquals(double_metaphone('schenker', 4), ('XNKR', 'SKNK'))
        self.assertEquals(double_metaphone('schermerhorn', 4), ('XRMR', 'SKRM'))
        self.assertEquals(double_metaphone('schmidt', 4), ('XMT', 'SMT'))
        self.assertEquals(double_metaphone('schneider', 4), ('XNTR', 'SNTR'))
        self.assertEquals(double_metaphone('school', 4), ('SKL', ''))
        self.assertEquals(double_metaphone('schooner', 4), ('SKNR', ''))
        self.assertEquals(double_metaphone('schrozberg', 4), ('XRSP', 'SRSP'))
        self.assertEquals(double_metaphone('schulman', 4), ('XLMN', ''))
        self.assertEquals(double_metaphone('schwabach', 4), ('XPK', 'XFPK'))
        self.assertEquals(double_metaphone('schwarzach', 4), ('XRSK', 'XFRT'))
        self.assertEquals(double_metaphone('smith', 4), ('SM0', 'XMT'))
        self.assertEquals(double_metaphone('snider', 4), ('SNTR', 'XNTR'))
        self.assertEquals(double_metaphone('succeed', 4), ('SKST', ''))
        self.assertEquals(double_metaphone('sugarcane', 4), ('XKRK', 'SKRK'))
        self.assertEquals(double_metaphone('svobodka', 4), ('SFPT', ''))
        self.assertEquals(double_metaphone('tagliaro', 4), ('TKLR', 'TLR'))
        self.assertEquals(double_metaphone('thames', 4), ('TMS', ''))
        self.assertEquals(double_metaphone('theilheim', 4), ('0LM', 'TLM'))
        self.assertEquals(double_metaphone('thomas', 4), ('TMS', ''))
        self.assertEquals(double_metaphone('thumb', 4), ('0M', 'TM'))
        self.assertEquals(double_metaphone('tichner', 4), ('TXNR', 'TKNR'))
        self.assertEquals(double_metaphone('tough', 4), ('TF', ''))
        self.assertEquals(double_metaphone('umbrella', 4), ('AMPR', ''))
        self.assertEquals(double_metaphone('vilshofen', 4), ('FLXF', ''))
        self.assertEquals(double_metaphone('von schuller', 4), ('FNXL', ''))
        self.assertEquals(double_metaphone('wachtler', 4), ('AKTL', 'FKTL'))
        self.assertEquals(double_metaphone('wechsler', 4), ('AKSL', 'FKSL'))
        self.assertEquals(double_metaphone('weikersheim', 4), ('AKRS', 'FKRS'))
        self.assertEquals(double_metaphone('zhao', 4), ('J', ''))


class caverphone_test_cases(unittest.TestCase):
    def test_caverphone2(self):
        self.assertEquals(caverphone(''), '1111111111')
        self.assertEquals(caverphone('', 2), '1111111111')
        self.assertEquals(caverphone('', version=2), '1111111111')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEquals(caverphone('Henrichsen'), 'ANRKSN1111')
        self.assertEquals(caverphone('Henricsson'), 'ANRKSN1111')
        self.assertEquals(caverphone('Henriksson'), 'ANRKSN1111')
        self.assertEquals(caverphone('Hinrichsen'), 'ANRKSN1111')
        self.assertEquals(caverphone('Izchaki'), 'ASKKA11111')
        self.assertEquals(caverphone('Maclaverty'), 'MKLFTA1111')
        self.assertEquals(caverphone('Mccleverty'), 'MKLFTA1111')
        self.assertEquals(caverphone('Mcclifferty'), 'MKLFTA1111')
        self.assertEquals(caverphone('Mclafferty'), 'MKLFTA1111')
        self.assertEquals(caverphone('Mclaverty'), 'MKLFTA1111')
        self.assertEquals(caverphone('Slocomb'), 'SLKM111111')
        self.assertEquals(caverphone('Slocombe'), 'SLKM111111')
        self.assertEquals(caverphone('Slocumb'), 'SLKM111111')
        self.assertEquals(caverphone('Whitlam'), 'WTLM111111')

        # http://caversham.otago.ac.nz/files/working/ctp150804.pdf
        self.assertEquals(caverphone('Stevenson'), 'STFNSN1111')
        self.assertEquals(caverphone('Peter'), 'PTA1111111')
        for w in ('Darda', 'Datha', 'Dedie', 'Deedee', 'Deerdre', 'Deidre',
                  'Deirdre', 'Detta', 'Didi', 'Didier', 'Dido', 'Dierdre',
                  'Dieter', 'Dita', 'Ditter', 'Dodi', 'Dodie', 'Dody',
                  'Doherty', 'Dorthea', 'Dorthy', 'Doti', 'Dotti', 'Dottie',
                  'Dotty', 'Doty', 'Doughty', 'Douty', 'Dowdell', 'Duthie',
                  'Tada', 'Taddeo', 'Tadeo', 'Tadio', 'Tati', 'Teador', 'Tedda',
                  'Tedder', 'Teddi', 'Teddie', 'Teddy', 'Tedi', 'Tedie',
                  'Teeter', 'Teodoor', 'Teodor', 'Terti', 'Theda', 'Theodor',
                  'Theodore', 'Theta', 'Thilda', 'Thordia', 'Tilda', 'Tildi',
                  'Tildie', 'Tildy', 'Tita', 'Tito', 'Tjader', 'Toddie',
                  'Toddy', 'Torto', 'Tuddor', 'Tudor', 'Turtle', 'Tuttle',
                  'Tutto'):
            self.assertEqual(caverphone(w), 'TTA1111111')
            self.assertEqual(caverphone(w, 2), 'TTA1111111')
            self.assertEqual(caverphone(w, version=2), 'TTA1111111')
        for w in ('Cailean', 'Calan', 'Calen', 'Callahan', 'Callan', 'Callean',
                  'Carleen', 'Carlen', 'Carlene', 'Carlin', 'Carline', 'Carlyn',
                  'Carlynn', 'Carlynne', 'Charlean', 'Charleen', 'Charlene',
                  'Charline', 'Cherlyn', 'Chirlin', 'Clein', 'Cleon', 'Cline',
                  'Cohleen', 'Colan', 'Coleen', 'Colene', 'Colin', 'Colleen',
                  'Collen', 'Collin', 'Colline', 'Colon', 'Cullan', 'Cullen',
                  'Cullin', 'Gaelan', 'Galan', 'Galen', 'Garlan', 'Garlen',
                  'Gaulin', 'Gayleen', 'Gaylene', 'Giliane', 'Gillan',
                  'Gillian', 'Glen', 'Glenn', 'Glyn', 'Glynn', 'Gollin',
                  'Gorlin', 'Kalin', 'Karlan', 'Karleen', 'Karlen', 'Karlene',
                  'Karlin', 'Karlyn', 'Kaylyn', 'Keelin', 'Kellen', 'Kellene',
                  'Kellyann', 'Kellyn', 'Khalin', 'Kilan', 'Kilian', 'Killen',
                  'Killian', 'Killion', 'Klein', 'Kleon', 'Kline', 'Koerlin',
                  'Kylen', 'Kylynn', 'Quillan', 'Quillon', 'Qulllon', 'Xylon'):
            self.assertEqual(caverphone(w), 'KLN1111111')
            self.assertEqual(caverphone(w, 2), 'KLN1111111')
            self.assertEqual(caverphone(w, version=2), 'KLN1111111')
        for w in ('Dan', 'Dane', 'Dann', 'Darn', 'Daune', 'Dawn', 'Ddene',
                  'Dean', 'Deane', 'Deanne', 'DeeAnn', 'Deeann', 'Deeanne',
                  'Deeyn', 'Den', 'Dene', 'Denn', 'Deonne', 'Diahann', 'Dian',
                  'Diane', 'Diann', 'Dianne', 'Diannne', 'Dine', 'Dion',
                  'Dione', 'Dionne', 'Doane', 'Doehne', 'Don', 'Donn', 'Doone',
                  'Dorn', 'Down', 'Downe', 'Duane', 'Dun', 'Dunn', 'Duyne',
                  'Dyan', 'Dyane', 'Dyann', 'Dyanne', 'Dyun', 'Tan', 'Tann',
                  'Teahan', 'Ten', 'Tenn', 'Terhune', 'Thain', 'Thaine',
                  'Thane', 'Thanh', 'Thayne', 'Theone', 'Thin', 'Thorn',
                  'Thorne', 'Thun', 'Thynne', 'Tien', 'Tine', 'Tjon', 'Town',
                  'Towne', 'Turne', 'Tyne'):
            self.assertEqual(caverphone(w), 'TN11111111')
            self.assertEqual(caverphone(w, 2), 'TN11111111')
            self.assertEqual(caverphone(w, version=2), 'TN11111111')

    def test_caverphone2_php_testset(self):
        # https://raw.githubusercontent.com/kiphughes/caverphone/master/unit_tests.php
        testset = (('aaron', 'ARN1111111'), ('abby', 'APA1111111'),\
                ('abdo', 'APTA111111'), ('abel', 'APA1111111'),\
                ('abigail', 'APKA111111'), ('abina', 'APNA111111'),\
                ('abool', 'APA1111111'), ('abraham', 'APRM111111'),\
                ('absalom', 'APSLM11111'), ('ada', 'ATA1111111'),\
                ('adalbert', 'ATPT111111'), ('adaline', 'ATLN111111'),\
                ('adam', 'ATM1111111'), ('adela', 'ATLA111111'),\
                ('adelaide', 'ATLT111111'), ('adeleen', 'ATLN111111'),\
                ('adelene', 'ATLN111111'), ('adelina', 'ATLNA11111'),\
                ('adeline', 'ATLN111111'), ('adolarious', 'ATLRS11111'),\
                ('adolph', 'ATF1111111'), ('adolphe', 'ATF1111111'),\
                ('adolphus', 'ATFS111111'), ('adonia', 'ATNA111111'),\
                ('adrian', 'ATRN111111'), ('aeneas', 'ANS1111111'),\
                ('afred', 'AFRT111111'), ('agatha', 'AKTA111111'),\
                ('aggie', 'AKA1111111'), ('agnes', 'AKNS111111'),\
                ('agness', 'AKNS111111'), ('ah', 'A111111111'),\
                ('ahira', 'ARA1111111'), ('aida', 'ATA1111111'),\
                ('aidan', 'ATN1111111'), ('aileen', 'ALN1111111'),\
                ('ailsa', 'ASA1111111'), ('aimee', 'AMA1111111'),\
                ('aimie', 'AMA1111111'), ('aird', 'AT11111111'),\
                ('airini', 'ARNA111111'), ('alak', 'ALK1111111'),\
                ('alan', 'ALN1111111'), ('alasdair', 'ALSTA11111'),\
                ('alastair', 'ALSTA11111'), ('alban', 'APN1111111'),\
                ('albany', 'APNA111111'), ('albert', 'APT1111111'),\
                ('alberta', 'APTA111111'), ('alberthina', 'APTNA11111'),\
                ('albertina', 'APTNA11111'), ('albertus', 'APTS111111'),\
                ('albina', 'APNA111111'), ('aldolf', 'ATF1111111'),\
                ('aldwyn', 'ATWN111111'), ('aleatha', 'ALTA111111'),\
                ('alec', 'ALK1111111'), ('alex', 'ALK1111111'),\
                ('alexander', 'ALKNTA1111'), ('alexanderina', 'ALKNTRNA11'),\
                ('alexandra', 'ALKNTRA111'), ('alexandrena', 'ALKNTRNA11'),\
                ('alexandrew', 'ALKNTRA111'), ('alexandria', 'ALKNTRA111'),\
                ('alexandrina', 'ALKNTRNA11'), ('alexina', 'ALKNA11111'),\
                ('alexius', 'ALKS111111'), ('alf', 'AF11111111'),\
                ('alfred', 'AFRT111111'), ('alfreda', 'AFRTA11111'),\
                ('alfrerd', 'AFRT111111'), ('algernon', 'AKNN111111'),\
                ('algier', 'AKA1111111'), ('alice', 'ALK1111111'),\
                ('alicia', 'ALSA111111'), ('alick', 'ALK1111111'),\
                ('aline', 'ALN1111111'), ('alinie', 'ALNA111111'),\
                ('alison', 'ALSN111111'), ('alister', 'ALSTA11111'),\
                ('alixe', 'ALK1111111'), ('allan', 'ALN1111111'),\
                ('allen', 'ALN1111111'), ('allison', 'ALSN111111'),\
                ('allon', 'ALN1111111'), ('alma', 'AMA1111111'),\
                ('alnie', 'ANA1111111'), ('aloysius', 'ALSS111111'),\
                ('alpheus', 'AFS1111111'), ('alphonso', 'AFNSA11111'),\
                ('alphonsos', 'AFNSS11111'), ('alphonsus', 'AFNSS11111'),\
                ('alston', 'ASTN111111'), ('althea', 'ATA1111111'),\
                ('alva', 'AFA1111111'), ('alvan', 'AFN1111111'),\
                ('alvia', 'AFA1111111'), ('alvida', 'AFTA111111'),\
                ('alvin', 'AFN1111111'), ('alvina', 'AFNA111111'),\
                ('alvirie', 'AFRA111111'), ('alwin', 'AWN1111111'),\
                ('alwyn', 'AWN1111111'), ('alys', 'ALS1111111'),\
                ('amanda', 'AMNTA11111'), ('ambrose', 'AMPRS11111'),\
                ('amelia', 'AMLA111111'), ('amida', 'AMTA111111'),\
                ('amie', 'AMA1111111'), ('amos', 'AMS1111111'),\
                ('amy', 'AMA1111111'), ('anabella', 'ANPLA11111'),\
                ('anastasia', 'ANSTSA1111'), ('andarena', 'ANTRNA1111'),\
                ('andereanie', 'ANTRNA1111'), ('anderena', 'ANTRNA1111'),\
                ('anderina', 'ANTRNA1111'), ('anders', 'ANTS111111'),\
                ('anderson', 'ANTSN11111'), ('andes', 'ANTS111111'),\
                ('andis', 'ANTS111111'), ('andrea', 'ANTRA11111'),\
                ('andreas', 'ANTRS11111'), ('andreen', 'ANTRN11111'),\
                ('andrena', 'ANTRNA1111'), ('andrew', 'ANTRA11111'),\
                ('andrewetta', 'ANTRWTA111'), ('andrewina', 'ANTRWNA111'),\
                ('andriana', 'ANTRNA1111'), ('andrina', 'ANTRNA1111'),\
                ('angela', 'ANKLA11111'), ('angelina', 'ANKLNA1111'),\
                ('anges', 'ANKS111111'), ('angnetta', 'ANKNTA1111'),\
                ('angus', 'ANKS111111'), ('angustus', 'ANKSTS1111'),\
                ('angy', 'ANKA111111'), ('anita', 'ANTA111111'),\
                ('anmore', 'ANMA111111'), ('ann', 'AN11111111'),\
                ('anna', 'ANA1111111'), ('annabel', 'ANPA111111'),\
                ('annabell', 'ANPA111111'), ('annabella', 'ANPLA11111'),\
                ('annastasia', 'ANSTSA1111'), ('anne', 'AN11111111'),\
                ('anners', 'ANS1111111'), ('annetta', 'ANTA111111'),\
                ('annette', 'ANT1111111'), ('annettta', 'ANTA111111'),\
                ('annie', 'ANA1111111'), ('annis', 'ANS1111111'),\
                ('anorah', 'ANRA111111'), ('ansley', 'ANSLA11111'),\
                ('antcliffe', 'ANTKLF1111'), ('anthony', 'ANTNA11111'),\
                ('antiss', 'ANTS111111'), ('anton', 'ANTN111111'),\
                ('antonica', 'ANTNKA1111'), ('antonie', 'ANTNA11111'),\
                ('antonio', 'ANTNA11111'), ('antony', 'ANTNA11111'),\
                ('aquila', 'AKLA111111'), ('ara', 'ARA1111111'),\
                ('arabella', 'ARPLA11111'), ('archibald', 'AKPT111111'),\
                ('archie', 'AKA1111111'), ('archina', 'AKNA111111'),\
                ('archur', 'AKA1111111'), ('areta', 'ARTA111111'),\
                ('argles', 'AKLS111111'), ('argyle', 'AKA1111111'),\
                ('aria', 'ARA1111111'), ('ariana', 'ARNA111111'),\
                ('ariti', 'ARTA111111'), ('arlene', 'ALN1111111'),\
                ('arnold', 'ANT1111111'), ('aroha', 'ARA1111111'),\
                ('arowie', 'ARWA111111'), ('arthur', 'ATA1111111'),\
                ('asenath', 'ASNT111111'), ('ashburn', 'ASPN111111'),\
                ('asher', 'ASA1111111'), ('ashley', 'ASLA111111'),\
                ('ashton', 'ASTN111111'), ('atalanta', 'ATLNTA1111'),\
                ('athel', 'ATA1111111'), ('athol', 'ATA1111111'),\
                ('atkinson', 'ATKNSN1111'), ('aubrer', 'APRA111111'),\
                ('aubrey', 'APRA111111'), ('audrew', 'ATRA111111'),\
                ('audrey', 'ATRA111111'), ('audrina', 'ATRNA11111'),\
                ('aufrere', 'AFRA111111'), ('augus', 'AKS1111111'),\
                ('august', 'AKST111111'), ('augusta', 'AKSTA11111'),\
                ('augustine', 'AKSTN11111'), ('augustus', 'AKSTS11111'),\
                ('aurora', 'ARRA111111'), ('austen', 'ASTN111111'),\
                ('austin', 'ASTN111111'), ('ava', 'AFA1111111'),\
                ('avery', 'AFRA111111'), ('avice', 'AFK1111111'),\
                ('avis', 'AFS1111111'), ('avondale', 'AFNTA11111'),\
                ('awdry', 'ATRA111111'), ('axel', 'AKA1111111'),\
                ('azel', 'ASA1111111'), ('azella', 'ASLA111111'),\
                ('baden', 'PTN1111111'), ('bailey', 'PLA1111111'),\
                ('balfour', 'PFA1111111'), ('barbara', 'PPRA111111'),\
                ('barnett', 'PNT1111111'), ('barry', 'PRA1111111'),\
                ('bartholomew', 'PTLMA11111'), ('bartlet', 'PTLT111111'),\
                ('bartlett', 'PTLT111111'), ('basil', 'PSA1111111'),\
                ('beaton', 'PTN1111111'), ('beatrice', 'PTRK111111'),\
                ('beatrix', 'PTRK111111'), ('bedelia', 'PTLA111111'),\
                ('belina', 'PLNA111111'), ('belinda', 'PLNTA11111'),\
                ('bella', 'PLA1111111'), ('ben', 'PN11111111'),\
                ('benetta', 'PNTA111111'), ('benita', 'PNTA111111'),\
                ('benjamin', 'PNMN111111'), ('bennet', 'PNT1111111'),\
                ('benson', 'PNSN111111'), ('bernadette', 'PNTT111111'),\
                ('bernard', 'PNT1111111'), ('bernhard', 'PNT1111111'),\
                ('bernhardt', 'PNT1111111'), ('bernice', 'PNK1111111'),\
                ('berrie', 'PRA1111111'), ('bert', 'PT11111111'),\
                ('berta', 'PTA1111111'), ('bertetta', 'PTTA111111'),\
                ('bertha', 'PTA1111111'), ('berthia', 'PTA1111111'),\
                ('bertie', 'PTA1111111'), ('bertina', 'PTNA111111'),\
                ('bertram', 'PTRM111111'), ('bertrand', 'PTRNT11111'),\
                ('berty', 'PTA1111111'), ('bertzow', 'PTSA111111'),\
                ('beryl', 'PRA1111111'), ('bessie', 'PSA1111111'),\
                ('bessy', 'PSA1111111'), ('beter', 'PTA1111111'),\
                ('beth', 'PT11111111'), ('bethea', 'PTA1111111'),\
                ('bethia', 'PTA1111111'), ('betsey', 'PTSA111111'),\
                ('betsy', 'PTSA111111'), ('bettie', 'PTA1111111'),\
                ('bettina', 'PTNA111111'), ('betty', 'PTA1111111'),\
                ('beulah', 'PLA1111111'), ('billy', 'PLA1111111'),\
                ('bina', 'PNA1111111'), ('binah', 'PNA1111111'),\
                ('birdie', 'PTA1111111'), ('blair', 'PLA1111111'),\
                ('blanch', 'PLNK111111'), ('blanche', 'PLNK111111'),\
                ('blenard', 'PLNT111111'), ('bodil', 'PTA1111111'),\
                ('bollettie', 'PLTA111111'), ('bordix', 'PTK1111111'),\
                ('bowman', 'PMN1111111'), ('boyd', 'PT11111111'),\
                ('brazil', 'PRSA111111'), ('breatne', 'PRTN111111'),\
                ('breezetta', 'PRSTA11111'), ('brenda', 'PRNTA11111'),\
                ('brian', 'PRN1111111'), ('bridget', 'PRKT111111'),\
                ('bridie', 'PRTA111111'), ('brigid', 'PRKT111111'),\
                ('browne', 'PRN1111111'), ('bruce', 'PRK1111111'),\
                ('bryan', 'PRN1111111'), ('bryda', 'PRTA111111'),\
                ('buchanan', 'PKNN111111'), ('bulimba', 'PLMPA11111'),\
                ('burma', 'PMA1111111'), ('burt', 'PT11111111'),\
                ('burton', 'PTN1111111'), ('bussorah', 'PSRA111111'),\
                ('byrel', 'PRA1111111'), ('byrl', 'PA11111111'),\
                ('camelia', 'KMLA111111'), ('camellia', 'KMLA111111'),\
                ('campbell', 'KMPA111111'), ('carden', 'KTN1111111'),\
                ('caren', 'KRN1111111'), ('carew', 'KRA1111111'),\
                ('carita', 'KRTA111111'), ('carl', 'KA11111111'),\
                ('carlile', 'KLA1111111'), ('carlin', 'KLN1111111'),\
                ('carlton', 'KTN1111111'), ('carmen', 'KMN1111111'),\
                ('carmichael', 'KMKA111111'), ('carnegie', 'KNKA111111'),\
                ('carole', 'KRA1111111'), ('carolina', 'KRLNA11111'),\
                ('caroline', 'KRLN111111'), ('carona', 'KRNA111111'),\
                ('carra', 'KRA1111111'), ('carrie', 'KRA1111111'),\
                ('carrington', 'KRNKTN1111'), ('cassandra', 'KSNTRA1111'),\
                ('cassie', 'KSA1111111'), ('catharine', 'KTRN111111'),\
                ('cathelus', 'KTLS111111'), ('catherina', 'KTRNA11111'),\
                ('catherine', 'KTRN111111'), ('cathilus', 'KTLS111111'),\
                ('cathleen', 'KTLN111111'), ('cathrien', 'KTRN111111'),\
                ('cathrine', 'KTRN111111'), ('catrina', 'KTRNA11111'),\
                ('cecelia', 'SSLA111111'), ('cecil', 'SSA1111111'),\
                ('cecile', 'SSA1111111'), ('cecilia', 'SSLA111111'),\
                ('cecily', 'SSLA111111'), ('cedric', 'STRK111111'),\
                ('cedrie', 'STRA111111'), ('celestine', 'SLSTN11111'),\
                ('celia', 'SLA1111111'), ('cessford', 'SSFT111111'),\
                ('chalmers', 'KMS1111111'), ('chapman', 'KPMN111111'),\
                ('charia', 'KRA1111111'), ('charitable', 'KRTPA11111'),\
                ('charles', 'KLS1111111'), ('charlesclarence', 'KLSKLRNK11'),\
                ('charleswilliam', 'KLSWLM1111'), ('charley', 'KLA1111111'),\
                ('charlie', 'KLA1111111'), ('charlott', 'KLT1111111'),\
                ('charlotte', 'KLT1111111'), ('chas', 'KS11111111'),\
                ('chatles', 'KTLS111111'), ('chester', 'KSTA111111'),\
                ('chistopher', 'KSTFA11111'), ('chrarles', 'KRLS111111'),\
                ('chrest', 'KRST111111'), ('chrissie', 'KRSA111111'),\
                ('chrissy', 'KRSA111111'), ('christabel', 'KRSTPA1111'),\
                ('christabella', 'KRSTPLA111'), ('christen', 'KRSTN11111'),\
                ('christena', 'KRSTNA1111'), ('christian', 'KRSN111111'),\
                ('christiana', 'KRSNA11111'), ('christie', 'KRSTA11111'),\
                ('christina', 'KRSTNA1111'), ('christine', 'KRSTN11111'),\
                ('christinn', 'KRSTN11111'), ('christobel', 'KRSTPA1111'),\
                ('christopher', 'KRSTFA1111'), ('cicely', 'SSLA111111'),\
                ('cicil', 'SSA1111111'), ('cissie', 'SSA1111111'),\
                ('cissy', 'SSA1111111'), ('claire', 'KLA1111111'),\
                ('clalence', 'KLLNK11111'), ('clance', 'KLNK111111'),\
                ('clara', 'KLRA111111'), ('clarance', 'KLRNK11111'),\
                ('clare', 'KLA1111111'), ('clarels', 'KLRS111111'),\
                ('clarence', 'KLRNK11111'), ('clarenda', 'KLRNTA1111'),\
                ('clarenee', 'KLRNA11111'), ('claretta', 'KLRTA11111'),\
                ('claribel', 'KLRPA11111'), ('clarice', 'KLRK111111'),\
                ('clarinda', 'KLRNTA1111'), ('clarissa', 'KLRSA11111'),\
                ('claritta', 'KLRTA11111'), ('clarkson', 'KLKSN11111'),\
                ('clarles', 'KLLS111111'), ('claud', 'KLT1111111'),\
                ('claude', 'KLT1111111'), ('claudia', 'KLTA111111'),\
                ('clement', 'KLMNT11111'), ('clementina', 'KLMNTNA111'),\
                ('clementine', 'KLMNTN1111'), ('clemont', 'KLMNT11111'),\
                ('clifford', 'KLFT111111'), ('cliford', 'KLFT111111'),\
                ('clifton', 'KLFTN11111'), ('clina', 'KLNA111111'),\
                ('clive', 'KLF1111111'), ('cllarles', 'KLLS111111'),\
                ('clrarles', 'KRLS111111'), ('clunnie', 'KLNA111111'),\
                ('clyde', 'KLT1111111'), ('clym', 'KLM1111111'),\
                ('cochrane', 'KKRN111111'), ('coila', 'KLA1111111'),\
                ('coleman', 'KLMN111111'), ('colena', 'KLNA111111'),\
                ('colin', 'KLN1111111'), ('colina', 'KLNA111111'),\
                ('colville', 'KFA1111111'), ('comrie', 'KMRA111111'),\
                ('connie', 'KNA1111111'), ('conrad', 'KNRT111111'),\
                ('conroy', 'KNRA111111'), ('constance', 'KNSTNK1111'),\
                ('conway', 'KNWA111111'), ('conwy', 'KNWA111111'),\
                ('cora', 'KRA1111111'), ('coral', 'KRA1111111'),\
                ('coralie', 'KRLA111111'), ('coraline', 'KRLN111111'),\
                ('corbett', 'KPT1111111'), ('cordelia', 'KTLA111111'),\
                ('cordon', 'KTN1111111'), ('corinna', 'KRNA111111'),\
                ('cornelia', 'KNLA111111'), ('cornelius', 'KNLS111111'),\
                ('corona', 'KRNA111111'), ('correll', 'KRA1111111'),\
                ('corrie', 'KRA1111111'), ('coverly', 'KFLA111111'),\
                ('cowan', 'KWN1111111'), ('crace', 'KRK1111111'),\
                ('craigie', 'KRKA111111'), ('cranley', 'KRNLA11111'),\
                ('crawford', 'KRFT111111'), ('cresser', 'KRSA111111'),\
                ('crissie', 'KRSA111111'), ('crissy', 'KRSA111111'),\
                ('croydon', 'KRTN111111'), ('cumming', 'KMNK111111'),\
                ('curle', 'KA11111111'), ('cusack', 'KSK1111111'),\
                ('cushla', 'KSLA111111'), ('cuthbert', 'KTPT111111'),\
                ('cvrus', 'KFRS111111'), ('cynthia', 'SNTA111111'),\
                ('cyprian', 'SPRN111111'), ('cyri1', 'SRA1111111'),\
                ('cyril', 'SRA1111111'), ('d\'arcy', 'TSA1111111'),\
                ('dagald', 'TKT1111111'), ('dagmar', 'TKMA111111'),\
                ('daisy', 'TSA1111111'), ('dalia', 'TLA1111111'),\
                ('dallas', 'TLS1111111'), ('dan', 'TN11111111'),\
                ('dand', 'TNT1111111'), ('dane', 'TN11111111'),\
                ('danes', 'TNS1111111'), ('daniel', 'TNA1111111'),\
                ('daphne', 'TFN1111111'), ('darcey', 'TSA1111111'),\
                ('darcy', 'TSA1111111'), ('dardanella', 'TTNLA11111'),\
                ('darwent', 'TWNT111111'), ('dave', 'TF11111111'),\
                ('davey', 'TFA1111111'), ('davicl', 'TFKA111111'),\
                ('david', 'TFT1111111'), ('davida', 'TFTA111111'),\
                ('davidena', 'TFTNA11111'), ('davina', 'TFNA111111'),\
                ('davis', 'TFS1111111'), ('davitl', 'TFTA111111'),\
                ('dawson', 'TSN1111111'), ('deab', 'TP11111111'),\
                ('deane', 'TN11111111'), ('deborah', 'TPRA111111'),\
                ('decima', 'TSMA111111'), ('decimus', 'TSMS111111'),\
                ('deia', 'TA11111111'), ('delcia', 'TSA1111111'),\
                ('delcie', 'TSA1111111'), ('delia', 'TLA1111111'),\
                ('delice', 'TLK1111111'), ('delilah', 'TLLA111111'),\
                ('della', 'TLA1111111'), ('delsie', 'TSA1111111'),\
                ('denis', 'TNS1111111'), ('denise', 'TNS1111111'),\
                ('dennis', 'TNS1111111'), ('denzil', 'TNSA111111'),\
                ('derice', 'TRK1111111'), ('derry', 'TRA1111111'),\
                ('desmond', 'TSMNT11111'), ('devina', 'TFNA111111'),\
                ('diana', 'TNA1111111'), ('dibb', 'TP11111111'),\
                ('dick', 'TK11111111'), ('digby', 'TKPA111111'),\
                ('dina', 'TNA1111111'), ('dinah', 'TNA1111111'),\
                ('dnniel', 'TNA1111111'), ('docy', 'TSA1111111'),\
                ('dod', 'TT11111111'), ('dolce', 'TK11111111'),\
                ('dolina', 'TLNA111111'), ('dollena', 'TLNA111111'),\
                ('dolly', 'TLA1111111'), ('dolores', 'TLRS111111'),\
                ('dominic', 'TMNK111111'), ('dominick', 'TMNK111111'),\
                ('domonic', 'TMNK111111'), ('don', 'TN11111111'),\
                ('donah', 'TNA1111111'), ('donald', 'TNT1111111'),\
                ('donaldina', 'TNTNA11111'), ('donalena', 'TNLNA11111'),\
                ('donella', 'TNLA111111'), ('dora', 'TRA1111111'),\
                ('dorathea', 'TRTA111111'), ('dorcas', 'TKS1111111'),\
                ('doreen', 'TRN1111111'), ('dorice', 'TRK1111111'),\
                ('doris', 'TRS1111111'), ('dorles', 'TLS1111111'),\
                ('dorothea', 'TRTA111111'), ('dorothy', 'TRTA111111'),\
                ('dorree', 'TRA1111111'), ('dorris', 'TRS1111111'),\
                ('douald', 'TT11111111'), ('dougal', 'TKA1111111'),\
                ('dougald', 'TKT1111111'), ('douglas', 'TKLS111111'),\
                ('dryden', 'TRTN111111'), ('dsmond', 'TSMNT11111'),\
                ('dudley', 'TTLA111111'), ('dugald', 'TKT1111111'),\
                ('dugall', 'TKA1111111'), ('dulcie', 'TSA1111111'),\
                ('duncan', 'TNKN111111'), ('dunncan', 'TNKN111111'),\
                ('dunstan', 'TNSTN11111'), ('e', '1111111111'),\
                ('eaber', 'APA1111111'), ('eadly', 'ATLA111111'),\
                ('earl', 'AA11111111'), ('earle', 'AA11111111'),\
                ('earnest', 'ANST111111'), ('earold', 'ART1111111'),\
                ('earry', 'ARA1111111'), ('eary', 'ARA1111111'),\
                ('easther', 'ASTA111111'), ('ebb', 'AP11111111'),\
                ('ebbie', 'APA1111111'), ('ebdom', 'APTM111111'),\
                ('ebdon', 'APTN111111'), ('eben', 'APN1111111'),\
                ('ebenezer', 'APNSA11111'), ('eccles', 'AKLS111111'),\
                ('eda', 'ATA1111111'), ('eden', 'ATN1111111'),\
                ('edgal', 'AKA1111111'), ('edgar', 'AKA1111111'),\
                ('edifer', 'ATFA111111'), ('edifu', 'ATFA111111'),\
                ('edith', 'ATT1111111'), ('edla', 'ATLA111111'),\
                ('edmond', 'ATMNT11111'), ('edmund', 'ATMNT11111'),\
                ('edna', 'ATNA111111'), ('edolph', 'ATF1111111'),\
                ('edric', 'ATRK111111'), ('edvina', 'ATFNA11111'),\
                ('edvward', 'ATFWT11111'), ('edwald', 'ATWT111111'),\
                ('edwarcl', 'ATWKA11111'), ('edward', 'ATWT111111'),\
                ('edwardd', 'ATWT111111'), ('edwardi', 'ATWTA11111'),\
                ('edwardl', 'ATWTA11111'), ('edwards', 'ATWTS11111'),\
                ('edwin', 'ATWN111111'), ('edwina', 'ATWNA11111'),\
                ('edyth', 'ATT1111111'), ('edythe', 'ATT1111111'),\
                ('eenry', 'ANRA111111'), ('eerbert', 'APT1111111'),\
                ('effie', 'AFA1111111'), ('effield', 'AFT1111111'),\
                ('efiza', 'AFSA111111'), ('eflie', 'AFLA111111'),\
                ('egbert', 'AKPT111111'), ('eglentine', 'AKLNTN1111'),\
                ('ehler', 'ALA1111111'), ('eila', 'ALA1111111'),\
                ('eileen', 'ALN1111111'), ('eileena', 'ALNA111111'),\
                ('eilene', 'ALN1111111'), ('eilzabeth', 'ASPT111111'),\
                ('eion', 'AN11111111'), ('eirene', 'ARN1111111'),\
                ('elaine', 'ALN1111111'), ('eldorado', 'ATRTA11111'),\
                ('eldrid', 'ATRT111111'), ('eleana', 'ALNA111111'),\
                ('eleanor', 'ALNA111111'), ('eleanora', 'ALNRA11111'),\
                ('eleanore', 'ALNA111111'), ('eleazar', 'ALSA111111'),\
                ('elena', 'ALNA111111'), ('elenor', 'ALNA111111'),\
                ('elenora', 'ALNRA11111'), ('eleonora', 'ALNRA11111'),\
                ('eleonore', 'ALNA111111'), ('elephalet', 'ALFLT11111'),\
                ('elezeard', 'ALST111111'), ('elfreda', 'AFRTA11111'),\
                ('elfrida', 'AFRTA11111'), ('eli', 'ALA1111111'),\
                ('elias', 'ALS1111111'), ('eliezer', 'ALSA111111'),\
                ('elijah', 'ALA1111111'), ('elinor', 'ALNA111111'),\
                ('eliot', 'ALT1111111'), ('eliphalet', 'ALFLT11111'),\
                ('elisabeth', 'ALSPT11111'), ('elise', 'ALS1111111'),\
                ('elisha', 'ALSA111111'), ('elishe', 'ALS1111111'),\
                ('elison', 'ALSN111111'), ('eliza', 'ALSA111111'),\
                ('elizabel', 'ALSPA11111'), ('elizabeth', 'ALSPT11111'),\
                ('elizie', 'ALSA111111'), ('ella', 'ALA1111111'),\
                ('ellaline', 'ALLN111111'), ('ellanor', 'ALNA111111'),\
                ('elleana', 'ALNA111111'), ('elleanor', 'ALNA111111'),\
                ('ellen', 'ALN1111111'), ('ellenor', 'ALNA111111'),\
                ('ellenora', 'ALNRA11111'), ('elleston', 'ALSTN11111'),\
                ('ellie', 'ALA1111111'), ('ellien', 'ALN1111111'),\
                ('ellinor', 'ALNA111111'), ('elliott', 'ALT1111111'),\
                ('ellis', 'ALS1111111'), ('ellison', 'ALSN111111'),\
                ('elliston', 'ALSTN11111'), ('ellsmere', 'ASMA111111'),\
                ('elma', 'AMA1111111'), ('elmira', 'AMRA111111'),\
                ('elsa', 'ASA1111111'), ('elsie', 'ASA1111111'),\
                ('elsinore', 'ASNA111111'), ('elspeth', 'ASPT111111'),\
                ('eluburt', 'ALPT111111'), ('elva', 'AFA1111111'),\
                ('elvena', 'AFNA111111'), ('elvene', 'AFN1111111'),\
                ('elvia', 'AFA1111111'), ('elvie', 'AFA1111111'),\
                ('elvina', 'AFNA111111'), ('elvira', 'AFRA111111'),\
                ('emanuel', 'AMNA111111'), ('emela', 'AMLA111111'),\
                ('emelia', 'AMLA111111'), ('emelie', 'AMLA111111'),\
                ('emeline', 'AMLN111111'), ('emely', 'AMLA111111'),\
                ('emest', 'AMST111111'), ('emil', 'AMA1111111'),\
                ('emile', 'AMA1111111'), ('emiley', 'AMLA111111'),\
                ('emilie', 'AMLA111111'), ('emilina', 'AMLNA11111'),\
                ('emiline', 'AMLN111111'), ('emilio', 'AMLA111111'),\
                ('emily', 'AMLA111111'), ('emma', 'AMA1111111'),\
                ('emmanuel', 'AMNA111111'), ('emmeline', 'AMLN111111'),\
                ('emmie', 'AMA1111111'), ('emmy', 'AMA1111111'),\
                ('ena', 'ANA1111111'), ('eneas', 'ANS1111111'),\
                ('english', 'ANKLS11111'), ('engo', 'ANKA111111'),\
                ('enid', 'ANT1111111'), ('enny', 'ANA1111111'),\
                ('enoch', 'ANK1111111'), ('ephraim', 'AFRM111111'),\
                ('ephrain', 'AFRN111111'), ('ephriam', 'AFRM111111'),\
                ('erana', 'ARNA111111'), ('erancis', 'ARNSS11111'),\
                ('erasmus', 'ARSMS11111'), ('erederick', 'ARTRK11111'),\
                ('erek', 'ARK1111111'), ('erenest', 'ARNST11111'),\
                ('eric', 'ARK1111111'), ('erich', 'ARK1111111'),\
                ('erie', 'ARA1111111'), ('erik', 'ARK1111111'),\
                ('erin', 'ARN1111111'), ('erle', 'AA11111111'),\
                ('ermina', 'AMNA111111'), ('ern', 'AN11111111'),\
                ('ernelst', 'ANST111111'), ('ernest', 'ANST111111'),\
                ('ernestina', 'ANSTNA1111'), ('ernestine', 'ANSTN11111'),\
                ('ernestreetfrancis', 'ANSTRTFRNS'), ('ernett', 'ANT1111111'),\
                ('ernie', 'ANA1111111'), ('ernma', 'ANMA111111'),\
                ('ernst', 'ANST111111'), ('errol', 'ARA1111111'),\
                ('erwin', 'AWN1111111'), ('esdaile', 'ASTA111111'),\
                ('esdale', 'ASTA111111'), ('esher', 'ASA1111111'),\
                ('esma', 'ASMA111111'), ('esme', 'ASM1111111'),\
                ('esmond', 'ASMNT11111'), ('essie', 'ASA1111111'),\
                ('estella', 'ASTLA11111'), ('estelle', 'ASTA111111'),\
                ('ester', 'ASTA111111'), ('esther', 'ASTA111111'),\
                ('ethel', 'ATA1111111'), ('ethelbert', 'ATPT111111'),\
                ('ethelinda', 'ATLNTA1111'), ('ethelwin', 'ATWN111111'),\
                ('ethelwyn', 'ATWN111111'), ('ethie', 'ATA1111111'),\
                ('etta', 'ATA1111111'), ('ettie', 'ATA1111111'),\
                ('ettrick', 'ATRK111111'), ('etty', 'ATA1111111'),\
                ('eubert', 'APT1111111'), ('eugene', 'AKN1111111'),\
                ('eugenie', 'AKNA111111'), ('eugh', 'AA11111111'),\
                ('eulla', 'ALA1111111'), ('eunice', 'ANK1111111'),\
                ('euphemia', 'AFMA111111'), ('eurice', 'ARK1111111'),\
                ('eustace', 'ASTK111111'), ('eva', 'AFA1111111'),\
                ('evaline', 'AFLN111111'), ('evalyn', 'AFLN111111'),\
                ('evan', 'AFN1111111'), ('evander', 'AFNTA11111'),\
                ('evandrina', 'AFNTRNA111'), ('evanelina', 'AFNLNA1111'),\
                ('evangaline', 'AFNKLN1111'), ('evangelina', 'AFNKLNA111'),\
                ('evangeline', 'AFNKLN1111'), ('evans', 'AFNS111111'),\
                ('evarard', 'AFRT111111'), ('eve', 'AF11111111'),\
                ('eveleen', 'AFLN111111'), ('evelina', 'AFLNA11111'),\
                ('eveline', 'AFLN111111'), ('evelyn', 'AFLN111111'),\
                ('evelyne', 'AFLN111111'), ('everard', 'AFRT111111'),\
                ('eveyleen', 'AFLN111111'), ('evin', 'AFN1111111'),\
                ('evinda', 'AFNTA11111'), ('ewan', 'AWN1111111'),\
                ('eward', 'AWT1111111'), ('ewart', 'AWT1111111'),\
                ('ewen', 'AWN1111111'), ('ezekiel', 'ASKA111111'),\
                ('ezra', 'ASRA111111'), ('faa', 'FA11111111'),\
                ('fabian', 'FPN1111111'), ('fairey', 'FRA1111111'),\
                ('faith', 'FT11111111'), ('fancis', 'FNSS111111'),\
                ('fannie', 'FNA1111111'), ('fanny', 'FNA1111111'),\
                ('farnham', 'FNM1111111'), ('farquhar', 'FKA1111111'),\
                ('fashoda', 'FSTA111111'), ('fay', 'FA11111111'),\
                ('felicha', 'FLKA111111'), ('felicia', 'FLSA111111'),\
                ('felix', 'FLK1111111'), ('fenwick', 'FNWK111111'),\
                ('ferdeanand', 'FTNNT11111'), ('ferdinand', 'FTNNT11111'),\
                ('ferdinnnd', 'FTNT111111'), ('fergus', 'FKS1111111'),\
                ('fergusson', 'FKSN111111'), ('ferme', 'FM11111111'),\
                ('ferne', 'FN11111111'), ('fides', 'FTS1111111'),\
                ('findlay', 'FNTLA11111'), ('finlay', 'FNLA111111'),\
                ('finley', 'FNLA111111'), ('fitzclarence', 'FTSKLRNK11'),\
                ('fitzelarence', 'FTSLRNK111'), ('fitzgerald', 'FTSKRT1111'),\
                ('fitzroy', 'FTSRA11111'), ('flank', 'FLNK111111'),\
                ('fleming', 'FLMNK11111'), ('fletcher', 'FLKA111111'),\
                ('flora', 'FLRA111111'), ('florabelle', 'FLRPA11111'),\
                ('florann', 'FLRN111111'), ('florencc', 'FLRNK11111'),\
                ('florence', 'FLRNK11111'), ('florice', 'FLRK111111'),\
                ('floris', 'FLRS111111'), ('florisse', 'FLRS111111'),\
                ('florita', 'FLRTA11111'), ('florrie', 'FLRA111111'),\
                ('flossie', 'FLSA111111'), ('forbes', 'FPS1111111'),\
                ('fordham', 'FTM1111111'), ('forrest', 'FRST111111'),\
                ('forrester', 'FRSTA11111'), ('forrestina', 'FRSTNA1111'),\
                ('forsyth', 'FST1111111'), ('fosbery', 'FSPRA11111'),\
                ('fracis', 'FRSS111111'), ('fraicis', 'FRSS111111'),\
                ('france', 'FRNK111111'), ('frances', 'FRNSS11111'),\
                ('franchise', 'FRNKS11111'), ('francie', 'FRNSA11111'),\
                ('francis', 'FRNSS11111'), ('francisca', 'FRNSSKA111'),\
                ('francois', 'FRNKS11111'), ('francusess', 'FRNKSS1111'),\
                ('frank', 'FRNK111111'), ('franklin', 'FRNKLN1111'),\
                ('franklyn', 'FRNKLN1111'), ('franz', 'FRNS111111'),\
                ('frarnk', 'FRNK111111'), ('fraser', 'FRSA111111'),\
                ('frcderick', 'FKTRK11111'), ('fred', 'FRT1111111'),\
                ('freda', 'FRTA111111'), ('fredeick', 'FRTK111111'),\
                ('fredelick', 'FRTLK11111'), ('fredercik', 'FRTSK11111'),\
                ('frederic', 'FRTRK11111'), ('frederica', 'FRTRKA1111'),\
                ('frederich', 'FRTRK11111'), ('frederick', 'FRTRK11111'),\
                ('fredericka', 'FRTRKA1111'), ('fredericld', 'FRTRKT1111'),\
                ('frederidck', 'FRTRTK1111'), ('frederiek', 'FRTRK11111'),\
                ('frederik', 'FRTRK11111'), ('frederlck', 'FRTK111111'),\
                ('fredierick', 'FRTRK11111'), ('fredk', 'FRTK111111'),\
                ('fredric', 'FRTRK11111'), ('fredrica', 'FRTRKA1111'),\
                ('fredrich', 'FRTRK11111'), ('fredrick', 'FRTRK11111'),\
                ('fredrik', 'FRTRK11111'), ('freid', 'FRT1111111'),\
                ('fric', 'FRK1111111'), ('friderick', 'FRTRK11111'),\
                ('fullenia', 'FLNA111111'), ('fulton', 'FTN1111111'),\
                ('gabriel', 'KPRA111111'), ('gabrielle', 'KPRA111111'),\
                ('gallacher', 'KLKA111111'), ('gamet', 'KMT1111111'),\
                ('gara', 'KRA1111111'), ('gardiner', 'KTNA111111'),\
                ('garibaldi', 'KRPTA11111'), ('garnet', 'KNT1111111'),\
                ('garrett', 'KRT1111111'), ('garry', 'KRA1111111'),\
                ('garth', 'KT11111111'), ('gary', 'KRA1111111'),\
                ('gavin', 'KFN1111111'), ('gaynor', 'KNA1111111'),\
                ('gcorge', 'KK11111111'), ('gebrge', 'KPK1111111'),\
                ('gecrge', 'KKK1111111'), ('geeorge', 'KK11111111'),\
                ('genrie', 'KNRA111111'), ('geo', 'KA11111111'),\
                ('geoffrev', 'KFRF111111'), ('geoffrey', 'KFRA111111'),\
                ('geoffry', 'KFRA111111'), ('geonge', 'KNK1111111'),\
                ('george', 'KK11111111'), ('georgei', 'KKA1111111'),\
                ('georgel', 'KKA1111111'), ('georger', 'KKA1111111'),\
                ('georgia', 'KKA1111111'), ('georgina', 'KKNA111111'),\
                ('georgo', 'KKA1111111'), ('georgte', 'KKT1111111'),\
                ('geortre', 'KTA1111111'), ('gerald', 'KRT1111111'),\
                ('geraldine', 'KRTN111111'), ('gerard', 'KRT1111111'),\
                ('gerge', 'KK11111111'), ('gershon', 'KSN1111111'),\
                ('gertie', 'KTA1111111'), ('gertrude', 'KTRT111111'),\
                ('gessenox', 'KSNK111111'), ('geytha', 'KTA1111111'),\
                ('geziena', 'KSNA111111'), ('gharles', 'LS11111111'),\
                ('gibson', 'KPSN111111'), ('gideon', 'KTN1111111'),\
                ('giener', 'KNA1111111'), ('gieorge', 'KK11111111'),\
                ('gilbert', 'KPT1111111'), ('gilberta', 'KPTA111111'),\
                ('gilhert', 'KT11111111'), ('girdwood', 'KTWT111111'),\
                ('gisella', 'KSLA111111'), ('gladstone', 'KLTSTN1111'),\
                ('gladwys', 'KLTWS11111'), ('gladys', 'KLTS111111'),\
                ('glen', 'KLN1111111'), ('gleorga', 'KLKA111111'),\
                ('gleorge', 'KLK1111111'), ('gleorgina', 'KLKNA11111'),\
                ('gleurge', 'KLK1111111'), ('glladys', 'KLTS111111'),\
                ('glordon', 'KLTN111111'), ('glover', 'KLFA111111'),\
                ('glrace', 'KRK1111111'), ('godfrey', 'KTFRA11111'),\
                ('godwin', 'KTWN111111'), ('golda', 'KTA1111111'),\
                ('gonzaga', 'KNSKA11111'), ('goorge', 'KK11111111'),\
                ('gordon', 'KTN1111111'), ('gorge', 'KK11111111'),\
                ('gottfred', 'KTFRT11111'), ('govan', 'KFN1111111'),\
                ('gowan', 'KWN1111111'), ('grace', 'KRK1111111'),\
                ('gracie', 'KRSA111111'), ('graham', 'KRM1111111'),\
                ('grahame', 'KRM1111111'), ('grainger', 'KRNKA11111'),\
                ('grange', 'KRNK111111'), ('grant', 'KRNT111111'),\
                ('grattan', 'KRTN111111'), ('gratton', 'KRTN111111'),\
                ('gray', 'KRA1111111'), ('grayce', 'KRK1111111'),\
                ('greer', 'KRA1111111'), ('greshon', 'KRSN111111'),\
                ('greta', 'KRTA111111'), ('gretchen', 'KRKN111111'),\
                ('gretta', 'KRTA111111'), ('griffith', 'KRFT111111'),\
                ('griffiths', 'KRFTS11111'), ('griselda', 'KRSTA11111'),\
                ('grosvenor', 'KRSFNA1111'), ('grover', 'KRFA111111'),\
                ('gteorge', 'KTK1111111'), ('guinevere', 'KNFA111111'),\
                ('gustav', 'KSTF111111'), ('gustava', 'KSTFA11111'),\
                ('gustave', 'KSTF111111'), ('guthrie', 'KTRA111111'),\
                ('guy', 'KA11111111'), ('gwen', 'KWN1111111'),\
                ('gwenath', 'KWNT111111'), ('gwenda', 'KWNTA11111'),\
                ('gwendaline', 'KWNTLN1111'), ('gwendelyne', 'KWNTLN1111'),\
                ('gwendolen', 'KWNTLN1111'), ('gwendolene', 'KWNTLN1111'),\
                ('gwendolin', 'KWNTLN1111'), ('gwendoline', 'KWNTLN1111'),\
                ('gwendolyn', 'KWNTLN1111'), ('gweneth', 'KWNT111111'),\
                ('gwenifer', 'KWNFA11111'), ('gwenoth', 'KWNT111111'),\
                ('gwenyth', 'KWNT111111'), ('gwladys', 'KLTS111111'),\
                ('gwyndoline', 'KWNTLN1111'), ('gwynneth', 'KWNT111111'),\
                ('gytha', 'KTA1111111'), ('gythar', 'KTA1111111'),\
                ('ha', 'AA11111111'), ('haas', 'AS11111111'),\
                ('hadley', 'ATLA111111'), ('haidee', 'ATA1111111'),\
                ('hamilton', 'AMTN111111'), ('hamish', 'AMS1111111'),\
                ('hamlin', 'AMLN111111'), ('hammond', 'AMNT111111'),\
                ('hampton', 'AMPTN11111'), ('hanley', 'ANLA111111'),\
                ('hanna', 'ANA1111111'), ('hannah', 'ANA1111111'),\
                ('hannora', 'ANRA111111'), ('hanora', 'ANRA111111'),\
                ('hanorah', 'ANRA111111'), ('hanoura', 'ANRA111111'),\
                ('hans', 'ANS1111111'), ('hansen', 'ANSN111111'),\
                ('hanson', 'ANSN111111'), ('harace', 'ARK1111111'),\
                ('harah', 'ARA1111111'), ('harbert', 'APT1111111'),\
                ('harion', 'ARN1111111'), ('harlold', 'ALT1111111'),\
                ('harly', 'ALA1111111'), ('harman', 'AMN1111111'),\
                ('harold', 'ART1111111'), ('harper', 'APA1111111'),\
                ('harriet', 'ART1111111'), ('harriett', 'ART1111111'),\
                ('harrietta', 'ARTA111111'), ('harriette', 'ART1111111'),\
                ('harriot', 'ART1111111'), ('harriott', 'ART1111111'),\
                ('harrv', 'AF11111111'), ('harry', 'ARA1111111'),\
                ('hartha', 'ATA1111111'), ('hartley', 'ATLA111111'),\
                ('harvey', 'AFA1111111'), ('hastings', 'ASTNKS1111'),\
                ('hatold', 'ATT1111111'), ('havilah', 'AFLA111111'),\
                ('havilland', 'AFLNT11111'), ('hayden', 'ATN1111111'),\
                ('haydn', 'ATN1111111'), ('hazel', 'ASA1111111'),\
                ('headley', 'ATLA111111'), ('hearstell', 'ASTA111111'),\
                ('heather', 'ATA1111111'), ('hebert', 'APT1111111'),\
                ('hector', 'AKTA111111'), ('hectorina', 'AKTRNA1111'),\
                ('hedley', 'ATLA111111'), ('hedwig', 'ATWK111111'),\
                ('heena', 'ANA1111111'), ('heinrich', 'ANRK111111'),\
                ('helan', 'ALN1111111'), ('helell', 'ALA1111111'),\
                ('helen', 'ALN1111111'), ('helena', 'ALNA111111'),\
                ('helene', 'ALN1111111'), ('helier', 'ALA1111111'),\
                ('hella', 'ALA1111111'), ('hellen', 'ALN1111111'),\
                ('hellurietta', 'ALRTA11111'), ('hemi', 'AMA1111111'),\
                ('hemingway', 'AMNKWA1111'), ('hemmingway', 'AMNKWA1111'),\
                ('hendry', 'ANTRA11111'), ('henery', 'ANRA111111'),\
                ('henn', 'AN11111111'), ('hennerrietta', 'ANRTA11111'),\
                ('henness', 'ANS1111111'), ('henrick', 'ANRK111111'),\
                ('henricus', 'ANRKS11111'), ('henrietta', 'ANRTA11111'),\
                ('henriette', 'ANRT111111'), ('henrv', 'ANF1111111'),\
                ('henry', 'ANRA111111'), ('henton', 'ANTN111111'),\
                ('henty', 'ANTA111111'), ('hephzibah', 'AFSPA11111'),\
                ('hera', 'ARA1111111'), ('herbert', 'APT1111111'),\
                ('herbrt', 'APT1111111'), ('hercules', 'AKLS111111'),\
                ('herman', 'AMN1111111'), ('hermione', 'AMN1111111'),\
                ('herry', 'ARA1111111'), ('hersee', 'ASA1111111'),\
                ('hessie', 'ASA1111111'), ('hester', 'ASTA111111'),\
                ('hettie', 'ATA1111111'), ('hetty', 'ATA1111111'),\
                ('heury', 'ARA1111111'), ('hezio', 'ASA1111111'),\
                ('hilary', 'ALRA111111'), ('hilda', 'ATA1111111'),\
                ('hildegarde', 'ATKT111111'), ('hillary', 'ALRA111111'),\
                ('hilma', 'AMA1111111'), ('hilton', 'ATN1111111'),\
                ('hinemoa', 'ANMA111111'), ('hinimoa', 'ANMA111111'),\
                ('hira', 'ARA1111111'), ('hiram', 'ARM1111111'),\
                ('hobart', 'APT1111111'), ('hobert', 'APT1111111'),\
                ('holly', 'ALA1111111'), ('honor', 'ANA1111111'),\
                ('honora', 'ANRA111111'), ('honoria', 'ANRA111111'),\
                ('honriotte', 'ANRT111111'), ('hope', 'AP11111111'),\
                ('horace', 'ARK1111111'), ('horatia', 'ARSA111111'),\
                ('horatio', 'ARSA111111'), ('horatius', 'ARTS111111'),\
                ('hortense', 'ATNS111111'), ('hosdell', 'ASTA111111'),\
                ('howard', 'AWT1111111'), ('howitt', 'AWT1111111'),\
                ('hua', 'AA11111111'), ('hubert', 'APT1111111'),\
                ('hugh', 'AA11111111'), ('hughina', 'AKNA111111'),\
                ('huh', 'AA11111111'), ('huia', 'AA11111111'),\
                ('hume', 'AM11111111'), ('humphrey', 'AMFRA11111'),\
                ('hunry', 'ANRA111111'), ('huntley', 'ANTLA11111'),\
                ('huron', 'ARN1111111'), ('hy', 'AA11111111'),\
                ('hyacinth', 'ASNT111111'), ('hylton', 'ATN1111111'),\
                ('hyman', 'AMN1111111'), ('ian', 'AN11111111'),\
                ('ianthe', 'ANT1111111'), ('iary', 'ARA1111111'),\
                ('ida', 'ATA1111111'), ('idean', 'ATN1111111'),\
                ('idelia', 'ATLA111111'), ('ieslie', 'ASLA111111'),\
                ('iirederick', 'ARTRK11111'), ('ilar', 'ALA1111111'),\
                ('ilena', 'ALNA111111'), ('ilma', 'AMA1111111'),\
                ('ima', 'AMA1111111'), ('imelda', 'AMTA111111'),\
                ('immaculate', 'AMKLT11111'), ('ina', 'ANA1111111'),\
                ('ineawa', 'ANWA111111'), ('inez', 'ANS1111111'),\
                ('ingo', 'ANKA111111'), ('ion', 'AN11111111'),\
                ('iona', 'ANA1111111'), ('ira', 'ARA1111111'),\
                ('irene', 'ARN1111111'), ('irine', 'ARN1111111'),\
                ('iris', 'ARS1111111'), ('irma', 'AMA1111111'),\
                ('irvine', 'AFN1111111'), ('irving', 'AFNK111111'),\
                ('irwin', 'AWN1111111'), ('isa', 'ASA1111111'),\
                ('isaac', 'ASK1111111'), ('isabel', 'ASPA111111'),\
                ('isabela', 'ASPLA11111'), ('isabell', 'ASPA111111'),\
                ('isabella', 'ASPLA11111'), ('isabelle', 'ASPA111111'),\
                ('isadore', 'ASTA111111'), ('isaiah', 'ASA1111111'),\
                ('isalella', 'ASLLA11111'), ('isbella', 'ASPLA11111'),\
                ('ishmael', 'ASMA111111'), ('isibelle', 'ASPA111111'),\
                ('isita', 'ASTA111111'), ('isla', 'ASLA111111'),\
                ('islay', 'ASLA111111'), ('ismay', 'ASMA111111'),\
                ('ismene', 'ASMN111111'), ('isobel', 'ASPA111111'),\
                ('isobella', 'ASPLA11111'), ('isola', 'ASLA111111'),\
                ('iton', 'ATN1111111'), ('iva', 'AFA1111111'),\
                ('ivan', 'AFN1111111'), ('ivie', 'AFA1111111'),\
                ('ivine', 'AFN1111111'), ('ivo', 'AFA1111111'),\
                ('ivon', 'AFN1111111'), ('ivor', 'AFA1111111'),\
                ('ivy', 'AFA1111111'), ('iza', 'ASA1111111'),\
                ('j', 'A111111111'), ('ja1es', 'YS11111111'),\
                ('jabez', 'YPS1111111'), ('jack', 'YK11111111'),\
                ('jacob', 'YKP1111111'), ('jacobina', 'YKPNA11111'),\
                ('jacues', 'YKS1111111'), ('jaimes', 'YMS1111111'),\
                ('jake', 'YK11111111'), ('jam', 'YM11111111'),\
                ('jamcs', 'YMKS111111'), ('jame', 'YM11111111'),\
                ('jamee', 'YMA1111111'), ('james', 'YMS1111111'),\
                ('jamesalbany', 'YMSPNA1111'), ('jamesina', 'YMSNA11111'),\
                ('jamesines', 'YMSNS11111'), ('jamies', 'YMS1111111'),\
                ('jamos', 'YMS1111111'), ('janbe', 'YNP1111111'),\
                ('jane', 'YN11111111'), ('janes', 'YNS1111111'),\
                ('janet', 'YNT1111111'), ('janetta', 'YNTA111111'),\
                ('janette', 'YNT1111111'), ('janie', 'YNA1111111'),\
                ('janies', 'YNS1111111'), ('janthe', 'YNT1111111'),\
                ('jardine', 'YTN1111111'), ('jarlies', 'YLS1111111'),\
                ('jarmes', 'YMS1111111'), ('jarnes', 'YNS1111111'),\
                ('jarrtes', 'YTS1111111'), ('jas', 'YS11111111'),\
                ('jason', 'YSN1111111'), ('jaspeh', 'YSPA111111'),\
                ('jasper', 'YSPA111111'), ('jean', 'YN11111111'),\
                ('jeane', 'YN11111111'), ('jeanet', 'YNT1111111'),\
                ('jeanetta', 'YNTA111111'), ('jeanette', 'YNT1111111'),\
                ('jeanie', 'YNA1111111'), ('jeanne', 'YN11111111'),\
                ('jeannetta', 'YNTA111111'), ('jeannette', 'YNT1111111'),\
                ('jeannie', 'YNA1111111'), ('jeesie', 'YSA1111111'),\
                ('jeffery', 'YFRA111111'), ('jeffrey', 'YFRA111111'),\
                ('jemima', 'YMMA111111'), ('jemina', 'YMNA111111'),\
                ('jen', 'YN11111111'), ('jenetta', 'YNTA111111'),\
                ('jenette', 'YNT1111111'), ('jenn', 'YN11111111'),\
                ('jennet', 'YNT1111111'), ('jennie', 'YNA1111111'),\
                ('jenny', 'YNA1111111'), ('jens', 'YNS1111111'),\
                ('jeoffrey', 'YFRA111111'), ('jephthah', 'YFTA111111'),\
                ('jeremiah', 'YRMA111111'), ('jervis', 'YFS1111111'),\
                ('jeseie', 'YSA1111111'), ('jesoph', 'YSF1111111'),\
                ('jess', 'YS11111111'), ('jessa', 'YSA1111111'),\
                ('jesse', 'YS11111111'), ('jessica', 'YSKA111111'),\
                ('jessie', 'YSA1111111'), ('jessy', 'YSA1111111'),\
                ('jethro', 'YTRA111111'), ('jewel', 'YWA1111111'),\
                ('jillian', 'YLN1111111'), ('jim', 'YM11111111'),\
                ('jinnie', 'YNA1111111'), ('joan', 'YN11111111'),\
                ('joann', 'YN11111111'), ('joanna', 'YNA1111111'),\
                ('joannie', 'YNA1111111'), ('job', 'YP11111111'),\
                ('jocelyn', 'YSLN111111'), ('joe', 'YA11111111'),\
                ('joffre', 'YFA1111111'), ('johan', 'YN11111111'),\
                ('johann', 'YN11111111'), ('johanna', 'YNA1111111'),\
                ('johannah', 'YNA1111111'), ('johannes', 'YNS1111111'),\
                ('johh', 'YA11111111'), ('john', 'YN11111111'),\
                ('johnann', 'YNN1111111'), ('johnanna', 'YNNA111111'),\
                ('johnina', 'YNNA111111'), ('johnpatrick', 'YNPTRK1111'),\
                ('johnson', 'YNSN111111'), ('johnthomas', 'YNTMS11111'),\
                ('johnwilliam', 'YNWLM11111'), ('johr', 'YA11111111'),\
                ('johrl', 'YA11111111'), ('johu', 'YA11111111'),\
                ('joiln', 'YN11111111'), ('jollanna', 'YLNA111111'),\
                ('jolm', 'YM11111111'), ('joln', 'YN11111111'),\
                ('jon', 'YN11111111'), ('jonah', 'YNA1111111'),\
                ('jonas', 'YNS1111111'), ('jonathan', 'YNTN111111'),\
                ('jones', 'YNS1111111'), ('jonl', 'YNA1111111'),\
                ('jonn', 'YN11111111'), ('jorgen', 'YKN1111111'),\
                ('josep', 'YSP1111111'), ('joseph', 'YSF1111111'),\
                ('josephgeorge', 'YSFKK11111'), ('josephia', 'YSFA111111'),\
                ('josephine', 'YSFN111111'), ('josh', 'YS11111111'),\
                ('joshua', 'YSA1111111'), ('josiah', 'YSA1111111'),\
                ('josie', 'YSA1111111'), ('josieph', 'YSF1111111'),\
                ('josoph', 'YSF1111111'), ('jospeh', 'YSPA111111'),\
                ('joy', 'YA11111111'), ('joyce', 'YK11111111'),\
                ('juanita', 'YNTA111111'), ('jules', 'YLS1111111'),\
                ('julia', 'YLA1111111'), ('julian', 'YLN1111111'),\
                ('juliana', 'YLNA111111'), ('juliann', 'YLN1111111'),\
                ('julianna', 'YLNA111111'), ('julie', 'YLA1111111'),\
                ('julius', 'YLS1111111'), ('june', 'YN11111111'),\
                ('justin', 'YSTN111111'), ('justina', 'YSTNA11111'),\
                ('kaiserin', 'KSRN111111'), ('karen', 'KRN1111111'),\
                ('karl', 'KA11111111'), ('kate', 'KT11111111'),\
                ('katern', 'KTN1111111'), ('kath', 'KT11111111'),\
                ('katharine', 'KTRN111111'), ('katherine', 'KTRN111111'),\
                ('kathleen', 'KTLN111111'), ('katie', 'KTA1111111'),\
                ('katrine', 'KTRN111111'), ('kay', 'KA11111111'),\
                ('keith', 'KT11111111'), ('keitha', 'KTA1111111'),\
                ('kelburne', 'KPN1111111'), ('kendal', 'KNTA111111'),\
                ('kennedy', 'KNTA111111'), ('kenneth', 'KNT1111111'),\
                ('kenny', 'KNA1111111'), ('keren', 'KRN1111111'),\
                ('keriah', 'KRA1111111'), ('kessel', 'KSA1111111'),\
                ('keturah', 'KTRA111111'), ('kezia', 'KSA1111111'),\
                ('keziah', 'KSA1111111'), ('king', 'KNK1111111'),\
                ('kingsley', 'KNKSLA1111'), ('kinnear', 'KNA1111111'),\
                ('kittie', 'KTA1111111'), ('kitty', 'KTA1111111'),\
                ('koa', 'KA11111111'), ('koren', 'KRN1111111'),\
                ('kuff', 'KF11111111'), ('kum', 'KM11111111'),\
                ('kurt', 'KT11111111'), ('kyra', 'KRA1111111'),\
                ('l', 'A111111111'), ('lachlan', 'LKLN111111'),\
                ('ladislas', 'LTSLS11111'), ('lallah', 'LLA1111111'),\
                ('lamsel', 'LMSA111111'), ('lan', 'LN11111111'),\
                ('lance', 'LNK1111111'), ('lancelot', 'LNSLT11111'),\
                ('langford', 'LNKFT11111'), ('langley', 'LNKLA11111'),\
                ('langlow', 'LNKLA11111'), ('lansley', 'LNSLA11111'),\
                ('lars', 'LS11111111'), ('lauchlan', 'LKLN111111'),\
                ('lauder', 'LTA1111111'), ('launa', 'LNA1111111'),\
                ('launcelot', 'LNSLT11111'), ('laura', 'LRA1111111'),\
                ('laurel', 'LRA1111111'), ('laurena', 'LRNA111111'),\
                ('laurence', 'LRNK111111'), ('laurencia', 'LRNSA11111'),\
                ('laurentine', 'LRNTN11111'), ('lauri', 'LRA1111111'),\
                ('laurie', 'LRA1111111'), ('laurinda', 'LRNTA11111'),\
                ('lauris', 'LRS1111111'), ('laveana', 'LFNA111111'),\
                ('lavender', 'LFNTA11111'), ('lavina', 'LFNA111111'),\
                ('lavinia', 'LFNA111111'), ('lavinla', 'LFNLA11111'),\
                ('lawford', 'LFT1111111'), ('lawrance', 'LRNK111111'),\
                ('lawrence', 'LRNK111111'), ('lawson', 'LSN1111111'),\
                ('leah', 'LA11111111'), ('ledestian', 'LTSN111111'),\
                ('lee', 'LA11111111'), ('leicester', 'LSSTA11111'),\
                ('leila', 'LLA1111111'), ('leith', 'LT11111111'),\
                ('lelia', 'LLA1111111'), ('lella', 'LLA1111111'),\
                ('lena', 'LNA1111111'), ('lenard', 'LNT1111111'),\
                ('lennie', 'LNA1111111'), ('lennox', 'LNK1111111'),\
                ('lenora', 'LNRA111111'), ('lenton', 'LNTN111111'),\
                ('leo', 'LA11111111'), ('leocadia', 'LKTA111111'),\
                ('leon', 'LN11111111'), ('leona', 'LNA1111111'),\
                ('leonard', 'LNT1111111'), ('leonia', 'LNA1111111'),\
                ('leonie', 'LNA1111111'), ('leonora', 'LNRA111111'),\
                ('leontine', 'LNTN111111'), ('leopold', 'LPT1111111'),\
                ('lerleine', 'LLN1111111'), ('lesla', 'LSLA111111'),\
                ('lesle', 'LSA1111111'), ('lesley', 'LSLA111111'),\
                ('leslie', 'LSLA111111'), ('leslle', 'LSA1111111'),\
                ('lesney', 'LSNA111111'), ('lester', 'LSTA111111'),\
                ('leta', 'LTA1111111'), ('letiris', 'LTRS111111'),\
                ('letita', 'LTTA111111'), ('letitia', 'LTSA111111'),\
                ('lettia', 'LTSA111111'), ('lettice', 'LTK1111111'),\
                ('lettie', 'LTA1111111'), ('letty', 'LTA1111111'),\
                ('levenia', 'LFNA111111'), ('levina', 'LFNA111111'),\
                ('levinia', 'LFNA111111'), ('levy', 'LFA1111111'),\
                ('lewellyn', 'LWLN111111'), ('lewis', 'LWS1111111'),\
                ('leyson', 'LSN1111111'), ('lezlie', 'LSLA111111'),\
                ('lil', 'LA11111111'), ('lila', 'LLA1111111'),\
                ('lilas', 'LLS1111111'), ('lileth', 'LLT1111111'),\
                ('lilia', 'LLA1111111'), ('liliam', 'LLM1111111'),\
                ('lilian', 'LLN1111111'), ('lilias', 'LLS1111111'),\
                ('lilla', 'LLA1111111'), ('lillan', 'LLN1111111'),\
                ('lillas', 'LLS1111111'), ('lilley', 'LLA1111111'),\
                ('lillia', 'LLA1111111'), ('lillian', 'LLN1111111'),\
                ('lillias', 'LLS1111111'), ('lillie', 'LLA1111111'),\
                ('lillingstone', 'LLNKSTN111'), ('lillis', 'LLS1111111'),\
                ('lilly', 'LLA1111111'), ('lilv', 'LF11111111'),\
                ('lily', 'LLA1111111'), ('lina', 'LNA1111111'),\
                ('lincoln', 'LNKN111111'), ('linda', 'LNTA111111'),\
                ('lindo', 'LNTA111111'), ('lindsay', 'LNTSA11111'),\
                ('linford', 'LNFT111111'), ('linnet', 'LNT1111111'),\
                ('lionel', 'LNA1111111'), ('lionella', 'LNLA111111'),\
                ('lionelle', 'LNA1111111'), ('lisette', 'LST1111111'),\
                ('lizzie', 'LSA1111111'), ('llewellyn', 'LWLN111111'),\
                ('llewelyn', 'LWLN111111'), ('lloyd', 'LT11111111'),\
                ('lna', 'NA11111111'), ('loftus', 'LFTS111111'),\
                ('lois', 'LS11111111'), ('loma', 'LMA1111111'),\
                ('lona', 'LNA1111111'), ('long', 'LNK1111111'),\
                ('lora', 'LRA1111111'), ('loreen', 'LRN1111111'),\
                ('loris', 'LRS1111111'), ('lorna', 'LNA1111111'),\
                ('lorraine', 'LRN1111111'), ('lot', 'LT11111111'),\
                ('lott', 'LT11111111'), ('lottia', 'LTSA111111'),\
                ('lottie', 'LTA1111111'), ('lotty', 'LTA1111111'),\
                ('louia', 'LA11111111'), ('louie', 'LA11111111'),\
                ('louis', 'LS11111111'), ('louisa', 'LSA1111111'),\
                ('louise', 'LS11111111'), ('lrene', 'RN11111111'),\
                ('lsaac', 'SK11111111'), ('lsabel', 'SPA1111111'),\
                ('lsabella', 'SPLA111111'), ('luanna', 'LNA1111111'),\
                ('lucerne', 'LSN1111111'), ('lucey', 'LSA1111111'),\
                ('lucie', 'LSA1111111'), ('lucilla', 'LSLA111111'),\
                ('lucille', 'LSA1111111'), ('lucina', 'LSNA111111'),\
                ('lucius', 'LSS1111111'), ('lucretia', 'LKRSA11111'),\
                ('lucy', 'LSA1111111'), ('ludwig', 'LTWK111111'),\
                ('luella', 'LLA1111111'), ('luke', 'LK11111111'),\
                ('lulu', 'LLA1111111'), ('lurline', 'LLN1111111'),\
                ('lva', 'FA11111111'), ('lvy', 'FA11111111'),\
                ('lyda', 'LTA1111111'), ('lydia', 'LTA1111111'),\
                ('lyell', 'LA11111111'), ('lygia', 'LKA1111111'),\
                ('lyla', 'LLA1111111'), ('lylah', 'LLA1111111'),\
                ('lyle', 'LA11111111'), ('lylie', 'LLA1111111'),\
                ('lylo', 'LLA1111111'), ('lynass', 'LNS1111111'),\
                ('lynda', 'LNTA111111'), ('lynden', 'LNTN111111'),\
                ('lyndon', 'LNTN111111'), ('lyndsay', 'LNTSA11111'),\
                ('lyndsey', 'LNTSA11111'), ('mabel', 'MPA1111111'),\
                ('mabelle', 'MPA1111111'), ('mable', 'MPA1111111'),\
                ('machell', 'MKA1111111'), ('madalene', 'MTLN111111'),\
                ('madaline', 'MTLN111111'), ('maddie', 'MTA1111111'),\
                ('madeleine', 'MTLN111111'), ('madeline', 'MTLN111111'),\
                ('madge', 'MK11111111'), ('madglene', 'MKLN111111'),\
                ('mae', 'MA11111111'), ('magdalen', 'MKTLN11111'),\
                ('magdalena', 'MKTLNA1111'), ('magdalene', 'MKTLN11111'),\
                ('magdaline', 'MKTLN11111'), ('magdeline', 'MKTLN11111'),\
                ('maggie', 'MKA1111111'), ('magnus', 'MKNS111111'),\
                ('magnustina', 'MKNSTNA111'), ('mahala', 'MLA1111111'),\
                ('mai', 'MA11111111'), ('maida', 'MTA1111111'),\
                ('maie', 'MA11111111'), ('maine', 'MN11111111'),\
                ('maira', 'MRA1111111'), ('maisie', 'MSA1111111'),\
                ('maitland', 'MTLNT11111'), ('majorie', 'MRA1111111'),\
                ('majory', 'MRA1111111'), ('malachi', 'MLKA111111'),\
                ('malcolm', 'MKM1111111'), ('maltravers', 'MTRFS11111'),\
                ('malvena', 'MFNA111111'), ('mamie', 'MMA1111111'),\
                ('mana', 'MNA1111111'), ('manes', 'MNS1111111'),\
                ('manie', 'MNA1111111'), ('mann', 'MN11111111'),\
                ('mano', 'MNA1111111'), ('mansfield', 'MNSFT11111'),\
                ('marah', 'MRA1111111'), ('marama', 'MRMA111111'),\
                ('maraval', 'MRFA111111'), ('marcella', 'MSLA111111'),\
                ('marcelle', 'MSA1111111'), ('marcia', 'MSA1111111'),\
                ('marcus', 'MKS1111111'), ('maree', 'MRA1111111'),\
                ('maretta', 'MRTA111111'), ('margaret', 'MKRT111111'),\
                ('margareta', 'MKRTA11111'), ('margarete', 'MKRT111111'),\
                ('margarett', 'MKRT111111'), ('margaretta', 'MKRTA11111'),\
                ('margarita', 'MKRTA11111'), ('margarretta', 'MKRTA11111'),\
                ('margerett', 'MKRT111111'), ('margerie', 'MKRA111111'),\
                ('margerite', 'MKRT111111'), ('margery', 'MKRA111111'),\
                ('margeurite', 'MKRT111111'), ('margharita', 'MRTA111111'),\
                ('margherita', 'MRTA111111'), ('margie', 'MKA1111111'),\
                ('margorie', 'MKRA111111'), ('margory', 'MKRA111111'),\
                ('margretta', 'MKRTA11111'), ('marguereta', 'MKRTA11111'),\
                ('margueretta', 'MKRTA11111'), ('marguerita', 'MKRTA11111'),\
                ('marguerite', 'MKRT111111'), ('margurerite', 'MKRRT11111'),\
                ('maria', 'MRA1111111'), ('mariam', 'MRM1111111'),\
                ('marian', 'MRN1111111'), ('marianne', 'MRN1111111'),\
                ('maribel', 'MRPA111111'), ('marica', 'MRKA111111'),\
                ('marie', 'MRA1111111'), ('marieta', 'MRTA111111'),\
                ('marina', 'MRNA111111'), ('marion', 'MRN1111111'),\
                ('marita', 'MRTA111111'), ('marius', 'MRS1111111'),\
                ('marjorie', 'MRRA111111'), ('marjorio', 'MRRA111111'),\
                ('marjory', 'MRRA111111'), ('mark', 'MK11111111'),\
                ('marmaduke', 'MMTK111111'), ('marrian', 'MRN1111111'),\
                ('marsella', 'MSLA111111'), ('marshall', 'MSA1111111'),\
                ('martha', 'MTA1111111'), ('martin', 'MTN1111111'),\
                ('marton', 'MTN1111111'), ('mary', 'MRA1111111'),\
                ('masie', 'MSA1111111'), ('mata', 'MTA1111111'),\
                ('mataura', 'MTRA111111'), ('mathea', 'MTA1111111'),\
                ('mathew', 'MTA1111111'), ('mathias', 'MTS1111111'),\
                ('mathina', 'MTNA111111'), ('matilda', 'MTTA111111'),\
                ('matthew', 'MTA1111111'), ('mattie', 'MTA1111111'),\
                ('maud', 'MT11111111'), ('mauda', 'MTA1111111'),\
                ('maude', 'MT11111111'), ('maudie', 'MTA1111111'),\
                ('maurce', 'MK11111111'), ('maureen', 'MRN1111111'),\
                ('maurice', 'MRK1111111'), ('mavis', 'MFS1111111'),\
                ('mavora', 'MFRA111111'), ('max', 'MK11111111'),\
                ('maxime', 'MKM1111111'), ('maxwell', 'MKWA111111'),\
                ('may', 'MA11111111'), ('mayda', 'MTA1111111'),\
                ('maye', 'MA11111111'), ('maynard', 'MNT1111111'),\
                ('maythal', 'MTA1111111'), ('mayvee', 'MFA1111111'),\
                ('mcewan', 'MSWN111111'), ('mcewen', 'MSWN111111'),\
                ('mchardy', 'MKTA111111'), ('meda', 'MTA1111111'),\
                ('melanie', 'MLNA111111'), ('melba', 'MPA1111111'),\
                ('melen', 'MLN1111111'), ('melia', 'MLA1111111'),\
                ('melton', 'MTN1111111'), ('melva', 'MFA1111111'),\
                ('melville', 'MFA1111111'), ('melvyn', 'MFN1111111'),\
                ('mena', 'MNA1111111'), ('menia', 'MNA1111111'),\
                ('menry', 'MNRA111111'), ('menzie', 'MNSA111111'),\
                ('menzies', 'MNSS111111'), ('mera', 'MRA1111111'),\
                ('mercedes', 'MSTS111111'), ('mercia', 'MSA1111111'),\
                ('mercy', 'MSA1111111'), ('meredith', 'MRTT111111'),\
                ('merian', 'MRN1111111'), ('merle', 'MA11111111'),\
                ('merlin', 'MLN1111111'), ('merrial', 'MRA1111111'),\
                ('merrin', 'MRN1111111'), ('merton', 'MTN1111111'),\
                ('mervyn', 'MFN1111111'), ('meryl', 'MRA1111111'),\
                ('meryle', 'MRA1111111'), ('meta', 'MTA1111111'),\
                ('metta', 'MTA1111111'), ('meynard', 'MNT1111111'),\
                ('miah', 'MA11111111'), ('michael', 'MKA1111111'),\
                ('michale', 'MKA1111111'), ('miehael', 'MA11111111'),\
                ('mignon', 'MKNN111111'), ('mildred', 'MTRT111111'),\
                ('milena', 'MLNA111111'), ('miles', 'MLS1111111'),\
                ('millar', 'MLA1111111'), ('millen', 'MLN1111111'),\
                ('millicent', 'MLSNT11111'), ('millie', 'MLA1111111'),\
                ('millis', 'MLS1111111'), ('milly', 'MLA1111111'),\
                ('milo', 'MLA1111111'), ('milton', 'MTN1111111'),\
                ('mima', 'MMA1111111'), ('mimie', 'MMA1111111'),\
                ('mina', 'MNA1111111'), ('minan', 'MNN1111111'),\
                ('minna', 'MNA1111111'), ('minnie', 'MNA1111111'),\
                ('mira', 'MRA1111111'), ('miranda', 'MRNTA11111'),\
                ('miriam', 'MRM1111111'), ('mirian', 'MRN1111111'),\
                ('miriel', 'MRA1111111'), ('mirnie', 'MNA1111111'),\
                ('miro', 'MRA1111111'), ('mister', 'MSTA111111'),\
                ('mitchell', 'MKA1111111'), ('moana', 'MNA1111111'),\
                ('moira', 'MRA1111111'), ('mollie', 'MLA1111111'),\
                ('molly', 'MLA1111111'), ('mona', 'MNA1111111'),\
                ('monatague', 'MNTKA11111'), ('moncrieff', 'MNKRF11111'),\
                ('monica', 'MNKA111111'), ('montague', 'MNTKA11111'),\
                ('monteith', 'MNTT111111'), ('mony', 'MNA1111111'),\
                ('morgan', 'MKN1111111'), ('morie', 'MRA1111111'),\
                ('moris', 'MRS1111111'), ('morison', 'MRSN111111'),\
                ('morris', 'MRS1111111'), ('morrison', 'MRSN111111'),\
                ('mortimer', 'MTMA111111'), ('morton', 'MTN1111111'),\
                ('moses', 'MSS1111111'), ('moura', 'MRA1111111'),\
                ('moyra', 'MRA1111111'), ('mrytle', 'MRTA111111'),\
                ('muareen', 'MRN1111111'), ('mugh', 'MA11111111'),\
                ('mungo', 'MNKA111111'), ('munro', 'MNRA111111'),\
                ('mura', 'MRA1111111'), ('murdo', 'MTA1111111'),\
                ('murdoch', 'MTK1111111'), ('murial', 'MRA1111111'),\
                ('muriel', 'MRA1111111'), ('murray', 'MRA1111111'),\
                ('murtha', 'MTA1111111'), ('myles', 'MLS1111111'),\
                ('mynot', 'MNT1111111'), ('myra', 'MRA1111111'),\
                ('myrtle', 'MTA1111111'), ('myttle', 'MTA1111111'),\
                ('naamah', 'NMA1111111'), ('nance', 'NNK1111111'),\
                ('nancie', 'NNSA111111'), ('nancy', 'NNSA111111'),\
                ('nancybell', 'NNSPA11111'), ('naney', 'NNA1111111'),\
                ('nano', 'NNA1111111'), ('nansbell', 'NNSPA11111'),\
                ('naomi', 'NMA1111111'), ('nardor', 'NTA1111111'),\
                ('narman', 'NMN1111111'), ('narotamdas', 'NRTMTS1111'),\
                ('natalie', 'NTLA111111'), ('nathan', 'NTN1111111'),\
                ('nathaniel', 'NTNA111111'), ('naylor', 'NLA1111111'),\
                ('neah', 'NA11111111'), ('neil', 'NA11111111'),\
                ('neilina', 'NLNA111111'), ('neill', 'NA11111111'),\
                ('nell', 'NA11111111'), ('nella', 'NLA1111111'),\
                ('nelletta', 'NLTA111111'), ('nellia', 'NLA1111111'),\
                ('nellic', 'NLK1111111'), ('nellie', 'NLA1111111'),\
                ('nellin', 'NLN1111111'), ('nelly', 'NLA1111111'),\
                ('nelson', 'NSN1111111'), ('nenetta', 'NNTA111111'),\
                ('nera', 'NRA1111111'), ('nesbit', 'NSPT111111'),\
                ('nessie', 'NSA1111111'), ('nesta', 'NSTA111111'),\
                ('nestor', 'NSTA111111'), ('netherton', 'NTTN111111'),\
                ('netta', 'NTA1111111'), ('netterwille', 'NTWA111111'),\
                ('nettie', 'NTA1111111'), ('neville', 'NFA1111111'),\
                ('newman', 'NMN1111111'), ('ngaere', 'NKA1111111'),\
                ('ngahuir', 'NKA1111111'), ('ngaira', 'NKRA111111'),\
                ('ngaire', 'NKA1111111'), ('ngaria', 'NKRA111111'),\
                ('ngarita', 'NKRTA11111'), ('ngyra', 'NKRA111111'),\
                ('ngyre', 'NKA1111111'), ('niary', 'NRA1111111'),\
                ('nicalena', 'NKLNA11111'), ('nichol', 'NKA1111111'),\
                ('nichola', 'NKLA111111'), ('nicholas', 'NKLS111111'),\
                ('nicol', 'NKA1111111'), ('nicolena', 'NKLNA11111'),\
                ('nicolina', 'NKLNA11111'), ('niel', 'NA11111111'),\
                ('niels', 'NS11111111'), ('nigel', 'NKA1111111'),\
                ('nils', 'NS11111111'), ('nina', 'NNA1111111'),\
                ('ninetta', 'NNTA111111'), ('nita', 'NTA1111111'),\
                ('no', 'NA11111111'), ('noel', 'NA11111111'),\
                ('noeleen', 'NLN1111111'), ('noeline', 'NLN1111111'),\
                ('noell', 'NA11111111'), ('noelle', 'NA11111111'),\
                ('noilina', 'NLNA111111'), ('nola', 'NLA1111111'),\
                ('nona', 'NNA1111111'), ('noney', 'NNA1111111'),\
                ('noni', 'NNA1111111'), ('nonie', 'NNA1111111'),\
                ('nora', 'NRA1111111'), ('norah', 'NRA1111111'),\
                ('noreen', 'NRN1111111'), ('norine', 'NRN1111111'),\
                ('norma', 'NMA1111111'), ('norman', 'NMN1111111'),\
                ('normena', 'NMNA111111'), ('normina', 'NMNA111111'),\
                ('norris', 'NRS1111111'), ('north', 'NT11111111'),\
                ('noslie', 'NSLA111111'), ('nova', 'NFA1111111'),\
                ('nozlie', 'NSLA111111'), ('nyra', 'NRA1111111'),\
                ('oban', 'APN1111111'), ('octavia', 'AKTFA11111'),\
                ('octavius', 'AKTFS11111'), ('odin', 'ATN1111111'),\
                ('ogier', 'AKA1111111'), ('ola', 'ALA1111111'),\
                ('olaf', 'ALF1111111'), ('olai', 'ALA1111111'),\
                ('ole', 'AA11111111'), ('olef', 'ALF1111111'),\
                ('olga', 'AKA1111111'), ('oliphant', 'ALFNT11111'),\
                ('olive', 'ALF1111111'), ('olivel', 'ALFA111111'),\
                ('oliver', 'ALFA111111'), ('olivera', 'ALFRA11111'),\
                ('oliverpaul', 'ALFPA11111'), ('olivia', 'ALFA111111'),\
                ('olivo', 'ALFA111111'), ('olliffe', 'ALF1111111'),\
                ('olof', 'ALF1111111'), ('oloff', 'ALF1111111'),\
                ('olvia', 'AFA1111111'), ('olwyn', 'AWN1111111'),\
                ('onawe', 'ANA1111111'), ('onie', 'ANA1111111'),\
                ('oonah', 'ANA1111111'), ('ophir', 'AFA1111111'),\
                ('ora', 'ARA1111111'), ('oral', 'ARA1111111'),\
                ('oriel', 'ARA1111111'), ('orlando', 'ALNTA11111'),\
                ('orma', 'AMA1111111'), ('ormandy', 'AMNTA11111'),\
                ('orme', 'AM11111111'), ('ormond', 'AMNT111111'),\
                ('orpah', 'APA1111111'), ('orpheus', 'AFS1111111'),\
                ('orthus', 'ATS1111111'), ('orton', 'ATN1111111'),\
                ('orvis', 'AFS1111111'), ('osald', 'AST1111111'),\
                ('osborn', 'ASPN111111'), ('osborne', 'ASPN111111'),\
                ('oscar', 'ASKA111111'), ('oslin', 'ASLN111111'),\
                ('oswald', 'ASWT111111'), ('othelia', 'ATLA111111'),\
                ('otilia', 'ATLA111111'), ('otto', 'ATA1111111'),\
                ('ough', 'AA11111111'), ('ouston', 'ASTN111111'),\
                ('overton', 'AFTN111111'), ('owen', 'AWN1111111'),\
                ('ozmond', 'ASMNT11111'), ('pamela', 'PMLA111111'),\
                ('pansy', 'PNSA111111'), ('par', 'PA11111111'),\
                ('paris', 'PRS1111111'), ('parke', 'PK11111111'),\
                ('parry', 'PRA1111111'), ('paterson', 'PTSN111111'),\
                ('patience', 'PTNK111111'), ('patrck', 'PTK1111111'),\
                ('patricia', 'PTRSA11111'), ('patrick', 'PTRK111111'),\
                ('patton', 'PTN1111111'), ('paul', 'PA11111111'),\
                ('paulina', 'PLNA111111'), ('pauline', 'PLN1111111'),\
                ('pearl', 'PA11111111'), ('pearlie', 'PLA1111111'),\
                ('peggie', 'PKA1111111'), ('peggotty', 'PKTA111111'),\
                ('peggy', 'PKA1111111'), ('penelope', 'PNLP111111'),\
                ('penrose', 'PNRS111111'), ('percival', 'PSFA111111'),\
                ('percy', 'PSA1111111'), ('percystreetclair', 'PSSTRTKLA1'),\
                ('pereival', 'PRFA111111'), ('perey', 'PRA1111111'),\
                ('pertha', 'PTA1111111'), ('pete', 'PT11111111'),\
                ('peter', 'PTA1111111'), ('phbe', 'FP11111111'),\
                ('phebe', 'FP11111111'), ('phedora', 'FTRA111111'),\
                ('pheodora', 'FTRA111111'), ('philip', 'FLP1111111'),\
                ('philippa', 'FLPA111111'), ('phillip', 'FLP1111111'),\
                ('phillipa', 'FLPA111111'), ('phillis', 'FLS1111111'),\
                ('philomena', 'FLMNA11111'), ('phoebe', 'FP11111111'),\
                ('phoenix', 'FNK1111111'), ('phylis', 'FLS1111111'),\
                ('phyliss', 'FLS1111111'), ('phyllis', 'FLS1111111'),\
                ('pierce', 'PK11111111'), ('pleasance', 'PLSNK11111'),\
                ('pleasant', 'PLSNT11111'), ('polly', 'PLA1111111'),\
                ('poppy', 'PPA1111111'), ('pretoria', 'PRTRA11111'),\
                ('prisca', 'PRSKA11111'), ('priscilla', 'PRSLA11111'),\
                ('prothesia', 'PRTSA11111'), ('prudence', 'PRTNK11111'),\
                ('prudentchia', 'PRTNKA1111'), ('pryna', 'PRNA111111'),\
                ('queen', 'KN11111111'), ('queenie', 'KNA1111111'),\
                ('quinton', 'KNTN111111'), ('rachael', 'RKA1111111'),\
                ('rachal', 'RKA1111111'), ('rachall', 'RKA1111111'),\
                ('rachel', 'RKA1111111'), ('radium', 'RTM1111111'),\
                ('rae', 'RA11111111'), ('raeburn', 'RPN1111111'),\
                ('raiph', 'RF11111111'), ('ralph', 'RF11111111'),\
                ('randall', 'RNTA111111'), ('randell', 'RNTA111111'),\
                ('randolph', 'RNTF111111'), ('rani', 'RNA1111111'),\
                ('raphael', 'RFA1111111'), ('rasmas', 'RSMS111111'),\
                ('rawena', 'RWNA111111'), ('ray', 'RA11111111'),\
                ('rayena', 'RNA1111111'), ('raymie', 'RMA1111111'),\
                ('raymond', 'RMNT111111'), ('raymonde', 'RMNT111111'),\
                ('raymund', 'RMNT111111'), ('rayna', 'RNA1111111'),\
                ('rea', 'RA11111111'), ('rebbecca', 'RPKA111111'),\
                ('rebecca', 'RPKA111111'), ('rebeckah', 'RPKA111111'),\
                ('rebekah', 'RPKA111111'), ('redmond', 'RTMNT11111'),\
                ('redvers', 'RTFS111111'), ('reece', 'RK11111111'),\
                ('regina', 'RKNA111111'), ('reginald', 'RKNT111111'),\
                ('reita', 'RTA1111111'), ('rema', 'RMA1111111'),\
                ('rena', 'RNA1111111'), ('rene', 'RN11111111'),\
                ('renee', 'RNA1111111'), ('renna', 'RNA1111111'),\
                ('rero', 'RRA1111111'), ('reta', 'RTA1111111'),\
                ('retta', 'RTA1111111'), ('reuben', 'RPN1111111'),\
                ('revina', 'RFNA111111'), ('rewa', 'RWA1111111'),\
                ('rewi', 'RWA1111111'), ('rex', 'RK11111111'),\
                ('rexiter', 'RKTA111111'), ('reyna', 'RNA1111111'),\
                ('reynolds', 'RNTS111111'), ('rhoda', 'TA11111111'),\
                ('rhoderick', 'TRK1111111'), ('rhoma', 'MA11111111'),\
                ('rhona', 'NA11111111'), ('rica', 'RKA1111111'),\
                ('richald', 'RKT1111111'), ('richard', 'RKT1111111'),\
                ('richena', 'RKNA111111'), ('richmond', 'RKMNT11111'),\
                ('ricka', 'RKA1111111'), ('ridley', 'RTLA111111'),\
                ('rieka', 'RKA1111111'), ('rieta', 'RTA1111111'),\
                ('riha', 'RA11111111'), ('rima', 'RMA1111111'),\
                ('rina', 'RNA1111111'), ('riparata', 'RPRTA11111'),\
                ('rita', 'RTA1111111'), ('ritchie', 'RKA1111111'),\
                ('roa', 'RA11111111'), ('roanna', 'RNA1111111'),\
                ('robena', 'RPNA111111'), ('robert', 'RPT1111111'),\
                ('roberta', 'RPTA111111'), ('robertina', 'RPTNA11111'),\
                ('roberton', 'RPTN111111'), ('roberts', 'RPTS111111'),\
                ('robertson', 'RPTSN11111'), ('robin', 'RPN1111111'),\
                ('robina', 'RPNA111111'), ('robins', 'RPNS111111'),\
                ('robinson', 'RPNSN11111'), ('roderick', 'RTRK111111'),\
                ('rodger', 'RKA1111111'), ('rodney', 'RTNA111111'),\
                ('rodrick', 'RTRK111111'), ('roger', 'RKA1111111'),\
                ('roland', 'RLNT111111'), ('roma', 'RMA1111111'),\
                ('rona', 'RNA1111111'), ('ronald', 'RNT1111111'),\
                ('ronstad', 'RNSTT11111'), ('rosa', 'RSA1111111'),\
                ('rosabell', 'RSPA111111'), ('rosabella', 'RSPLA11111'),\
                ('rosaland', 'RSLNT11111'), ('rosaleene', 'RSLN111111'),\
                ('rosalie', 'RSLA111111'), ('rosalind', 'RSLNT11111'),\
                ('rosaline', 'RSLN111111'), ('rosalla', 'RSLA111111'),\
                ('rosamond', 'RSMNT11111'), ('rosamund', 'RSMNT11111'),\
                ('rosana', 'RSNA111111'), ('rosanah', 'RSNA111111'),\
                ('rosanna', 'RSNA111111'), ('rosannah', 'RSNA111111'),\
                ('rosanne', 'RSN1111111'), ('roscena', 'RSNA111111'),\
                ('rose', 'RS11111111'), ('roseana', 'RSNA111111'),\
                ('roseanna', 'RSNA111111'), ('roseina', 'RSNA111111'),\
                ('rosella', 'RSLA111111'), ('rosemay', 'RSMA111111'),\
                ('rosemond', 'RSMNT11111'), ('rosena', 'RSNA111111'),\
                ('rosetta', 'RSTA111111'), ('rosie', 'RSA1111111'),\
                ('rosiena', 'RSNA111111'), ('rosina', 'RSNA111111'),\
                ('rosins', 'RSNS111111'), ('ross', 'RS11111111'),\
                ('roustad', 'RSTT111111'), ('rowena', 'RWNA111111'),\
                ('rowland', 'RLNT111111'), ('roy', 'RA11111111'),\
                ('rozel', 'RSA1111111'), ('rua', 'RA11111111'),\
                ('ruahine', 'RN11111111'), ('ruben', 'RPN1111111'),\
                ('rubena', 'RPNA111111'), ('rubenia', 'RPNA111111'),\
                ('rubina', 'RPNA111111'), ('rubins', 'RPNS111111'),\
                ('rubv', 'RPF1111111'), ('ruby', 'RPA1111111'),\
                ('rubye', 'RPA1111111'), ('rudolf', 'RTF1111111'),\
                ('rudolph', 'RTF1111111'), ('rufus', 'RFS1111111'),\
                ('rugby', 'RKPA111111'), ('rui', 'RA11111111'),\
                ('ruia', 'RA11111111'), ('runa', 'RNA1111111'),\
                ('ruper', 'RPA1111111'), ('rupert', 'RPT1111111'),\
                ('ruruhira', 'RRRA111111'), ('russell', 'RSA1111111'),\
                ('ruth', 'RT11111111'), ('rutherford', 'RTFT111111'),\
                ('saah', 'SA11111111'), ('saba', 'SPA1111111'),\
                ('sabina', 'SPNA111111'), ('sadie', 'STA1111111'),\
                ('saidie', 'STA1111111'), ('sam', 'SM11111111'),\
                ('sampson', 'SMPSN11111'), ('samson', 'SMSN111111'),\
                ('samuel', 'SMA1111111'), ('samuelena', 'SMLNA11111'),\
                ('sanuel', 'SNA1111111'), ('sara', 'SRA1111111'),\
                ('sarah', 'SRA1111111'), ('saverio', 'SFRA111111'),\
                ('saxon', 'SKN1111111'), ('scott', 'SKT1111111'),\
                ('scoular', 'SKLA111111'), ('seaward', 'SWT1111111'),\
                ('sedden', 'STN1111111'), ('seddon', 'STN1111111'),\
                ('selah', 'SLA1111111'), ('selem', 'SLM1111111'),\
                ('selena', 'SLNA111111'), ('selina', 'SLNA111111'),\
                ('selinda', 'SLNTA11111'), ('selma', 'SMA1111111'),\
                ('selwyn', 'SWN1111111'), ('septimus', 'SPTMS11111'),\
                ('serafina', 'SRFNA11111'), ('sergia', 'SKA1111111'),\
                ('seth', 'ST11111111'), ('sharland', 'SLNT111111'),\
                ('sheddan', 'STN1111111'), ('sheila', 'SLA1111111'),\
                ('shelia', 'SLA1111111'), ('shiela', 'SLA1111111'),\
                ('shirley', 'SLA1111111'), ('shona', 'SNA1111111'),\
                ('siah', 'SA11111111'), ('sibyl', 'SPA1111111'),\
                ('sidey', 'STA1111111'), ('sidney', 'STNA111111'),\
                ('sidona', 'STNA111111'), ('signa', 'SKNA111111'),\
                ('signe', 'SKN1111111'), ('sigrid', 'SKRT111111'),\
                ('silas', 'SLS1111111'), ('silena', 'SLNA111111'),\
                ('silva', 'SFA1111111'), ('simeon', 'SMN1111111'),\
                ('simon', 'SMN1111111'), ('simpson', 'SMPSN11111'),\
                ('sina', 'SNA1111111'), ('sinclair', 'SNKLA11111'),\
                ('singleton', 'SNKLTN1111'), ('sissy', 'SSA1111111'),\
                ('solomon', 'SLMN111111'), ('somerled', 'SMLT111111'),\
                ('sophia', 'SFA1111111'), ('sophie', 'SFA1111111'),\
                ('sophrania', 'SFRNA11111'), ('sophrona', 'SFRNA11111'),\
                ('sophronia', 'SFRNA11111'), ('sophy', 'SFA1111111'),\
                ('spence', 'SPNK111111'), ('spencer', 'SPNSA11111'),\
                ('spenseley', 'SPNSLA1111'), ('spensley', 'SPNSLA1111'),\
                ('squire', 'SKA1111111'), ('st', 'ST11111111'),\
                ('stafford', 'STFT111111'), ('stanhope', 'STNP111111'),\
                ('stanislaus', 'STNSLS1111'), ('stanislaw', 'STNSLA1111'),\
                ('stanislaws', 'STNSLS1111'), ('stanley', 'STNLA11111'),\
                ('stanton', 'STNTN11111'), ('stasia', 'STSA111111'),\
                ('statney', 'STTNA11111'), ('stella', 'STLA111111'),\
                ('stephanie', 'STFNA11111'), ('stephen', 'STFN111111'),\
                ('steven', 'STFN111111'), ('steward', 'STWT111111'),\
                ('stewart', 'STWT111111'), ('stewarty', 'STWTA11111'),\
                ('stisie', 'STSA111111'), ('stratford', 'STRTFT1111'),\
                ('strelna', 'STRNA11111'), ('strop', 'STRP111111'),\
                ('struan', 'STRN111111'), ('stuart', 'STT1111111'),\
                ('sturz', 'STS1111111'), ('surrey', 'SRA1111111'),\
                ('susan', 'SSN1111111'), ('susanah', 'SSNA111111'),\
                ('susanna', 'SSNA111111'), ('susannah', 'SSNA111111'),\
                ('susanne', 'SSN1111111'), ('susie', 'SSA1111111'),\
                ('susy', 'SSA1111111'), ('sybella', 'SPLA111111'),\
                ('sybil', 'SPA1111111'), ('sydnev', 'STNF111111'),\
                ('sydney', 'STNA111111'), ('sylva', 'SFA1111111'),\
                ('sylvia', 'SFA1111111'), ('sylvie', 'SFA1111111'),\
                ('syril', 'SRA1111111'), ('tabitha', 'TPTA111111'),\
                ('talbert', 'TPT1111111'), ('tamar', 'TMA1111111'),\
                ('tasma', 'TSMA111111'), ('tasman', 'TSMN111111'),\
                ('tate', 'TT11111111'), ('taylor', 'TLA1111111'),\
                ('teariki', 'TRKA111111'), ('temperence', 'TMPRNK1111'),\
                ('terence', 'TRNK111111'), ('teresa', 'TRSA111111'),\
                ('teresae', 'TRSA111111'), ('ternce', 'TNK1111111'),\
                ('tesse', 'TS11111111'), ('tessie', 'TSA1111111'),\
                ('thaddeus', 'TTS1111111'), ('thea', 'TA11111111'),\
                ('theima', 'TMA1111111'), ('thelma', 'TMA1111111'),\
                ('theodocia', 'TTSA111111'), ('theodora', 'TTRA111111'),\
                ('theodore', 'TTA1111111'), ('theodosia', 'TTSA111111'),\
                ('theophilus', 'TFLS111111'), ('theresa', 'TRSA111111'),\
                ('therese', 'TRS1111111'), ('thirza', 'TSA1111111'),\
                ('tholmas', 'TMS1111111'), ('thomas', 'TMS1111111'),\
                ('thomasena', 'TMSNA11111'), ('thomasina', 'TMSNA11111'),\
                ('thompson', 'TMPSN11111'), ('thomson', 'TMSN111111'),\
                ('thora', 'TRA1111111'), ('thorburn', 'TPN1111111'),\
                ('thorita', 'TRTA111111'), ('thornton', 'TNTN111111'),\
                ('thriza', 'TRSA111111'), ('thursa', 'TSA1111111'),\
                ('thurstan', 'TSTN111111'), ('thurston', 'TSTN111111'),\
                ('thurza', 'TSA1111111'), ('thyrza', 'TSA1111111'),\
                ('thyza', 'TSA1111111'), ('tillie', 'TLA1111111'),\
                ('timothy', 'TMTA111111'), ('tiney', 'TNA1111111'),\
                ('tini', 'TNA1111111'), ('tiny', 'TNA1111111'),\
                ('tizzie', 'TSA1111111'), ('tom', 'TM11111111'),\
                ('touncy', 'TNSA111111'), ('tousseint', 'TSNT111111'),\
                ('treacy', 'TRSA111111'), ('tremella', 'TRMLA11111'),\
                ('trena', 'TRNA111111'), ('trene', 'TRN1111111'),\
                ('trentham', 'TRNTM11111'), ('tresa', 'TRSA111111'),\
                ('trevor', 'TRFA111111'), ('trilby', 'TRPA111111'),\
                ('trixie', 'TRKA111111'), ('tryphena', 'TRFNA11111'),\
                ('tui', 'TA11111111'), ('ulick', 'ALK1111111'),\
                ('ulrica', 'ARKA111111'), ('ulricka', 'ARKA111111'),\
                ('una', 'ANA1111111'), ('ural', 'ARA1111111'),\
                ('uresilla', 'ARSLA11111'), ('ureta', 'ARTA111111'),\
                ('ursula', 'ASLA111111'), ('uta', 'ATA1111111'),\
                ('valarie', 'FLRA111111'), ('valda', 'FTA1111111'),\
                ('valdemar', 'FTMA111111'), ('valencia', 'FLNSA11111'),\
                ('valentine', 'FLNTN11111'), ('valerie', 'FLRA111111'),\
                ('vallance', 'FLNK111111'), ('valma', 'FMA1111111'),\
                ('van', 'FN11111111'), ('vanda', 'FNTA111111'),\
                ('vanessa', 'FNSA111111'), ('vara', 'FRA1111111'),\
                ('varey', 'FRA1111111'), ('vashti', 'FSTA111111'),\
                ('vaughan', 'FKN1111111'), ('veda', 'FTA1111111'),\
                ('veida', 'FTA1111111'), ('vendella', 'FNTLA11111'),\
                ('venessa', 'FNSA111111'), ('venus', 'FNS1111111'),\
                ('vera', 'FRA1111111'), ('verdon', 'FTN1111111'),\
                ('verdun', 'FTN1111111'), ('vere', 'FA11111111'),\
                ('verena', 'FRNA111111'), ('verion', 'FRN1111111'),\
                ('verna', 'FNA1111111'), ('verner', 'FNA1111111'),\
                ('vernon', 'FNN1111111'), ('verona', 'FRNA111111'),\
                ('veronica', 'FRNKA11111'), ('vesper', 'FSPA111111'),\
                ('vickers', 'FKS1111111'), ('victor', 'FKTA111111'),\
                ('victoria', 'FKTRA11111'), ('vida', 'FTA1111111'),\
                ('vietoria', 'FTRA111111'), ('vilera', 'FLRA111111'),\
                ('vilhelm', 'FM11111111'), ('villa', 'FLA1111111'),\
                ('vina', 'FNA1111111'), ('vincent', 'FNSNT11111'),\
                ('vioiet', 'FT11111111'), ('viola', 'FLA1111111'),\
                ('violet', 'FLT1111111'), ('violetta', 'FLTA111111'),\
                ('violette', 'FLT1111111'), ('virgil', 'FKA1111111'),\
                ('virginia', 'FKNA111111'), ('viva', 'FFA1111111'),\
                ('vivian', 'FFN1111111'), ('vivien', 'FFN1111111'),\
                ('vivienne', 'FFN1111111'), ('vona', 'FNA1111111'),\
                ('walker', 'WKA1111111'), ('wallace', 'WLK1111111'),\
                ('wallis', 'WLS1111111'), ('walter', 'WTA1111111'),\
                ('walton', 'WTN1111111'), ('waltor', 'WTA1111111'),\
                ('wance', 'WNK1111111'), ('ward', 'WT11111111'),\
                ('warren', 'WRN1111111'), ('warrington', 'WRNKTN1111'),\
                ('water', 'WTA1111111'), ('watson', 'WTSN111111'),\
                ('wee', 'WA11111111'), ('welby', 'WPA1111111'),\
                ('wesby', 'WSPA111111'), ('wesley', 'WSLA111111'),\
                ('west', 'WST1111111'), ('wharten', 'WTN1111111'),\
                ('wharton', 'WTN1111111'), ('whenua', 'WNA1111111'),\
                ('whyndham', 'WNTM111111'), ('wicko', 'WKA1111111'),\
                ('wilbert', 'WPT1111111'), ('wilbur', 'WPA1111111'),\
                ('wilfred', 'WFRT111111'), ('wilfrid', 'WFRT111111'),\
                ('wilhelm', 'WM11111111'), ('wilhelmena', 'WMNA111111'),\
                ('wilhelmina', 'WMNA111111'), ('wilhemenia', 'WMNA111111'),\
                ('wilhemina', 'WMNA111111'), ('wilheminia', 'WMNA111111'),\
                ('wilkinson', 'WKNSN11111'), ('will', 'WA11111111'),\
                ('willamina', 'WLMNA11111'), ('willen', 'WLN1111111'),\
                ('william', 'WLM1111111'), ('williamina', 'WLMNA11111'),\
                ('williammina', 'WLMNA11111'), ('williams', 'WLMS111111'),\
                ('williamson', 'WLMSN11111'), ('willie', 'WLA1111111'),\
                ('willis', 'WLS1111111'), ('willitn', 'WLTN111111'),\
                ('wilma', 'WMA1111111'), ('wilmot', 'WMT1111111'),\
                ('wilson', 'WSN1111111'), ('windsor', 'WNTSA11111'),\
                ('winfred', 'WNFRT11111'), ('winifred', 'WNFRT11111'),\
                ('winnie', 'WNA1111111'), ('winniefred', 'WNFRT11111'),\
                ('winnifred', 'WNFRT11111'), ('winnifrid', 'WNFRT11111'),\
                ('winston', 'WNSTN11111'), ('wong', 'WNK1111111'),\
                ('wright', 'RT11111111'), ('wynie', 'WNA1111111'),\
                ('yetti', 'YTA1111111'), ('ysabel', 'ASPA111111'),\
                ('yvetta', 'AFTA111111'), ('yvonne', 'AFN1111111'),\
                ('zealandia', 'SLNTA11111'), ('zeby', 'SPA1111111'),\
                ('zela', 'SLA1111111'), ('zella', 'SLA1111111'),\
                ('zelma', 'SMA1111111'), ('zetta', 'STA1111111'),\
                ('zillah', 'SLA1111111'), ('zita', 'STA1111111'),\
                ('zoe', 'SA11111111'), ('zohra', 'SRA1111111'),\
                ('zola', 'SLA1111111'), ('zona', 'SNA1111111'),\
                ('aaskow', 'ASKA111111'), ('aaysford', 'ASFT111111'),\
                ('abbott', 'APT1111111'), ('abel', 'APA1111111'),\
                ('abelsted', 'APSTT11111'), ('abercrombie', 'APKRMPA111'),\
                ('abernathy', 'APNTA11111'), ('abernethie', 'APNTA11111'),\
                ('abernethy', 'APNTA11111'), ('abley', 'APLA111111'),\
                ('abraham', 'APRM111111'), ('abrams', 'APRMS11111'),\
                ('aburn', 'APN1111111'), ('acheson', 'AKSN111111'),\
                ('adair', 'ATA1111111'), ('adam', 'ATM1111111'),\
                ('adams', 'ATMS111111'), ('adamson', 'ATMSN11111'),\
                ('adcock', 'ATKK111111'), ('addison', 'ATSN111111'),\
                ('aderman', 'ATMN111111'), ('adess', 'ATS1111111'),\
                ('adie', 'ATA1111111'), ('adkins', 'ATKNS11111'),\
                ('affleck', 'AFLK111111'), ('agent', 'AKNT111111'),\
                ('agnew', 'AKNA111111'), ('ahern', 'AN11111111'),\
                ('ahlbrandt', 'APRNT11111'), ('ahlfeld', 'AFT1111111'),\
                ('aicheson', 'AKSN111111'), ('aidridge', 'ATRK111111'),\
                ('aiken', 'AKN1111111'), ('ailen', 'ALN1111111'),\
                ('aimers', 'AMS1111111'), ('aimes', 'AMS1111111'),\
                ('ainge', 'ANK1111111'), ('ainger', 'ANKA111111'),\
                ('air', 'AA11111111'), ('airey', 'ARA1111111'),\
                ('airley', 'ALA1111111'), ('aitcheson', 'AKSN111111'),\
                ('aitchison', 'AKSN111111'), ('aithenhead', 'ATNT111111'),\
                ('aitken', 'ATKN111111'), ('aitkenhead', 'ATKNT11111'),\
                ('aitkens', 'ATKNS11111'), ('aitkinson', 'ATKNSN1111'),\
                ('alberti', 'APTA111111'), ('alcock', 'AKK1111111'),\
                ('alden', 'ATN1111111'), ('alder', 'ATA1111111'),\
                ('alderdice', 'ATTK111111'), ('alderson', 'ATSN111111'),\
                ('alderton', 'ATTN111111'), ('aldous', 'ATS1111111'),\
                ('aldred', 'ATRT111111'), ('aldridge', 'ATRK111111'),\
                ('alen', 'ALN1111111'), ('alert', 'ALT1111111'),\
                ('alexander', 'ALKNTA1111'), ('alfrey', 'AFRA111111'),\
                ('algar', 'AKA1111111'), ('algeo', 'AKA1111111'),\
                ('algie', 'AKA1111111'), ('alison', 'ALSN111111'),\
                ('allan', 'ALN1111111'), ('alldred', 'ATRT111111'),\
                ('allen', 'ALN1111111'), ('alley', 'ALA1111111'),\
                ('allis', 'ALS1111111'), ('allison', 'ALSN111111'),\
                ('allman', 'AMN1111111'), ('allom', 'ALM1111111'),\
                ('alloo', 'ALA1111111'), ('allott', 'ALT1111111'),\
                ('allpress', 'APRS111111'), ('allum', 'ALM1111111'),\
                ('allwood', 'AWT1111111'), ('allworden', 'AWTN111111'),\
                ('almers', 'AMS1111111'), ('almond', 'AMNT111111'),\
                ('almquist', 'AMKST11111'), ('alpine', 'APN1111111'),\
                ('alston', 'ASTN111111'), ('amalfitano', 'AMFTNA1111'),\
                ('amalric', 'AMRK111111'), ('ambridge', 'AMPRK11111'),\
                ('amer', 'AMA1111111'), ('amos', 'AMS1111111'),\
                ('amouri', 'AMRA111111'), ('amtman', 'AMTMN11111'),\
                ('amunie', 'AMNA111111'), ('ancell', 'ANSA111111'),\
                ('anchor', 'ANKA111111'), ('andersen', 'ANTSN11111'),\
                ('andersoll', 'ANTSA11111'), ('anderson', 'ANTSN11111'),\
                ('anderton', 'ANTTN11111'), ('andorson', 'ANTSN11111'),\
                ('andreassend', 'ANTRSNT111'), ('andrew', 'ANTRA11111'),\
                ('andrewe', 'ANTRA11111'), ('andrewes', 'ANTRWS1111'),\
                ('andrews', 'ANTRS11111'), ('angeli', 'ANKLA11111'),\
                ('angell', 'ANKA111111'), ('angus', 'ANKS111111'),\
                ('annan', 'ANN1111111'), ('annand', 'ANNT111111'),\
                ('annett', 'ANT1111111'), ('anning', 'ANNK111111'),\
                ('annison', 'ANSN111111'), ('annson', 'ANSN111111'),\
                ('anscombe', 'ANSKM11111'), ('ansdell', 'ANSTA11111'),\
                ('ansell', 'ANSA111111'), ('anstruther', 'ANSTRTA111'),\
                ('anthony', 'ANTNA11111'), ('apes', 'APS1111111'),\
                ('appleby', 'APLPA11111'), ('applegart', 'APLKT11111'),\
                ('applegarth', 'APLKT11111'), ('applegate', 'APLKT11111'),\
                ('applelby', 'APLPA11111'), ('apstein', 'APSTN11111'),\
                ('arbuckle', 'APKA111111'), ('archbold', 'AKPT111111'),\
                ('archer', 'AKA1111111'), ('archibald', 'AKPT111111'),\
                ('archie', 'AKA1111111'), ('argue', 'AKA1111111'),\
                ('arkel', 'AKA1111111'), ('arkins', 'AKNS111111'),\
                ('arkle', 'AKA1111111'), ('arlidge', 'ALK1111111'),\
                ('armatrong', 'AMTRNK1111'), ('armishaw', 'AMSA111111'),\
                ('armit', 'AMT1111111'), ('armitage', 'AMTK111111'),\
                ('armour', 'AMA1111111'), ('armroyd', 'AMRT111111'),\
                ('armstead', 'AMSTT11111'), ('armstrong', 'AMSTRNK111'),\
                ('arnal', 'ANA1111111'), ('arneil', 'ANA1111111'),\
                ('arnel', 'ANA1111111'), ('arnett', 'ANT1111111'),\
                ('arnold', 'ANT1111111'), ('arnot', 'ANT1111111'),\
                ('arnott', 'ANT1111111'), ('arnstrong', 'ANSTRNK111'),\
                ('arroll', 'ARA1111111'), ('arrow', 'ARA1111111'),\
                ('arthur', 'ATA1111111'), ('artlett', 'ATLT111111'),\
                ('arundale', 'ARNTA11111'), ('arundel', 'ARNTA11111'),\
                ('ash', 'AS11111111'), ('ashbey', 'ASPA111111'),\
                ('ashbury', 'ASPRA11111'), ('ashby', 'ASPA111111'),\
                ('ashcroft', 'ASKRFT1111'), ('ashenden', 'ASNTN11111'),\
                ('asher', 'ASA1111111'), ('ashford', 'ASFT111111'),\
                ('ashley', 'ASLA111111'), ('ashman', 'ASMN111111'),\
                ('ashmore', 'ASMA111111'), ('ashron', 'ASRN111111'),\
                ('ashton', 'ASTN111111'), ('ashwell', 'ASWA111111'),\
                ('ashworth', 'ASWT111111'), ('askor', 'ASKA111111'),\
                ('aslin', 'ASLN111111'), ('asquith', 'ASKT111111'),\
                ('aston', 'ASTN111111'), ('astor', 'ASTA111111'),\
                ('atchison', 'AKSN111111'), ('atherfold', 'ATFT111111'),\
                ('athfield', 'ATFT111111'), ('athldeld', 'ATTT111111'),\
                ('atkin', 'ATKN111111'), ('atkins', 'ATKNS11111'),\
                ('atkinson', 'ATKNSN1111'), ('atmore', 'ATMA111111'),\
                ('atto', 'ATA1111111'), ('attwell', 'ATWA111111'),\
                ('atwill', 'ATWA111111'), ('audeison', 'ATSN111111'),\
                ('augus', 'AKS1111111'), ('auld', 'AT11111111'),\
                ('austad', 'ASTT111111'), ('austen', 'ASTN111111'),\
                ('austin', 'ASTN111111'), ('austing', 'ASTNK11111'),\
                ('auty', 'ATA1111111'), ('averill', 'AFRA111111'),\
                ('avery', 'AFRA111111'), ('awdry', 'ATRA111111'),\
                ('ayers', 'AS11111111'), ('aylwin', 'AWN1111111'),\
                ('ayres', 'ARS1111111'), ('ayrey', 'ARA1111111'),\
                ('ayshford', 'ASFT111111'), ('ayson', 'ASN1111111'),\
                ('ayto', 'ATA1111111'), ('azzariti', 'ASRTA11111'),\
                ('baber', 'PPA1111111'), ('bachop', 'PKP1111111'),\
                ('back', 'PK11111111'), ('backholm', 'PKM1111111'),\
                ('bacon', 'PKN1111111'), ('badcock', 'PTKK111111'),\
                ('badham', 'PTM1111111'), ('badman', 'PTMN111111'),\
                ('baeyertz', 'PTS1111111'), ('bagley', 'PKLA111111'),\
                ('bagnell', 'PKNA111111'), ('bagrie', 'PKRA111111'),\
                ('bail', 'PA11111111'), ('baildon', 'PTN1111111'),\
                ('bailer', 'PLA1111111'), ('bailes', 'PLS1111111'),\
                ('bailey', 'PLA1111111'), ('baillie', 'PLA1111111'),\
                ('bailoni', 'PLNA111111'), ('bain', 'PN11111111'),\
                ('baines', 'PNS1111111'), ('baird', 'PT11111111'),\
                ('baker', 'PKA1111111'), ('balchin', 'PKN1111111'),\
                ('balding', 'PTNK111111'), ('baldock', 'PTK1111111'),\
                ('baldwin', 'PTWN111111'), ('baley', 'PLA1111111'),\
                ('baliantyne', 'PLNTN11111'), ('ball', 'PA11111111'),\
                ('ballantyne', 'PLNTN11111'), ('ballard', 'PLT1111111'),\
                ('ballentyne', 'PLNTN11111'), ('ballintyne', 'PLNTN11111'),\
                ('balloch', 'PLK1111111'), ('balneaves', 'PNFS111111'),\
                ('bamber', 'PMPA111111'), ('bambery', 'PMPRA11111'),\
                ('bambury', 'PMPRA11111'), ('bamfield', 'PMFT111111'),\
                ('bamford', 'PMFT111111'), ('bamwell', 'PMWA111111'),\
                ('bandeen', 'PNTN111111'), ('banfield', 'PNFT111111'),\
                ('banks', 'PNKS111111'), ('bankshaw', 'PNKSA11111'),\
                ('banlow', 'PNLA111111'), ('bannantyne', 'PNNTN11111'),\
                ('bannatyne', 'PNTN111111'), ('bannerman', 'PNMN111111'),\
                ('banwell', 'PNWA111111'), ('baoumgren', 'PMKRN11111'),\
                ('barbara', 'PPRA111111'), ('barbeau', 'PPA1111111'),\
                ('barber', 'PPA1111111'), ('barbour', 'PPA1111111'),\
                ('barclay', 'PKLA111111'), ('bardsiey', 'PTSA111111'),\
                ('bardsley', 'PTSLA11111'), ('bardwell', 'PTWA111111'),\
                ('bare', 'PA11111111'), ('barfield', 'PFT1111111'),\
                ('barham', 'PM11111111'), ('barker', 'PKA1111111'),\
                ('barkla', 'PKLA111111'), ('barkman', 'PKMN111111'),\
                ('barling', 'PLNK111111'), ('barlow', 'PLA1111111'),\
                ('barlthrop', 'PTRP111111'), ('barltrop', 'PTRP111111'),\
                ('barnard', 'PNT1111111'), ('barnes', 'PNS1111111'),\
                ('barnett', 'PNT1111111'), ('barney', 'PNA1111111'),\
                ('barnfield', 'PNFT111111'), ('barnford', 'PNFT111111'),\
                ('barns', 'PNS1111111'), ('baron', 'PRN1111111'),\
                ('barr', 'PA11111111'), ('barrass', 'PRS1111111'),\
                ('barratt', 'PRT1111111'), ('barrell', 'PRA1111111'),\
                ('barret', 'PRT1111111'), ('barrett', 'PRT1111111'),\
                ('barrie', 'PRA1111111'), ('barrington', 'PRNKTN1111'),\
                ('barritt', 'PRT1111111'), ('barron', 'PRN1111111'),\
                ('barrow', 'PRA1111111'), ('barrowclou', 'PRKLA11111'),\
                ('barrowclough', 'PRKLA11111'), ('barrowman', 'PRMN111111'),\
                ('barry', 'PRA1111111'), ('barsdell', 'PSTA111111'),\
                ('barth', 'PT11111111'), ('bartholome', 'PTLM111111'),\
                ('bartholomew', 'PTLMA11111'), ('bartlett', 'PTLT111111'),\
                ('bartley', 'PTLA111111'), ('barton-bro', 'PTNPRA1111'),\
                ('barton-browne', 'PTNPRN1111'), ('barton', 'PTN1111111'),\
                ('bartram', 'PTRM111111'), ('barwell', 'PWA1111111'),\
                ('barwick', 'PWK1111111'), ('basan', 'PSN1111111'),\
                ('baskett', 'PSKT111111'), ('bassett', 'PST1111111'),\
                ('bastings', 'PSTNKS1111'), ('batcheior', 'PKA1111111'),\
                ('batchelor', 'PKLA111111'), ('bate', 'PT11111111'),\
                ('bateman', 'PTMN111111'), ('bates', 'PTS1111111'),\
                ('bath', 'PT11111111'), ('batham', 'PTM1111111'),\
                ('bathgate', 'PTKT111111'), ('bats', 'PTS1111111'),\
                ('batt', 'PT11111111'), ('battersby', 'PTSPA11111'),\
                ('batty', 'PTA1111111'), ('battye', 'PTA1111111'),\
                ('bauchop', 'PKP1111111'), ('baughen', 'PKN1111111'),\
                ('bauld', 'PT11111111'), ('baverstock', 'PFSTK11111'),\
                ('bawden', 'PTN1111111'), ('baxter', 'PKTA111111'),\
                ('baylee', 'PLA1111111'), ('bayley', 'PLA1111111'),\
                ('baylis', 'PLS1111111'), ('bayliss', 'PLS1111111'),\
                ('bayly', 'PLA1111111'), ('bayne', 'PN11111111'),\
                ('bazley', 'PSLA111111'), ('beach', 'PK11111111'),\
                ('beadle', 'PTA1111111'), ('beagle', 'PKA1111111'),\
                ('beal', 'PA11111111'), ('beale', 'PA11111111'),\
                ('bean', 'PN11111111'), ('bear', 'PA11111111'),\
                ('beardsley', 'PTSLA11111'), ('beardsmore', 'PTSMA11111'),\
                ('beasley', 'PSLA111111'), ('beath', 'PT11111111'),\
                ('beaton', 'PTN1111111'), ('beatson', 'PTSN111111'),\
                ('beattie', 'PTA1111111'), ('beatty', 'PTA1111111'),\
                ('beauchamp', 'PKMP111111'), ('beaufort', 'PFT1111111'),\
                ('beaumont', 'PMNT111111'), ('beautort', 'PTT1111111'),\
                ('beavars', 'PFS1111111'), ('beaven', 'PFN1111111'),\
                ('beaver', 'PFA1111111'), ('beavers', 'PFS1111111'),\
                ('beazley', 'PSLA111111'), ('beck', 'PK11111111'),\
                ('beckersta', 'PKSTA11111'), ('beckerstoff', 'PKSTF11111'),\
                ('beckett', 'PKT1111111'), ('beckingham', 'PKNM111111'),\
                ('beckingsale', 'PKNKSA1111'), ('bedford', 'PTFT111111'),\
                ('bee', 'PA11111111'), ('beeby', 'PPA1111111'),\
                ('beecher', 'PKA1111111'), ('beecot', 'PKT1111111'),\
                ('beecroft', 'PKRFT11111'), ('beedie', 'PTA1111111'),\
                ('beekman', 'PKMN111111'), ('beel', 'PA11111111'),\
                ('been', 'PN11111111'), ('beer', 'PA11111111'),\
                ('beeson', 'PSN1111111'), ('begbie', 'PKPA111111'),\
                ('begg', 'PK11111111'), ('beigbson', 'PKPSN11111'),\
                ('beighton', 'PTN1111111'), ('beil', 'PA11111111'),\
                ('beilby', 'PPA1111111'), ('beirne', 'PN11111111'),\
                ('beissel', 'PSA1111111'), ('belcher', 'PKA1111111'),\
                ('belford', 'PFT1111111'), ('bell', 'PA11111111'),\
                ('bellamy', 'PLMA111111'), ('bellaney', 'PLNA111111'),\
                ('bellet', 'PLT1111111'), ('bellett', 'PLT1111111'),\
                ('bellve', 'PF11111111'), ('belotti', 'PLTA111111'),\
                ('belsey', 'PSA1111111'), ('belstead', 'PSTT111111'),\
                ('belve', 'PF11111111'), ('belworthy', 'PWTA111111'),\
                ('bendall', 'PNTA111111'), ('benfell', 'PNFA111111'),\
                ('benfield', 'PNFT111111'), ('benham', 'PNM1111111'),\
                ('benjamin', 'PNMN111111'), ('benn', 'PN11111111'),\
                ('bennell', 'PNA1111111'), ('bennet', 'PNT1111111'),\
                ('bennett', 'PNT1111111'), ('bennetto', 'PNTA111111'),\
                ('bennetts', 'PNTS111111'), ('bennie', 'PNA1111111'),\
                ('bennison', 'PNSN111111'), ('benson', 'PNSN111111'),\
                ('benston', 'PNSTN11111'), ('benth', 'PNT1111111'),\
                ('bentley', 'PNTLA11111'), ('benton', 'PNTN111111'),\
                ('benzie', 'PNSA111111'), ('ber', 'PA11111111'),\
                ('berg', 'PK11111111'), ('bergin', 'PKN1111111'),\
                ('berkeley', 'PKLA111111'), ('berkinshaw', 'PKNSA11111'),\
                ('berland', 'PLNT111111'), ('berman', 'PMN1111111'),\
                ('bern', 'PN11111111'), ('bernard', 'PNT1111111'),\
                ('bernet', 'PNT1111111'), ('berney', 'PNA1111111'),\
                ('bernie', 'PNA1111111'), ('bernstein', 'PNSTN11111'),\
                ('berrett', 'PRT1111111'), ('berry', 'PRA1111111'),\
                ('berryman', 'PRMN111111'), ('berryrnan', 'PRNN111111'),\
                ('bertenshaw', 'PTNSA11111'), ('berti', 'PTA1111111'),\
                ('berwick', 'PWK1111111'), ('besley', 'PSLA111111'),\
                ('best', 'PST1111111'), ('bestic', 'PSTK111111'),\
                ('bethune', 'PTN1111111'), ('bettle', 'PTA1111111'),\
                ('bettridge', 'PTRK111111'), ('betts', 'PTS1111111'),\
                ('betty', 'PTA1111111'), ('beuth', 'PT11111111'),\
                ('bevan', 'PFN1111111'), ('bevars', 'PFS1111111'),\
                ('beven', 'PFN1111111'), ('beveridge', 'PFRK111111'),\
                ('bevin', 'PFN1111111'), ('bevis', 'PFS1111111'),\
                ('bewley', 'PLA1111111'), ('bews', 'PS11111111'),\
                ('bewsher', 'PSA1111111'), ('beyer', 'PA11111111'),\
                ('bezar', 'PSA1111111'), ('bezett', 'PST1111111'),\
                ('bggs', 'PKS1111111'), ('biack', 'PK11111111'),\
                ('bichan', 'PKN1111111'), ('bichard', 'PKT1111111'),\
                ('bickerdike', 'PKTK111111'), ('bicknell', 'PKNA111111'),\
                ('bidgood', 'PKT1111111'), ('bierstorf', 'PSTF111111'),\
                ('biggar', 'PKA1111111'), ('biggins', 'PKNS111111'),\
                ('biggs', 'PKS1111111'), ('billingham', 'PLNM111111'),\
                ('billington', 'PLNKTN1111'), ('bills', 'PS11111111'),\
                ('bilson', 'PSN1111111'), ('bingham', 'PNM1111111'),\
                ('binney', 'PNA1111111'), ('binnie', 'PNA1111111'),\
                ('binsted', 'PNSTT11111'), ('bioss', 'PS11111111'),\
                ('birch', 'PK11111111'), ('birchall', 'PKA1111111'),\
                ('birchwood', 'PKWT111111'), ('bird', 'PT11111111'),\
                ('birkenshaw', 'PKNSA11111'), ('birkett', 'PKT1111111'),\
                ('birkner', 'PKNA111111'), ('birnie', 'PNA1111111'),\
                ('birrell', 'PRA1111111'), ('birse', 'PS11111111'),\
                ('birss', 'PS11111111'), ('birt', 'PT11111111'),\
                ('birtles', 'PTLS111111'), ('bishop', 'PSP1111111'),\
                ('bisset', 'PST1111111'), ('bissett', 'PST1111111'),\
                ('bissland', 'PSLNT11111'), ('black', 'PLK1111111'),\
                ('blackbrn', 'PLKPN11111'), ('blackburn', 'PLKPN11111'),\
                ('blacke', 'PLK1111111'), ('blackford', 'PLKFT11111'),\
                ('blackie', 'PLKA111111'), ('blackledge', 'PLKLK11111'),\
                ('blackley', 'PLKLA11111'), ('blacklock', 'PLKLK11111'),\
                ('blacklow', 'PLKLA11111'), ('blackmore', 'PLKMA11111'),\
                ('blackock', 'PLKK111111'), ('blackwell', 'PLKWA11111'),\
                ('blackwood', 'PLKWT11111'), ('blagdon', 'PLKTN11111'),\
                ('blaikie', 'PLKA111111'), ('blair', 'PLA1111111'),\
                ('blake', 'PLK1111111'), ('blakeley', 'PLKLA11111'),\
                ('blakely', 'PLKLA11111'), ('blanc', 'PLNK111111'),\
                ('blanch', 'PLNK111111'), ('blanchard', 'PLNKT11111'),\
                ('blanchfield', 'PLNKFT1111'), ('bland', 'PLNT111111'),\
                ('blandford', 'PLNTFT1111'), ('blaney', 'PLNA111111'),\
                ('blayden', 'PLTN111111'), ('bleach', 'PLK1111111'),\
                ('blease', 'PLS1111111'), ('blee', 'PLA1111111'),\
                ('blell', 'PLA1111111'), ('blick', 'PLK1111111'),\
                ('blincoe', 'PLNKA11111'), ('blines', 'PLNS111111'),\
                ('blomfield', 'PLMFT11111'), ('bloomfield', 'PLMFT11111'),\
                ('bloss', 'PLS1111111'), ('blott', 'PLT1111111'),\
                ('bloxham', 'PLKM111111'), ('bloy', 'PLA1111111'),\
                ('blue', 'PLA1111111'), ('bluett', 'PLT1111111'),\
                ('blunt', 'PLNT111111'), ('blyth', 'PLT1111111'),\
                ('blythe', 'PLT1111111'), ('bnker', 'PNKA111111'),\
                ('boag', 'PK11111111'), ('boardman', 'PTMN111111'),\
                ('boatwood', 'PTWT111111'), ('boaz', 'PS11111111'),\
                ('bobbett', 'PPT1111111'), ('boberg', 'PPK1111111'),\
                ('bobsien', 'PPSN111111'), ('boddy', 'PTA1111111'),\
                ('boddye', 'PTA1111111'), ('bode', 'PT11111111'),\
                ('bodkin', 'PTKN111111'), ('boecking', 'PKNK111111'),\
                ('boelke', 'PK11111111'), ('bogue', 'PKA1111111'),\
                ('bohm', 'PM11111111'), ('bohrsman', 'PSMN111111'),\
                ('boland', 'PLNT111111'), ('bollard', 'PLT1111111'),\
                ('bollett', 'PLT1111111'), ('bolsand', 'PSNT111111'),\
                ('bolstad', 'PSTT111111'), ('bolt', 'PT11111111'),\
                ('bolting', 'PTNK111111'), ('bolton', 'PTN1111111'),\
                ('bolwell', 'PWA1111111'), ('bolwill', 'PWA1111111'),\
                ('bonar', 'PNA1111111'), ('bonasich', 'PNSK111111'),\
                ('bond', 'PNT1111111'), ('bone', 'PN11111111'),\
                ('boner', 'PNA1111111'), ('bonetti', 'PNTA111111'),\
                ('bongard', 'PNKT111111'), ('bonham', 'PNM1111111'),\
                ('boniface', 'PNFK111111'), ('bonifant', 'PNFNT11111'),\
                ('bonney', 'PNA1111111'), ('bonnie', 'PNA1111111'),\
                ('bonnin', 'PNN1111111'), ('booker', 'PKA1111111'),\
                ('bool', 'PA11111111'), ('booley', 'PLA1111111'),\
                ('boot', 'PT11111111'), ('booten', 'PTN1111111'),\
                ('booth', 'PT11111111'), ('boothroyd', 'PTRT111111'),\
                ('bootten', 'PTN1111111'), ('boraman', 'PRMN111111'),\
                ('boreham', 'PRM1111111'), ('borjeson', 'PRSN111111'),\
                ('borland', 'PLNT111111'), ('borley', 'PLA1111111'),\
                ('borne', 'PN11111111'), ('borrie', 'PRA1111111'),\
                ('borthwick', 'PTWK111111'), ('borton', 'PTN1111111'),\
                ('borwick', 'PWK1111111'), ('boswell', 'PSWA111111'),\
                ('bosworth', 'PSWT111111'), ('bott', 'PT11111111'),\
                ('botting', 'PTNK111111'), ('boucher', 'PKA1111111'),\
                ('bouchor', 'PKA1111111'), ('boud', 'PT11111111'),\
                ('boulnois', 'PNS1111111'), ('boult', 'PT11111111'),\
                ('boulter', 'PTA1111111'), ('boulton', 'PTN1111111'),\
                ('bouquet', 'PKT1111111'), ('bourke', 'PK11111111'),\
                ('bourne', 'PN11111111'), ('boutcher', 'PKA1111111'),\
                ('bouterey', 'PTRA111111'), ('bowdell', 'PTA1111111'),\
                ('bowden', 'PTN1111111'), ('bowdler', 'PTLA111111'),\
                ('bowen', 'PWN1111111'), ('bower', 'PWA1111111'),\
                ('bowers', 'PWS1111111'), ('bowie', 'PWA1111111'),\
                ('bowker', 'PKA1111111'), ('bowkett', 'PKT1111111'),\
                ('bowler', 'PLA1111111'), ('bowles', 'PLS1111111'),\
                ('bowling', 'PLNK111111'), ('bowls', 'PS11111111'),\
                ('bowman', 'PMN1111111'), ('bowmar', 'PMA1111111'),\
                ('bowser', 'PSA1111111'), ('boxall', 'PKA1111111'),\
                ('boyall', 'PA11111111'), ('boyd', 'PT11111111'),\
                ('boyer', 'PA11111111'), ('boyes', 'PS11111111'),\
                ('boyison', 'PSN1111111'), ('boyland', 'PLNT111111'),\
                ('boyle', 'PA11111111'), ('boylen', 'PLN1111111'),\
                ('boyles', 'PLS1111111'), ('boys', 'PS11111111'),\
                ('brabant', 'PRPNT11111'), ('brabyn', 'PRPN111111'),\
                ('bracegirdle', 'PRSKTA1111'), ('brackenridge', 'PRKNRK1111'),\
                ('brackley', 'PRKLA11111'), ('bracks', 'PRKS111111'),\
                ('braden', 'PRTN111111'), ('bradford', 'PRTFT11111'),\
                ('brading', 'PRTNK11111'), ('bradley', 'PRTLA11111'),\
                ('bradshaw', 'PRTSA11111'), ('brady', 'PRTA111111'),\
                ('bragg', 'PRK1111111'), ('braham', 'PRM1111111'),\
                ('braid', 'PRT1111111'), ('braidwood', 'PRTWT11111'),\
                ('brail', 'PRA1111111'), ('braimbridge', 'PRMPRK1111'),\
                ('brain', 'PRN1111111'), ('braithiwaite', 'PRTWT11111'),\
                ('braithwaite', 'PRTWT11111'), ('bramley', 'PRMLA11111'),\
                ('bramwell', 'PRMWA11111'), ('brand', 'PRNT111111'),\
                ('brander', 'PRNTA11111'), ('brandon', 'PRNTN11111'),\
                ('brands', 'PRNTS11111'), ('brandt', 'PRNT111111'),\
                ('bransgrove', 'PRNSKRF111'), ('branson', 'PRNSN11111'),\
                ('brass', 'PRS1111111'), ('bratby', 'PRTPA11111'),\
                ('brathwaite', 'PRTWT11111'), ('bray', 'PRA1111111'),\
                ('breach', 'PRK1111111'), ('brebner', 'PRPNA11111'),\
                ('bree', 'PRA1111111'), ('breen', 'PRN1111111'),\
                ('breese', 'PRS1111111'), ('breeze', 'PRS1111111'),\
                ('bregmen', 'PRKMN11111'), ('brehaut', 'PRT1111111'),\
                ('bremford', 'PRMFT11111'), ('bremmer', 'PRMA111111'),\
                ('bremner', 'PRMNA11111'), ('brennan', 'PRNN111111'),\
                ('brenssell', 'PRNSA11111'), ('brent', 'PRNT111111'),\
                ('bresanello', 'PRSNLA1111'), ('bresnahan', 'PRSNN11111'),\
                ('bretherton', 'PRTTN11111'), ('brett', 'PRT1111111'),\
                ('brettell', 'PRTA111111'), ('brew', 'PRA1111111'),\
                ('brewer', 'PRWA111111'), ('brewster', 'PRSTA11111'),\
                ('brian', 'PRN1111111'), ('briant', 'PRNT111111'),\
                ('briasco', 'PRSKA11111'), ('brice', 'PRK1111111'),\
                ('brickell', 'PRKA111111'), ('brickland', 'PRKLNT1111'),\
                ('briden', 'PRTN111111'), ('bridge', 'PRK1111111'),\
                ('bridgeman', 'PRKMN11111'), ('bridger', 'PRKA111111'),\
                ('bridges', 'PRKS111111'), ('bridget', 'PRKT111111'),\
                ('bridgman', 'PRKMN11111'), ('brien', 'PRN1111111'),\
                ('brierley', 'PRLA111111'), ('briggs', 'PRKS111111'),\
                ('bright', 'PRT1111111'), ('brighting', 'PRTNK11111'),\
                ('brightling', 'PRTLNK1111'), ('brightmore', 'PRTMA11111'),\
                ('brightwell', 'PRTWA11111'), ('briley', 'PRLA111111'),\
                ('brill', 'PRA1111111'), ('bringans', 'PRNKNS1111'),\
                ('bringarts', 'PRNKTS1111'), ('brinkworth', 'PRNKWT1111'),\
                ('brinn', 'PRN1111111'), ('brinsdon', 'PRNSTN1111'),\
                ('brinsley', 'PRNSLA1111'), ('brisbane', 'PRSPN11111'),\
                ('briscoe', 'PRSKA11111'), ('brisley', 'PRSLA11111'),\
                ('briston', 'PRSTN11111'), ('bristow', 'PRSTA11111'),\
                ('briton', 'PRTN111111'), ('britten', 'PRTN111111'),\
                ('brittenden', 'PRTNTN1111'), ('britton', 'PRTN111111'),\
                ('brixton', 'PRKTN11111'), ('broad', 'PRT1111111'),\
                ('broadbent', 'PRTPNT1111'), ('broadfoot', 'PRTFT11111'),\
                ('broadhead', 'PRTT111111'), ('broadley', 'PRTLA11111'),\
                ('brock', 'PRK1111111'), ('brocket', 'PRKT111111'),\
                ('brockie', 'PRKA111111'), ('brocklebank', 'PRKLPNK111'),\
                ('brocklehurst', 'PRKLST1111'), ('broderick', 'PRTRK11111'),\
                ('brodie', 'PRTA111111'), ('brodrick', 'PRTRK11111'),\
                ('broenaham', 'PRNM111111'), ('bromley', 'PRMLA11111'),\
                ('brook', 'PRK1111111'), ('brooke', 'PRK1111111'),\
                ('brooker', 'PRKA111111'), ('brookes', 'PRKS111111'),\
                ('brooket', 'PRKT111111'), ('brooklehurst', 'PRKLST1111'),\
                ('brooks', 'PRKS111111'), ('brool', 'PRA1111111'),\
                ('broolcs', 'PRKS111111'), ('broom', 'PRM1111111'),\
                ('broome', 'PRM1111111'), ('broomfield', 'PRMFT11111'),\
                ('broomhall', 'PRMA111111'), ('brosnahan', 'PRSNN11111'),\
                ('brosnan', 'PRSNN11111'), ('brotherhoo', 'PRTA111111'),\
                ('brotherhood', 'PRTT111111'), ('brotherston', 'PRTSTN1111'),\
                ('brotherton', 'PRTTN11111'), ('brough', 'PRA1111111'),\
                ('broughton', 'PRTN111111'), ('browett', 'PRWT111111'),\
                ('brown-durie', 'PRNTRA1111'), ('brown-rennie', 'PRNRNA1111'),\
                ('brown', 'PRN1111111'), ('browne', 'PRN1111111'),\
                ('brownell', 'PRNA111111'), ('brownie', 'PRNA111111'),\
                ('browning', 'PRNNK11111'), ('brownlie', 'PRNLA11111'),\
                ('bruce', 'PRK1111111'), ('bruco', 'PRKA111111'),\
                ('brugh', 'PRA1111111'), ('bruhns', 'PRNS111111'),\
                ('brundell', 'PRNTA11111'), ('bruno', 'PRNA111111'),\
                ('brunton', 'PRNTN11111'), ('bruten', 'PRTN111111'),\
                ('bruton', 'PRTN111111'), ('bryan', 'PRN1111111'),\
                ('bryant', 'PRNT111111'), ('bryce', 'PRK1111111'),\
                ('bryden', 'PRTN111111'), ('brydone', 'PRTN111111'),\
                ('bryson', 'PRSN111111'), ('btrns', 'PTNS111111'),\
                ('buchan', 'PKN1111111'), ('buchanan', 'PKNN111111'),\
                ('buck', 'PK11111111'), ('buckingham', 'PKNM111111'),\
                ('buckland', 'PKLNT11111'), ('buckley', 'PKLA111111'),\
                ('buddicom', 'PTKM111111'), ('buddicomb', 'PTKM111111'),\
                ('buddicombe', 'PTKM111111'), ('buddle', 'PTA1111111'),\
                ('budge', 'PK11111111'), ('bugby', 'PKPA111111'),\
                ('bugden', 'PKTN111111'), ('buist', 'PST1111111'),\
                ('bulfin', 'PFN1111111'), ('bulger', 'PKA1111111'),\
                ('bull', 'PA11111111'), ('bullars', 'PLS1111111'),\
                ('bullen', 'PLN1111111'), ('bullett', 'PLT1111111'),\
                ('bullock', 'PLK1111111'), ('bullot', 'PLT1111111'),\
                ('bullough', 'PLA1111111'), ('bulmer', 'PMA1111111'),\
                ('bum', 'PM11111111'), ('bums', 'PMS1111111'),\
                ('bunce', 'PNK1111111'), ('bundo', 'PNTA111111'),\
                ('bungard', 'PNKT111111'), ('bungardt', 'PNKT111111'),\
                ('bunting', 'PNTNK11111'), ('burbery', 'PPRA111111'),\
                ('burbury', 'PPRA111111'), ('burcoll', 'PKA1111111'),\
                ('burdekin', 'PTKN111111'), ('burden', 'PTN1111111'),\
                ('burdett', 'PTT1111111'), ('burdon', 'PTN1111111'),\
                ('burford', 'PFT1111111'), ('burger', 'PKA1111111'),\
                ('burgess', 'PKS1111111'), ('burk', 'PK11111111'),\
                ('burke', 'PK11111111'), ('burkinshaw', 'PKNSA11111'),\
                ('burley', 'PLA1111111'), ('burlinson', 'PLNSN11111'),\
                ('burn', 'PN11111111'), ('burnard', 'PNT1111111'),\
                ('burnes', 'PNS1111111'), ('burnett', 'PNT1111111'),\
                ('burns', 'PNS1111111'), ('burnside', 'PNST111111'),\
                ('burrell', 'PRA1111111'), ('burridge', 'PRK1111111'),\
                ('burrow', 'PRA1111111'), ('burrowes', 'PRWS111111'),\
                ('burrows', 'PRS1111111'), ('burson', 'PSN1111111'),\
                ('burt', 'PT11111111'), ('burton', 'PTN1111111'),\
                ('busbridge', 'PSPRK11111'), ('busby', 'PSPA111111'),\
                ('bush', 'PS11111111'), ('bushell', 'PSA1111111'),\
                ('buss', 'PS11111111'), ('busst', 'PST1111111'),\
                ('bustin', 'PSTN111111'), ('butchart', 'PKT1111111'),\
                ('butcher', 'PKA1111111'), ('butel', 'PTA1111111'),\
                ('butler', 'PTLA111111'), ('butlin', 'PTLN111111'),\
                ('butt', 'PT11111111'), ('butterfield', 'PTFT111111'),\
                ('buttermore', 'PTMA111111'), ('butterworth', 'PTWT111111'),\
                ('buttimore', 'PTMA111111'), ('button', 'PTN1111111'),\
                ('butts', 'PTS1111111'), ('buxton', 'PKTN111111'),\
                ('buzzard', 'PST1111111'), ('bvrne', 'PFN1111111'),\
                ('byfield', 'PFT1111111'), ('byford', 'PFT1111111'),\
                ('byrne', 'PN11111111'), ('byrnes', 'PNS1111111'),\
                ('byrno', 'PNA1111111'), ('cabena', 'KPNA111111'),\
                ('cabral', 'KPRA111111'), ('caddie', 'KTA1111111'),\
                ('cadigan', 'KTKN111111'), ('cadogan', 'KTKN111111'),\
                ('caerwood', 'KWT1111111'), ('caffin', 'KFN1111111'),\
                ('cagney', 'KKNA111111'), ('cahill', 'KA11111111'),\
                ('caidwell', 'KTWA111111'), ('caigou', 'KKA1111111'),\
                ('cain', 'KN11111111'), ('caird', 'KT11111111'),\
                ('cairney', 'KNA1111111'), ('cairns', 'KNS1111111'),\
                ('caithness', 'KTNS111111'), ('calcott', 'KKT1111111'),\
                ('calcutt', 'KKT1111111'), ('calder', 'KTA1111111'),\
                ('calderwood', 'KTWT111111'), ('caldow', 'KTA1111111'),\
                ('caldweil', 'KTWA111111'), ('caldwell', 'KTWA111111'),\
                ('calex', 'KLK1111111'), ('caley', 'KLA1111111'),\
                ('callaghan', 'KLKN111111'), ('callam', 'KLM1111111'),\
                ('callan', 'KLN1111111'), ('callanan', 'KLNN111111'),\
                ('calland', 'KLNT111111'), ('callander', 'KLNTA11111'),\
                ('callaster', 'KLSTA11111'), ('callaway', 'KLWA111111'),\
                ('callender', 'KLNTA11111'), ('calley', 'KLA1111111'),\
                ('callighan', 'KLKN111111'), ('callinder', 'KLNTA11111'),\
                ('callis', 'KLS1111111'), ('callister', 'KLSTA11111'),\
                ('callon', 'KLN1111111'), ('calverley', 'KFLA111111'),\
                ('calvert', 'KFT1111111'), ('calvey', 'KFA1111111'),\
                ('cameron', 'KMRN111111'), ('cammock', 'KMK1111111'),\
                ('campbell', 'KMPA111111'), ('campion', 'KMPN111111'),\
                ('camplell', 'KMPLA11111'), ('can1eron', 'KNRN111111'),\
                ('canavan', 'KNFN111111'), ('canning', 'KNNK111111'),\
                ('cannon', 'KNN1111111'), ('cannons', 'KNNS111111'),\
                ('canpbell', 'KNPA111111'), ('canter', 'KNTA111111'),\
                ('cantrell', 'KNTRA11111'), ('cantwell', 'KNTWA11111'),\
                ('canty', 'KNTA111111'), ('capitaneas', 'KPTNS11111'),\
                ('caple', 'KPA1111111'), ('capstick', 'KPSTK11111'),\
                ('caraclus', 'KRKLS11111'), ('caradus', 'KRTS111111'),\
                ('caravan', 'KRFN111111'), ('carber', 'KPA1111111'),\
                ('carberry', 'KPRA111111'), ('cardale', 'KTA1111111'),\
                ('carden', 'KTN1111111'), ('carder', 'KTA1111111'),\
                ('cardno', 'KTNA111111'), ('care', 'KA11111111'),\
                ('carey', 'KRA1111111'), ('cargill', 'KKA1111111'),\
                ('carlene', 'KLN1111111'), ('carley', 'KLA1111111'),\
                ('carlin', 'KLN1111111'), ('carline', 'KLN1111111'),\
                ('carlson', 'KSN1111111'), ('carlyle', 'KLA1111111'),\
                ('carmalt', 'KMT1111111'), ('carman', 'KMN1111111'),\
                ('carmichael', 'KMKA111111'), ('carmody', 'KMTA111111'),\
                ('carnahan', 'KNN1111111'), ('carnegie', 'KNKA111111'),\
                ('carney', 'KNA1111111'), ('carnie', 'KNA1111111'),\
                ('carolin', 'KRLN111111'), ('carpenter', 'KPNTA11111'),\
                ('carr', 'KA11111111'), ('carrick', 'KRK1111111'),\
                ('carrigan', 'KRKN111111'), ('carrington', 'KRNKTN1111'),\
                ('carrodus', 'KRTS111111'), ('carroll', 'KRA1111111'),\
                ('carruther', 'KRTA111111'), ('carruthers', 'KRTS111111'),\
                ('carrutlers', 'KRTLS11111'), ('carside', 'KST1111111'),\
                ('carslaw', 'KSLA111111'), ('carson', 'KSN1111111'),\
                ('carswe11', 'KSA1111111'), ('carswell', 'KSWA111111'),\
                ('carter', 'KTA1111111'), ('carton', 'KTN1111111'),\
                ('cartwright', 'KTRT111111'), ('caruthers', 'KRTS111111'),\
                ('carvalho', 'KFA1111111'), ('carvell', 'KFA1111111'),\
                ('carver', 'KFA1111111'), ('carvosso', 'KFSA111111'),\
                ('case', 'KS11111111'), ('caselberg', 'KSPK111111'),\
                ('caser', 'KSA1111111'), ('casey', 'KSA1111111'),\
                ('cash', 'KS11111111'), ('cashman', 'KSMN111111'),\
                ('caskie', 'KSKA111111'), ('cass', 'KS11111111'),\
                ('cassells', 'KSS1111111'), ('cassels', 'KSS1111111'),\
                ('casserley', 'KSLA111111'), ('casserly', 'KSLA111111'),\
                ('cassidv', 'KSTF111111'), ('cassidy', 'KSTA111111'),\
                ('cassitly', 'KSTLA11111'), ('casson', 'KSN1111111'),\
                ('castelli', 'KSTLA11111'), ('caster', 'KSTA111111'),\
                ('castle', 'KSTA111111'), ('castlehow', 'KSTLA11111'),\
                ('catchpole', 'KKPA111111'), ('cate', 'KT11111111'),\
                ('cater', 'KTA1111111'), ('cathro', 'KTRA111111'),\
                ('catto', 'KTA1111111'), ('caughey', 'KKA1111111'),\
                ('caulcutt', 'KKT1111111'), ('caulton', 'KTN1111111'),\
                ('caunter', 'KNTA111111'), ('cavanagh', 'KFNA111111'),\
                ('cave', 'KF11111111'), ('cavell', 'KFA1111111'),\
                ('cawley', 'KLA1111111'), ('cawston', 'KSTN111111'),\
                ('cawthorn', 'KTN1111111'), ('cayford', 'KFT1111111'),\
                ('caygill', 'KKA1111111'), ('cayzer', 'KSA1111111'),\
                ('cessford', 'SSFT111111'), ('chadwick', 'KTWK111111'),\
                ('challis', 'KLS1111111'), ('chalmer', 'KMA1111111'),\
                ('chalmers', 'KMS1111111'), ('chamberlain', 'KMPLN11111'),\
                ('chambers', 'KMPS111111'), ('chammen', 'KMN1111111'),\
                ('champion', 'KMPN111111'), ('chanbers', 'KNPS111111'),\
                ('chander', 'KNTA111111'), ('chandler', 'KNTLA11111'),\
                ('chaney', 'KNA1111111'), ('chanldler', 'KNTLA11111'),\
                ('channon', 'KNN1111111'), ('chantrill', 'KNTRA11111'),\
                ('chaplain', 'KPLN111111'), ('chaplin', 'KPLN111111'),\
                ('chapman', 'KPMN111111'), ('chappell', 'KPA1111111'),\
                ('charker', 'KKA1111111'), ('charles', 'KLS1111111'),\
                ('charleston', 'KLSTN11111'), ('charlsworth', 'KSWT111111'),\
                ('charlton', 'KTN1111111'), ('charnley', 'KNLA111111'),\
                ('charters', 'KTS1111111'), ('chase', 'KS11111111'),\
                ('chaston', 'KSTN111111'), ('chatterton', 'KTTN111111'),\
                ('chave', 'KF11111111'), ('chayman', 'KMN1111111'),\
                ('cheeseman', 'KSMN111111'), ('cheesman', 'KSMN111111'),\
                ('chennells', 'KNS1111111'), ('cherrie', 'KRA1111111'),\
                ('cherrv', 'KF11111111'), ('cherry', 'KRA1111111'),\
                ('cheshire', 'KSA1111111'), ('chesney', 'KSNA111111'),\
                ('chesterman', 'KSTMN11111'), ('chetham', 'KTM1111111'),\
                ('chettiebur', 'KTPA111111'), ('chettleburgh', 'KTLPA11111'),\
                ('chetwil', 'KTWA111111'), ('chetwin', 'KTWN111111'),\
                ('cheyne', 'KN11111111'), ('chickley', 'KKLA111111'),\
                ('chilcott', 'KKT1111111'), ('child', 'KT11111111'),\
                ('childs', 'KTS1111111'), ('chiles', 'KLS1111111'),\
                ('chimside', 'KMST111111'), ('chin shin', 'KNSN111111'),\
                ('chin shing', 'KNSNK11111'), ('chin', 'KN11111111'),\
                ('ching', 'KNK1111111'), ('chirnside', 'KNST111111'),\
                ('chisholm', 'KSM1111111'), ('chiswell', 'KSWA111111'),\
                ('chits', 'KTS1111111'), ('chittock', 'KTK1111111'),\
                ('chitty', 'KTA1111111'), ('chivers', 'KFS1111111'),\
                ('cholmondeley', 'KMNTLA1111'), ('choo quee', 'KKA1111111'),\
                ('chooquee', 'KKA1111111'), ('choules', 'KLS1111111'),\
                ('chrisp', 'KRSP111111'), ('christens', 'KRSTNS1111'),\
                ('christensen', 'KRSTNSN111'), ('christenson', 'KRSTNSN111'),\
                ('christeson', 'KRSTSN1111'), ('christian', 'KRSN111111'),\
                ('christie', 'KRSTA11111'), ('christophe', 'KRSTF11111'),\
                ('christopher', 'KRSTFA1111'), ('chronican', 'KRNKN11111'),\
                ('chronichan', 'KRNKN11111'), ('chrystall', 'KRSTA11111'),\
                ('chudley', 'KTLA111111'), ('church', 'KK11111111'),\
                ('churchill', 'KKA1111111'), ('churley', 'KLA1111111'),\
                ('ciark', 'SK11111111'), ('ciarke', 'SK11111111'),\
                ('cieveland', 'SFLNT11111'), ('ciiff', 'SF11111111'),\
                ('ciose', 'SS11111111'), ('citfield', 'STFT111111'),\
                ('clack', 'KLK1111111'), ('clancy', 'KLNSA11111'),\
                ('clapman', 'KLPMN11111'), ('clapp', 'KLP1111111'),\
                ('clapperton', 'KLPTN11111'), ('clapshaw', 'KLPSA11111'),\
                ('clare', 'KLA1111111'), ('claridge', 'KLRK111111'),\
                ('clark', 'KLK1111111'), ('clarke', 'KLK1111111'),\
                ('clarkson', 'KLKSN11111'), ('clarson', 'KLSN111111'),\
                ('clatworthy', 'KLTWTA1111'), ('claughly', 'KLLA111111'),\
                ('clay', 'KLA1111111'), ('clayden', 'KLTN111111'),\
                ('clayforth', 'KLFT111111'), ('clayton', 'KLTN111111'),\
                ('clearwater', 'KLWTA11111'), ('cleary', 'KLRA111111'),\
                ('cleaver', 'KLFA111111'), ('cleavin', 'KLFN111111'),\
                ('cleeland', 'KLLNT11111'), ('clegg', 'KLK1111111'),\
                ('cleghorn', 'KLKN111111'), ('cleland', 'KLLNT11111'),\
                ('clelland', 'KLLNT11111'), ('clemenger', 'KLMNKA1111'),\
                ('clemens', 'KLMNS11111'), ('clement', 'KLMNT11111'),\
                ('clements', 'KLMNTS1111'), ('clementson', 'KLMNTSN111'),\
                ('clemmey', 'KLMA111111'), ('clent', 'KLNT111111'),\
                ('clery', 'KLRA111111'), ('cleveland', 'KLFLNT1111'),\
                ('clevelandt', 'KLFLNT1111'), ('cleverley', 'KLFLA11111'),\
                ('cliff', 'KLF1111111'), ('clifford', 'KLFT111111'),\
                ('clifton', 'KLFTN11111'), ('clinch', 'KLNK111111'),\
                ('clinkard', 'KLNKT11111'), ('clint', 'KLNT111111'),\
                ('clisby', 'KLSPA11111'), ('clitheroe', 'KLTRA11111'),\
                ('clode', 'KLT1111111'), ('cloharty', 'KLTA111111'),\
                ('close', 'KLS1111111'), ('clothier', 'KLTA111111'),\
                ('clough', 'KLA1111111'), ('cloughly', 'KLLA111111'),\
                ('clow', 'KLA1111111'), ('clugston', 'KLKSTN1111'),\
                ('clulee', 'KLLA111111'), ('clune', 'KLN1111111'),\
                ('clutterbuck', 'KLTPK11111'), ('clydesdale', 'KLTSTA1111'),\
                ('clyma', 'KLMA111111'), ('clymer', 'KLMA111111'),\
                ('coates', 'KTS1111111'), ('coats', 'KTS1111111'),\
                ('coatsworth', 'KTSWT11111'), ('cobb', 'KP11111111'),\
                ('coburn', 'KPN1111111'), ('cochrane', 'KKRN111111'),\
                ('cock', 'KK11111111'), ('cockburn', 'KKPN111111'),\
                ('cockerell', 'KKRA111111'), ('cockerill', 'KKRA111111'),\
                ('cocking', 'KKNK111111'), ('cockroft', 'KKRFT11111'),\
                ('cody', 'KTA1111111'), ('coffey', 'KFA1111111'),\
                ('cogan', 'KKN1111111'), ('cogger', 'KKA1111111'),\
                ('coghill', 'KKA1111111'), ('coghlan', 'KLN1111111'),\
                ('cohen', 'KN11111111'), ('coker', 'KKA1111111'),\
                ('colbert', 'KPT1111111'), ('cole', 'KA11111111'),\
                ('coleman', 'KLMN111111'), ('coley', 'KLA1111111'),\
                ('colgan', 'KKN1111111'), ('coller', 'KLA1111111'),\
                ('collet', 'KLT1111111'), ('collett', 'KLT1111111'),\
                ('collie', 'KLA1111111'), ('collier', 'KLA1111111'),\
                ('collin', 'KLN1111111'), ('colling', 'KLNK111111'),\
                ('collingwood', 'KLNKWT1111'), ('collins', 'KLNS111111'),\
                ('collinson', 'KLNSN11111'), ('collis', 'KLS1111111'),\
                ('colman', 'KMN1111111'), ('colombus', 'KLMPS11111'),\
                ('colquhoun', 'KKN1111111'), ('colrmack', 'KMK1111111'),\
                ('colson', 'KSN1111111'), ('colston', 'KSTN111111'),\
                ('colton', 'KTN1111111'), ('columb', 'KLM1111111'),\
                ('colville', 'KFA1111111'), ('colvin', 'KFN1111111'),\
                ('colyer', 'KLA1111111'), ('comber', 'KMPA111111'),\
                ('combie', 'KMPA111111'), ('combs', 'KMPS111111'),\
                ('comer', 'KMA1111111'), ('cometti', 'KMTA111111'),\
                ('comissiong', 'KMSNK11111'), ('common', 'KMN1111111'),\
                ('comrie', 'KMRA111111'), ('comyn', 'KMN1111111'),\
                ('concher', 'KNKA111111'), ('conder', 'KNTA111111'),\
                ('condliffe', 'KNTLF11111'), ('condon', 'KNTN111111'),\
                ('cone', 'KN11111111'), ('coneys', 'KNS1111111'),\
                ('congalton', 'KNKTN11111'), ('conheady', 'KNTA111111'),\
                ('conley', 'KNLA111111'), ('conn', 'KN11111111'),\
                ('connally', 'KNLA111111'), ('connel]y', 'KNLA111111'),\
                ('connell', 'KNA1111111'), ('connelly', 'KNLA111111'),\
                ('connely', 'KNLA111111'), ('conner', 'KNA1111111'),\
                ('conniff', 'KNF1111111'), ('connolly', 'KNLA111111'),\
                ('connor', 'KNA1111111'), ('connors', 'KNS1111111'),\
                ('conolly', 'KNLA111111'), ('conradi', 'KNRTA11111'),\
                ('conroy', 'KNRA111111'), ('consins', 'KNSNS11111'),\
                ('constable', 'KNSTPA1111'), ('conway', 'KNWA111111'),\
                ('cook', 'KK11111111'), ('cooke', 'KK11111111'),\
                ('coolay', 'KLA1111111'), ('coombes', 'KMPS111111'),\
                ('coombs', 'KMPS111111'), ('coomer', 'KMA1111111'),\
                ('cooney', 'KNA1111111'), ('coop', 'KP11111111'),\
                ('cooper', 'KPA1111111'), ('coorobs', 'KRPS111111'),\
                ('coory', 'KRA1111111'), ('cop]ey', 'KPA1111111'),\
                ('cope', 'KP11111111'), ('copland', 'KPLNT11111'),\
                ('copley', 'KPLA111111'), ('coppell', 'KPA1111111'),\
                ('coppin', 'KPN1111111'), ('corbett', 'KPT1111111'),\
                ('corcoran', 'KKRN111111'), ('corder', 'KTA1111111'),\
                ('cordue', 'KTA1111111'), ('coreoran', 'KRRN111111'),\
                ('corfield', 'KFT1111111'), ('corke', 'KK11111111'),\
                ('corkin', 'KKN1111111'), ('corkran', 'KKRN111111'),\
                ('corlett', 'KLT1111111'), ('corley', 'KLA1111111'),\
                ('corliss', 'KLS1111111'), ('cormack', 'KMK1111111'),\
                ('cornack', 'KNK1111111'), ('cornaga', 'KNKA111111'),\
                ('cornelius', 'KNLS111111'), ('cornell', 'KNA1111111'),\
                ('corner', 'KNA1111111'), ('cornish', 'KNS1111111'),\
                ('cornwall', 'KNWA111111'), ('cornwell', 'KNWA111111'),\
                ('corr', 'KA11111111'), ('corrigall', 'KRKA111111'),\
                ('corrigan', 'KRKN111111'), ('corsar', 'KSA1111111'),\
                ('corsion', 'KSN1111111'), ('corston', 'KSTN111111'),\
                ('cortisson', 'KTSN111111'), ('cortissos', 'KTSS111111'),\
                ('cosegrove', 'KSKRF11111'), ('cosgriff', 'KSKRF11111'),\
                ('cosgrove', 'KSKRF11111'), ('cossens', 'KSNS111111'),\
                ('cossum', 'KSM1111111'), ('costall', 'KSTA111111'),\
                ('costello', 'KSTLA11111'), ('coster', 'KSTA111111'),\
                ('costigan', 'KSTKN11111'), ('costley', 'KSTLA11111'),\
                ('cother', 'KTA1111111'), ('cotston', 'KTSTN11111'),\
                ('cottam', 'KTM1111111'), ('cotter', 'KTA1111111'),\
                ('cotterill', 'KTRA111111'), ('cottghlan', 'KTLN111111'),\
                ('cottle', 'KTA1111111'), ('cotton', 'KTN1111111'),\
                ('cottrell', 'KTRA111111'), ('couch', 'KK11111111'),\
                ('couchman', 'KKMN111111'), ('coughlan', 'KFLN111111'),\
                ('coughtrey', 'KFTRA11111'), ('couling', 'KLNK111111'),\
                ('coull', 'KA11111111'), ('coulson', 'KSN1111111'),\
                ('coulston', 'KSTN111111'), ('coulter', 'KTA1111111'),\
                ('counar', 'KNA1111111'), ('counihan', 'KNN1111111'),\
                ('coupar', 'KPA1111111'), ('couper', 'KPA1111111'),\
                ('coupland', 'KPLNT11111'), ('course', 'KS11111111'),\
                ('court', 'KT11111111'), ('courtayne', 'KTN1111111'),\
                ('courter', 'KTA1111111'), ('courtis', 'KTS1111111'),\
                ('courtney', 'KTNA111111'), ('cousins', 'KSNS111111'),\
                ('couston', 'KSTN111111'), ('coutts', 'KTS1111111'),\
                ('coventry', 'KFNTRA1111'), ('cowan', 'KWN1111111'),\
                ('coward', 'KWT1111111'), ('cowen', 'KWN1111111'),\
                ('cowey', 'KWA1111111'), ('cowie', 'KWA1111111'),\
                ('cowle', 'KA11111111'), ('cowles', 'KLS1111111'),\
                ('cowper', 'KPA1111111'), ('cox', 'KK11111111'),\
                ('coxhead', 'KKT1111111'), ('coxhend', 'KKNT111111'),\
                ('coxon', 'KKN1111111'), ('coy', 'KA11111111'),\
                ('crabb', 'KRP1111111'), ('crabbe', 'KRP1111111'),\
                ('cragg', 'KRK1111111'), ('craib', 'KRP1111111'),\
                ('craies', 'KRS1111111'), ('craig', 'KRK1111111'),\
                ('craige', 'KRK1111111'), ('craigie', 'KRKA111111'),\
                ('craik', 'KRK1111111'), ('crammond', 'KRMNT11111'),\
                ('cramond', 'KRMNT11111'), ('crampton', 'KRMPTN1111'),\
                ('cran', 'KRN1111111'), ('crandle', 'KRNTA11111'),\
                ('crane', 'KRN1111111'), ('cranefield', 'KRNFT11111'),\
                ('cranford', 'KRNFT11111'), ('cranley', 'KRNLA11111'),\
                ('crannitch', 'KRNK111111'), ('cranshaw', 'KRNSA11111'),\
                ('cranston', 'KRNSTN1111'), ('craven-carden', 'KRFNKTN111'),\
                ('craven', 'KRFN111111'), ('crawford', 'KRFT111111'),\
                ('crawfurd', 'KRFT111111'), ('crawley', 'KRLA111111'),\
                ('crawshaw', 'KRSA111111'), ('creagh', 'KRA1111111'),\
                ('credgington', 'KRKNKTN111'), ('creed', 'KRT1111111'),\
                ('creeser', 'KRSA111111'), ('creevey', 'KRFA111111'),\
                ('creighton', 'KRTN111111'), ('cremmens', 'KRMNS11111'),\
                ('crerar', 'KRRA111111'), ('cress', 'KRS1111111'),\
                ('crews', 'KRS1111111'), ('crichton', 'KRKTN11111'),\
                ('crighton', 'KRTN111111'), ('crilly', 'KRLA111111'),\
                ('crimp', 'KRMP111111'), ('cripps', 'KRPS111111'),\
                ('crisp', 'KRSP111111'), ('critchfie', 'KRKFA11111'),\
                ('critchfiel', 'KRKFA11111'), ('critchfield', 'KRKFT11111'),\
                ('critchley', 'KRKLA11111'), ('croad', 'KRT1111111'),\
                ('croal', 'KRA1111111'), ('crocome', 'KRKM111111'),\
                ('croft', 'KRFT111111'), ('croker', 'KRKA111111'),\
                ('crolly', 'KRLA111111'), ('cromarty', 'KRMTA11111'),\
                ('crombie', 'KRMPA11111'), ('crome', 'KRM1111111'),\
                ('crompton', 'KRMPTN1111'), ('crone', 'KRN1111111'),\
                ('cronhie', 'KRNA111111'), ('cronin', 'KRNN111111'),\
                ('crooke', 'KRK1111111'), ('crookes', 'KRKS111111'),\
                ('crooks', 'KRKS111111'), ('crookshanks', 'KRKSNKS111'),\
                ('croot', 'KRT1111111'), ('cropley', 'KRPLA11111'),\
                ('cropp', 'KRP1111111'), ('crosado', 'KRSTA11111'),\
                ('crosbie', 'KRSPA11111'), ('crosby', 'KRSPA11111'),\
                ('crosland', 'KRSLNT1111'), ('cross', 'KRS1111111'),\
                ('crossan-moffat', 'KRSNMFT111'), ('crossan', 'KRSN111111'),\
                ('crossens', 'KRSNS11111'), ('crossian', 'KRSN111111'),\
                ('crossley', 'KRSLA11111'), ('crosswell', 'KRSWA11111'),\
                ('crossweller', 'KRSWLA1111'), ('crostie', 'KRSTA11111'),\
                ('croswell', 'KRSWA11111'), ('crouch', 'KRK1111111'),\
                ('crow', 'KRA1111111'), ('crowan', 'KRWN111111'),\
                ('crowder', 'KRTA111111'), ('crowe', 'KRA1111111'),\
                ('crowhurst', 'KRWST11111'), ('crowley', 'KRLA111111'),\
                ('crowther', 'KRTA111111'), ('croxford', 'KRKFT11111'),\
                ('croy', 'KRA1111111'), ('crozier', 'KRSA111111'),\
                ('cruickshank', 'KRKSNK1111'), ('cruikshank', 'KRKSNK1111'),\
                ('crum', 'KRM1111111'), ('crump', 'KRMP111111'),\
                ('cruse', 'KRS1111111'), ('crust', 'KRST111111'),\
                ('cubbins', 'KPNS111111'), ('cuddihy', 'KTA1111111'),\
                ('cuff', 'KF11111111'), ('culbert', 'KPT1111111'),\
                ('culhane', 'KN11111111'), ('cull', 'KA11111111'),\
                ('cullen', 'KLN1111111'), ('culling', 'KLNK111111'),\
                ('cullinger', 'KLNKA11111'), ('culsey', 'KSA1111111'),\
                ('cumberbeac', 'KMPPK11111'), ('cumberbeach', 'KMPPK11111'),\
                ('cuming', 'KMNK111111'), ('cumins', 'KMNS111111'),\
                ('cumming', 'KMNK111111'), ('cummings', 'KMNKS11111'),\
                ('cummins', 'KMNS111111'), ('cummock', 'KMK1111111'),\
                ('cundall', 'KNTA111111'), ('cunhingham', 'KNNM111111'),\
                ('cunliffe', 'KNLF111111'), ('cunming', 'KNMNK11111'),\
                ('cunningham', 'KNNM111111'), ('cunninghame', 'KNNM111111'),\
                ('cupid', 'KPT1111111'), ('cupples', 'KPLS111111'),\
                ('curey', 'KRA1111111'), ('curfie', 'KFA1111111'),\
                ('curie', 'KRA1111111'), ('curle', 'KA11111111'),\
                ('curline', 'KLN1111111'), ('curran', 'KRN1111111'),\
                ('curren', 'KRN1111111'), ('currie', 'KRA1111111'),\
                ('curry', 'KRA1111111'), ('cursey', 'KSA1111111'),\
                ('curtayne', 'KTN1111111'), ('curties', 'KTS1111111'),\
                ('curtin', 'KTN1111111'), ('curtis', 'KTS1111111'),\
                ('curye', 'KRA1111111'), ('curzon-sig', 'KSNSK11111'),\
                ('curzon-siggers', 'KSNSKS1111'), ('cusach', 'KSK1111111'),\
                ('cusack', 'KSK1111111'), ('cushen', 'KSN1111111'),\
                ('cushman', 'KSMN111111'), ('cushnan', 'KSNN111111'),\
                ('cushnie', 'KSNA111111'), ('cutbush', 'KTPS111111'),\
                ('cuthbertson', 'KTPTSN1111'), ('cuthterts', 'KTTTS11111'),\
                ('cutler', 'KTLA111111'), ('cutriss', 'KTRS111111'),\
                ('cuttance', 'KTNK111111'), ('cutten', 'KTN1111111'),\
                ('cutter', 'KTA1111111'), ('cuttle', 'KTA1111111'),\
                ('cuttriss', 'KTRS111111'), ('cutts', 'KTS1111111'),\
                ('cuzens', 'KSNS111111'), ('cvitanovich', 'KFTNFK1111'),\
                ('d\'auvergne', 'TFKN111111'), ('dabinett', 'TPNT111111'),\
                ('dacker', 'TKA1111111'), ('dagg', 'TK11111111'),\
                ('dagger', 'TKA1111111'), ('dagleish', 'TKLS111111'),\
                ('daglish', 'TKLS111111'), ('dagnall', 'TKNA111111'),\
                ('dagnell', 'TKNA111111'), ('dahren', 'TRN1111111'),\
                ('dakers', 'TKS1111111'), ('dale', 'TA11111111'),\
                ('dales', 'TLS1111111'), ('dalgar', 'TKA1111111'),\
                ('dalgarno', 'TKNA111111'), ('dalgeish', 'TKS1111111'),\
                ('dalgleish', 'TKLS111111'), ('dalgliesh', 'TKLS111111'),\
                ('dall', 'TA11111111'), ('dallard', 'TLT1111111'),\
                ('dallas', 'TLS1111111'), ('dallaston', 'TLSTN11111'),\
                ('dallen', 'TLN1111111'), ('dalley', 'TLA1111111'),\
                ('dalrymple', 'TRMPA11111'), ('dalton', 'TTN1111111'),\
                ('daly', 'TLA1111111'), ('dalzell', 'TSA1111111'),\
                ('dalziel', 'TSA1111111'), ('dandie', 'TNTA111111'),\
                ('daniel', 'TNA1111111'), ('daniell', 'TNA1111111'),\
                ('daniels', 'TNS1111111'), ('dann', 'TN11111111'),\
                ('danner', 'TNA1111111'), ('danskin', 'TNSKN11111'),\
                ('darcy', 'TSA1111111'), ('dark', 'TK11111111'),\
                ('darley', 'TLA1111111'), ('darling', 'TLNK111111'),\
                ('darlison', 'TLSN111111'), ('darracott', 'TRKT111111'),\
                ('darragh', 'TRA1111111'), ('darroch', 'TRK1111111'),\
                ('dash', 'TS11111111'), ('dashper', 'TSPA111111'),\
                ('dashwood', 'TSWT111111'), ('dasler', 'TSLA111111'),\
                ('daubney', 'TPNA111111'), ('daunt', 'TNT1111111'),\
                ('davany', 'TFNA111111'), ('daveis', 'TFS1111111'),\
                ('davenport', 'TFNPT11111'), ('davey', 'TFA1111111'),\
                ('david', 'TFT1111111'), ('davidson', 'TFTSN11111'),\
                ('davie', 'TFA1111111'), ('davies', 'TFS1111111'),\
                ('davis', 'TFS1111111'), ('davison', 'TFSN111111'),\
                ('davy', 'TFA1111111'), ('davys', 'TFS1111111'),\
                ('dawe', 'TA11111111'), ('dawes', 'TWS1111111'),\
                ('dawkins', 'TKNS111111'), ('dawsett', 'TST1111111'),\
                ('dawson', 'TSN1111111'), ('day', 'TA11111111'),\
                ('daysh', 'TS11111111'), ('de bazin', 'TPSN111111'),\
                ('de berry', 'TPRA111111'), ('de boyett', 'TPT1111111'),\
                ('de carle', 'TKA1111111'), ('de castro', 'TKSTRA1111'),\
                ('de clifford', 'TKLFT11111'), ('de clive lowe', 'TKLFLA1111'),\
                ('de colmar', 'TKMA111111'), ('de courcey', 'TKSA111111'),\
                ('de courcy', 'TKSA111111'), ('de lacey', 'TLSA111111'),\
                ('de largey', 'TLKA111111'), ('de lautour', 'TLTA111111'),\
                ('de malmanche', 'TMMNK11111'), ('de ment', 'TMNT111111'),\
                ('de silva', 'TSFA111111'), ('de spong', 'TSPNK11111'),\
                ('de st croix', 'TSTKRK1111'), ('de st. croix', 'TSTKRK1111'),\
                ('de vere', 'TFA1111111'), ('de-clive-low', 'TKLFLA1111'),\
                ('deaker', 'TKA1111111'), ('deamy', 'TMA1111111'),\
                ('dean', 'TN11111111'), ('deane', 'TN11111111'),\
                ('deans', 'TNS1111111'), ('dear', 'TA11111111'),\
                ('dease', 'TS11111111'), ('debenham', 'TPNM111111'),\
                ('deberry', 'TPRA111111'), ('decourcy', 'TKSA111111'),\
                ('dee', 'TA11111111'), ('deegan', 'TKN1111111'),\
                ('deehan', 'TN11111111'), ('deem', 'TM11111111'),\
                ('deikle', 'TKA1111111'), ('deiley', 'TLA1111111'),\
                ('deisher', 'TSA1111111'), ('delahunty', 'TLNTA11111'),\
                ('delaney', 'TLNA111111'), ('delany', 'TLNA111111'),\
                ('delargey', 'TLKA111111'), ('delargy', 'TLKA111111'),\
                ('delbridge', 'TPRK111111'), ('dell', 'TA11111111'),\
                ('dely', 'TLA1111111'), ('dement', 'TMNT111111'),\
                ('demontalk', 'TMNTK11111'), ('demouth', 'TMT1111111'),\
                ('dempsey', 'TMPSA11111'), ('dempster', 'TMPSTA1111'),\
                ('dench', 'TNK1111111'), ('dencker', 'TNKA111111'),\
                ('denfold', 'TNFT111111'), ('denfolrd', 'TNFT111111'),\
                ('denford', 'TNFT111111'), ('denham', 'TNM1111111'),\
                ('denhehy', 'TNA1111111'), ('denholm', 'TNM1111111'),\
                ('denholme', 'TNM1111111'), ('denne', 'TN11111111'),\
                ('dennehy', 'TNA1111111'), ('dennis', 'TNS1111111'),\
                ('dennison', 'TNSN111111'), ('denniston', 'TNSTN11111'),\
                ('denny', 'TNA1111111'), ('densem', 'TNSM111111'),\
                ('dent', 'TNT1111111'), ('dentith', 'TNTT111111'),\
                ('denton', 'TNTN111111'), ('depellett', 'TPLT111111'),\
                ('dephoff', 'TFF1111111'), ('derbie', 'TPA1111111'),\
                ('derbyshire', 'TPSA111111'), ('dermer', 'TMA1111111'),\
                ('dernehy', 'TNA1111111'), ('derrick', 'TRK1111111'),\
                ('derry', 'TRA1111111'), ('desmond', 'TSMNT11111'),\
                ('desmoulins', 'TSMLNS1111'), ('dessarthe', 'TST1111111'),\
                ('dester', 'TSTA111111'), ('deuchrass', 'TKRS111111'),\
                ('devaney', 'TFNA111111'), ('devany', 'TFNA111111'),\
                ('devenie', 'TFNA111111'), ('devenney', 'TFNA111111'),\
                ('dever', 'TFA1111111'), ('devereux', 'TFRK111111'),\
                ('devery', 'TFRA111111'), ('devine', 'TFN1111111'),\
                ('devlill', 'TFLA111111'), ('devlin', 'TFLN111111'),\
                ('dew', 'TA11111111'), ('dewar', 'TWA1111111'),\
                ('dexter', 'TKTA111111'), ('dey', 'TA11111111'),\
                ('diack', 'TK11111111'), ('diamond', 'TMNT111111'),\
                ('dick', 'TK11111111'), ('dickens', 'TKNS111111'),\
                ('dickeon', 'TKN1111111'), ('dicker', 'TKA1111111'),\
                ('dickey', 'TKA1111111'), ('dickie', 'TKA1111111'),\
                ('dickinson', 'TKNSN11111'), ('dickison', 'TKSN111111'),\
                ('dicksan', 'TKSN111111'), ('dickson', 'TKSN111111'),\
                ('didham', 'TTM1111111'), ('didsbury', 'TTSPRA1111'),\
                ('diefenbach', 'TFNPK11111'), ('diehl', 'TA11111111'),\
                ('digby-smith', 'TKPSMT1111'), ('dillan', 'TLN1111111'),\
                ('dillon-kin', 'TLNKN11111'), ('dillon', 'TLN1111111'),\
                ('dimond', 'TMNT111111'), ('dineen', 'TNN1111111'),\
                ('dingle', 'TNKA111111'), ('dingwall', 'TNKWA11111'),\
                ('dinning', 'TNNK111111'), ('dinsell', 'TNSA111111'),\
                ('dippie', 'TPA1111111'), ('direen', 'TRN1111111'),\
                ('diston', 'TSTN111111'), ('diver', 'TFA1111111'),\
                ('divers', 'TFS1111111'), ('divett', 'TFT1111111'),\
                ('dix', 'TK11111111'), ('dixon', 'TKN1111111'),\
                ('dixs', 'TKS1111111'), ('doak', 'TK11111111'),\
                ('doake', 'TK11111111'), ('dobbie', 'TPA1111111'),\
                ('dobbin', 'TPN1111111'), ('dobble', 'TPA1111111'),\
                ('dobbs', 'TPS1111111'), ('dobe', 'TP11111111'),\
                ('dobie', 'TPA1111111'), ('dobson', 'TPSN111111'),\
                ('docherty', 'TKTA111111'), ('dockworth', 'TKWT111111'),\
                ('dodd', 'TT11111111'), ('doddridge', 'TTRK111111'),\
                ('dodds', 'TTS1111111'), ('dods', 'TTS1111111'),\
                ('doggart', 'TKT1111111'), ('doherty', 'TTA1111111'),\
                ('dohig', 'TK11111111'), ('doig', 'TK11111111'),\
                ('dolan', 'TLN1111111'), ('dolman', 'TMN1111111'),\
                ('dolphin', 'TFN1111111'), ('domigan', 'TMKN111111'),\
                ('dommett', 'TMT1111111'), ('don', 'TN11111111'),\
                ('donald', 'TNT1111111'), ('donaldson', 'TNTSN11111'),\
                ('done', 'TN11111111'), ('donellan', 'TNLN111111'),\
                ('donglas', 'TNKLS11111'), ('donlan', 'TNLN111111'),\
                ('donn', 'TN11111111'), ('donnald', 'TNT1111111'),\
                ('donne', 'TN11111111'), ('donneily', 'TNLA111111'),\
                ('donnelly', 'TNLA111111'), ('donoghue', 'TNKA111111'),\
                ('donovan', 'TNFN111111'), ('doocey', 'TSA1111111'),\
                ('doody', 'TTA1111111'), ('dooley', 'TLA1111111'),\
                ('doorley', 'TLA1111111'), ('doran', 'TRN1111111'),\
                ('dore', 'TA11111111'), ('doreman', 'TRMN111111'),\
                ('dorman', 'TMN1111111'), ('dormer', 'TMA1111111'),\
                ('dorney', 'TNA1111111'), ('dorreen', 'TRN1111111'),\
                ('dorrian', 'TRN1111111'), ('dorsey', 'TSA1111111'),\
                ('dorward', 'TWT1111111'), ('dossett', 'TST1111111'),\
                ('double', 'TPA1111111'), ('doudle', 'TTA1111111'),\
                ('dougal', 'TKA1111111'), ('dougali', 'TKLA111111'),\
                ('dougall', 'TKA1111111'), ('dougan', 'TKN1111111'),\
                ('dougherty', 'TKTA111111'), ('doughty', 'TTA1111111'),\
                ('douglans', 'TKLNS11111'), ('douglas', 'TKLS111111'),\
                ('douglass', 'TKLS111111'), ('douherty', 'TTA1111111'),\
                ('doulass', 'TLS1111111'), ('douli', 'TLA1111111'),\
                ('doull', 'TA11111111'), ('dov', 'TF11111111'),\
                ('dove', 'TF11111111'), ('dow', 'TA11111111'),\
                ('dowdall', 'TTA1111111'), ('dowden', 'TTN1111111'),\
                ('dowell', 'TWA1111111'), ('dowey', 'TWA1111111'),\
                ('dowie', 'TWA1111111'), ('dowland', 'TLNT111111'),\
                ('dowling', 'TLNK111111'), ('down', 'TN11111111'),\
                ('downer', 'TNA1111111'), ('downes', 'TNS1111111'),\
                ('downey', 'TNA1111111'), ('downie', 'TNA1111111'),\
                ('downs', 'TNS1111111'), ('doyle', 'TA11111111'),\
                ('drain', 'TRN1111111'), ('drake', 'TRK1111111'),\
                ('drane', 'TRN1111111'), ('draper', 'TRPA111111'),\
                ('dray', 'TRA1111111'), ('drayton', 'TRTN111111'),\
                ('dreaver', 'TRFA111111'), ('dreavor', 'TRFA111111'),\
                ('drees', 'TRS1111111'), ('drench', 'TRNK111111'),\
                ('drennan', 'TRNN111111'), ('drew-daniels', 'TRTNS11111'),\
                ('drew', 'TRA1111111'), ('dripps', 'TRPS111111'),\
                ('driscole', 'TRSKA11111'), ('driscoll-shaw', 'TRSKSA1111'),\
                ('driscoll', 'TRSKA11111'), ('driver', 'TRFA111111'),\
                ('droaver', 'TRFA111111'), ('droscher', 'TRSKA11111'),\
                ('drosier', 'TRSA111111'), ('drumm', 'TRM1111111'),\
                ('drummond', 'TRMNT11111'), ('drury', 'TRRA111111'),\
                ('dry', 'TRA1111111'), ('dryden', 'TRTN111111'),\
                ('drysdale', 'TRSTA11111'), ('duckett', 'TKT1111111'),\
                ('duckmanton', 'TKMNTN1111'), ('duckworth', 'TKWT111111'),\
                ('dudding', 'TTNK111111'), ('duder', 'TTA1111111'),\
                ('dudley', 'TTLA111111'), ('dudson', 'TTSN111111'),\
                ('duell', 'TA11111111'), ('duerden', 'TTN1111111'),\
                ('duff', 'TF11111111'), ('duffy', 'TFA1111111'),\
                ('dugdale', 'TKTA111111'), ('duggan', 'TKN1111111'),\
                ('dugleby', 'TKLPA11111'), ('duguid', 'TKT1111111'),\
                ('duhig', 'TK11111111'), ('duig', 'TK11111111'),\
                ('duigan', 'TKN1111111'), ('duignan', 'TKNN111111'),\
                ('duke', 'TK11111111'), ('dull', 'TA11111111'),\
                ('dulward', 'TWT1111111'), ('dumas', 'TMS1111111'),\
                ('dumble', 'TMPA111111'), ('dumsday', 'TMSTA11111'),\
                ('dun', 'TN11111111'), ('dunbar', 'TNPA111111'),\
                ('duncall', 'TNKA111111'), ('duncan', 'TNKN111111'),\
                ('dundas', 'TNTS111111'), ('dunean', 'TNN1111111'),\
                ('dunford', 'TNFT111111'), ('dungan', 'TNKN111111'),\
                ('dungey', 'TNKA111111'), ('dunham', 'TNM1111111'),\
                ('dunhar', 'TNA1111111'), ('dunipace', 'TNPK111111'),\
                ('dunkerton', 'TNKTN11111'), ('dunkin', 'TNKN111111'),\
                ('dunkley', 'TNKLA11111'), ('dunlop', 'TNLP111111'),\
                ('dunn', 'TN11111111'), ('dunnage', 'TNK1111111'),\
                ('dunne', 'TN11111111'), ('dunnet', 'TNT1111111'),\
                ('dunnig', 'TNK1111111'), ('dunning', 'TNNK111111'),\
                ('dunring', 'TNRNK11111'), ('dunshea', 'TNSA111111'),\
                ('dunsmuir', 'TNSMA11111'), ('dunstan', 'TNSTN11111'),\
                ('dunster', 'TNSTA11111'), ('durand', 'TRNT111111'),\
                ('durie', 'TRA1111111'), ('durning', 'TNNK111111'),\
                ('duro', 'TRA1111111'), ('durrand', 'TRNT111111'),\
                ('durrant', 'TRNT111111'), ('durreen', 'TRN1111111'),\
                ('durry', 'TRA1111111'), ('duthie', 'TTA1111111'),\
                ('dutton', 'TTN1111111'), ('dwan', 'TWN1111111'),\
                ('dwight', 'TWT1111111'), ('dwyer', 'TWA1111111'),\
                ('dyas', 'TS11111111'), ('dyer', 'TA11111111'),\
                ('dyke', 'TK11111111'), ('dykes', 'TKS1111111'),\
                ('dykins', 'TKNS111111'), ('dysart', 'TST1111111'),\
                ('dysaski', 'TSSKA11111'), ('dyson', 'TSN1111111'),\
                ('eade', 'AT11111111'), ('eades', 'ATS1111111'),\
                ('eadie', 'ATA1111111'), ('eady', 'ATA1111111'),\
                ('eagan', 'AKN1111111'), ('eagar', 'AKA1111111'),\
                ('eager', 'AKA1111111'), ('eagle', 'AKA1111111'),\
                ('eagles', 'AKLS111111'), ('eagleton', 'AKLTN11111'),\
                ('eamilton', 'AMTN111111'), ('eardley', 'ATLA111111'),\
                ('eardly', 'ATLA111111'), ('earl', 'AA11111111'),\
                ('earland', 'ALNT111111'), ('earley', 'ALA1111111'),\
                ('early', 'ALA1111111'), ('earnshaw', 'ANSA111111'),\
                ('earp', 'AP11111111'), ('eason', 'ASN1111111'),\
                ('easson', 'ASN1111111'), ('east', 'AST1111111'),\
                ('easther', 'ASTA111111'), ('easton', 'ASTN111111'),\
                ('eastwood', 'ASTWT11111'), ('eaton', 'ATN1111111'),\
                ('eayes', 'AS11111111'), ('ebzery', 'APSRA11111'),\
                ('eccles', 'AKLS111111'), ('eckhoff', 'AKF1111111'),\
                ('eckhold', 'AKT1111111'), ('ecsex', 'AKSK111111'),\
                ('eddington', 'ATNKTN1111'), ('ede-clendinnen', 'ATKLNTNN11'),\
                ('ede', 'AT11111111'), ('eden', 'ATN1111111'),\
                ('edgar', 'AKA1111111'), ('edgares', 'AKRS111111'),\
                ('edge', 'AK11111111'), ('edginton', 'AKNTN11111'),\
                ('edie', 'ATA1111111'), ('ediin', 'ATN1111111'),\
                ('edin', 'ATN1111111'), ('edinger', 'ATNKA11111'),\
                ('edington', 'ATNKTN1111'), ('edis', 'ATS1111111'),\
                ('edkins', 'ATKNS11111'), ('edlin', 'ATLN111111'),\
                ('edmenson', 'ATMNSN1111'), ('edmond', 'ATMNT11111'),\
                ('edmonds', 'ATMNTS1111'), ('edridge', 'ATRK111111'),\
                ('edsall', 'ATSA111111'), ('edson', 'ATSN111111'),\
                ('edward', 'ATWT111111'), ('edwards', 'ATWTS11111'),\
                ('edwardson', 'ATWTSN1111'), ('egan', 'AKN1111111'),\
                ('egerton', 'AKTN111111'), ('eggelton', 'AKTN111111'),\
                ('eggers', 'AKS1111111'), ('egglestone', 'AKLSTN1111'),\
                ('eggleton', 'AKLTN11111'), ('eilis', 'ALS1111111'),\
                ('elbra', 'APRA111111'), ('elder', 'ATA1111111'),\
                ('elders', 'ATS1111111'), ('elding', 'ATNK111111'),\
                ('eldridge', 'ATRK111111'), ('elias', 'ALS1111111'),\
                ('eliot', 'ALT1111111'), ('eliott', 'ALT1111111'),\
                ('ellacombe', 'ALKM111111'), ('ellens', 'ALNS111111'),\
                ('ellery', 'ALRA111111'), ('elliffe', 'ALF1111111'),\
                ('elliis', 'ALS1111111'), ('ellingwood', 'ALNKWT1111'),\
                ('elliobt', 'ALPT111111'), ('elliot', 'ALT1111111'),\
                ('elliott', 'ALT1111111'), ('elliotte', 'ALT1111111'),\
                ('ellis', 'ALS1111111'), ('ellison', 'ALSN111111'),\
                ('ellisson', 'ALSN111111'), ('ells', 'AS11111111'),\
                ('elms', 'AMS1111111'), ('elmsly', 'AMSLA11111'),\
                ('elphick', 'AFK1111111'), ('elphinstone', 'AFNSTN1111'),\
                ('elsey', 'ASA1111111'), ('elsom', 'ASM1111111'),\
                ('elston', 'ASTN111111'), ('elstow', 'ASTA111111'),\
                ('elton', 'ATN1111111'), ('elvidge', 'AFK1111111'),\
                ('emerson', 'AMSN111111'), ('emery', 'AMRA111111'),\
                ('emlis', 'AMLS111111'), ('emmerson', 'AMSN111111'),\
                ('emond', 'AMNT111111'), ('empey', 'AMPA111111'),\
                ('emslie', 'AMSLA11111'), ('endicott davies', 'ANTKTFS111'),\
                ('endicott-davies', 'ANTKTFS111'),\
                ('endicottdavies', 'ANTKTFS111'),\
                ('engelbert', 'ANKPT11111'), ('england', 'ANKLNT1111'),\
                ('englefield', 'ANKLFT1111'), ('english', 'ANKLS11111'),\
                ('engstrom', 'ANKSTRM111'), ('enright', 'ANRT111111'),\
                ('ensor', 'ANSA111111'), ('enticote', 'ANTKT11111'),\
                ('eorne', 'AN11111111'), ('erenstrom', 'ARNSTRM111'),\
                ('erickson', 'ARKSN11111'), ('ericson', 'ARKSN11111'),\
                ('erlandson', 'ALNTSN1111'), ('erlidge', 'ALK1111111'),\
                ('erridge', 'ARK1111111'), ('errington', 'ARNKTN1111'),\
                ('erskine', 'ASKN111111'), ('erwin', 'AWN1111111'),\
                ('escott', 'ASKT111111'), ('eskdale', 'ASKTA11111'),\
                ('esperson', 'ASPSN11111'), ('espie', 'ASPA111111'),\
                ('esplin', 'ASPLN11111'), ('esquilant', 'ASKLNT1111'),\
                ('essex', 'ASK1111111'), ('esson', 'ASN1111111'),\
                ('essson', 'ASN1111111'), ('esther', 'ASTA111111'),\
                ('etheridge', 'ATRK111111'), ('eunson', 'ANSN111111'),\
                ('eustace', 'ASTK111111'), ('eva', 'AFA1111111'),\
                ('evan', 'AFN1111111'), ('evana', 'AFNA111111'),\
                ('evans', 'AFNS111111'), ('evatt', 'AFT1111111'),\
                ('evavs', 'AFFS111111'), ('everest', 'AFRST11111'),\
                ('everett', 'AFRT111111'), ('everitt', 'AFRT111111'),\
                ('everleigh', 'AFLA111111'), ('everson', 'AFSN111111'),\
                ('every', 'AFRA111111'), ('ewan', 'AWN1111111'),\
                ('ewart', 'AWT1111111'), ('ewens', 'AWNS111111'),\
                ('ewing', 'AWNK111111'), ('ewington-bell', 'AWNKTNPA11'),\
                ('exler', 'AKLA111111'), ('eyles', 'ALS1111111'),\
                ('eyre', 'AA11111111'), ('facer', 'FSA1111111'),\
                ('facey', 'FSA1111111'), ('fache', 'FK11111111'),\
                ('fackender', 'FKNTA11111'), ('facoory', 'FKRA111111'),\
                ('fagan', 'FKN1111111'), ('fahey', 'FA11111111'),\
                ('fahy', 'FA11111111'), ('faid', 'FT11111111'),\
                ('faigan', 'FKN1111111'), ('fail', 'FA11111111'),\
                ('fair', 'FA11111111'), ('fairbairn', 'FPN1111111'),\
                ('fairburn', 'FPN1111111'), ('faircloth', 'FKLT111111'),\
                ('fairhall', 'FA11111111'), ('fairhurst', 'FST1111111'),\
                ('fairley', 'FLA1111111'), ('fairlie', 'FLA1111111'),\
                ('fairmaid', 'FMT1111111'), ('fairweather', 'FWTA111111'),\
                ('faith', 'FT11111111'), ('faithful', 'FTFA111111'),\
                ('faithfull', 'FTFA111111'), ('falck', 'FK11111111'),\
                ('falcon', 'FKN1111111'), ('falconar', 'FKNA111111'),\
                ('falconer', 'FKNA111111'), ('falgar', 'FKA1111111'),\
                ('falkinar', 'FKNA111111'), ('falkner', 'FKNA111111'),\
                ('fall', 'FA11111111'), ('fallon', 'FLN1111111'),\
                ('fallowfield', 'FLFT111111'), ('familton', 'FMTN111111'),\
                ('fancourt', 'FNKT111111'), ('fanner', 'FNA1111111'),\
                ('fanning', 'FNNK111111'), ('fannon', 'FNN1111111'),\
                ('fantham', 'FNTM111111'), ('fargie', 'FKA1111111'),\
                ('faris', 'FRS1111111'), ('farland', 'FLNT111111'),\
                ('farmer', 'FMA1111111'), ('farminger', 'FMNKA11111'),\
                ('farquhar', 'FKA1111111'), ('farquharon', 'FKRN111111'),\
                ('farquhars', 'FKS1111111'), ('farquharson', 'FKSN111111'),\
                ('farr', 'FA11111111'), ('farra', 'FRA1111111'),\
                ('farrant', 'FRNT111111'), ('farrell', 'FRA1111111'),\
                ('farrelly', 'FRLA111111'), ('farrington', 'FRNKTN1111'),\
                ('farrow', 'FRA1111111'), ('farry', 'FRA1111111'),\
                ('fastier', 'FSTA111111'), ('faul', 'FA11111111'),\
                ('faulder', 'FTA1111111'), ('faulds', 'FTS1111111'),\
                ('faulkner', 'FKNA111111'), ('faulks', 'FKS1111111'),\
                ('faull', 'FA11111111'), ('favel', 'FFA1111111'),\
                ('favell', 'FFA1111111'), ('fawcett', 'FST1111111'),\
                ('fay', 'FA11111111'), ('fazakerley', 'FSKLA11111'),\
                ('fearn', 'FN11111111'), ('feast', 'FST1111111'),\
                ('feathersto', 'FTSTA11111'), ('featherstone', 'FTSTN11111'),\
                ('feely', 'FLA1111111'), ('feeney', 'FNA1111111'),\
                ('feichley', 'FKLA111111'), ('feil', 'FA11111111'),\
                ('fell', 'FA11111111'), ('felmingha', 'FMNA111111'),\
                ('felmingham', 'FMNM111111'), ('feltham', 'FTM1111111'),\
                ('felton', 'FTN1111111'), ('fenby', 'FNPA111111'),\
                ('fendall', 'FNTA111111'), ('fenelon', 'FNLN111111'),\
                ('fennessey', 'FNSA111111'), ('fennessy', 'FNSA111111'),\
                ('fenton', 'FNTN111111'), ('fenwick', 'FNWK111111'),\
                ('ferdinand', 'FTNNT11111'), ('ferens', 'FRNS111111'),\
                ('fergus', 'FKS1111111'), ('ferguson', 'FKSN111111'),\
                ('fergusson', 'FKSN111111'), ('fern', 'FN11111111'),\
                ('fernie', 'FNA1111111'), ('feron', 'FRN1111111'),\
                ('ferrier', 'FRA1111111'), ('ferris', 'FRS1111111'),\
                ('ferry', 'FRA1111111'), ('fewtrell', 'FTRA111111'),\
                ('ffrost', 'FRST111111'), ('fibbes', 'FPS1111111'),\
                ('fiddes', 'FTS1111111'), ('fiddis', 'FTS1111111'),\
                ('field', 'FT11111111'), ('fielden', 'FTN1111111'),\
                ('fielder', 'FTA1111111'), ('fielding', 'FTNK111111'),\
                ('fieldwick', 'FTWK111111'), ('fifield', 'FFT1111111'),\
                ('figgins', 'FKNS111111'), ('filewood', 'FLWT111111'),\
                ('fillingham', 'FLNM111111'), ('finch', 'FNK1111111'),\
                ('findlater', 'FNTLTA1111'), ('findlav', 'FNTLF11111'),\
                ('findlay', 'FNTLA11111'), ('findley', 'FNTLA11111'),\
                ('findon', 'FNTN111111'), ('finlavson', 'FNLFSN1111'),\
                ('finlay', 'FNLA111111'), ('finlayson', 'FNLSN11111'),\
                ('finley', 'FNLA111111'), ('finlin', 'FNLN111111'),\
                ('finn', 'FN11111111'), ('finnegan', 'FNKN111111'),\
                ('finnerty', 'FNTA111111'), ('finnie', 'FNA1111111'),\
                ('firkin', 'FKN1111111'), ('firth', 'FT11111111'),\
                ('fish', 'FS11111111'), ('fisher', 'FSA1111111'),\
                ('fisken', 'FSKN111111'), ('fisse', 'FS11111111'),\
                ('fitspatrick', 'FTSPTRK111'), ('fitt', 'FT11111111'),\
                ('fitz patrick', 'FTSPTRK111'), ('fitz-patrick', 'FTSPTRK111'),\
                ('fitzell', 'FTSA111111'), ('fitzer', 'FTSA111111'),\
                ('fitzgeral', 'FTSKRA1111'), ('fitzgerald', 'FTSKRT1111'),\
                ('fitzgibbons', 'FTSKPNS111'), ('fitzpatric', 'FTSPTRK111'),\
                ('fitzpatrick', 'FTSPTRK111'), ('fiynn', 'FN11111111'),\
                ('flaherty', 'FLTA111111'), ('flahive', 'FLF1111111'),\
                ('flanagan', 'FLNKN11111'), ('flanigan', 'FLNKN11111'),\
                ('flannagan', 'FLNKN11111'), ('flannery', 'FLNRA11111'),\
                ('flanning', 'FLNNK11111'), ('flawn', 'FLN1111111'),\
                ('flaws', 'FLS1111111'), ('fleck', 'FLK1111111'),\
                ('fleet', 'FLT1111111'), ('fleming', 'FLMNK11111'),\
                ('flening', 'FLNNK11111'), ('fletcher', 'FLKA111111'),\
                ('fleteher', 'FLTA111111'), ('flethcher', 'FLTKA11111'),\
                ('flett', 'FLT1111111'), ('fleury', 'FLRA111111'),\
                ('flinders', 'FLNTS11111'), ('flint', 'FLNT111111'),\
                ('flockton', 'FLKTN11111'), ('flood', 'FLT1111111'),\
                ('floyd', 'FLT1111111'), ('flugge', 'FLK1111111'),\
                ('flynn', 'FLN1111111'), ('foate', 'FT11111111'),\
                ('fogarty', 'FKTA111111'), ('fogo', 'FKA1111111'),\
                ('foley', 'FLA1111111'), ('folwell', 'FWA1111111'),\
                ('foord', 'FT11111111'), ('foote', 'FT11111111'),\
                ('forbes', 'FPS1111111'), ('force', 'FK11111111'),\
                ('ford', 'FT11111111'), ('forde', 'FT11111111'),\
                ('fordham', 'FTM1111111'), ('fordyce', 'FTK1111111'),\
                ('foreman', 'FRMN111111'), ('forest', 'FRST111111'),\
                ('forgeson', 'FKSN111111'), ('forgie', 'FKA1111111'),\
                ('forman', 'FMN1111111'), ('forno', 'FNA1111111'),\
                ('forrest', 'FRST111111'), ('forrester', 'FRSTA11111'),\
                ('forreter', 'FRTA111111'), ('forscutt', 'FSKT111111'),\
                ('forster', 'FSTA111111'), ('forsyth', 'FST1111111'),\
                ('fort', 'FT11111111'), ('fortune', 'FTN1111111'),\
                ('foster', 'FSTA111111'), ('fothergill', 'FTKA111111'),\
                ('fotheringh', 'FTRN111111'), ('fotheringham', 'FTRNM11111'),\
                ('fotheringharn', 'FTRNN11111'), ('fougere', 'FKA1111111'),\
                ('foulkes', 'FKS1111111'), ('fountain', 'FNTN111111'),\
                ('fow', 'FA11111111'), ('fowell', 'FWA1111111'),\
                ('foweraker', 'FWRKA11111'), ('fowler', 'FLA1111111'),\
                ('fox', 'FK11111111'), ('fox.', 'FK11111111'),\
                ('foxton', 'FKTN111111'), ('fraer', 'FRA1111111'),\
                ('frago', 'FRKA111111'), ('fraher', 'FRA1111111'),\
                ('frame', 'FRM1111111'), ('france', 'FRNK111111'),\
                ('francer', 'FRNSA11111'), ('francis', 'FRNSS11111'),\
                ('frank', 'FRNK111111'), ('frankham', 'FRNKM11111'),\
                ('franklin', 'FRNKLN1111'), ('frankpitt', 'FRNKPT1111'),\
                ('frapwell', 'FRPWA11111'), ('frascr', 'FRSKA11111'),\
                ('frasel', 'FRSA111111'), ('fraser', 'FRSA111111'),\
                ('frasor', 'FRSA111111'), ('frazer', 'FRSA111111'),\
                ('frederic', 'FRTRK11111'), ('fredric', 'FRTRK11111'),\
                ('freed', 'FRT1111111'), ('freedman', 'FRTMN11111'),\
                ('freeman', 'FRMN111111'), ('freernan', 'FRNN111111'),\
                ('french', 'FRNK111111'), ('fretwell', 'FRTWA11111'),\
                ('frew', 'FRA1111111'), ('frewen', 'FRWN111111'),\
                ('fricker', 'FRKA111111'), ('friedlander', 'FRTLNTA111'),\
                ('friedlich', 'FRTLK11111'), ('friend', 'FRNT111111'),\
                ('frier', 'FRA1111111'), ('frith', 'FRT1111111'),\
                ('froggatt', 'FRKT111111'), ('frood', 'FRT1111111'),\
                ('frost', 'FRST111111'), ('froude', 'FRT1111111'),\
                ('fruhstuch', 'FRSTK11111'), ('fruhstuck', 'FRSTK11111'),\
                ('fruish', 'FRS1111111'), ('fry', 'FRA1111111'),\
                ('frye', 'FRA1111111'), ('fryer', 'FRA1111111'),\
                ('ftzpatrck', 'FTSPTK1111'), ('fuell', 'FA11111111'),\
                ('fulcher', 'FKA1111111'), ('fuldseth', 'FTST111111'),\
                ('fullam', 'FLM1111111'), ('fullarton', 'FLTN111111'),\
                ('fuller', 'FLA1111111'), ('fullerton', 'FLTN111111'),\
                ('fulton', 'FTN1111111'), ('furminger', 'FMNKA11111'),\
                ('furness', 'FNS1111111'), ('fursdon', 'FSTN111111'),\
                ('fussell', 'FSA1111111'), ('fyfe', 'FF11111111'),\
                ('fyffe', 'FF11111111'), ('fynmore', 'FNMA111111'),\
                ('gabites', 'KPTS111111'), ('gable', 'KPA1111111'),\
                ('gadd', 'KT11111111'), ('gaffaney', 'KFNA111111'),\
                ('gaffeney', 'KFNA111111'), ('gaffey', 'KFA1111111'),\
                ('gaffney', 'KFNA111111'), ('gaiger', 'KKA1111111'),\
                ('gailichan', 'KLKN111111'), ('gain', 'KN11111111'),\
                ('gairdner', 'KTNA111111'), ('galagher', 'KLKA111111'),\
                ('galbraith', 'KPRT111111'), ('gale', 'KA11111111'),\
                ('gall', 'KA11111111'), ('gallacher', 'KLKA111111'),\
                ('gallagher', 'KLKA111111'), ('gallaher', 'KLA1111111'),\
                ('gallan', 'KLN1111111'), ('galland', 'KLNT111111'),\
                ('gallanders', 'KLNTS11111'), ('gallant', 'KLNT111111'),\
                ('gallaway', 'KLWA111111'), ('gallbraith', 'KPRT111111'),\
                ('gallichan', 'KLKN111111'), ('gallie', 'KLA1111111'),\
                ('galliven', 'KLFN111111'), ('gallngher', 'KNA1111111'),\
                ('galloway', 'KLWA111111'), ('gallschef', 'KSKF111111'),\
                ('galt', 'KT11111111'), ('galvin', 'KFN1111111'),\
                ('galway', 'KWA1111111'), ('gambell', 'KMPA111111'),\
                ('gamble', 'KMPA111111'), ('ganderton', 'KNTTN11111'),\
                ('gantley', 'KNTLA11111'), ('garbutt', 'KPT1111111'),\
                ('garcho', 'KKA1111111'), ('garchow', 'KKA1111111'),\
                ('gard\'ner', 'KTNA111111'), ('garden', 'KTN1111111'),\
                ('gardham', 'KTM1111111'), ('gardiner', 'KTNA111111'),\
                ('gardner', 'KTNA111111'), ('gardyne', 'KTN1111111'),\
                ('gare', 'KA11111111'), ('garforth', 'KFT1111111'),\
                ('garham', 'KM11111111'), ('garland', 'KLNT111111'),\
                ('garlyutt', 'KLT1111111'), ('garnctt', 'KNKT111111'),\
                ('garner', 'KNA1111111'), ('garnett', 'KNT1111111'),\
                ('garohow', 'KRA1111111'), ('garr', 'KA11111111'),\
                ('garret', 'KRT1111111'), ('garrett', 'KRT1111111'),\
                ('garrich', 'KRK1111111'), ('garrick', 'KRK1111111'),\
                ('garrigan', 'KRKN111111'), ('garron', 'KRN1111111'),\
                ('garrow', 'KRA1111111'), ('garside', 'KST1111111'),\
                ('garstang', 'KSTNK11111'), ('garty', 'KTA1111111'),\
                ('garvey', 'KFA1111111'), ('gascoigne', 'KSKKN11111'),\
                ('gasey', 'KSA1111111'), ('gaspar', 'KSPA111111'),\
                ('gaston', 'KSTN111111'), ('gatehouse', 'KTS1111111'),\
                ('gatfield', 'KTFT111111'), ('gatside', 'KTST111111'),\
                ('gatton', 'KTN1111111'), ('gaudin', 'KTN1111111'),\
                ('gaul', 'KA11111111'), ('gauld', 'KT11111111'),\
                ('gault', 'KT11111111'), ('gavan', 'KFN1111111'),\
                ('gavegan', 'KFKN111111'), ('gavigan', 'KFKN111111'),\
                ('gavin', 'KFN1111111'), ('gaw', 'KA11111111'),\
                ('gawn', 'KN11111111'), ('gawne', 'KN11111111'),\
                ('gay', 'KA11111111'), ('gaylor', 'KLA1111111'),\
                ('gaytan', 'KTN1111111'), ('geaney', 'KNA1111111'),\
                ('gear', 'KA11111111'), ('gearing', 'KRNK111111'),\
                ('geary', 'KRA1111111'), ('geddes', 'KTS1111111'),\
                ('geddis', 'KTS1111111'), ('gedney', 'KTNA111111'),\
                ('gee', 'KA11111111'), ('geen', 'KN11111111'),\
                ('geering', 'KRNK111111'), ('geeson', 'KSN1111111'),\
                ('geeves', 'KFS1111111'), ('geiger', 'KKA1111111'),\
                ('geleatly', 'KLTLA11111'), ('gellatly', 'KLTLA11111'),\
                ('gemmell', 'KMA1111111'), ('gene', 'KN11111111'),\
                ('genge', 'KNK1111111'), ('gensik', 'KNSK111111'),\
                ('gent', 'KNT1111111'), ('gentleman', 'KNTLMN1111'),\
                ('geoffrey', 'KFRA111111'), ('george', 'KK11111111'),\
                ('georgeison', 'KKSN111111'), ('georgeson', 'KKSN111111'),\
                ('gerard', 'KRT1111111'), ('gerken', 'KKN1111111'),\
                ('gerrard', 'KRT1111111'), ('gerrie', 'KRA1111111'),\
                ('gether', 'KTA1111111'), ('getken', 'KTKN111111'),\
                ('gevin', 'KFN1111111'), ('gey', 'KA11111111'),\
                ('ghadwick', 'TWK1111111'), ('gibb', 'KP11111111'),\
                ('gibbons', 'KPNS111111'), ('gibbs', 'KPS1111111'),\
                ('gibson', 'KPSN111111'), ('gifford', 'KFT1111111'),\
                ('giford-browne', 'KFTPRN1111'), ('gil1', 'KA11111111'),\
                ('gilan', 'KLN1111111'), ('gilbert', 'KPT1111111'),\
                ('gilbride', 'KPRT111111'), ('gilchrist', 'KKRST11111'),\
                ('gilder', 'KTA1111111'), ('giles', 'KLS1111111'),\
                ('gilfedder', 'KFTA111111'), ('gilfillan', 'KFLN111111'),\
                ('gilkison', 'KKSN111111'), ('gilks', 'KKS1111111'),\
                ('gill', 'KA11111111'), ('gillam', 'KLM1111111'),\
                ('gillan', 'KLN1111111'), ('gillanders', 'KLNTS11111'),\
                ('gillard', 'KLT1111111'), ('gillender', 'KLNTA11111'),\
                ('giller', 'KLA1111111'), ('gillers', 'KLS1111111'),\
                ('gillespie', 'KLSPA11111'), ('gillett', 'KLT1111111'),\
                ('gilliand', 'KLNT111111'), ('gillick', 'KLK1111111'),\
                ('gillies', 'KLS1111111'), ('gilligan', 'KLKN111111'),\
                ('gillions', 'KLNS111111'), ('gillispie', 'KLSPA11111'),\
                ('gillon', 'KLN1111111'), ('gillooly', 'KLLA111111'),\
                ('gilmolr', 'KMLA111111'), ('gilmore', 'KMA1111111'),\
                ('gilmour', 'KMA1111111'), ('girdler', 'KTLA111111'),\
                ('girdwood', 'KTWT111111'), ('girvan', 'KFN1111111'),\
                ('gittos', 'KTS1111111'), ('gjersen', 'KSN1111111'),\
                ('gladding', 'KLTNK11111'), ('gladstone', 'KLTSTN1111'),\
                ('gladwin', 'KLTWN11111'), ('gladwish', 'KLTWS11111'),\
                ('gladwith', 'KLTWT11111'), ('glaister', 'KLSTA11111'),\
                ('glanvill', 'KLNFA11111'), ('glasgow', 'KLSKA11111'),\
                ('glass', 'KLS1111111'), ('glasse', 'KLS1111111'),\
                ('glassett', 'KLST111111'), ('glasson', 'KLSN111111'),\
                ('glau', 'KLA1111111'), ('glault', 'KLT1111111'),\
                ('gledinning', 'KLTNNK1111'), ('glen', 'KLN1111111'),\
                ('glendining', 'KLNTNNK111'), ('glendinnin', 'KLNTNN1111'),\
                ('glendinning', 'KLNTNNK111'), ('glengarry', 'KLNKRA1111'),\
                ('glenn', 'KLN1111111'), ('glennie', 'KLNA111111'),\
                ('glennon', 'KLNN111111'), ('glerrie', 'KLRA111111'),\
                ('glibb', 'KLP1111111'), ('gliddon', 'KLTN111111'),\
                ('glisby', 'KLSPA11111'), ('gllespte', 'KLSPT11111'),\
                ('gloag', 'KLK1111111'), ('glossop', 'KLSP111111'),\
                ('glover', 'KLFA111111'), ('glozier', 'KLSA111111'),\
                ('glroves', 'KRFS111111'), ('glubbins', 'KLPNS11111'),\
                ('glue', 'KLA1111111'), ('glynn', 'KLN1111111'),\
                ('goatham', 'KTM1111111'), ('gobbitt', 'KPT1111111'),\
                ('goble', 'KPA1111111'), ('godber', 'KTPA111111'),\
                ('godby', 'KTPA111111'), ('goddard', 'KTT1111111'),\
                ('godden', 'KTN1111111'), ('godfred', 'KTFRT11111'),\
                ('godfrey', 'KTFRA11111'), ('goding', 'KTNK111111'),\
                ('godirey', 'KTRA111111'), ('godso', 'KTSA111111'),\
                ('godward', 'KTWT111111'), ('godwin', 'KTWN111111'),\
                ('golden', 'KTN1111111'), ('goldie', 'KTA1111111'),\
                ('golding', 'KTNK111111'), ('goldsmid', 'KTSMT11111'),\
                ('goldsmith', 'KTSMT11111'), ('goldstein', 'KTSTN11111'),\
                ('golightly', 'KLTLA11111'), ('gollan', 'KLN1111111'),\
                ('gollar', 'KLA1111111'), ('gomersall', 'KMSA111111'),\
                ('gomm', 'KM11111111'), ('gong', 'KNK1111111'),\
                ('goninon', 'KNNN111111'), ('gooch', 'KK11111111'),\
                ('good', 'KT11111111'), ('goodall', 'KTA1111111'),\
                ('goode', 'KT11111111'), ('goodeve', 'KTF1111111'),\
                ('goodey', 'KTA1111111'), ('goodfellow', 'KTFLA11111'),\
                ('goodhall', 'KTA1111111'), ('goodison', 'KTSN111111'),\
                ('goodlet', 'KTLT111111'), ('goodlot', 'KTLT111111'),\
                ('goodman', 'KTMN111111'), ('goodmanson', 'KTMNSN1111'),\
                ('goodridge', 'KTRK111111'), ('goodsir', 'KTSA111111'),\
                ('goodwin', 'KTWN111111'), ('goodyer', 'KTA1111111'),\
                ('gooseman', 'KSMN111111'), ('gordin', 'KTN1111111'),\
                ('gordon', 'KTN1111111'), ('gore-johnston', 'KRNSTN1111'),\
                ('gore', 'KA11111111'), ('gorge', 'KK11111111'),\
                ('gorgeson', 'KKSN111111'), ('gorham', 'KM11111111'),\
                ('gormack', 'KMK1111111'), ('gorman', 'KMN1111111'),\
                ('gormly', 'KMLA111111'), ('gorton', 'KTN1111111'),\
                ('gosham', 'KSM1111111'), ('gosling', 'KSLNK11111'),\
                ('gosney', 'KSNA111111'), ('goudie', 'KTA1111111'),\
                ('gough', 'KA11111111'), ('gould', 'KT11111111'),\
                ('goulston', 'KSTN111111'), ('goulstone', 'KSTN111111'),\
                ('gourlay', 'KLA1111111'), ('gourley', 'KLA1111111'),\
                ('gourlie', 'KLA1111111'), ('govan', 'KFN1111111'),\
                ('gover', 'KFA1111111'), ('gow', 'KA11111111'),\
                ('gowans', 'KWNS111111'), ('gowdy', 'KTA1111111'),\
                ('gowie', 'KWA1111111'), ('goy', 'KA11111111'),\
                ('goyen', 'KN11111111'), ('grace', 'KRK1111111'),\
                ('gracie', 'KRSA111111'), ('grady', 'KRTA111111'),\
                ('graf', 'KRF1111111'), ('graham', 'KRM1111111'),\
                ('grahame', 'KRM1111111'), ('grahan', 'KRN1111111'),\
                ('grahm', 'KRM1111111'), ('graig', 'KRK1111111'),\
                ('grainger', 'KRNKA11111'), ('grainm', 'KRNM111111'),\
                ('grallam', 'KRLM111111'), ('grame', 'KRM1111111'),\
                ('grammer', 'KRMA111111'), ('grandison', 'KRNTSN1111'),\
                ('grant', 'KRNT111111'), ('grantham', 'KRNTM11111'),\
                ('grass', 'KRS1111111'), ('gratton', 'KRTN111111'),\
                ('gratwick', 'KRTWK11111'), ('grave', 'KRF1111111'),\
                ('graves', 'KRFS111111'), ('grawford', 'KRFT111111'),\
                ('gray', 'KRA1111111'), ('graye', 'KRA1111111'),\
                ('grealish', 'KRLS111111'), ('greaney', 'KRNA111111'),\
                ('greatrex', 'KRTRK11111'), ('greaves', 'KRFS111111'),\
                ('green', 'KRN1111111'), ('greenall', 'KRNA111111'),\
                ('greene', 'KRN1111111'), ('greenfield', 'KRNFT11111'),\
                ('greenhalgh', 'KRNA111111'), ('greenhough', 'KRNA111111'),\
                ('greenish', 'KRNS111111'), ('greenland', 'KRNLNT1111'),\
                ('greenslade', 'KRNSLT1111'), ('greensmith', 'KRNSMT1111'),\
                ('greenway', 'KRNWA11111'), ('greenwood-wilson', 'KRNWTWSN11'),\
                ('greenwood', 'KRNWT11111'), ('greenyer', 'KRNA111111'),\
                ('greer', 'KRA1111111'), ('greeves', 'KRFS111111'),\
                ('gregan', 'KRKN111111'), ('gregg', 'KRK1111111'),\
                ('gregory', 'KRKRA11111'), ('greig', 'KRK1111111'),\
                ('greigory', 'KRKRA11111'), ('grenfell', 'KRNFA11111'),\
                ('gresham', 'KRSM111111'), ('greves', 'KRFS111111'),\
                ('grey', 'KRA1111111'), ('gribben', 'KRPN111111'),\
                ('grice', 'KRK1111111'), ('gridgeman', 'KRKMN11111'),\
                ('grierson', 'KRSN111111'), ('grieve', 'KRF1111111'),\
                ('griffen', 'KRFN111111'), ('griffin', 'KRFN111111'),\
                ('griffith', 'KRFT111111'), ('griffiths', 'KRFTS11111'),\
                ('griffths', 'KRFTS11111'), ('griflin', 'KRFLN11111'),\
                ('grig', 'KRK1111111'), ('grigg', 'KRK1111111'),\
                ('grigsby', 'KRKSPA1111'), ('grimaldi', 'KRMTA11111'),\
                ('grimman', 'KRMN111111'), ('grimmest', 'KRMST11111'),\
                ('grimmett', 'KRMT111111'), ('grimsdale', 'KRMSTA1111'),\
                ('grimsey', 'KRMSA11111'), ('grimshaw', 'KRMSA11111'),\
                ('grimwood', 'KRMWT11111'), ('grin', 'KRN1111111'),\
                ('grindlay', 'KRNTLA1111'), ('grindley', 'KRNTLA1111'),\
                ('grinyer', 'KRNA111111'), ('grocott', 'KRKT111111'),\
                ('grogan', 'KRKN111111'), ('groom', 'KRM1111111'),\
                ('grose', 'KRS1111111'), ('grosse', 'KRS1111111'),\
                ('grounds', 'KRNTS11111'), ('grover', 'KRFA111111'),\
                ('groves', 'KRFS111111'), ('growden', 'KRTN111111'),\
                ('grubb', 'KRP1111111'), ('grubh', 'KRP1111111'),\
                ('gruitt', 'KRT1111111'), ('grundy', 'KRNTA11111'),\
                ('gruszning', 'KRSNNK1111'), ('grut', 'KRT1111111'),\
                ('gubbins', 'KPNS111111'), ('guest', 'KST1111111'),\
                ('guffie', 'KFA1111111'), ('guild', 'KT11111111'),\
                ('guildford', 'KTFT111111'), ('guilen', 'KLN1111111'),\
                ('guilford', 'KFT1111111'), ('guillmot', 'KMT1111111'),\
                ('guinan', 'KNN1111111'), ('guinness', 'KNS1111111'),\
                ('gulbins', 'KPNS111111'), ('gullan', 'KLN1111111'),\
                ('gulland', 'KLNT111111'), ('gullen', 'KLN1111111'),\
                ('gum', 'KM11111111'), ('gummer', 'KMA1111111'),\
                ('gumpatzes', 'KMPTSS1111'), ('gunion', 'KNN1111111'),\
                ('gunn', 'KN11111111'), ('gunner', 'KNA1111111'),\
                ('gunning', 'KNNK111111'), ('gunton', 'KNTN111111'),\
                ('gurming', 'KMNK111111'), ('gurr', 'KA11111111'),\
                ('gustafson', 'KSTFSN1111'), ('guthrie', 'KTRA111111'),\
                ('gutschlag', 'KTSKLK1111'), ('gutsell', 'KTSA111111'),\
                ('guy', 'KA11111111'), ('guyton', 'KTN1111111'),\
                ('gve', 'KF11111111'), ('gwilliams', 'KWLMS11111'),\
                ('gwyn', 'KWN1111111'), ('gwynne', 'KWN1111111'),\
                ('gye', 'KA11111111'), ('haake', 'AK11111111'),\
                ('haberfield', 'APFT111111'), ('habershon', 'APSN111111'),\
                ('hack', 'AK11111111'), ('hackett', 'AKT1111111'),\
                ('haddon', 'ATN1111111'), ('haddrell', 'ATRA111111'),\
                ('hade', 'AT11111111'), ('hadfield', 'ATFT111111'),\
                ('hadlee', 'ATLA111111'), ('hadlow', 'ATLA111111'),\
                ('haffenden', 'AFNTN11111'), ('hagan', 'AKN1111111'),\
                ('hagarty', 'AKTA111111'), ('hagen', 'AKN1111111'),\
                ('haggart', 'AKT1111111'), ('haggett', 'AKT1111111'),\
                ('haggitt', 'AKT1111111'), ('hague', 'AKA1111111'),\
                ('haig', 'AK11111111'), ('haigh', 'AA11111111'),\
                ('hailes', 'ALS1111111'), ('hailton', 'ATN1111111'),\
                ('haines', 'ANS1111111'), ('hair', 'AA11111111'),\
                ('hakely', 'AKLA111111'), ('hal', 'AA11111111'),\
                ('halberg', 'APK1111111'), ('halcrow', 'AKRA111111'),\
                ('haldane', 'ATN1111111'), ('hale', 'AA11111111'),\
                ('hales', 'ALS1111111'), ('halfka', 'AFKA111111'),\
                ('halford', 'AFT1111111'), ('halies', 'ALS1111111'),\
                ('halket', 'AKT1111111'), ('halkett', 'AKT1111111'),\
                ('hall', 'AA11111111'), ('hallam', 'ALM1111111'),\
                ('hallas', 'ALS1111111'), ('hallet', 'ALT1111111'),\
                ('hallett', 'ALT1111111'), ('halley', 'ALA1111111'),\
                ('halliday', 'ALTA111111'), ('halligan', 'ALKN111111'),\
                ('hallinan', 'ALNN111111'), ('hallsen', 'ASN1111111'),\
                ('hally', 'ALA1111111'), ('halpin', 'APN1111111'),\
                ('halsinger', 'ASNKA11111'), ('haly', 'ALA1111111'),\
                ('ham', 'AM11111111'), ('hamann', 'AMN1111111'),\
                ('hambleton', 'AMPLTN1111'), ('hamblett', 'AMPLT11111'),\
                ('hamblin', 'AMPLN11111'), ('hambly', 'AMPLA11111'),\
                ('hamer', 'AMA1111111'), ('hames', 'AMS1111111'),\
                ('hamiiton', 'AMTN111111'), ('hamill', 'AMA1111111'),\
                ('hamilton', 'AMTN111111'), ('hamlyn', 'AMLN111111'),\
                ('hammer', 'AMA1111111'), ('hammerly', 'AMLA111111'),\
                ('hammill', 'AMA1111111'), ('hammond', 'AMNT111111'),\
                ('hamon', 'AMN1111111'), ('hanan', 'ANN1111111'),\
                ('hananeia', 'ANNA111111'), ('hancock', 'ANKK111111'),\
                ('hancox', 'ANKK111111'), ('hand', 'ANT1111111'),\
                ('handforth', 'ANTFT11111'), ('handisides', 'ANTSTS1111'),\
                ('handley', 'ANTLA11111'), ('hands', 'ANTS111111'),\
                ('handscomb', 'ANTSKM1111'), ('handyside', 'ANTST11111'),\
                ('hanenina', 'ANNNA11111'), ('hanger', 'ANKA111111'),\
                ('hanham', 'ANM1111111'), ('hankey', 'ANKA111111'),\
                ('hankins', 'ANKNS11111'), ('hanley', 'ANLA111111'),\
                ('hanlin', 'ANLN111111'), ('hanlon', 'ANLN111111'),\
                ('hanly', 'ANLA111111'), ('hanna', 'ANA1111111'),\
                ('hannagan', 'ANKN111111'), ('hannah', 'ANA1111111'),\
                ('hannan', 'ANN1111111'), ('hannigan', 'ANKN111111'),\
                ('hanning', 'ANNK111111'), ('hannon', 'ANN1111111'),\
                ('hanon', 'ANN1111111'), ('hanrahan', 'ANRN111111'),\
                ('hansbury', 'ANSPRA1111'), ('hansen', 'ANSN111111'),\
                ('hansford', 'ANSFT11111'), ('hansforrl', 'ANSFA11111'),\
                ('hanson', 'ANSN111111'), ('hansson', 'ANSN111111'),\
                ('hanton', 'ANTN111111'), ('hanvey', 'ANFA111111'),\
                ('haran', 'ARN1111111'), ('harborne', 'APN1111111'),\
                ('harborow', 'APRA111111'), ('harbott', 'APT1111111'),\
                ('harbrow', 'APRA111111'), ('hardcastle', 'ATKSTA1111'),\
                ('harden', 'ATN1111111'), ('hardey', 'ATA1111111'),\
                ('hardie', 'ATA1111111'), ('harding', 'ATNK111111'),\
                ('hardman', 'ATMN111111'), ('hardoy', 'ATA1111111'),\
                ('hards', 'ATS1111111'), ('hardwick', 'ATWK111111'),\
                ('hardy', 'ATA1111111'), ('hare', 'AA11111111'),\
                ('harford', 'AFT1111111'), ('hargood', 'AKT1111111'),\
                ('hargrave', 'AKRF111111'), ('hargraves', 'AKRFS11111'),\
                ('hargreave', 'AKRF111111'), ('hargreaves', 'AKRFS11111'),\
                ('harker', 'AKA1111111'), ('harkess', 'AKS1111111'),\
                ('harkness', 'AKNS111111'), ('harl', 'AA11111111'),\
                ('harland', 'ALNT111111'), ('harle', 'AA11111111'),\
                ('harley', 'ALA1111111'), ('harliwich', 'ALWK111111'),\
                ('harlow', 'ALA1111111'), ('harman', 'AMN1111111'),\
                ('harneiss', 'ANS1111111'), ('harness', 'ANS1111111'),\
                ('harney', 'ANA1111111'), ('harold', 'ART1111111'),\
                ('harper', 'APA1111111'), ('harrah', 'ARA1111111'),\
                ('harrap', 'ARP1111111'), ('harraway', 'ARWA111111'),\
                ('harre', 'AA11111111'), ('harrhy', 'AA11111111'),\
                ('harridge', 'ARK1111111'), ('harries', 'ARS1111111'),\
                ('harrington', 'ARNKTN1111'), ('harris', 'ARS1111111'),\
                ('harrison', 'ARSN111111'), ('harrisorl', 'ARSA111111'),\
                ('harrod', 'ART1111111'), ('harrold', 'ART1111111'),\
                ('harrop', 'ARP1111111'), ('harrould', 'ART1111111'),\
                ('harrow', 'ARA1111111'), ('harry', 'ARA1111111'),\
                ('hart', 'AT11111111'), ('hartaway', 'ATWA111111'),\
                ('hartle', 'ATA1111111'), ('hartley', 'ATLA111111'),\
                ('hartman', 'ATMN111111'), ('hartmann', 'ATMN111111'),\
                ('hartstonge', 'ATSTNK1111'), ('harty', 'ATA1111111'),\
                ('harvey', 'AFA1111111'), ('harvie', 'AFA1111111'),\
                ('harwood', 'AWT1111111'), ('haselden', 'ASTN111111'),\
                ('haskell', 'ASKA111111'), ('haskins', 'ASKNS11111'),\
                ('haskoll', 'ASKA111111'), ('haslett', 'ASLT111111'),\
                ('hason', 'ASN1111111'), ('hassall', 'ASA1111111'),\
                ('hassan', 'ASN1111111'), ('hast', 'AST1111111'),\
                ('hastie', 'ASTA111111'), ('hastings', 'ASTNKS1111'),\
                ('hastngs', 'ASTNKS1111'), ('hatcher', 'AKA1111111'),\
                ('hately', 'ATLA111111'), ('hathaway', 'ATWA111111'),\
                ('hatt', 'AT11111111'), ('hatten', 'ATN1111111'),\
                ('hatton', 'ATN1111111'), ('haub', 'AP11111111'),\
                ('haugh', 'AA11111111'), ('haughton', 'ATN1111111'),\
                ('haurahan', 'ARN1111111'), ('haush', 'AS11111111'),\
                ('havard', 'AFT1111111'), ('havelock', 'AFLK111111'),\
                ('havill', 'AFA1111111'), ('havward', 'AFWT111111'),\
                ('hawes', 'AWS1111111'), ('hawke', 'AK11111111'),\
                ('hawken', 'AKN1111111'), ('hawker', 'AKA1111111'),\
                ('hawkes', 'AKS1111111'), ('hawkhead', 'AKT1111111'),\
                ('hawkine', 'AKN1111111'), ('hawkins', 'AKNS111111'),\
                ('hawkley', 'AKLA111111'), ('hawley', 'ALA1111111'),\
                ('haworth', 'AWT1111111'), ('hawthorn', 'ATN1111111'),\
                ('haxlett', 'AKLT111111'), ('hay', 'AA11111111'),\
                ('haybittle', 'APTA111111'), ('hayden', 'ATN1111111'),\
                ('haydock', 'ATK1111111'), ('haydon', 'ATN1111111'),\
                ('haye', 'AA11111111'), ('hayes', 'AS11111111'),\
                ('hayman', 'AMN1111111'), ('haymes', 'AMS1111111'),\
                ('hayne', 'AN11111111'), ('haynes', 'ANS1111111'),\
                ('hayr', 'AA11111111'), ('hayward', 'AWT1111111'),\
                ('hazard', 'AST1111111'), ('hazelwood', 'ASWT111111'),\
                ('hazlett', 'ASLT111111'), ('head', 'AT11111111'),\
                ('heads', 'ATS1111111'), ('heal', 'AA11111111'),\
                ('heald', 'AT11111111'), ('healer', 'ALA1111111'),\
                ('healey', 'ALA1111111'), ('healy', 'ALA1111111'),\
                ('heaney', 'ANA1111111'), ('heaps', 'APS1111111'),\
                ('heard', 'AT11111111'), ('hearile', 'ARA1111111'),\
                ('hearne', 'AN11111111'), ('hearty', 'ATA1111111'),\
                ('heasley', 'ASLA111111'), ('heasman', 'ASMN111111'),\
                ('heath', 'AT11111111'), ('heathcote', 'ATKT111111'),\
                ('heather', 'ATA1111111'), ('heathman', 'ATMN111111'),\
                ('heatley', 'ATLA111111'), ('heaton', 'ATN1111111'),\
                ('heaven', 'AFN1111111'), ('heaxlewood', 'AKLWT11111'),\
                ('heazelwood', 'ASWT111111'), ('heazlewood', 'ASLWT11111'),\
                ('hebbard', 'APT1111111'), ('hebditch', 'APTK111111'),\
                ('hector', 'AKTA111111'), ('hedges', 'AKS1111111'),\
                ('hedgman', 'AKMN111111'), ('hedlges', 'ATKS111111'),\
                ('hedrick', 'ATRK111111'), ('heenan', 'ANN1111111'),\
                ('heffernan', 'AFNN111111'), ('heft', 'AFT1111111'),\
                ('hegarty', 'AKTA111111'), ('heggerty', 'AKTA111111'),\
                ('heggie', 'AKA1111111'), ('heileson', 'ALSN111111'),\
                ('helder', 'ATA1111111'), ('helean', 'ALN1111111'),\
                ('helier', 'ALA1111111'), ('hellawell', 'ALWA111111'),\
                ('heller', 'ALA1111111'), ('helleyer', 'ALA1111111'),\
                ('hellier', 'ALA1111111'), ('hellriegel', 'ARKA111111'),\
                ('hellyer', 'ALA1111111'), ('helm', 'AM11111111'),\
                ('helmore', 'AMA1111111'), ('helms', 'AMS1111111'),\
                ('helson', 'ASN1111111'), ('hely', 'ALA1111111'),\
                ('hemingway', 'AMNKWA1111'), ('hemsley', 'AMSLA11111'),\
                ('henaghan', 'ANKN111111'), ('hende', 'ANT1111111'),\
                ('hendebourck', 'ANTPK11111'), ('henden', 'ANTN111111'),\
                ('henderson', 'ANTSN11111'), ('hendetson', 'ANTTSN1111'),\
                ('hendley', 'ANTLA11111'), ('hendren', 'ANTRN11111'),\
                ('hendrick', 'ANTRK11111'), ('hendry', 'ANTRA11111'),\
                ('hendy', 'ANTA111111'), ('heneghan', 'ANKN111111'),\
                ('henery', 'ANRA111111'), ('heney', 'ANA1111111'),\
                ('henke', 'ANK1111111'), ('henks', 'ANKS111111'),\
                ('henley', 'ANLA111111'), ('hennessey', 'ANSA111111'),\
                ('hennessy', 'ANSA111111'), ('hennig', 'ANK1111111'),\
                ('henning', 'ANNK111111'), ('henry', 'ANRA111111'),\
                ('hensleigh', 'ANSLA11111'), ('hensley', 'ANSLA11111'),\
                ('henton', 'ANTN111111'), ('henty', 'ANTA111111'),\
                ('henwood', 'ANWT111111'), ('hepburn', 'APN1111111'),\
                ('heppelthwa', 'APTWA11111'), ('heppelthwaite', 'APTWT11111'),\
                ('herbert', 'APT1111111'), ('herbison', 'APSN111111'),\
                ('herd', 'AT11111111'), ('herman', 'AMN1111111'),\
                ('hern', 'AN11111111'), ('heron', 'ARN1111111'),\
                ('herrich', 'ARK1111111'), ('herrick', 'ARK1111111'),\
                ('herring', 'ARNK111111'), ('herriot', 'ART1111111'),\
                ('hertz', 'ATS1111111'), ('hervey', 'AFA1111111'),\
                ('heselwood', 'ASWT111111'), ('hesford', 'ASFT111111'),\
                ('heslington', 'ASLNKTN111'), ('heslip', 'ASLP111111'),\
                ('heslop', 'ASLP111111'), ('hessell', 'ASA1111111'),\
                ('hessey', 'ASA1111111'), ('hessian', 'ASN1111111'),\
                ('hestinger', 'ASTNKA1111'), ('hethering', 'ATRNK11111'),\
                ('hetherington', 'ATRNKTN111'), ('hett', 'AT11111111'),\
                ('heward', 'AWT1111111'), ('hewat', 'AWT1111111'),\
                ('hewett', 'AWT1111111'), ('hewitson', 'AWTSN11111'),\
                ('hewitt', 'AWT1111111'), ('hewlett', 'ALT1111111'),\
                ('hewton', 'ATN1111111'), ('hey', 'AA11111111'),\
                ('heydon', 'ATN1111111'), ('heyward', 'AWT1111111'),\
                ('hickey', 'AKA1111111'), ('hickinbot', 'AKNPT11111'),\
                ('hickinbotham', 'AKNPTM1111'), ('hickman', 'AKMN111111'),\
                ('hicks', 'AKS1111111'), ('hickson', 'AKSN111111'),\
                ('hiddle', 'ATA1111111'), ('higgie', 'AKA1111111'),\
                ('higgins', 'AKNS111111'), ('higginson', 'AKNSN11111'),\
                ('higgs', 'AKS1111111'), ('higham', 'AKM1111111'),\
                ('highet', 'AKT1111111'), ('highley', 'ALA1111111'),\
                ('highs', 'AS11111111'), ('higman', 'AKMN111111'),\
                ('hiil', 'AA11111111'), ('hill', 'AA11111111'),\
                ('hillary', 'ALRA111111'), ('hilliar', 'ALA1111111'),\
                ('hilliard', 'ALT1111111'), ('hillier', 'ALA1111111'),\
                ('hilliker', 'ALKA111111'), ('hillis', 'ALS1111111'),\
                ('hilllker', 'AKA1111111'), ('hilslop', 'ASLP111111'),\
                ('hilton', 'ATN1111111'), ('himburg', 'AMPK111111'),\
                ('himmel', 'AMA1111111'), ('hinchcliff', 'ANKKLF1111'),\
                ('hinchcliffe', 'ANKKLF1111'), ('hincheliff', 'ANKLF11111'),\
                ('hincks', 'ANKS111111'), ('hind', 'ANT1111111'),\
                ('hinde', 'ANT1111111'), ('hindes', 'ANTS111111'),\
                ('hindle', 'ANTA111111'), ('hindmarsh', 'ANTMS11111'),\
                ('hinds', 'ANTS111111'), ('hines', 'ANS1111111'),\
                ('hinex', 'ANK1111111'), ('hingley', 'ANKLA11111'),\
                ('hinkley', 'ANKLA11111'), ('hinton', 'ANTN111111'),\
                ('hiorns', 'ANS1111111'), ('hirt', 'AT11111111'),\
                ('hiscock', 'ASKK111111'), ('hiscoke', 'ASKK111111'),\
                ('hisgrove', 'ASKRF11111'), ('hislol', 'ASLA111111'),\
                ('hislop', 'ASLP111111'), ('hisshion', 'ASN1111111'),\
                ('hitchcock', 'AKKK111111'), ('hitchcox', 'AKKK111111'),\
                ('hitchell', 'AKA1111111'), ('hitchon', 'AKN1111111'),\
                ('hits', 'ATS1111111'), ('hitt', 'AT11111111'),\
                ('hoad', 'AT11111111'), ('hoar', 'AA11111111'),\
                ('hoare', 'AA11111111'), ('hoatten', 'ATN1111111'),\
                ('hobbs', 'APS1111111'), ('hobby', 'APA1111111'),\
                ('hobcraft', 'APKRFT1111'), ('hobcroft', 'APKRFT1111'),\
                ('hobday', 'APTA111111'), ('hobsoil', 'APSA111111'),\
                ('hobson', 'APSN111111'), ('hocking', 'AKNK111111'),\
                ('hodgaon', 'AKN1111111'), ('hodge', 'AK11111111'),\
                ('hodges', 'AKS1111111'), ('hodgetts', 'AKTS111111'),\
                ('hodgins', 'AKNS111111'), ('hodgkins', 'AKNS111111'),\
                ('hodgkinson', 'AKNSN11111'), ('hodgsin', 'AKSN111111'),\
                ('hodgson', 'AKSN111111'), ('hodkins', 'ATKNS11111'),\
                ('hodson', 'ATSN111111'), ('hoeking', 'AKNK111111'),\
                ('hoff', 'AF11111111'), ('hoffman', 'AFMN111111'),\
                ('hoffmann', 'AFMN111111'), ('hoffmeister', 'AFMSTA1111'),\
                ('hofland', 'AFLNT11111'), ('hog', 'AK11111111'),\
                ('hogan', 'AKN1111111'), ('hogarth', 'AKT1111111'),\
                ('hogg', 'AK11111111'), ('hogue', 'AKA1111111'),\
                ('hoirns', 'ANS1111111'), ('holander', 'ALNTA11111'),\
                ('holben', 'APN1111111'), ('holdaway', 'ATWA111111'),\
                ('holden', 'ATN1111111'), ('holder', 'ATA1111111'),\
                ('holderness', 'ATNS111111'), ('holdgate', 'AKT1111111'),\
                ('holdsworth', 'ATSWT11111'), ('holgate', 'AKT1111111'),\
                ('holiand', 'ALNT111111'), ('hollamby', 'ALMPA11111'),\
                ('holland', 'ALNT111111'), ('hollander', 'ALNTA11111'),\
                ('hollands', 'ALNTS11111'), ('hollebon', 'ALPN111111'),\
                ('holley', 'ALA1111111'), ('hollick', 'ALK1111111'),\
                ('hollingshead', 'ALNKST1111'), ('hollingworth', 'ALNKWT1111'),\
                ('hollner', 'ANA1111111'), ('hollow', 'ALA1111111'),\
                ('holloway', 'ALWA111111'), ('hollows', 'ALS1111111'),\
                ('holman', 'AMN1111111'), ('holmes-libbis', 'AMSLPS1111'),\
                ('holmes', 'AMS1111111'), ('holmess', 'AMS1111111'),\
                ('holroyd', 'ART1111111'), ('holst', 'AST1111111'),\
                ('holsted', 'ASTT111111'), ('holsten', 'ASTN111111'),\
                ('holt', 'AT11111111'), ('homan', 'AMN1111111'),\
                ('home', 'AM11111111'), ('homer', 'AMA1111111'),\
                ('homfray', 'AMFRA11111'), ('honer', 'ANA1111111'),\
                ('honeybone', 'ANPN111111'), ('honeywood', 'ANWT111111'),\
                ('honner', 'ANA1111111'), ('hoochoo', 'AKA1111111'),\
                ('hood', 'AT11111111'), ('hoogee', 'AKA1111111'),\
                ('hook', 'AK11111111'), ('hooker', 'AKA1111111'),\
                ('hoole', 'AA11111111'), ('hooley', 'ALA1111111'),\
                ('hooper', 'APA1111111'), ('hopcraft', 'APKRFT1111'),\
                ('hope', 'AP11111111'), ('hopewell', 'APWA111111'),\
                ('hopgood', 'APKT111111'), ('hopkins', 'APKNS11111'),\
                ('hopkinson', 'APKNSN1111'), ('hopkirk', 'APKK111111'),\
                ('hopper', 'APA1111111'), ('hopwood', 'APWT111111'),\
                ('horan', 'ARN1111111'), ('hordern', 'ATN1111111'),\
                ('hore', 'AA11111111'), ('hormann', 'AMN1111111'),\
                ('horn', 'AN11111111'), ('hornal', 'ANA1111111'),\
                ('hornby', 'ANPA111111'), ('horncastle', 'ANKSTA1111'),\
                ('horncy', 'ANSA111111'), ('horne', 'AN11111111'),\
                ('hornell', 'ANA1111111'), ('horner', 'ANA1111111'),\
                ('horniblow', 'ANPLA11111'), ('hornsby', 'ANSPA11111'),\
                ('horris', 'ARS1111111'), ('horrobin', 'ARPN111111'),\
                ('horsburg', 'ASPK111111'), ('horsburgh', 'ASPA111111'),\
                ('horsecroft', 'ASKRFT1111'), ('horsham', 'ASM1111111'),\
                ('horsman', 'ASMN111111'), ('hortle', 'ATA1111111'),\
                ('horton', 'ATN1111111'), ('horwood', 'AWT1111111'),\
                ('hosee', 'ASA1111111'), ('hoseit', 'AST1111111'),\
                ('hosie', 'ASA1111111'), ('hoskin', 'ASKN111111'),\
                ('hosking', 'ASKNK11111'), ('hoskins', 'ASKNS11111'),\
                ('hossack', 'ASK1111111'), ('hotop', 'ATP1111111'),\
                ('hotton', 'ATN1111111'), ('houghton', 'ATN1111111'),\
                ('houlahan', 'ALN1111111'), ('hould', 'AT11111111'),\
                ('houliston', 'ALSTN11111'), ('houlston', 'ASTN111111'),\
                ('houston', 'ASTN111111'), ('how', 'AA11111111'),\
                ('howard', 'AWT1111111'), ('howarth', 'AWT1111111'),\
                ('howat', 'AWT1111111'), ('howatson', 'AWTSN11111'),\
                ('howden', 'ATN1111111'), ('howe', 'AA11111111'),\
                ('howejohns', 'AWNS111111'), ('howell', 'AWA1111111'),\
                ('howes', 'AWS1111111'), ('howie', 'AWA1111111'),\
                ('howison', 'AWSN111111'), ('howlett', 'ALT1111111'),\
                ('howley', 'ALA1111111'), ('howman', 'AMN1111111'),\
                ('howorth', 'AWT1111111'), ('howrth', 'AT11111111'),\
                ('hows', 'AS11111111'), ('hoy', 'AA11111111'),\
                ('hoyne', 'AN11111111'), ('huband', 'APNT111111'),\
                ('hubbard', 'APT1111111'), ('hubble', 'APA1111111'),\
                ('hucker', 'AKA1111111'), ('hucklebridge', 'AKLPRK1111'),\
                ('hudd', 'AT11111111'), ('huddleston', 'ATLSTN1111'),\
                ('huddlestone', 'ATLSTN1111'), ('hudson', 'ATSN111111'),\
                ('hugget', 'AKT1111111'), ('huggett', 'AKT1111111'),\
                ('huggins', 'AKNS111111'), ('hughan', 'AKN1111111'),\
                ('hughes', 'AKS1111111'), ('hughson', 'ASN1111111'),\
                ('hulands', 'ALNTS11111'), ('hulme', 'AM11111111'),\
                ('hume', 'AM11111111'), ('humphrey', 'AMFRA11111'),\
                ('humphreys', 'AMFRS11111'), ('humphries', 'AMFRS11111'),\
                ('hungerford', 'ANKFT11111'), ('hunker', 'ANKA111111'),\
                ('hunrter', 'ANTA111111'), ('hunt', 'ANT1111111'),\
                ('hunter', 'ANTA111111'), ('huntley', 'ANTLA11111'),\
                ('hurd', 'AT11111111'), ('hurdley', 'ATLA111111'),\
                ('hurley', 'ALA1111111'), ('hurlson', 'ASN1111111'),\
                ('hurndell', 'ANTA111111'), ('hurrell', 'ARA1111111'),\
                ('hurring', 'ARNK111111'), ('hurst', 'AST1111111'),\
                ('hurt', 'AT11111111'), ('husband', 'ASPNT11111'),\
                ('hussey', 'ASA1111111'), ('huston', 'ASTN111111'),\
                ('hutcheon', 'AKN1111111'), ('hutcheson', 'AKSN111111'),\
                ('hutchings', 'AKNKS11111'), ('hutchins', 'AKNS111111'),\
                ('hutchinson', 'AKNSN11111'), ('hutchison', 'AKSN111111'),\
                ('huts', 'ATS1111111'), ('hutt', 'AT11111111'),\
                ('hutton', 'ATN1111111'), ('huxtable', 'AKTPA11111'),\
                ('hvslop', 'AFSLP11111'), ('hyde harris', 'ATRS111111'),\
                ('hyde-harris', 'ATRS111111'), ('hyde', 'AT11111111'),\
                ('hyder', 'ATA1111111'), ('hydes', 'ATS1111111'),\
                ('hyland', 'ALNT111111'), ('hylnen', 'ANN1111111'),\
                ('hymen', 'AMN1111111'), ('hyndman', 'ANTMN11111'),\
                ('hynes', 'ANS1111111'), ('hynet', 'ANT1111111'),\
                ('hypes', 'APS1111111'), ('hyslop', 'ASLP111111'),\
                ('iaing', 'ANK1111111'), ('ibbetson', 'APTSN11111'),\
                ('ibbotson', 'APTSN11111'), ('idiens', 'ATNS111111'),\
                ('idour', 'ATA1111111'), ('iggo', 'AKA1111111'),\
                ('iles', 'ALS1111111'), ('illes', 'ALS1111111'),\
                ('illingworth', 'ALNKWT1111'), ('imrie', 'AMRA111111'),\
                ('ince', 'ANK1111111'), ('incrocci', 'ANKRKSA111'),\
                ('inder', 'ANTA111111'), ('ingle', 'ANKA111111'),\
                ('ingles', 'ANKLS11111'), ('inglis', 'ANKLS11111'),\
                ('ingram', 'ANKRM11111'), ('ings', 'ANKS111111'),\
                ('ingstolle', 'ANKSTA1111'), ('ingstone', 'ANKSTN1111'),\
                ('innes', 'ANS1111111'), ('innis', 'ANS1111111'),\
                ('inram', 'ANRM111111'), ('instone', 'ANSTN11111'),\
                ('inward', 'ANWT111111'), ('inwood', 'ANWT111111'),\
                ('iones', 'ANS1111111'), ('ireland', 'ARLNT11111'),\
                ('ironside', 'ARNST11111'), ('irvine', 'AFN1111111'),\
                ('irving', 'AFNK111111'), ('irwin', 'AWN1111111'),\
                ('isaac', 'ASK1111111'), ('isaacs', 'ASKS111111'),\
                ('isaae', 'ASA1111111'), ('isbister', 'ASPSTA1111'),\
                ('isdale', 'ASTA111111'), ('isitt', 'AST1111111'),\
                ('islip', 'ASLP111111'), ('israel', 'ASRA111111'),\
                ('isteed', 'ASTT111111'), ('ives', 'AFS1111111'),\
                ('ivimev', 'AFMF111111'), ('ivimey', 'AFMA111111'),\
                ('ivory', 'AFRA111111'), ('jaap', 'YP11111111'),\
                ('jack', 'YK11111111'), ('jackison', 'YKSN111111'),\
                ('jacksoh', 'YKSA111111'), ('jackson', 'YKSN111111'),\
                ('jackways', 'YKWS111111'), ('jacl', 'YKA1111111'),\
                ('jacob', 'YKP1111111'), ('jacobs', 'YKPS111111'),\
                ('jacobsen', 'YKPSN11111'), ('jacobson', 'YKPSN11111'),\
                ('jacques', 'YKS1111111'), ('jager', 'YKA1111111'),\
                ('jago', 'YKA1111111'), ('jaicobs', 'YKPS111111'),\
                ('james', 'YMS1111111'), ('jameson', 'YMSN111111'),\
                ('jamieson', 'YMSN111111'), ('jamison', 'YMSN111111'),\
                ('jane', 'YN11111111'), ('janowsky', 'YNSKA11111'),\
                ('jansen', 'YNSN111111'), ('janson', 'YNSN111111'),\
                ('jaokson', 'YKSN111111'), ('japp', 'YP11111111'),\
                ('jaquiery', 'YKRA111111'), ('jarden', 'YTN1111111'),\
                ('jardine', 'YTN1111111'), ('jarman', 'YMN1111111'),\
                ('jarnes', 'YNS1111111'), ('jarves', 'YFS1111111'),\
                ('jarvie', 'YFA1111111'), ('jarvis', 'YFS1111111'),\
                ('jeannings', 'YNNKS11111'), ('jeavons', 'YFNS111111'),\
                ('jefcoate', 'YFKT111111'), ('jefferson', 'YFSN111111'),\
                ('jeffery', 'YFRA111111'), ('jeffrey', 'YFRA111111'),\
                ('jeffreys', 'YFRS111111'), ('jeffries', 'YFRS111111'),\
                ('jeffs', 'YFS1111111'), ('jefierson', 'YFSN111111'),\
                ('jefterson', 'YFTSN11111'), ('jelley', 'YLA1111111'),\
                ('jells', 'YS11111111'), ('jelly', 'YLA1111111'),\
                ('jenkin', 'YNKN111111'), ('jenkins', 'YNKNS11111'),\
                ('jenks', 'YNKS111111'), ('jenner', 'YNA1111111'),\
                ('jennings', 'YNNKS11111'), ('jensen', 'YNSN111111'),\
                ('jenson', 'YNSN111111'), ('jenvey', 'YNFA111111'),\
                ('jephson', 'YFSN111111'), ('jepson', 'YPSN111111'),\
                ('jerkins', 'YKNS111111'), ('jesse', 'YS11111111'),\
                ('jessep', 'YSP1111111'), ('jewett', 'YWT1111111'),\
                ('jewiss', 'YWS1111111'), ('jlardey', 'ALTA111111'),\
                ('jobberns', 'YPNS111111'), ('jober', 'YPA1111111'),\
                ('joblin', 'YPLN111111'), ('joe', 'YA11111111'),\
                ('joel', 'YA11111111'), ('johansen', 'YNSN111111'),\
                ('johansson', 'YNSN111111'), ('johhston', 'YSTN111111'),\
                ('john', 'YN11111111'), ('johns', 'YNS1111111'),\
                ('johnsen', 'YNSN111111'), ('johnson', 'YNSN111111'),\
                ('johnston', 'YNSTN11111'), ('johnstone', 'YNSTN11111'),\
                ('jolly', 'YLA1111111'), ('jolmson', 'YMSN111111'),\
                ('joncs', 'YNKS111111'), ('jondon', 'YNTN111111'),\
                ('jones-neilson', 'YNSNSN1111'), ('jones', 'YNS1111111'),\
                ('jopp', 'YP11111111'), ('jopsen', 'YPSN111111'),\
                ('jopson', 'YPSN111111'), ('jordan', 'YTN1111111'),\
                ('jory', 'YRA1111111'), ('joseph', 'YSF1111111'),\
                ('josephson', 'YSFSN11111'), ('josland', 'YSLNT11111'),\
                ('joslin', 'YSLN111111'), ('joss', 'YS11111111'),\
                ('joues', 'YS11111111'), ('joughin', 'YKN1111111'),\
                ('jovce', 'YFK1111111'), ('jowey', 'YWA1111111'),\
                ('jowitt', 'YWT1111111'), ('jowsey', 'YSA1111111'),\
                ('jowsy', 'YSA1111111'), ('joyce', 'YK11111111'),\
                ('joyee', 'YA11111111'), ('joyner', 'YNA1111111'),\
                ('joynt', 'YNT1111111'), ('judd', 'YT11111111'),\
                ('judson', 'YTSN111111'), ('jukes', 'YKS1111111'),\
                ('julian', 'YLN1111111'), ('julie', 'YLA1111111'),\
                ('julin', 'YLN1111111'), ('julius', 'YLS1111111'),\
                ('jull', 'YA11111111'), ('junge', 'YNK1111111'),\
                ('jurdine', 'YTN1111111'), ('juries', 'YRS1111111'),\
                ('jury', 'YRA1111111'), ('justice', 'YSTK111111'),\
                ('justin', 'YSTN111111'), ('kahlenberg', 'KLNPK11111'),\
                ('kain', 'KN11111111'), ('kaler', 'KLA1111111'),\
                ('kane', 'KN11111111'), ('kania', 'KNA1111111'),\
                ('kannervischer', 'KNFSKA1111'),\
                ('kannewischer', 'KNWSKA1111'),\
                ('karney', 'KNA1111111'), ('kavanagh', 'KFNA111111'),\
                ('kay', 'KA11111111'), ('kaye', 'KA11111111'),\
                ('keach', 'KK11111111'), ('kean', 'KN11111111'),\
                ('keane', 'KN11111111'), ('kearney', 'KNA1111111'),\
                ('kearns', 'KNS1111111'), ('kearsley', 'KSLA111111'),\
                ('keast', 'KST1111111'), ('keates', 'KTS1111111'),\
                ('keating', 'KTNK111111'), ('kebblewhite', 'KPLWT11111'),\
                ('kedzlie', 'KTSLA11111'), ('kee', 'KA11111111'),\
                ('kee]ey', 'KA11111111'), ('keeler', 'KLA1111111'),\
                ('keeley', 'KLA1111111'), ('keeling', 'KLNK111111'),\
                ('keen', 'KN11111111'), ('keenall', 'KNA1111111'),\
                ('keenan oli', 'KNNLA11111'), ('keenan', 'KNN1111111'),\
                ('keene', 'KN11111111'), ('keennelly', 'KNLA111111'),\
                ('keeshan', 'KSN1111111'), ('kehoe', 'KA11111111'),\
                ('keillor', 'KLA1111111'), ('keinan', 'KNN1111111'),\
                ('keir', 'KA11111111'), ('keirnan', 'KNN1111111'),\
                ('keith', 'KT11111111'), ('keliher', 'KLA1111111'),\
                ('kellahan', 'KLN1111111'), ('kellan', 'KLN1111111'),\
                ('kellas', 'KLS1111111'), ('kellehan', 'KLN1111111'),\
                ('keller', 'KLA1111111'), ('kelley', 'KLA1111111'),\
                ('kelliher', 'KLA1111111'), ('kelly', 'KLA1111111'),\
                ('kemohan', 'KMN1111111'), ('kemp', 'KMP1111111'),\
                ('kempson', 'KMPSN11111'), ('kempthorne', 'KMPTN11111'),\
                ('kempton', 'KMPTN11111'), ('kemshed', 'KMST111111'),\
                ('kemsley', 'KMSLA11111'), ('kendall', 'KNTA111111'),\
                ('kendell', 'KNTA111111'), ('kendrick', 'KNTRK11111'),\
                ('kenllard', 'KNLT111111'), ('kenn', 'KN11111111'),\
                ('kenna', 'KNA1111111'), ('kennard', 'KNT1111111'),\
                ('kenneally', 'KNLA111111'), ('kennealy', 'KNLA111111'),\
                ('kennedy', 'KNTA111111'), ('kennelly', 'KNLA111111'),\
                ('kennerly', 'KNLA111111'), ('kenney', 'KNA1111111'),\
                ('kenny', 'KNA1111111'), ('kenshole', 'KNSA111111'),\
                ('kensington', 'KNSNKTN111'), ('kensler', 'KNSLA11111'),\
                ('kent', 'KNT1111111'), ('kenward', 'KNWT111111'),\
                ('kenyon', 'KNN1111111'), ('keogh', 'KA11111111'),\
                ('keohane', 'KN11111111'), ('keown', 'KN11111111'),\
                ('ker', 'KA11111111'), ('kernick', 'KNK1111111'),\
                ('kernohan', 'KNN1111111'), ('kerr', 'KA11111111'),\
                ('kerrigan', 'KRKN111111'), ('kerse', 'KS11111111'),\
                ('kershaw', 'KSA1111111'), ('kesteven', 'KSTFN11111'),\
                ('kett', 'KT11111111'), ('kettle', 'KTA1111111'),\
                ('kewish', 'KWS1111111'), ('key', 'KA11111111'),\
                ('keyes', 'KS11111111'), ('keys', 'KS11111111'),\
                ('kibblewhite', 'KPLWT11111'), ('kidd', 'KT11111111'),\
                ('kidston', 'KTSTN11111'), ('kiee', 'KA11111111'),\
                ('kiely', 'KLA1111111'), ('kienan', 'KNN1111111'),\
                ('kieran', 'KRN1111111'), ('kiernan', 'KNN1111111'),\
                ('kilchin', 'KKN1111111'), ('kilgariff', 'KKRF111111'),\
                ('kilgarrif', 'KKRF111111'), ('kilgour', 'KKA1111111'),\
                ('kilkeary', 'KKRA111111'), ('killilea', 'KLLA111111'),\
                ('killin', 'KLN1111111'), ('kilner', 'KNA1111111'),\
                ('kilpatrick', 'KPTRK11111'), ('kilroy', 'KRA1111111'),\
                ('kimber', 'KMPA111111'), ('kincaid', 'KNKT111111'),\
                ('kinch', 'KNK1111111'), ('kindley', 'KNTLA11111'),\
                ('king', 'KNK1111111'), ('kingford', 'KNKFT11111'),\
                ('kingsford', 'KNKSFT1111'), ('kingsland', 'KNKSLNT111'),\
                ('kingston', 'KNKSTN1111'), ('kininmonth', 'KNNMNT1111'),\
                ('kinloch', 'KNLK111111'), ('kinlock', 'KNLK111111'),\
                ('kinmont', 'KNMNT11111'), ('kinnaird', 'KNT1111111'),\
                ('kinnear', 'KNA1111111'), ('kinney', 'KNA1111111'),\
                ('kippenberg', 'KPNPK11111'), ('kippenberger', 'KPNPKA1111'),\
                ('kirby', 'KPA1111111'), ('kirk', 'KK11111111'),\
                ('kirkaldie', 'KKTA111111'), ('kirkby', 'KKPA111111'),\
                ('kirkcaldie', 'KKTA111111'), ('kirkcaldy', 'KKTA111111'),\
                ('kirke', 'KK11111111'), ('kirkham', 'KKM1111111'),\
                ('kirkland', 'KKLNT11111'), ('kirkly', 'KKLA111111'),\
                ('kirkness', 'KKNS111111'), ('kirkpatrick', 'KKPTRK1111'),\
                ('kirkwood', 'KKWT111111'), ('kirnan', 'KNN1111111'),\
                ('kirton', 'KTN1111111'), ('kirwan', 'KWN1111111'),\
                ('kitchen', 'KKN1111111'), ('kitchin', 'KKN1111111'),\
                ('kitching', 'KKNK111111'), ('kite', 'KT11111111'),\
                ('kitt', 'KT11111111'), ('kitterick', 'KTRK111111'),\
                ('kitto', 'KTA1111111'), ('klahn', 'KLN1111111'),\
                ('klee', 'KLA1111111'), ('kleeber', 'KLPA111111'),\
                ('klimeck', 'KLMK111111'), ('knewstubb', 'KNSTP11111'),\
                ('knigbt', 'KNKPT11111'), ('knight', 'KNT1111111'),\
                ('knights', 'KNTS111111'), ('knipe', 'KNP1111111'),\
                ('knopp', 'KNP1111111'), ('knowles', 'KNLS111111'),\
                ('knox', 'KNK1111111'), ('knudsen', 'KNTSN11111'),\
                ('knudson', 'KNTSN11111'), ('kofoed', 'KFT1111111'),\
                ('kollberg', 'KPK1111111'), ('koller', 'KLA1111111'),\
                ('korner', 'KNA1111111'), ('kraus', 'KRS1111111'),\
                ('krause', 'KRS1111111'), ('kreft', 'KRFT111111'),\
                ('kroon', 'KRN1111111'), ('kropp', 'KRP1111111'),\
                ('krox', 'KRK1111111'), ('kruskoff', 'KRSKF11111'),\
                ('kruskopf', 'KRSKPF1111'), ('kummert', 'KMT1111111'),\
                ('ky]e', 'KA11111111'), ('kydd', 'KT11111111'),\
                ('kyle', 'KA11111111'), ('kyle\'', 'KA11111111'),\
                ('l\'estrange', 'LSTRNK1111'), ('la roche', 'LRK1111111'),\
                ('labes', 'LPS1111111'), ('lacey', 'LSA1111111'),\
                ('lack', 'LK11111111'), ('ladd', 'LT11111111'),\
                ('laery', 'LRA1111111'), ('laffey', 'LFA1111111'),\
                ('lafranchie', 'LFRNKA1111'), ('lagan', 'LKN1111111'),\
                ('lahman', 'LMN1111111'), ('lahood', 'LT11111111'),\
                ('laidlaw', 'LTLA111111'), ('lain', 'LN11111111'),\
                ('laine', 'LN11111111'), ('laing', 'LNK1111111'),\
                ('laird', 'LT11111111'), ('lake', 'LK11111111'),\
                ('lakeman', 'LKMN111111'), ('lale', 'LA11111111'),\
                ('laley', 'LLA1111111'), ('laloli', 'LLLA111111'),\
                ('lamb', 'LM11111111'), ('lambert', 'LMPT111111'),\
                ('lambeth', 'LMPT111111'), ('lambie', 'LMPA111111'),\
                ('lamborn', 'LMPN111111'), ('lambton', 'LMPTN11111'),\
                ('lamham', 'LMM1111111'), ('lamont', 'LMNT111111'),\
                ('lampard', 'LMPT111111'), ('lampen', 'LMPN111111'),\
                ('lancaster', 'LNKSTA1111'), ('landerson', 'LNTSN11111'),\
                ('landrebe', 'LNTRP11111'), ('landreth', 'LNTRT11111'),\
                ('landriken', 'LNTRKN1111'), ('lane', 'LN11111111'),\
                ('laney', 'LNA1111111'), ('lang', 'LNK1111111'),\
                ('langdon', 'LNKTN11111'), ('langevad', 'LNKFT11111'),\
                ('langford', 'LNKFT11111'), ('langham', 'LNM1111111'),\
                ('langlands', 'LNKLNTS111'), ('langley', 'LNKLA11111'),\
                ('langmuir', 'LNKMA11111'), ('langston', 'LNKSTN1111'),\
                ('lanham', 'LNM1111111'), ('lanini', 'LNNA111111'),\
                ('lappan', 'LPN1111111'), ('lapsley', 'LPSLA11111'),\
                ('lardner', 'LTNA111111'), ('larkin', 'LKN1111111'),\
                ('larking', 'LKNK111111'), ('larkins', 'LKNS111111'),\
                ('larldng', 'LTNK111111'), ('larner', 'LNA1111111'),\
                ('laroche', 'LRK1111111'), ('larsen', 'LSN1111111'),\
                ('larson', 'LSN1111111'), ('larty', 'LTA1111111'),\
                ('lascelles', 'LSLS111111'), ('latham', 'LTM1111111'),\
                ('latimer', 'LTMA111111'), ('latta', 'LTA1111111'),\
                ('latter', 'LTA1111111'), ('lattimer', 'LTMA111111'),\
                ('lattimore', 'LTMA111111'), ('lauchlan', 'LKLN111111'),\
                ('laug', 'LK11111111'), ('laughland', 'LLNT111111'),\
                ('laughlin', 'LLN1111111'), ('lauren', 'LRN1111111'),\
                ('laurenson', 'LRNSN11111'), ('laurie', 'LRA1111111'),\
                ('lavender', 'LFNTA11111'), ('laverty', 'LFTA111111'),\
                ('lavery', 'LFRA111111'), ('law', 'LA11111111'),\
                ('lawence', 'LWNK111111'), ('lawer', 'LWA1111111'),\
                ('lawfield', 'LFT1111111'), ('lawless', 'LLS1111111'),\
                ('lawliss', 'LLS1111111'), ('lawlor', 'LLA1111111'),\
                ('lawloss', 'LLS1111111'), ('lawrence', 'LRNK111111'),\
                ('lawrenson', 'LRNSN11111'), ('lawrie', 'LRA1111111'),\
                ('lawry', 'LRA1111111'), ('laws', 'LS11111111'),\
                ('lawson', 'LSN1111111'), ('lawton', 'LTN1111111'),\
                ('lax', 'LK11111111'), ('layburn', 'LPN1111111'),\
                ('laycock', 'LKK1111111'), ('laytham', 'LTM1111111'),\
                ('layton', 'LTN1111111'), ('lazarus', 'LSRS111111'),\
                ('lbbetson', 'PTSN111111'), ('le brun', 'LPRN111111'),\
                ('le couteur', 'LKTA111111'), ('le fevre', 'LFFA111111'),\
                ('le gal', 'LKA1111111'), ('le page', 'LPK1111111'),\
                ('le sueur', 'LSA1111111'), ('le vavasour', 'LFFSA11111'),\
                ('lea', 'LA11111111'), ('leach', 'LK11111111'),\
                ('leadbetter', 'LTPTA11111'), ('leahy', 'LA11111111'),\
                ('lealy', 'LLA1111111'), ('lean', 'LN11111111'),\
                ('leaper', 'LPA1111111'), ('lear', 'LA11111111'),\
                ('learmond', 'LMNT111111'), ('leary', 'LRA1111111'),\
                ('leask', 'LSK1111111'), ('leatham', 'LTM1111111'),\
                ('leathem', 'LTM1111111'), ('leather', 'LTA1111111'),\
                ('leatherland', 'LTLNT11111'), ('leathley', 'LTLA111111'),\
                ('leckie', 'LKA1111111'), ('leclie', 'LKLA111111'),\
                ('lecouteur', 'LKTA111111'), ('leddicott', 'LTKT111111'),\
                ('ledgerwood', 'LKWT111111'), ('ledlie', 'LTLA111111'),\
                ('lee', 'LA11111111'), ('leece', 'LK11111111'),\
                ('leech', 'LK11111111'), ('leedale', 'LTA1111111'),\
                ('leeden', 'LTN1111111'), ('leemin', 'LMN1111111'),\
                ('leeming', 'LMNK111111'), ('leery', 'LRA1111111'),\
                ('lees', 'LS11111111'), ('leete', 'LT11111111'),\
                ('lefevre', 'LFFA111111'), ('legal', 'LKA1111111'),\
                ('legall', 'LKA1111111'), ('legat', 'LKT1111111'),\
                ('legg', 'LK11111111'), ('legge', 'LK11111111'),\
                ('leggett', 'LKT1111111'), ('leggott', 'LKT1111111'),\
                ('lehmann', 'LMN1111111'), ('leigh', 'LA11111111'),\
                ('leighton', 'LTN1111111'), ('leihy', 'LA11111111'),\
                ('leishman', 'LSMN111111'), ('leitch', 'LK11111111'),\
                ('leith', 'LT11111111'), ('lelliott', 'LLT1111111'),\
                ('lemin', 'LMN1111111'), ('lemon', 'LMN1111111'),\
                ('lendrum', 'LNTRM11111'), ('leng', 'LNK1111111'),\
                ('lenihan', 'LNN1111111'), ('lennan', 'LNN1111111'),\
                ('lennard', 'LNT1111111'), ('lennon', 'LNN1111111'),\
                ('lennox', 'LNK1111111'), ('lenz', 'LNS1111111'),\
                ('leo', 'LA11111111'), ('leonard', 'LNT1111111'),\
                ('leper', 'LPA1111111'), ('lepine', 'LPN1111111'),\
                ('lepper', 'LPA1111111'), ('leppingvell', 'LPNKFA1111'),\
                ('leppingwell', 'LPNKWA1111'), ('lerrigo', 'LRKA111111'),\
                ('leslie', 'LSLA111111'), ('lester', 'LSTA111111'),\
                ('lesueur', 'LSA1111111'), ('lethaby', 'LTPA111111'),\
                ('lethbridge', 'LTPRK11111'), ('lethridge', 'LTRK111111'),\
                ('letts', 'LTS1111111'), ('leung chung', 'LNKNK11111'),\
                ('levi', 'LFA1111111'), ('levido', 'LFTA111111'),\
                ('levinsohn', 'LFNSN11111'), ('levy', 'LFA1111111'),\
                ('lewies', 'LWS1111111'), ('lewis', 'LWS1111111'),\
                ('lewisham', 'LWSM111111'), ('leyden', 'LTN1111111'),\
                ('leydon', 'LTN1111111'), ('leyland', 'LLNT111111'),\
                ('leys', 'LS11111111'), ('lichtenstein', 'LKTNSTN111'),\
                ('lickie', 'LKA1111111'), ('liddell', 'LTA1111111'),\
                ('liddicoat', 'LTKT111111'), ('liddle', 'LTA1111111'),\
                ('lidston', 'LTSTN11111'), ('lied', 'LT11111111'),\
                ('liggins', 'LKNS111111'), ('lightbourne', 'LTPN111111'),\
                ('lightfoot', 'LTFT111111'), ('lilburn', 'LPN1111111'),\
                ('lilburne', 'LPN1111111'), ('lilley', 'LLA1111111'),\
                ('lillie', 'LLA1111111'), ('lilly', 'LLA1111111'),\
                ('lincoln', 'LNKN111111'), ('lind', 'LNT1111111'),\
                ('lindley', 'LNTLA11111'), ('lindon', 'LNTN111111'),\
                ('lindsay', 'LNTSA11111'), ('lineham', 'LNM1111111'),\
                ('ling', 'LNK1111111'), ('linklater', 'LNKLTA1111'),\
                ('linkston', 'LNKSTN1111'), ('linnane', 'LNN1111111'),\
                ('linney', 'LNA1111111'), ('linsdell', 'LNSTA11111'),\
                ('lintern', 'LNTN111111'), ('linton', 'LNTN111111'),\
                ('lipman', 'LPMN111111'), ('lippert', 'LPT1111111'),\
                ('lischner', 'LSKNA11111'), ('lisle', 'LSA1111111'),\
                ('list', 'LST1111111'), ('lister', 'LSTA111111'),\
                ('liston', 'LSTN111111'), ('listor', 'LSTA111111'),\
                ('litolff', 'LTF1111111'), ('littie', 'LTA1111111'),\
                ('little', 'LTA1111111'), ('littlejohn', 'LTLN111111'),\
                ('littlewood', 'LTLWT11111'), ('livingston', 'LFNKSTN111'),\
                ('livingstone', 'LFNKSTN111'), ('llles', 'LS11111111'),\
                ('lloyd', 'LT11111111'), ('lngram', 'NKRM111111'),\
                ('lnwood', 'NWT1111111'), ('loader', 'LTA1111111'),\
                ('loades', 'LTS1111111'), ('loan', 'LN11111111'),\
                ('loasby', 'LSPA111111'), ('lobb', 'LP11111111'),\
                ('loche', 'LK11111111'), ('lochhead', 'LKT1111111'),\
                ('lochore', 'LKA1111111'), ('lock', 'LK11111111'),\
                ('lockerbie', 'LKPA111111'), ('lockett', 'LKT1111111'),\
                ('lockhart', 'LKT1111111'), ('lockhead', 'LKT1111111'),\
                ('lockie', 'LKA1111111'), ('lockstone', 'LKSTN11111'),\
                ('lockwood', 'LKWT111111'), ('lockyer', 'LKA1111111'),\
                ('lodge', 'LK11111111'), ('loeffler', 'LFLA111111'),\
                ('logan', 'LKN1111111'), ('logg', 'LK11111111'),\
                ('loggie', 'LKA1111111'), ('logic', 'LKK1111111'),\
                ('logie', 'LKA1111111'), ('logue', 'LKA1111111'),\
                ('lohrey', 'LRA1111111'), ('loke', 'LK11111111'),\
                ('lomas', 'LMS1111111'), ('lombardi', 'LMPTA11111'),\
                ('loney', 'LNA1111111'), ('long', 'LNK1111111'),\
                ('longhurst', 'LNST111111'), ('longley', 'LNKLA11111'),\
                ('longman', 'LNKMN11111'), ('longmore', 'LNKMA11111'),\
                ('longstaff', 'LNKSTF1111'), ('longworth', 'LNKWT11111'),\
                ('lonie', 'LNA1111111'), ('lonsdale', 'LNSTA11111'),\
                ('loraine', 'LRN1111111'), ('lord', 'LT11111111'),\
                ('lorenz', 'LRNS111111'), ('lorimer', 'LRMA111111'),\
                ('loring', 'LRNK111111'), ('lory', 'LRA1111111'),\
                ('lothian', 'LTN1111111'), ('louden', 'LTN1111111'),\
                ('louder', 'LTA1111111'), ('loudon', 'LTN1111111'),\
                ('lough', 'LA11111111'), ('loughill', 'LKA1111111'),\
                ('loughlin', 'LLN1111111'), ('loughnan', 'LNN1111111'),\
                ('loughran', 'LRN1111111'), ('loughrey', 'LRA1111111'),\
                ('louis', 'LS11111111'), ('lousley', 'LSLA111111'),\
                ('lovatt', 'LFT1111111'), ('love', 'LF11111111'),\
                ('loveless', 'LFLS111111'), ('lovell', 'LFA1111111'),\
                ('lovelock', 'LFLK111111'), ('low', 'LA11111111'),\
                ('lowden', 'LTN1111111'), ('lowe', 'LA11111111'),\
                ('lowen', 'LWN1111111'), ('lower', 'LWA1111111'),\
                ('lowery', 'LWRA111111'), ('lowes', 'LWS1111111'),\
                ('lowie', 'LWA1111111'), ('lowrey', 'LRA1111111'),\
                ('lowry', 'LRA1111111'), ('loyd', 'LT11111111'),\
                ('loydall', 'LTA1111111'), ('lrvine', 'FN11111111'),\
                ('lsaacs', 'SKS1111111'), ('lucas', 'LKS1111111'),\
                ('luckhurst', 'LKST111111'), ('ludlow', 'LTLA111111'),\
                ('luff', 'LF11111111'), ('luke', 'LK11111111'),\
                ('lukey', 'LKA1111111'), ('lumb', 'LM11111111'),\
                ('lumsden', 'LMSTN11111'), ('lunam', 'LNM1111111'),\
                ('lunan', 'LNN1111111'), ('lunardi', 'LNTA111111'),\
                ('lund', 'LNT1111111'), ('lundberg', 'LNTPK11111'),\
                ('lundon', 'LNTN111111'), ('lundquist', 'LNTKST1111'),\
                ('lungley', 'LNKLA11111'), ('lunham', 'LNM1111111'),\
                ('lunn', 'LN11111111'), ('lunnam', 'LNM1111111'),\
                ('luscombe', 'LSKM111111'), ('lusher', 'LSA1111111'),\
                ('lusk', 'LSK1111111'), ('luskie', 'LSKA111111'),\
                ('luslie', 'LSLA111111'), ('lust', 'LST1111111'),\
                ('lvingstone', 'FNKSTN1111'), ('lyall', 'LA11111111'),\
                ('lyddy', 'LTA1111111'), ('lyders', 'LTS1111111'),\
                ('lydiate', 'LTT1111111'), ('lye', 'LA11111111'),\
                ('lyeaght', 'LT11111111'), ('lyle', 'LA11111111'),\
                ('lymburn', 'LMPN111111'), ('lynch', 'LNK1111111'),\
                ('lyndburst', 'LNTPST1111'), ('lyndhurst', 'LNTST11111'),\
                ('lyng', 'LNK1111111'), ('lynn', 'LN11111111'),\
                ('lynskey', 'LNSKA11111'), ('lyon', 'LN11111111'),\
                ('lyons', 'LNS1111111'), ('lysaght', 'LST1111111'),\
                ('lythgoe', 'LTKA111111'), ('lytle', 'LTA1111111'),\
                ('lyttle', 'LTA1111111'), ('m orris', 'MRS1111111'),\
                ('mabon', 'MPN1111111'), ('macale', 'MKA1111111'),\
                ('macallan', 'MKLN111111'), ('macallum', 'MKLM111111'),\
                ('macan', 'MKN1111111'), ('macandrew', 'MKNTRA1111'),\
                ('macarthur', 'MKTA111111'), ('macartney', 'MKTNA11111'),\
                ('macaskill', 'MKSKA11111'), ('macassey', 'MKSA111111'),\
                ('macaulay', 'MKLA111111'), ('macauley', 'MKLA111111'),\
                ('macavoy', 'MKFA111111'), ('macbeath', 'MKPT111111'),\
                ('macbeth', 'MKPT111111'), ('macbryde', 'MKPRT11111'),\
                ('maccallum', 'MKLM111111'), ('maccartie', 'MKTA111111'),\
                ('maccoll', 'MKA1111111'), ('macdonald', 'MKTNT11111'),\
                ('macdonall', 'MKTNA11111'), ('macdonell', 'MKTNA11111'),\
                ('macdonnell', 'MKTNA11111'), ('macdougall', 'MKTKA11111'),\
                ('macduff', 'MKTF111111'), ('mace', 'MK11111111'),\
                ('maceewan', 'MSWN111111'), ('macer', 'MSA1111111'),\
                ('macewan', 'MSWN111111'), ('macey', 'MSA1111111'),\
                ('macfarlane', 'MKFLN11111'), ('macfie', 'MKFA111111'),\
                ('macghie', 'MKA1111111'), ('macgibbon', 'MKPN111111'),\
                ('macgregor', 'MKRKA11111'), ('macguire', 'MKA1111111'),\
                ('machell', 'MKA1111111'), ('machin', 'MKN1111111'),\
                ('machridge', 'MKRK111111'), ('maciean', 'MSN1111111'),\
                ('macildowie', 'MSTWA11111'), ('macinnes', 'MSNS111111'),\
                ('macintosh', 'MSNTS11111'), ('macintyre', 'MSNTA11111'),\
                ('macivor', 'MSFA111111'), ('mack', 'MK11111111'),\
                ('mackay', 'MKA1111111'), ('mackean', 'MKN1111111'),\
                ('mackechnic', 'MKKNK11111'), ('mackechnie', 'MKKNA11111'),\
                ('mackellar', 'MKLA111111'), ('mackenzie', 'MKNSA11111'),\
                ('mackersey', 'MKSA111111'), ('mackersy', 'MKSA111111'),\
                ('mackey', 'MKA1111111'), ('mackie', 'MKA1111111'),\
                ('mackinnon', 'MKNN111111'), ('mackintosh', 'MKNTS11111'),\
                ('mackisack', 'MKSK111111'), ('mackney', 'MKNA111111'),\
                ('macknight', 'MKNT111111'), ('mackrell', 'MKRA111111'),\
                ('mackridge', 'MKRK111111'), ('mackway jones', 'MKWNS11111'),\
                ('mackway-jones', 'MKWNS11111'), ('mackwayjones', 'MKWNS11111'),\
                ('macky', 'MKA1111111'), ('maclachlan', 'MKLKLN1111'),\
                ('maclaren', 'MKLRN11111'), ('maclatchy', 'MKLKA11111'),\
                ('maclean', 'MKLN111111'), ('maclellan', 'MKLLN11111'),\
                ('maclennan', 'MKLNN11111'), ('macleod', 'MKLT111111'),\
                ('maclonald', 'MKLNT11111'), ('macmanus', 'MKMNS11111'),\
                ('macmaster', 'MKMSTA1111'), ('macmillan', 'MKMLN11111'),\
                ('macnee', 'MKNA111111'), ('macnicol', 'MKNKA11111'),\
                ('macniven', 'MKNFN11111'), ('macomish', 'MKMS111111'),\
                ('macpherson', 'MKFSN11111'), ('macquaid', 'MKT1111111'),\
                ('macrae', 'MKRA111111'), ('macswain', 'MKSWN11111'),\
                ('macwilliam', 'MKWLM11111'), ('madarlane', 'MTLN111111'),\
                ('madden', 'MTN1111111'), ('maddern', 'MTN1111111'),\
                ('maddigan', 'MTKN111111'), ('maddox', 'MTK1111111'),\
                ('maddren', 'MTRN111111'), ('madell', 'MTA1111111'),\
                ('maden', 'MTN1111111'), ('madigan', 'MTKN111111'),\
                ('maffan', 'MFN1111111'), ('magee', 'MKA1111111'),\
                ('magner', 'MKNA111111'), ('magnus', 'MKNS111111'),\
                ('magorian', 'MKRN111111'), ('maguire', 'MKA1111111'),\
                ('mahalm', 'MM11111111'), ('mahan', 'MN11111111'),\
                ('maharey', 'MRA1111111'), ('maher', 'MA11111111'),\
                ('mahon', 'MN11111111'), ('mahoney', 'MNA1111111'),\
                ('mahony', 'MNA1111111'), ('maicolm', 'MKM1111111'),\
                ('maills', 'MS11111111'), ('maim', 'MM11111111'),\
                ('main', 'MN11111111'), ('maine', 'MN11111111'),\
                ('maines', 'MNS1111111'), ('mainland', 'MNLNT11111'),\
                ('mains', 'MNS1111111'), ('mair', 'MA11111111'),\
                ('maitland', 'MTLNT11111'), ('major', 'MA11111111'),\
                ('maker', 'MKA1111111'), ('malcolm', 'MKM1111111'),\
                ('malcolmson', 'MKMSN11111'), ('malden', 'MTN1111111'),\
                ('maleod', 'MLT1111111'), ('maler', 'MLA1111111'),\
                ('maley', 'MLA1111111'), ('malladew', 'MLTA111111'),\
                ('mallett', 'MLT1111111'), ('malley', 'MLA1111111'),\
                ('malloch', 'MLK1111111'), ('malone', 'MLN1111111'),\
                ('maloney', 'MLNA111111'), ('malthus', 'MTS1111111'),\
                ('manallack', 'MNLK111111'), ('manaton', 'MNTN111111'),\
                ('mander', 'MNTA111111'), ('manderson', 'MNTSN11111'),\
                ('mangan', 'MNKN111111'), ('mangin', 'MNKN111111'),\
                ('manion', 'MNN1111111'), ('manley', 'MNLA111111'),\
                ('manlove', 'MNLF111111'), ('mann', 'MN11111111'),\
                ('mannin', 'MNN1111111'), ('manning', 'MNNK111111'),\
                ('mannix', 'MNK1111111'), ('mansell', 'MNSA111111'),\
                ('mansfield', 'MNSFT11111'), ('manson', 'MNSN111111'),\
                ('mantell', 'MNTA111111'), ('maples', 'MPLS111111'),\
                ('marchant', 'MKNT111111'), ('marcussen', 'MKSN111111'),\
                ('mardon', 'MTN1111111'), ('marechal', 'MRKA111111'),\
                ('marett', 'MRT1111111'), ('marette', 'MRT1111111'),\
                ('maris', 'MRS1111111'), ('mark', 'MK11111111'),\
                ('markby', 'MKPA111111'), ('markham', 'MKM1111111'),\
                ('markland', 'MKLNT11111'), ('marks', 'MKS1111111'),\
                ('marlovv', 'MLF1111111'), ('marlow', 'MLA1111111'),\
                ('marple', 'MPA1111111'), ('marr', 'MA11111111'),\
                ('marrah', 'MRA1111111'), ('marrett', 'MRT1111111'),\
                ('marrette', 'MRT1111111'), ('marriage', 'MRK1111111'),\
                ('marriner', 'MRNA111111'), ('marriott', 'MRT1111111'),\
                ('marris', 'MRS1111111'), ('marrison', 'MRSN111111'),\
                ('marryatt', 'MRT1111111'), ('marsden', 'MSTN111111'),\
                ('marsh', 'MS11111111'), ('marshall', 'MSA1111111'),\
                ('marsllall', 'MSLA111111'), ('marson', 'MSN1111111'),\
                ('marston', 'MSTN111111'), ('martin', 'MTN1111111'),\
                ('marwick', 'MWK1111111'), ('marychurch', 'MRKK111111'),\
                ('mashers', 'MSS1111111'), ('maskell', 'MSKA111111'),\
                ('maskill', 'MSKA111111'), ('maskrey', 'MSKRA11111'),\
                ('maslen', 'MSLN111111'), ('maslin', 'MSLN111111'),\
                ('mason', 'MSN1111111'), ('massetti', 'MSTA111111'),\
                ('massey', 'MSA1111111'), ('masson', 'MSN1111111'),\
                ('masters', 'MSTS111111'), ('masterton', 'MSTTN11111'),\
                ('mather', 'MTA1111111'), ('mathers', 'MTS1111111'),\
                ('matheson', 'MTSN111111'), ('mathews', 'MTS1111111'),\
                ('mathewson', 'MTSN111111'), ('mathias', 'MTS1111111'),\
                ('mathie', 'MTA1111111'), ('mathieson', 'MTSN111111'),\
                ('mathison', 'MTSN111111'), ('matier', 'MTA1111111'),\
                ('matlewson', 'MTLSN11111'), ('matravers', 'MTRFS11111'),\
                ('matron', 'MTRN111111'), ('matthews', 'MTS1111111'),\
                ('matthewson', 'MTSN111111'), ('mattingle', 'MTNKA11111'),\
                ('mattingley', 'MTNKLA1111'), ('mattinglv', 'MTNKF11111'),\
                ('mattingly', 'MTNKLA1111'), ('mattllews', 'MTLS111111'),\
                ('mattson', 'MTSN111111'), ('matuschka', 'MTSKKA1111'),\
                ('maubon', 'MPN1111111'), ('maude', 'MT11111111'),\
                ('mauger', 'MKA1111111'), ('maunder', 'MNTA111111'),\
                ('maurie', 'MRA1111111'), ('mavbee', 'MFPA111111'),\
                ('maving', 'MFNK111111'), ('maw', 'MA11111111'),\
                ('mawer', 'MWA1111111'), ('mawhinney', 'MWNA111111'),\
                ('mawson', 'MSN1111111'), ('maxton', 'MKTN111111'),\
                ('maxwell', 'MKWA111111'), ('may', 'MA11111111'),\
                ('mayall', 'MA11111111'), ('maybee', 'MPA1111111'),\
                ('mayer', 'MA11111111'), ('mayers', 'MS11111111'),\
                ('mayfield', 'MFT1111111'), ('mayhew', 'MA11111111'),\
                ('mayn', 'MN11111111'), ('maynard', 'MNT1111111'),\
                ('mayne', 'MN11111111'), ('mayo', 'MA11111111'),\
                ('mays', 'MS11111111'), ('mayston', 'MSTN111111'),\
                ('mayze', 'MS11111111'), ('mazey', 'MSA1111111'),\
                ('mcadam', 'MKTM111111'), ('mcade', 'MKT1111111'),\
                ('mcadie', 'MKTA111111'), ('mcalister', 'MKLSTA1111'),\
                ('mcallan', 'MKLN111111'), ('mcallen', 'MKLN111111'),\
                ('mcalliste', 'MKLST11111'), ('mcallister', 'MKLSTA1111'),\
                ('mcalpine', 'MKPN111111'), ('mcanally', 'MKNLA11111'),\
                ('mcansh', 'MKNS111111'), ('mcanulty', 'MKNTA11111'),\
                ('mcara', 'MKRA111111'), ('mcarley', 'MKLA111111'),\
                ('mcarthur', 'MKTA111111'), ('mcartney', 'MKTNA11111'),\
                ('mcatamney', 'MKTMNA1111'), ('mcateer', 'MKTA111111'),\
                ('mcaulay', 'MKLA111111'), ('mcauley', 'MKLA111111'),\
                ('mcauliff', 'MKLF111111'), ('mcauliffe', 'MKLF111111'),\
                ('mcauslin', 'MKSLN11111'), ('mcbain', 'MKPN111111'),\
                ('mcbeath', 'MKPT111111'), ('mcbetah', 'MKPTA11111'),\
                ('mcbeth', 'MKPT111111'), ('mcbey', 'MKPA111111'),\
                ('mcbricle', 'MKPRKA1111'), ('mcbride', 'MKPRT11111'),\
                ('mcbryde', 'MKPRT11111'), ('mccabe', 'MKP1111111'),\
                ('mccafferty', 'MKFTA11111'), ('mccaffry', 'MKFRA11111'),\
                ('mccaig', 'MKK1111111'), ('mccall', 'MKA1111111'),\
                ('mccallion', 'MKLN111111'), ('mccallum', 'MKLM111111'),\
                ('mccalman', 'MKMN111111'), ('mccambie', 'MKMPA11111'),\
                ('mccammon', 'MKMN111111'), ('mccann', 'MKN1111111'),\
                ('mccardell', 'MKTA111111'), ('mccarrigan', 'MKRKN11111'),\
                ('mccarten', 'MKTN111111'), ('mccarter', 'MKTA111111'),\
                ('mccarthy', 'MKTA111111'), ('mccartney', 'MKTNA11111'),\
                ('mccarty', 'MKTA111111'), ('mccash', 'MKS1111111'),\
                ('mccaskill', 'MKSKA11111'), ('mccaughan', 'MKKN111111'),\
                ('mccaul', 'MKA1111111'), ('mccauley', 'MKLA111111'),\
                ('mccauseland', 'MKSLNT1111'), ('mccausland', 'MKSLNT1111'),\
                ('mccaw', 'MKA1111111'), ('mccawe', 'MKA1111111'),\
                ('mccay', 'MKA1111111'), ('mcchesney', 'MKSNA11111'),\
                ('mccielland', 'MKSLNT1111'), ('mcciue', 'MKSA111111'),\
                ('mcclatchv', 'MKLKF11111'), ('mcclatchy', 'MKLKA11111'),\
                ('mcclean', 'MKLN111111'), ('mccleery', 'MKLRA11111'),\
                ('mcclelland', 'MKLLNT1111'), ('mcclenaghan', 'MKLNKN1111'),\
                ('mcclintock', 'MKLNTK1111'), ('mcclue', 'MKLA111111'),\
                ('mccluggage', 'MKLKK11111'), ('mcclure', 'MKLA111111'),\
                ('mccluskey', 'MKLSKA1111'), ('mcclusky', 'MKLSKA1111'),\
                ('mcclymont', 'MKLMNT1111'), ('mccoll', 'MKA1111111'),\
                ('mccolloch', 'MKLK111111'), ('mccolluch', 'MKLK111111'),\
                ('mccombe', 'MKM1111111'), ('mccombie', 'MKMPA11111'),\
                ('mcconechy', 'MKNKA11111'), ('mcconnachie', 'MKNKA11111'),\
                ('mcconnel', 'MKNA111111'), ('mcconnell', 'MKNA111111'),\
                ('mcconnichie', 'MKNKA11111'), ('mcconnochi', 'MKNKA11111'),\
                ('mcconnochie', 'MKNKA11111'), ('mcconnohie', 'MKNA111111'),\
                ('mccord', 'MKT1111111'), ('mccorie', 'MKRA111111'),\
                ('mccorkinda', 'MKKNTA1111'), ('mccorkindale', 'MKKNTA1111'),\
                ('mccorkingdale', 'MKKNKTA111'), ('mccormack', 'MKMK111111'),\
                ('mccormacl', 'MKMKA11111'), ('mccormick', 'MKMK111111'),\
                ('mccort', 'MKT1111111'), ('mccowan', 'MKWN111111'),\
                ('mccoy', 'MKA1111111'), ('mccracken', 'MKRKN11111'),\
                ('mccreadie', 'MKRTA11111'), ('mccreath', 'MKRT111111'),\
                ('mccrindle', 'MKRNTA1111'), ('mccrone', 'MKRN111111'),\
                ('mccrorie', 'MKRRA11111'), ('mccrory', 'MKRRA11111'),\
                ('mccrossan', 'MKRSN11111'), ('mccrossin', 'MKRSN11111'),\
                ('mccubbin', 'MKPN111111'), ('mcculloch', 'MKLK111111'),\
                ('mccullock', 'MKLK111111'), ('mccullough', 'MKLA111111'),\
                ('mccune', 'MKN1111111'), ('mccunn', 'MKN1111111'),\
                ('mccurdie', 'MKTA111111'), ('mccurdy', 'MKTA111111'),\
                ('mccurrach', 'MKRK111111'), ('mccurrie', 'MKRA111111'),\
                ('mccusker', 'MKSKA11111'), ('mccuskey', 'MKSKA11111'),\
                ('mccutcheon', 'MKKN111111'), ('mcdermid', 'MKTMT11111'),\
                ('mcdermitt', 'MKTMT11111'), ('mcdermott', 'MKTMT11111'),\
                ('mcdevitt', 'MKTFT11111'), ('mcdiarmid', 'MKTMT11111'),\
                ('mcdonald', 'MKTNT11111'), ('mcdonall', 'MKTNA11111'),\
                ('mcdonell', 'MKTNA11111'), ('mcdonnell', 'MKTNA11111'),\
                ('mcdouall', 'MKTA111111'), ('mcdougall', 'MKTKA11111'),\
                ('mcdowall', 'MKTWA11111'), ('mcdowell', 'MKTWA11111'),\
                ('mcduff', 'MKTF111111'), ('mceachern', 'MSKN111111'),\
                ('mceachran', 'MSKRN11111'), ('mceay', 'MSA1111111'),\
                ('mcelhenny', 'MSNA111111'), ('mcelivee', 'MSLFA11111'),\
                ('mcelroy', 'MSRA111111'), ('mceneany', 'MSNNA11111'),\
                ('mcentee', 'MSNTA11111'), ('mcevoy', 'MSFA111111'),\
                ('mcewan', 'MSWN111111'), ('mcewen', 'MSWN111111'),\
                ('mcfadden', 'MKFTN11111'), ('mcfadgen', 'MKFKN11111'),\
                ('mcfadyen', 'MKFTN11111'), ('mcfadzen', 'MKFTSN1111'),\
                ('mcfarlane', 'MKFLN11111'), ('mcfaull', 'MKFA111111'),\
                ('mcfeeters', 'MKFTS11111'), ('mcfelin', 'MKFLN11111'),\
                ('mcfetridge', 'MKFTRK1111'), ('mcfie', 'MKFA111111'),\
                ('mcgahan', 'MKN1111111'), ('mcgarrigle', 'MKRKA11111'),\
                ('mcgarry', 'MKRA111111'), ('mcgavick', 'MKFK111111'),\
                ('mcgavin', 'MKFN111111'), ('mcgaw', 'MKA1111111'),\
                ('mcgee', 'MKA1111111'), ('mcgeorge', 'MKK1111111'),\
                ('mcgetrick', 'MKTRK11111'), ('mcgettigan', 'MKTKN11111'),\
                ('mcghee', 'MKA1111111'), ('mcghie', 'MKA1111111'),\
                ('mcgill brown', 'MKPRN11111'), ('mcgill-bro', 'MKPRA11111'),\
                ('mcgill-brown', 'MKPRN11111'), ('mcgill', 'MKA1111111'),\
                ('mcgillivary', 'MKLFRA1111'), ('mcgilvary', 'MKFRA11111'),\
                ('mcgilvray', 'MKFRA11111'), ('mcgimpsey', 'MKMPSA1111'),\
                ('mcginness', 'MKNS111111'), ('mcginty', 'MKNTA11111'),\
                ('mcgirr', 'MKA1111111'), ('mcgirt', 'MKT1111111'),\
                ('mcglashan', 'MKLSN11111'), ('mcgllie', 'MKLA111111'),\
                ('mcgoldrick', 'MKTRK11111'), ('mcgolligal', 'MKLKA11111'),\
                ('mcgonigal', 'MKNKA11111'), ('mcgoogan', 'MKKN111111'),\
                ('mcgoun', 'MKN1111111'), ('mcgoverne', 'MKFN111111'),\
                ('mcgowan', 'MKWN111111'), ('mcgradie', 'MKRTA11111'),\
                ('mcgrath', 'MKRT111111'), ('mcgregor', 'MKRKA11111'),\
                ('mcgriffiths', 'MKRFTS1111'), ('mcguckin', 'MKKN111111'),\
                ('mcguffie', 'MKFA111111'), ('mcguigan', 'MKKN111111'),\
                ('mcguire', 'MKA1111111'), ('mchardy', 'MKTA111111'),\
                ('mcharry', 'MKRA111111'), ('mchealy', 'MKLA111111'),\
                ('mchenry', 'MKNRA11111'), ('mchoull', 'MKA1111111'),\
                ('mchugh', 'MKA1111111'), ('mchutchcson', 'MKKKSN1111'),\
                ('mchutcheson', 'MKKSN11111'), ('mchutchon', 'MKKN111111'),\
                ('mciachlan', 'MSKLN11111'), ('mciaren', 'MSRN111111'),\
                ('mciean', 'MSN1111111'), ('mcielland', 'MSLNT11111'),\
                ('mcieod', 'MST1111111'), ('mciintyre', 'MSNTA11111'),\
                ('mcilroy', 'MSRA111111'), ('mcindoe', 'MSNTA11111'),\
                ('mcinerney', 'MSNNA11111'), ('mcinnes', 'MSNS111111'),\
                ('mcintosh', 'MSNTS11111'), ('mcintosn', 'MSNTSN1111'),\
                ('mcintyre', 'MSNTA11111'), ('mcisaac', 'MSSK111111'),\
                ('mciver', 'MSFA111111'), ('mcivor', 'MSFA111111'),\
                ('mckague', 'MKKA111111'), ('mckane', 'MKN1111111'),\
                ('mckay', 'MKA1111111'), ('mckaye', 'MKA1111111'),\
                ('mckean', 'MKN1111111'), ('mckeand', 'MKNT111111'),\
                ('mckeay', 'MKA1111111'), ('mckechie', 'MKKA111111'),\
                ('mckechnie', 'MKKNA11111'), ('mckecknie', 'MKKNA11111'),\
                ('mckee', 'MKA1111111'), ('mckeefry', 'MKFRA11111'),\
                ('mckeeiry', 'MKRA111111'), ('mckeeman', 'MKMN111111'),\
                ('mckeen', 'MKN1111111'), ('mckeenan', 'MKNN111111'),\
                ('mckeich', 'MKK1111111'), ('mckellar', 'MKLA111111'),\
                ('mckelvey', 'MKFA111111'), ('mckelvie', 'MKFA111111'),\
                ('mckendry', 'MKNTRA1111'), ('mckenna', 'MKNA111111'),\
                ('mckenney', 'MKNA111111'), ('mckenzie', 'MKNSA11111'),\
                ('mckeown', 'MKN1111111'), ('mckernan', 'MKNN111111'),\
                ('mckerras', 'MKRS111111'), ('mckerrow', 'MKRA111111'),\
                ('mckessar', 'MKSA111111'), ('mcketterick', 'MKTRK11111'),\
                ('mckewell', 'MKWA111111'), ('mckewen', 'MKWN111111'),\
                ('mckey', 'MKA1111111'), ('mckibbin', 'MKPN111111'),\
                ('mckie', 'MKA1111111'), ('mckillop', 'MKLP111111'),\
                ('mckinlay', 'MKNLA11111'), ('mckinley', 'MKNLA11111'),\
                ('mckinnel', 'MKNA111111'), ('mckinney', 'MKNA111111'),\
                ('mckinnie', 'MKNA111111'), ('mckinnon', 'MKNN111111'),\
                ('mckirdy', 'MKTA111111'), ('mckissock', 'MKSK111111'),\
                ('mckitterick', 'MKTRK11111'), ('mcknight', 'MKNT111111'),\
                ('mckone', 'MKN1111111'), ('mclachlan', 'MKLKLN1111'),\
                ('mclanachan', 'MKLNKN1111'), ('mclaren', 'MKLRN11111'),\
                ('mclatchie', 'MKLKA11111'), ('mclauchan', 'MKLKN11111'),\
                ('mclauchlan', 'MKLKLN1111'), ('mclauchlin', 'MKLKLN1111'),\
                ('mclaughlan', 'MKLLN11111'), ('mclaughlin', 'MKLLN11111'),\
                ('mclav', 'MKLF111111'), ('mclay', 'MKLA111111'),\
                ('mclcan', 'MKKN111111'), ('mclean', 'MKLN111111'),\
                ('mclear', 'MKLA111111'), ('mcleary', 'MKLRA11111'),\
                ('mcleavey', 'MKLFA11111'), ('mcleay', 'MKLA111111'),\
                ('mcledd', 'MKLT111111'), ('mcledowne', 'MKLTN11111'),\
                ('mcledowney', 'MKLTNA1111'), ('mcleely', 'MKLLA11111'),\
                ('mclellan', 'MKLLN11111'), ('mclelland', 'MKLLNT1111'),\
                ('mclenaghin', 'MKLNKN1111'), ('mclennan', 'MKLNN11111'),\
                ('mcleod', 'MKLT111111'), ('mclevie', 'MKLFA11111'),\
                ('mclintock', 'MKLNTK1111'), ('mcliskey', 'MKLSKA1111'),\
                ('mcllroy', 'MKRA111111'), ('mclndoe', 'MKNTA11111'),\
                ('mclnnes', 'MKNS111111'), ('mclntosh', 'MKNTS11111'),\
                ('mclntvre', 'MKNTFA1111'), ('mclntyre', 'MKNTA11111'),\
                ('mcloud', 'MKLT111111'), ('mcloughlin', 'MKLLN11111'),\
                ('mclure', 'MKLA111111'), ('mcluskey', 'MKLSKA1111'),\
                ('mclusky', 'MKLSKA1111'), ('mclver', 'MKFA111111'),\
                ('mclvor', 'MKFA111111'), ('mcmahon', 'MKMN111111'),\
                ('mcmann', 'MKMN111111'), ('mcmannes', 'MKMNS11111'),\
                ('mcmanus', 'MKMNS11111'), ('mcmaster', 'MKMSTA1111'),\
                ('mcmath', 'MKMT111111'), ('mcmeeking', 'MKMKNK1111'),\
                ('mcmillan', 'MKMLN11111'), ('mcmillen', 'MKMLN11111'),\
                ('mcminn', 'MKMN111111'), ('mcmorran', 'MKMRN11111'),\
                ('mcmulen', 'MKMLN11111'), ('mcmullan', 'MKMLN11111'),\
                ('mcmullen', 'MKMLN11111'), ('mcmurray', 'MKMRA11111'),\
                ('mcmurtrie', 'MKMTRA1111'), ('mcnab', 'MKNP111111'),\
                ('mcnair', 'MKNA111111'), ('mcnally', 'MKNLA11111'),\
                ('mcnalty', 'MKNTA11111'), ('mcnama', 'MKNMA11111'),\
                ('mcnamara', 'MKNMRA1111'), ('mcnamee', 'MKNMA11111'),\
                ('mcnarey', 'MKNRA11111'), ('mcnarry', 'MKNRA11111'),\
                ('mcnatty', 'MKNTA11111'), ('mcnaught', 'MKNT111111'),\
                ('mcnaughton', 'MKNTN11111'), ('mcnauglton', 'MKNKTN1111'),\
                ('mcnee', 'MKNA111111'), ('mcneil', 'MKNA111111'),\
                ('mcneill', 'MKNA111111'), ('mcneish', 'MKNS111111'),\
                ('mcnicol', 'MKNKA11111'), ('mcnicoll', 'MKNKA11111'),\
                ('mcnie', 'MKNA111111'), ('mcniel', 'MKNA111111'),\
                ('mcnish', 'MKNS111111'), ('mcnoe', 'MKNA111111'),\
                ('mcnulty', 'MKNTA11111'), ('mcnultz', 'MKNTS11111'),\
                ('mconie', 'MKNA111111'), ('mcouarrie', 'MKRA111111'),\
                ('mcoueen', 'MKN1111111'), ('mcowan', 'MKWN111111'),\
                ('mcpate', 'MKPT111111'), ('mcpeak', 'MKPK111111'),\
                ('mcphail', 'MKFA111111'), ('mcpheat', 'MKFT111111'),\
                ('mcphee', 'MKFA111111'), ('mcphersoll', 'MKFSA11111'),\
                ('mcpherson', 'MKFSN11111'), ('mcquaid', 'MKT1111111'),\
                ('mcquarrie', 'MKRA111111'), ('mcqueen', 'MKN1111111'),\
                ('mcquilty', 'MKTA111111'), ('mcrae', 'MKRA111111'),\
                ('mcritchie', 'MKRKA11111'), ('mcrobie', 'MKRPA11111'),\
                ('mcrohie', 'MKRA111111'), ('mcshain', 'MKSN111111'),\
                ('mcshaw', 'MKSA111111'), ('mcskimming', 'MKSKMNK111'),\
                ('mcsoriley', 'MKSRLA1111'), ('mcsorlay', 'MKSLA11111'),\
                ('mcsourley', 'MKSLA11111'), ('mcstay', 'MKSTA11111'),\
                ('mcswan', 'MKSWN11111'), ('mcsweeney', 'MKSWNA1111'),\
                ('mcsweeny', 'MKSWNA1111'), ('mctaggart', 'MKTKT11111'),\
                ('mctagget', 'MKTKT11111'), ('mctaggett', 'MKTKT11111'),\
                ('mctague', 'MKTKA11111'), ('mctainsh', 'MKTNS11111'),\
                ('mctamney', 'MKTMNA1111'), ('mctavish', 'MKTFS11111'),\
                ('mcternan', 'MKTNN11111'), ('mctigue', 'MKTKA11111'),\
                ('mcveigh', 'MKFA111111'), ('mcvey', 'MKFA111111'),\
                ('mcvicar', 'MKFKA11111'), ('mcvickar', 'MKFKA11111'),\
                ('mcvicker', 'MKFKA11111'), ('mcvie', 'MKFA111111'),\
                ('mcwatt', 'MKWT111111'), ('mcwen', 'MKWN111111'),\
                ('mcwilliam', 'MKWLM11111'), ('mcwillian', 'MKWLN11111'),\
                ('mead', 'MT11111111'), ('meade', 'MT11111111'),\
                ('meadowcroft', 'MTKRFT1111'), ('meadows', 'MTS1111111'),\
                ('mearns', 'MNS1111111'), ('mears', 'MS11111111'),\
                ('mechaelis', 'MKLS111111'), ('mechen', 'MKN1111111'),\
                ('mecracken', 'MKRKN11111'), ('medder', 'MTA1111111'),\
                ('meder', 'MTA1111111'), ('medhurst', 'MTST111111'),\
                ('medley', 'MTLA111111'), ('medlicott', 'MTLKT11111'),\
                ('medlin', 'MTLN111111'), ('mee', 'MA11111111'),\
                ('meehan', 'MN11111111'), ('meek', 'MK11111111'),\
                ('meekin', 'MKN1111111'), ('meekison', 'MKSN111111'),\
                ('meeks', 'MKS1111111'), ('meenan', 'MNN1111111'),\
                ('meevoy', 'MFA1111111'), ('mefarlane', 'MFLN111111'),\
                ('meffan', 'MFN1111111'), ('mefie', 'MFA1111111'),\
                ('mehalski', 'MSKA111111'), ('meighan', 'MKN1111111'),\
                ('meikle', 'MKA1111111'), ('meiklejohn', 'MKLN111111'),\
                ('meiklejolm', 'MKLM111111'), ('meikljohn', 'MKLN111111'),\
                ('meinung', 'MNNK111111'), ('meivor', 'MFA1111111'),\
                ('mekee', 'MKA1111111'), ('mekenzie', 'MKNSA11111'),\
                ('meldrum', 'MTRM111111'), ('melean', 'MLN1111111'),\
                ('melhop', 'MP11111111'), ('melitus', 'MLTS111111'),\
                ('melladew', 'MLTA111111'), ('mellars', 'MLS1111111'),\
                ('mellett', 'MLT1111111'), ('mellon', 'MLN1111111'),\
                ('mellor', 'MLA1111111'), ('melrose', 'MRS1111111'),\
                ('melser', 'MSA1111111'), ('melton', 'MTN1111111'),\
                ('melville', 'MFA1111111'), ('melvin', 'MFN1111111'),\
                ('melvlle', 'MFA1111111'), ('mendelsohn', 'MNTSN11111'),\
                ('mendoza', 'MNTSA11111'), ('menhinick', 'MNNK111111'),\
                ('menlove', 'MNLF111111'), ('menton', 'MNTN111111'),\
                ('menzies', 'MNSS111111'), ('mercer', 'MSA1111111'),\
                ('merchant', 'MKNT111111'), ('mercier', 'MSA1111111'),\
                ('meredith', 'MRTT111111'), ('merrie', 'MRA1111111'),\
                ('merry', 'MRA1111111'), ('mervyn', 'MFN1111111'),\
                ('messenger', 'MSNKA11111'), ('messent', 'MSNT111111'),\
                ('messer', 'MSA1111111'), ('meston', 'MSTN111111'),\
                ('met', 'MT11111111'), ('metcalf', 'MTKF111111'),\
                ('metcalfe', 'MTKF111111'), ('methers', 'MTS1111111'),\
                ('methven', 'MTFN111111'), ('metson', 'MTSN111111'),\
                ('metz', 'MTS1111111'), ('mew', 'MA11111111'),\
                ('mewhinney', 'MWNA111111'), ('meyer', 'MA11111111'),\
                ('michael', 'MKA1111111'), ('michaelis', 'MKLS111111'),\
                ('michelle', 'MKA1111111'), ('michie', 'MKA1111111'),\
                ('middendorf', 'MTNTF11111'), ('middlebrook', 'MTLPRK1111'),\
                ('middleditch', 'MTLTK11111'), ('middlemass', 'MTLMS11111'),\
                ('middlemiss', 'MTLMS11111'), ('middleton', 'MTLTN11111'),\
                ('midgley', 'MKLA111111'), ('miils', 'MS11111111'),\
                ('mil1er', 'MLA1111111'), ('milbum', 'MPM1111111'),\
                ('milburn', 'MPN1111111'), ('milburne', 'MPN1111111'),\
                ('mildenhall', 'MTNA111111'), ('miles', 'MLS1111111'),\
                ('milgrove', 'MKRF111111'), ('milis', 'MLS1111111'),\
                ('mill', 'MA11111111'), ('millar', 'MLA1111111'),\
                ('millard', 'MLT1111111'), ('millca', 'MKA1111111'),\
                ('millea', 'MLA1111111'), ('millen', 'MLN1111111'),\
                ('miller', 'MLA1111111'), ('millet', 'MLT1111111'),\
                ('millian', 'MLN1111111'), ('millie', 'MLA1111111'),\
                ('milligan', 'MLKN111111'), ('milliken', 'MLKN111111'),\
                ('millin', 'MLN1111111'), ('milliner', 'MLNA111111'),\
                ('millington', 'MLNKTN1111'), ('millow', 'MLA1111111'),\
                ('mills', 'MS11111111'), ('milne', 'MN11111111'),\
                ('milner', 'MNA1111111'), ('milnes', 'MNS1111111'),\
                ('milsom', 'MSM1111111'), ('milton', 'MTN1111111'),\
                ('milward', 'MWT1111111'), ('mindo', 'MNTA111111'),\
                ('mine', 'MN11111111'), ('minehan', 'MNN1111111'),\
                ('miners', 'MNS1111111'), ('minihan', 'MNN1111111'),\
                ('minn', 'MN11111111'), ('minton', 'MNTN111111'),\
                ('mirams', 'MRMS111111'), ('miscall', 'MSKA111111'),\
                ('miskel', 'MSKA111111'), ('missen', 'MSN1111111'),\
                ('mitchall', 'MKA1111111'), ('mitchel', 'MKA1111111'),\
                ('mitchell', 'MKA1111111'), ('mitehell', 'MTA1111111'),\
                ('mitson', 'MTSN111111'), ('mitten', 'MTN1111111'),\
                ('mlburn', 'MPN1111111'), ('mlls', 'MS11111111'),\
                ('mnlloy', 'MNLA111111'), ('moar', 'MA11111111'),\
                ('moara', 'MRA1111111'), ('mobbs', 'MPS1111111'),\
                ('mockford', 'MKFT111111'), ('mockler', 'MKLA111111'),\
                ('modonald', 'MTNT111111'), ('moen', 'MN11111111'),\
                ('moffat', 'MFT1111111'), ('moffatt', 'MFT1111111'),\
                ('moffett', 'MFT1111111'), ('moffitt', 'MFT1111111'),\
                ('mogie', 'MKA1111111'), ('moher', 'MA11111111'),\
                ('moir', 'MA11111111'), ('moirison', 'MRSN111111'),\
                ('mokenzie', 'MKNSA11111'), ('moles', 'MLS1111111'),\
                ('moller', 'MLA1111111'), ('mollison', 'MLSN111111'),\
                ('molloy', 'MLA1111111'), ('moloney', 'MLNA111111'),\
                ('molonoy', 'MLNA111111'), ('mona', 'MNA1111111'),\
                ('monaghan', 'MNKN111111'), ('monagon', 'MNKN111111'),\
                ('monahan', 'MNN1111111'), ('monckton', 'MNKTN11111'),\
                ('moncrieff', 'MNKRF11111'), ('moncrieft', 'MNKRFT1111'),\
                ('moncur', 'MNKA111111'), ('mong', 'MNK1111111'),\
                ('monihan', 'MNN1111111'), ('monk', 'MNK1111111'),\
                ('monkman', 'MNKMN11111'), ('monro', 'MNRA111111'),\
                ('monson', 'MNSN111111'), ('montague', 'MNTKA11111'),\
                ('monteath', 'MNTT111111'), ('monteith', 'MNTT111111'),\
                ('montgomery', 'MNTKMRA111'), ('montgomor', 'MNTKMA1111'),\
                ('montgoner', 'MNTKNA1111'), ('moodie', 'MTA1111111'),\
                ('moody', 'MTA1111111'), ('moon', 'MN11111111'),\
                ('mooney', 'MNA1111111'), ('moor', 'MA11111111'),\
                ('moore-wrig', 'MRRK111111'), ('moore-wright', 'MRRT111111'),\
                ('moore', 'MA11111111'), ('moorehead', 'MRT1111111'),\
                ('moores', 'MRS1111111'), ('moorhonse', 'MNS1111111'),\
                ('moorhouse', 'MS11111111'), ('mora', 'MRA1111111'),\
                ('moran', 'MRN1111111'), ('more', 'MA11111111'),\
                ('moreland', 'MRLNT11111'), ('morell', 'MRA1111111'),\
                ('moreton', 'MRTN111111'), ('morgan roberts', 'MKNRPTS111'),\
                ('morgan-roberts', 'MKNRPTS111'), ('morgan', 'MKN1111111'),\
                ('morgon', 'MKN1111111'), ('moriarty', 'MRTA111111'),\
                ('morice', 'MRK1111111'), ('moriee', 'MRA1111111'),\
                ('morison', 'MRSN111111'), ('moritzson', 'MRTSN11111'),\
                ('morkane', 'MKN1111111'), ('morland', 'MLNT111111'),\
                ('morley', 'MLA1111111'), ('moro', 'MRA1111111'),\
                ('moroney', 'MRNA111111'), ('morpeth', 'MPT1111111'),\
                ('morrall', 'MRA1111111'), ('morrell', 'MRA1111111'),\
                ('morris', 'MRS1111111'), ('morrisey', 'MRSA111111'),\
                ('morrison', 'MRSN111111'), ('morriss', 'MRS1111111'),\
                ('morrissey', 'MRSA111111'), ('morrow', 'MRA1111111'),\
                ('mortimer', 'MTMA111111'), ('morton', 'MTN1111111'),\
                ('morwood', 'MWT1111111'), ('moseley', 'MSLA111111'),\
                ('moses', 'MSS1111111'), ('mosley', 'MSLA111111'),\
                ('moss', 'MS11111111'), ('mothes', 'MTS1111111'),\
                ('motion', 'MSN1111111'), ('mouat', 'MT11111111'),\
                ('moulin', 'MLN1111111'), ('mount', 'MNT1111111'),\
                ('mountford', 'MNTFT11111'), ('mountney', 'MNTNA11111'),\
                ('mouritsen', 'MRTSN11111'), ('mowat', 'MWT1111111'),\
                ('mowatt', 'MWT1111111'), ('mowbray', 'MPRA111111'),\
                ('mower', 'MWA1111111'), ('mowhray', 'MRA1111111'),\
                ('moyal', 'MA11111111'), ('moyle', 'MA11111111'),\
                ('moynihan', 'MNN1111111'), ('mudge', 'MK11111111'),\
                ('mueller', 'MLA1111111'), ('muiorhead', 'MT11111111'),\
                ('muir', 'MA11111111'), ('muirbead', 'MPT1111111'),\
                ('muirhead', 'MT11111111'), ('muithead', 'MTT1111111'),\
                ('mulcahy', 'MKA1111111'), ('mulch', 'MK11111111'),\
                ('muldowney', 'MTNA111111'), ('mulgrew', 'MKRA111111'),\
                ('mulhern', 'MN11111111'), ('mulhollan', 'MLN1111111'),\
                ('mulholland', 'MLNT111111'), ('mullally', 'MLLA111111'),\
                ('mullaly', 'MLLA111111'), ('mullan', 'MLN1111111'),\
                ('mullay', 'MLA1111111'), ('mullen', 'MLN1111111'),\
                ('mullholland', 'MLNT111111'), ('mulligan', 'MLKN111111'),\
                ('mullin', 'MLN1111111'), ('mulling', 'MLNK111111'),\
                ('mullins', 'MLNS111111'), ('mulloy', 'MLA1111111'),\
                ('mulqueen', 'MKN1111111'), ('mulquin', 'MKN1111111'),\
                ('mulrine', 'MRN1111111'), ('mulrooney', 'MRNA111111'),\
                ('mulvihill', 'MFA1111111'), ('mumford', 'MMFT111111'),\
                ('muncaster', 'MNKSTA1111'), ('munday', 'MNTA111111'),\
                ('munden', 'MNTN111111'), ('mundie', 'MNTA111111'),\
                ('mundy', 'MNTA111111'), ('munford', 'MNFT111111'),\
                ('munibe', 'MNP1111111'), ('munn', 'MN11111111'),\
                ('munrly', 'MNLA111111'), ('munro', 'MNRA111111'),\
                ('munton', 'MNTN111111'), ('muntz', 'MNTS111111'),\
                ('muray', 'MRA1111111'), ('murch', 'MK11111111'),\
                ('murchison', 'MKSN111111'), ('murchland', 'MKLNT11111'),\
                ('murcott', 'MKT1111111'), ('murdie', 'MTA1111111'),\
                ('murdoch', 'MTK1111111'), ('murdock', 'MTK1111111'),\
                ('murdoeh', 'MTA1111111'), ('murfitt', 'MFT1111111'),\
                ('murie', 'MRA1111111'), ('murison', 'MRSN111111'),\
                ('murly', 'MLA1111111'), ('murphy', 'MFA1111111'),\
                ('murray', 'MRA1111111'), ('murrow', 'MRA1111111'),\
                ('murtagh', 'MTA1111111'), ('mussen', 'MSN1111111'),\
                ('mustard', 'MSTT111111'), ('mutch', 'MK11111111'),\
                ('mutimer', 'MTMA111111'), ('mutter', 'MTA1111111'),\
                ('mvers', 'MFS1111111'), ('myers', 'MS11111111'),\
                ('myfert', 'MFT1111111'), ('myles', 'MLS1111111'),\
                ('naesmith', 'NSMT111111'), ('nairn', 'NN11111111'),\
                ('naismith', 'NSMT111111'), ('nalder', 'NTA1111111'),\
                ('nancarrow', 'NNKRA11111'), ('nankivell', 'NNKFA11111'),\
                ('nanney', 'NNA1111111'), ('nantes', 'NNTS111111'),\
                ('naphtali', 'NFTLA11111'), ('napier', 'NPA1111111'),\
                ('napoleon', 'NPLN111111'), ('napper', 'NPA1111111'),\
                ('narracott', 'NRKT111111'), ('nash', 'NS11111111'),\
                ('nasham', 'NSM1111111'), ('nathan', 'NTN1111111'),\
                ('natta', 'NTA1111111'), ('natusch', 'NTSK111111'),\
                ('naughton', 'NTN1111111'), ('naumann', 'NMN1111111'),\
                ('naylon', 'NLN1111111'), ('naylor', 'NLA1111111'),\
                ('neal', 'NA11111111'), ('neale', 'NA11111111'),\
                ('neame', 'NM11111111'), ('neason', 'NSN1111111'),\
                ('neave', 'NF11111111'), ('needham', 'NTM1111111'),\
                ('nees', 'NS11111111'), ('neeve', 'NF11111111'),\
                ('nehoff', 'NF11111111'), ('neil', 'NA11111111'),\
                ('neilands', 'NLNTS11111'), ('neill', 'NA11111111'),\
                ('neilson', 'NSN1111111'), ('neiper', 'NPA1111111'),\
                ('neiss', 'NS11111111'), ('neitch', 'NK11111111'),\
                ('nelilson', 'NLSN111111'), ('nellson', 'NSN1111111'),\
                ('nelon', 'NLN1111111'), ('nelsion', 'NSN1111111'),\
                ('nelslon', 'NSLN111111'), ('nelson-thyberg', 'NSNTPK1111'),\
                ('nelson', 'NSN1111111'), ('nesbett', 'NSPT111111'),\
                ('nesbit', 'NSPT111111'), ('nesbitt', 'NSPT111111'),\
                ('ness', 'NS11111111'), ('nester', 'NSTA111111'),\
                ('neumann', 'NMN1111111'), ('nevill', 'NFA1111111'),\
                ('neville', 'NFA1111111'), ('nevin', 'NFN1111111'),\
                ('nevison', 'NFSN111111'), ('new', 'NA11111111'),\
                ('newall', 'NWA1111111'), ('newands', 'NWNTS11111'),\
                ('newbold', 'NPT1111111'), ('newbound', 'NPNT111111'),\
                ('newbury', 'NPRA111111'), ('newell', 'NWA1111111'),\
                ('newey', 'NWA1111111'), ('newland', 'NLNT111111'),\
                ('newlands', 'NLNTS11111'), ('newman', 'NMN1111111'),\
                ('newmark', 'NMK1111111'), ('newmarsh', 'NMS1111111'),\
                ('newsham-west', 'NSMWST1111'), ('newsome', 'NSM1111111'),\
                ('newson', 'NSN1111111'), ('newton', 'NTN1111111'),\
                ('neylan', 'NLN1111111'), ('neylon', 'NLN1111111'),\
                ('niall', 'NA11111111'), ('nichol', 'NKA1111111'),\
                ('nicholas', 'NKLS111111'), ('nicholis', 'NKLS111111'),\
                ('nicholl', 'NKA1111111'), ('nicholls', 'NKS1111111'),\
                ('nichols', 'NKS1111111'), ('nicholson', 'NKSN111111'),\
                ('nickels', 'NKS1111111'), ('nickoll', 'NKA1111111'),\
                ('nicol', 'NKA1111111'), ('nicoll', 'NKA1111111'),\
                ('nicolson', 'NKSN111111'), ('nielson', 'NSN1111111'),\
                ('nieper', 'NPA1111111'), ('nightingale', 'NTNKA11111'),\
                ('nikander', 'NKNTA11111'), ('nikel', 'NKA1111111'),\
                ('niles', 'NLS1111111'), ('nilson', 'NSN1111111'),\
                ('nilsson', 'NSN1111111'), ('nimmo', 'NMA1111111'),\
                ('nina', 'NNA1111111'), ('nind', 'NNT1111111'),\
                ('ninian', 'NNN1111111'), ('nisbet', 'NSPT111111'),\
                ('nisbitt', 'NSPT111111'), ('nissen', 'NSN1111111'),\
                ('niven', 'NFN1111111'), ('nixon', 'NKN1111111'),\
                ('nixson', 'NKSN111111'), ('noble', 'NPA1111111'),\
                ('nohar', 'NA11111111'), ('nolan', 'NLN1111111'),\
                ('noonal', 'NNA1111111'), ('noonan', 'NNN1111111'),\
                ('noone', 'NN11111111'), ('norden', 'NTN1111111'),\
                ('norman', 'NMN1111111'), ('norris', 'NRS1111111'),\
                ('norrish', 'NRS1111111'), ('north', 'NT11111111'),\
                ('northcoat', 'NTKT111111'), ('northey', 'NTA1111111'),\
                ('norton taylor', 'NTNTLA1111'), ('norton-taylor', 'NTNTLA1111'),\
                ('norton', 'NTN1111111'), ('norwood', 'NWT1111111'),\
                ('noseda', 'NSTA111111'), ('noster', 'NSTA111111'),\
                ('notlen', 'NTLN111111'), ('notman', 'NTMN111111'),\
                ('nottage', 'NTK1111111'), ('nowland', 'NLNT111111'),\
                ('nowlands', 'NLNTS11111'), ('noy', 'NA11111111'),\
                ('ntowland', 'NTLNT11111'), ('nugent', 'NKNT111111'),\
                ('nunn', 'NN11111111'), ('nunns', 'NNS1111111'),\
                ('nuttall', 'NTA1111111'), ('nutting', 'NTNK111111'),\
                ('nxon', 'NKN1111111'), ('nyhon', 'NN11111111'),\
                ('o \'neil', 'ANA1111111'), ('o sullivan', 'ASLFN11111'),\
                ('o\' kane', 'AKN1111111'), ('o\'\'connor', 'AKNA111111'),\
                ('o\'beirne', 'APN1111111'), ('o\'berg', 'APK1111111'),\
                ('o\'brian', 'APRN111111'), ('o\'briean', 'APRN111111'),\
                ('o\'brien', 'APRN111111'), ('o\'calaghan', 'AKLKN11111'),\
                ('o\'callagh', 'AKLA111111'), ('o\'callaghan', 'AKLKN11111'),\
                ('o\'connell', 'AKNA111111'), ('o\'connor', 'AKNA111111'),\
                ('o\'corrnan', 'AKNN111111'), ('o\'dea', 'ATA1111111'),\
                ('o\'docherty', 'ATKTA11111'), ('o\'donnell', 'ATNA111111'),\
                ('o\'donohue', 'ATNA111111'), ('o\'dowd', 'ATT1111111'),\
                ('o\'driscoll', 'ATRSKA1111'), ('o\'dwyer', 'ATWA111111'),\
                ('o\'farrell', 'AFRA111111'), ('o\'fee', 'AFA1111111'),\
                ('o\'gorman', 'AKMN111111'), ('o\'grady', 'AKRTA11111'),\
                ('o\'hallora', 'ALRA111111'), ('o\'halloran', 'ALRN111111'),\
                ('o\'hara', 'ARA1111111'), ('o\'hare', 'AA11111111'),\
                ('o\'kane', 'AKN1111111'), ('o\'kean', 'AKN1111111'),\
                ('o\'keefe', 'AKF1111111'), ('o\'keeffe', 'AKF1111111'),\
                ('o\'leary', 'ALRA111111'), ('o\'loughlin', 'ALLN111111'),\
                ('o\'mahoney', 'AMNA111111'), ('o\'malley', 'AMLA111111'),\
                ('o\'meara', 'AMRA111111'), ('o\'neil', 'ANA1111111'),\
                ('o\'neill', 'ANA1111111'), ('o\'rawe', 'ARA1111111'),\
                ('o\'regan', 'ARKN111111'), ('o\'reilly', 'ARLA111111'),\
                ('o\'rogan', 'ARKN111111'), ('o\'rourke', 'ARK1111111'),\
                ('o\'shannessy', 'ASNSA11111'),\
                ('o\'shaughnessy', 'ASNSA11111'),\
                ('o\'shea', 'ASA1111111'), ('o\'sullivan', 'ASLFN11111'),\
                ('o\'toole', 'ATA1111111'), ('o1sen', 'ASN1111111'),\
                ('oag', 'AK11111111'), ('oakden', 'AKTN111111'),\
                ('oakes', 'AKS1111111'), ('oare', 'AA11111111'),\
                ('oaten', 'ATN1111111'), ('oates', 'ATS1111111'),\
                ('oben', 'APN1111111'), ('ockwell', 'AKWA111111'),\
                ('ocwell', 'AKWA111111'), ('oddie', 'ATA1111111'),\
                ('odham', 'ATM1111111'), ('oenond', 'ANNT111111'),\
                ('oettli', 'ATLA111111'), ('offen', 'AFN1111111'),\
                ('officer', 'AFSA111111'), ('ofllen', 'AFLN111111'),\
                ('often', 'AFTN111111'), ('ogborne', 'AKPN111111'),\
                ('ogden', 'AKTN111111'), ('ogg', 'AK11111111'),\
                ('ogilvie', 'AKFA111111'), ('ogivie', 'AKFA111111'),\
                ('ogston', 'AKSTN11111'), ('old', 'AT11111111'),\
                ('oldenburg', 'ATNPK11111'), ('oldham', 'ATM1111111'),\
                ('oldman', 'ATMN111111'), ('olds', 'ATS1111111'),\
                ('oley', 'ALA1111111'), ('oliphant', 'ALFNT11111'),\
                ('olive', 'ALF1111111'), ('oliver', 'ALFA111111'),\
                ('ollerensh', 'ALRNS11111'), ('ollerenshaw', 'ALRNSA1111'),\
                ('olliffe', 'ALF1111111'), ('olliver', 'ALFA111111'),\
                ('olsen', 'ASN1111111'), ('olsien', 'ASN1111111'),\
                ('olson', 'ASN1111111'), ('olvie', 'AFA1111111'),\
                ('omand', 'AMNT111111'), ('ombler', 'AMPLA11111'),\
                ('orange', 'ARNK111111'), ('orbell', 'APA1111111'),\
                ('orchard', 'AKT1111111'), ('orchiston', 'AKSTN11111'),\
                ('organ', 'AKN1111111'), ('orlowski', 'ALSKA11111'),\
                ('orlowsli', 'ALSLA11111'), ('orm', 'AM11111111'),\
                ('ormand', 'AMNT111111'), ('ormond', 'AMNT111111'),\
                ('ormrod', 'AMRT111111'), ('ormston', 'AMSTN11111'),\
                ('orpwood', 'APWT111111'), ('orr', 'AA11111111'),\
                ('orton', 'ATN1111111'), ('ory', 'ARA1111111'),\
                ('osborn', 'ASPN111111'), ('osborne', 'ASPN111111'),\
                ('osmand', 'ASMNT11111'), ('osmond', 'ASMNT11111'),\
                ('oson', 'ASN1111111'), ('ostarasch', 'ASTRSK1111'),\
                ('osten', 'ASTN111111'), ('oswald', 'ASWT111111'),\
                ('oswin', 'ASWN111111'), ('otten', 'ATN1111111'),\
                ('otto', 'ATA1111111'), ('ottrey', 'ATRA111111'),\
                ('otway', 'ATWA111111'), ('oudaille', 'ATA1111111'),\
                ('ouinn', 'AN11111111'), ('outram', 'ATRM111111'),\
                ('ovenden', 'AFNTN11111'), ('overell', 'AFRA111111'),\
                ('overton', 'AFTN111111'), ('overtop', 'AFTP111111'),\
                ('owen', 'AWN1111111'), ('owens', 'AWNS111111'),\
                ('owles', 'ALS1111111'), ('oxford', 'AKFT111111'),\
                ('oxiey', 'AKA1111111'), ('ozanne', 'ASN1111111'),\
                ('paap', 'PP11111111'), ('paape', 'PP11111111'),\
                ('paaris', 'PRS1111111'), ('pacey', 'PSA1111111'),\
                ('packer', 'PKA1111111'), ('packfr', 'PKFA111111'),\
                ('packman', 'PKMN111111'), ('padget', 'PKT1111111'),\
                ('padgett', 'PKT1111111'), ('paganini', 'PKNNA11111'),\
                ('page', 'PK11111111'), ('pagel', 'PKA1111111'),\
                ('paget', 'PKT1111111'), ('paimer', 'PMA1111111'),\
                ('painc', 'PNK1111111'), ('paine', 'PN11111111'),\
                ('painter', 'PNTA111111'), ('painton', 'PNTN111111'),\
                ('paisley', 'PSLA111111'), ('palatchie', 'PLKA111111'),\
                ('palenski', 'PLNSKA1111'), ('palleson', 'PLSN111111'),\
                ('pallister', 'PLSTA11111'), ('palmer', 'PMA1111111'),\
                ('palser', 'PSA1111111'), ('pank', 'PNK1111111'),\
                ('panting', 'PNTNK11111'), ('panton', 'PNTN111111'),\
                ('paranthoiene', 'PRNTN11111'), ('parata', 'PRTA111111'),\
                ('parcell', 'PSA1111111'), ('parcells', 'PSS1111111'),\
                ('pargiter', 'PKTA111111'), ('paris', 'PRS1111111'),\
                ('parish', 'PRS1111111'), ('park', 'PK11111111'),\
                ('parke', 'PK11111111'), ('parker', 'PKA1111111'),\
                ('parkes', 'PKS1111111'), ('parkhill', 'PKA1111111'),\
                ('parkin', 'PKN1111111'), ('parkinson', 'PKNSN11111'),\
                ('parler', 'PLA1111111'), ('parlett', 'PLT1111111'),\
                ('parnell', 'PNA1111111'), ('parr', 'PA11111111'),\
                ('parrish', 'PRS1111111'), ('parry', 'PRA1111111'),\
                ('parslow', 'PSLA111111'), ('parsond', 'PSNT111111'),\
                ('parsons', 'PSNS111111'), ('parsonson', 'PSNSN11111'),\
                ('partel', 'PTA1111111'), ('partridge', 'PTRK111111'),\
                ('pasco', 'PSKA111111'), ('pascoe', 'PSKA111111'),\
                ('paskell', 'PSKA111111'), ('passmore', 'PSMA111111'),\
                ('pastor', 'PSTA111111'), ('pastorell', 'PSTRA11111'),\
                ('pastorelli', 'PSTRLA1111'), ('patay', 'PTA1111111'),\
                ('patch', 'PK11111111'), ('patchett', 'PKT1111111'),\
                ('patcrson', 'PTKSN11111'), ('pate', 'PT11111111'),\
                ('paterson', 'PTSN111111'), ('patey', 'PTA1111111'),\
                ('paton', 'PTN1111111'), ('patorson', 'PTSN111111'),\
                ('patrick', 'PTRK111111'), ('pattenden', 'PTNTN11111'),\
                ('patterson', 'PTSN111111'), ('pattillo', 'PTLA111111'),\
                ('pattinson', 'PTNSN11111'), ('pattison', 'PTSN111111'),\
                ('patton', 'PTN1111111'), ('pattorson', 'PTSN111111'),\
                ('pattrick', 'PTRK111111'), ('paul', 'PA11111111'),\
                ('pauley', 'PLA1111111'), ('paulin', 'PLN1111111'),\
                ('paull', 'PA11111111'), ('paviour-smith', 'PFSMT11111'),\
                ('pavioursmith', 'PFSMT11111'), ('pavitt', 'PFT1111111'),\
                ('pavletich', 'PFLTK11111'), ('paxton', 'PKTN111111'),\
                ('pay', 'PA11111111'), ('payne', 'PN11111111'),\
                ('paynter', 'PNTA111111'), ('payton', 'PTN1111111'),\
                ('pcrteous', 'PKTS111111'), ('peace', 'PK11111111'),\
                ('peach', 'PK11111111'), ('peacock', 'PKK1111111'),\
                ('peake', 'PK11111111'), ('pearce', 'PK11111111'),\
                ('pearless', 'PLS1111111'), ('pearn', 'PN11111111'),\
                ('pears', 'PS11111111'), ('pearse', 'PS11111111'),\
                ('pearson', 'PSN1111111'), ('peart', 'PT11111111'),\
                ('peat', 'PT11111111'), ('peate', 'PT11111111'),\
                ('peates', 'PTS1111111'), ('peattie', 'PTA1111111'),\
                ('peck', 'PK11111111'), ('pedder', 'PTA1111111'),\
                ('peddie', 'PTA1111111'), ('peden', 'PTN1111111'),\
                ('pedlar', 'PTLA111111'), ('pedlow', 'PTLA111111'),\
                ('pedofsky', 'PTFSKA1111'), ('peebles', 'PPLS111111'),\
                ('peel', 'PA11111111'), ('pegg', 'PK11111111'),\
                ('peggie', 'PKA1111111'), ('pelatchie', 'PLKA111111'),\
                ('pell', 'PA11111111'), ('pellett', 'PLT1111111'),\
                ('pellowe', 'PLA1111111'), ('pelvin', 'PFN1111111'),\
                ('pemberton', 'PMPTN11111'), ('penfold', 'PNFT111111'),\
                ('penhey', 'PNA1111111'), ('penman', 'PNMN111111'),\
                ('pennell', 'PNA1111111'), ('pennington', 'PNNKTN1111'),\
                ('penno', 'PNA1111111'), ('penny', 'PNA1111111'),\
                ('pennychuick', 'PNKK111111'), ('pennycuick', 'PNKK111111'),\
                ('penpiatt', 'PNPT111111'), ('penrose', 'PNRS111111'),\
                ('penson', 'PNSN111111'), ('pentecost', 'PNTKST1111'),\
                ('penty', 'PNTA111111'), ('peoples', 'PPLS111111'),\
                ('pepper', 'PPA1111111'), ('pepperell', 'PPRA111111'),\
                ('pepperill', 'PPRA111111'), ('peppiatt', 'PPT1111111'),\
                ('peppler', 'PPLA111111'), ('percy', 'PSA1111111'),\
                ('pereira', 'PRRA111111'), ('perera', 'PRRA111111'),\
                ('perfin', 'PFN1111111'), ('perguson', 'PKSN111111'),\
                ('perkins', 'PKNS111111'), ('perks', 'PKS1111111'),\
                ('pernisky', 'PNSKA11111'), ('perrers', 'PRS1111111'),\
                ('perriam', 'PRM1111111'), ('perriman', 'PRMN111111'),\
                ('perrin', 'PRN1111111'), ('perriton', 'PRTN111111'),\
                ('perry', 'PRA1111111'), ('peson', 'PSN1111111'),\
                ('peters', 'PTS1111111'), ('petersen', 'PTSN111111'),\
                ('peterson', 'PTSN111111'), ('petherick', 'PTRK111111'),\
                ('petre', 'PTA1111111'), ('petrie', 'PTRA111111'),\
                ('petterson', 'PTSN111111'), ('pettet', 'PTT1111111'),\
                ('pettigrew', 'PTKRA11111'), ('pettit', 'PTT1111111'),\
                ('pettitt', 'PTT1111111'), ('pfeifer', 'PFFA111111'),\
                ('phair', 'FA11111111'), ('phaup', 'FP11111111'),\
                ('phelan', 'FLN1111111'), ('philip', 'FLP1111111'),\
                ('philips', 'FLPS111111'), ('phillipps', 'FLPS111111'),\
                ('phillips', 'FLPS111111'), ('philp', 'FP11111111'),\
                ('philpott', 'FPT1111111'), ('phimester', 'FMSTA11111'),\
                ('phimister', 'FMSTA11111'), ('picard', 'PKT1111111'),\
                ('pice', 'PK11111111'), ('pickard', 'PKT1111111'),\
                ('picken', 'PKN1111111'), ('pickering', 'PKRNK11111'),\
                ('picket', 'PKT1111111'), ('pickett', 'PKT1111111'),\
                ('pickford', 'PKFT111111'), ('pickles', 'PKLS111111'),\
                ('picklis', 'PKLS111111'), ('pickup', 'PKP1111111'),\
                ('pickworth', 'PKWT111111'), ('picton', 'PKTN111111'),\
                ('piddingto', 'PTNKTA1111'), ('piddington', 'PTNKTN1111'),\
                ('pidduck', 'PTK1111111'), ('pierard', 'PRT1111111'),\
                ('pierce', 'PK11111111'), ('piercy', 'PSA1111111'),\
                ('pigott', 'PKT1111111'), ('pike', 'PK11111111'),\
                ('pilbrow', 'PPRA111111'), ('pile', 'PA11111111'),\
                ('pilet', 'PLT1111111'), ('pilkington', 'PKNKTN1111'),\
                ('pilling', 'PLNK111111'), ('pimley', 'PMLA111111'),\
                ('pinder', 'PNTA111111'), ('pine', 'PN11111111'),\
                ('pinfold', 'PNFT111111'), ('pink', 'PNK1111111'),\
                ('pinkerton', 'PNKTN11111'), ('pinkham', 'PNKM111111'),\
                ('pinkney', 'PNKNA11111'), ('pinnington', 'PNNKTN1111'),\
                ('piper', 'PPA1111111'), ('pirie', 'PRA1111111'),\
                ('pirrett', 'PRT1111111'), ('pistor', 'PSTA111111'),\
                ('pitcher', 'PKA1111111'), ('pitfield', 'PTFT111111'),\
                ('pithie', 'PTA1111111'), ('pitkethley', 'PTKTLA1111'),\
                ('pittaway', 'PTWA111111'), ('pitts', 'PTS1111111'),\
                ('pizey', 'PSA1111111'), ('plaice', 'PLK1111111'),\
                ('plank', 'PLNK111111'), ('plato', 'PLTA111111'),\
                ('plaw', 'PLA1111111'), ('playter', 'PLTA111111'),\
                ('pleace', 'PLK1111111'), ('pledger', 'PLKA111111'),\
                ('plew', 'PLA1111111'), ('plimmer', 'PLMA111111'),\
                ('pluck', 'PLK1111111'), ('plumb', 'PLM1111111'),\
                ('plumley', 'PLMLA11111'), ('plumridge', 'PLMRK11111'),\
                ('plunket', 'PLNKT11111'), ('plunkett', 'PLNKT11111'),\
                ('poat', 'PT11111111'), ('pocklingto', 'PKLNKTA111'),\
                ('pocklington', 'PKLNKTN111'), ('pockson', 'PKSN111111'),\
                ('poff', 'PF11111111'), ('poilock', 'PLK1111111'),\
                ('pointon', 'PNTN111111'), ('poland', 'PLNT111111'),\
                ('polglase', 'PKLS111111'), ('polkinghorn', 'PKNN111111'),\
                ('polkinghorne', 'PKNN111111'), ('pollard', 'PLT1111111'),\
                ('pollett', 'PLT1111111'), ('pollock', 'PLK1111111'),\
                ('polloek', 'PLK1111111'), ('pollon', 'PLN1111111'),\
                ('polson', 'PSN1111111'), ('polwarth', 'PWT1111111'),\
                ('polworth', 'PWT1111111'), ('pomeroy', 'PMRA111111'),\
                ('pomies', 'PMS1111111'), ('ponsford', 'PNSFT11111'),\
                ('pont', 'PNT1111111'), ('ponton', 'PNTN111111'),\
                ('pontor', 'PNTA111111'), ('pool', 'PA11111111'),\
                ('poole', 'PA11111111'), ('pope', 'PP11111111'),\
                ('popham', 'PFM1111111'), ('poppelwell', 'PPWA111111'),\
                ('popperell', 'PPRA111111'), ('popple', 'PPA1111111'),\
                ('poppleton', 'PPLTN11111'), ('porrott', 'PRT1111111'),\
                ('port', 'PT11111111'), ('port.eous', 'PTS1111111'),\
                ('porteous', 'PTS1111111'), ('porter', 'PTA1111111'),\
                ('porthous', 'PTS1111111'), ('porthouse', 'PTS1111111'),\
                ('portwine', 'PTWN111111'), ('potter', 'PTA1111111'),\
                ('potts', 'PTS1111111'), ('poulsen', 'PSN1111111'),\
                ('poulson', 'PSN1111111'), ('poulter', 'PTA1111111'),\
                ('pound', 'PNT1111111'), ('poupart', 'PPT1111111'),\
                ('povey', 'PFA1111111'), ('powe', 'PA11111111'),\
                ('powell', 'PWA1111111'), ('power', 'PWA1111111'),\
                ('powley', 'PLA1111111'), ('poyntz', 'PNTS111111'),\
                ('prain', 'PRN1111111'), ('pratchel', 'PRKA111111'),\
                ('pratt', 'PRT1111111'), ('prattey', 'PRTA111111'),\
                ('prattley', 'PRTLA11111'), ('pratzall', 'PRTSA11111'),\
                ('pratzel', 'PRTSA11111'), ('pre', 'PA11111111'),\
                ('prebble', 'PRPA111111'), ('preddy', 'PRTA111111'),\
                ('preece', 'PRK1111111'), ('preen', 'PRN1111111'),\
                ('prendergast', 'PRNTKST111'), ('prenderville', 'PRNTFA1111'),\
                ('prentice', 'PRNTK11111'), ('presbury', 'PRSPRA1111'),\
                ('prescott', 'PRSKT11111'), ('preston', 'PRSTN11111'),\
                ('pretty', 'PRTA111111'), ('price', 'PRK1111111'),\
                ('prichard', 'PRKT111111'), ('prictor', 'PRKTA11111'),\
                ('pridham', 'PRTM111111'), ('priee', 'PRA1111111'),\
                ('priest', 'PRST111111'), ('priestly', 'PRSTLA1111'),\
                ('prince', 'PRNK111111'), ('pringle', 'PRNKA11111'),\
                ('pringle:', 'PRNKA11111'), ('printz', 'PRNTS11111'),\
                ('prior', 'PRA1111111'), ('priston', 'PRSTN11111'),\
                ('pritchard', 'PRKT111111'), ('pritchett', 'PRKT111111'),\
                ('procter', 'PRKTA11111'), ('proctor', 'PRKTA11111'),\
                ('pronse', 'PRNS111111'), ('propsting', 'PRPSTNK111'),\
                ('prosser', 'PRSA111111'), ('proud', 'PRT1111111'),\
                ('proudfoot', 'PRTFT11111'), ('prouse', 'PRS1111111'),\
                ('prout', 'PRT1111111'), ('provan', 'PRFN111111'),\
                ('proven', 'PRFN111111'), ('provo', 'PRFA111111'),\
                ('prowse', 'PRS1111111'), ('prvde', 'PFT1111111'),\
                ('pryde', 'PRT1111111'), ('pryor', 'PRA1111111'),\
                ('pucchegud', 'PKKT111111'), ('puddy', 'PTA1111111'),\
                ('pullar', 'PLA1111111'), ('puller', 'PLA1111111'),\
                ('pullyn', 'PLN1111111'), ('punch', 'PNK1111111'),\
                ('purcell', 'PSA1111111'), ('purches', 'PKS1111111'),\
                ('purdie', 'PTA1111111'), ('purnell', 'PNA1111111'),\
                ('purtill', 'PTA1111111'), ('purton', 'PTN1111111'),\
                ('purves', 'PFS1111111'), ('purvis', 'PFS1111111'),\
                ('pybus', 'PPS1111111'), ('pye', 'PA11111111'),\
                ('pyke', 'PK11111111'), ('pyle', 'PA11111111'),\
                ('pym', 'PM11111111'), ('pyn', 'PN11111111'),\
                ('pyne', 'PN11111111'), ('pynor', 'PNA1111111'),\
                ('pyott', 'PT11111111'), ('pyper', 'PPA1111111'),\
                ('pyrke', 'PK11111111'), ('pyster', 'PSTA111111'),\
                ('pywell', 'PWA1111111'), ('q uinn', 'KN11111111'),\
                ('qtto', 'KTA1111111'), ('quaid', 'KT11111111'),\
                ('quaife', 'KF11111111'), ('quaile', 'KA11111111'),\
                ('quam', 'KM11111111'), ('quan', 'KN11111111'),\
                ('quarterma', 'KTMA111111'), ('quartermain', 'KTMN111111'),\
                ('quartermaln', 'KTMN111111'), ('quarterman', 'KTMN111111'),\
                ('quelch', 'KK11111111'), ('quennell', 'KNA1111111'),\
                ('queree', 'KRA1111111'), ('quest', 'KST1111111'),\
                ('quested', 'KSTT111111'), ('quickenden', 'KKNTN11111'),\
                ('quickfall', 'KKFA111111'), ('quigg', 'KK11111111'),\
                ('quigley', 'KKLA111111'), ('quill', 'KA11111111'),\
                ('quin', 'KN11111111'), ('quine', 'KN11111111'),\
                ('quinlan', 'KNLN111111'), ('quinn', 'KN11111111'),\
                ('quinton', 'KNTN111111'), ('quirk', 'KK11111111'),\
                ('quirke', 'KK11111111'), ('qvam', 'KFM1111111'),\
                ('rabbidge', 'RPK1111111'), ('rabbitt', 'RPT1111111'),\
                ('rac1kley', 'RKLA111111'), ('race', 'RK11111111'),\
                ('rackham', 'RKM1111111'), ('rackley', 'RKLA111111'),\
                ('radd', 'RT11111111'), ('radford', 'RTFT111111'),\
                ('rae', 'RA11111111'), ('raffills', 'RFS1111111'),\
                ('raglan', 'RKLN111111'), ('raillsford', 'RSFT111111'),\
                ('railton', 'RTN1111111'), ('rainbow', 'RNPA111111'),\
                ('raine', 'RN11111111'), ('raines', 'RNS1111111'),\
                ('rainham', 'RNM1111111'), ('rains', 'RNS1111111'),\
                ('rainsay', 'RNSA111111'), ('rainsford', 'RNSFT11111'),\
                ('rainton', 'RNTN111111'), ('raitt', 'RT11111111'),\
                ('raler', 'RLA1111111'), ('rallinshaw', 'RLNSA11111'),\
                ('ralor', 'RLA1111111'), ('ralph', 'RF11111111'),\
                ('ralston', 'RSTN111111'), ('ralusay', 'RLSA111111'),\
                ('ramage', 'RMK1111111'), ('rambaum', 'RMPM111111'),\
                ('rampton', 'RMPTN11111'), ('ramsay', 'RMSA111111'),\
                ('ramsbottom-isherwood', 'RMSPTMSWT1'),\
                ('ramsden', 'RMSTN11111'),\
                ('ramsey', 'RMSA111111'), ('randal', 'RNTA111111'),\
                ('randall', 'RNTA111111'), ('randell', 'RNTA111111'),\
                ('randle', 'RNTA111111'), ('ranger', 'RNKA111111'),\
                ('rankin', 'RNKN111111'), ('ransay', 'RNSA111111'),\
                ('ransom', 'RNSM111111'), ('raper', 'RPA1111111'),\
                ('rappe', 'RP11111111'), ('rapsom', 'RPSM111111'),\
                ('rapson', 'RPSN111111'), ('rasmussen', 'RSMSN11111'),\
                ('rasrnussen', 'RSNSN11111'), ('rattigan', 'RTKN111111'),\
                ('rattley', 'RTLA111111'), ('rattray', 'RTRA111111'),\
                ('raven', 'RFN1111111'), ('ravenscroft', 'RFNSKRFT11'),\
                ('ravenswood', 'RFNSWT1111'), ('ravenvood', 'RFNFT11111'),\
                ('ravenwood', 'RFNWT11111'), ('rawcliffe', 'RKLF111111'),\
                ('rawe', 'RA11111111'), ('rawei', 'RWA1111111'),\
                ('rawlence', 'RLNK111111'), ('rawley', 'RLA1111111'),\
                ('rawlings', 'RLNKS11111'), ('rawlins', 'RLNS111111'),\
                ('rawlinson', 'RLNSN11111'), ('rawnsley', 'RNSLA11111'),\
                ('rawon', 'RWN1111111'), ('rawson', 'RSN1111111'),\
                ('rawstron', 'RSTRN11111'), ('ray', 'RA11111111'),\
                ('raymond', 'RMNT111111'), ('rayner', 'RNA1111111'),\
                ('rayson', 'RSN1111111'), ('rea', 'RA11111111'),\
                ('read', 'RT11111111'), ('reader', 'RTA1111111'),\
                ('readman', 'RTMN111111'), ('ready', 'RTA1111111'),\
                ('real', 'RA11111111'), ('reardon', 'RTN1111111'),\
                ('reay', 'RA11111111'), ('reddell', 'RTA1111111'),\
                ('redder', 'RTA1111111'), ('reddie', 'RTA1111111'),\
                ('redding', 'RTNK111111'), ('reddington', 'RTNKTN1111'),\
                ('redfearn', 'RTFN111111'), ('redidingto', 'RTTNKTA111'),\
                ('redman', 'RTMN111111'), ('redmayne', 'RTMN111111'),\
                ('redmond', 'RTMNT11111'), ('redwood', 'RTWT111111'),\
                ('reece', 'RK11111111'), ('reed', 'RT11111111'),\
                ('reeder', 'RTA1111111'), ('reekie', 'RKA1111111'),\
                ('rees', 'RS11111111'), ('reeve', 'RF11111111'),\
                ('reeves', 'RFS1111111'), ('reggett', 'RKT1111111'),\
                ('reggiardo', 'RKTA111111'), ('regnault', 'RKNT111111'),\
                ('reid', 'RT11111111'), ('reidboult', 'RTPT111111'),\
                ('reider', 'RTA1111111'), ('reidle', 'RTA1111111'),\
                ('reidy', 'RTA1111111'), ('reilly', 'RLA1111111'),\
                ('reimer', 'RMA1111111'), ('rein', 'RN11111111'),\
                ('reiss', 'RS11111111'), ('rekowski', 'RKSKA11111'),\
                ('remie', 'RMA1111111'), ('remlie', 'RMLA111111'),\
                ('rendall', 'RNTA111111'), ('rendel', 'RNTA111111'),\
                ('render', 'RNTA111111'), ('rendle', 'RNTA111111'),\
                ('renfree', 'RNFRA11111'), ('renfrew', 'RNFRA11111'),\
                ('renney', 'RNA1111111'), ('rennie', 'RNA1111111'),\
                ('rennolds', 'RNTS111111'), ('renton', 'RNTN111111'),\
                ('rentoul', 'RNTA111111'), ('renwick', 'RNWK111111'),\
                ('reny', 'RNA1111111'), ('restieaux', 'RSTK111111'),\
                ('rex', 'RK11111111'), ('reynell', 'RNA1111111'),\
                ('reynolds', 'RNTS111111'), ('rhind', 'NT11111111'),\
                ('rhodes', 'TS11111111'), ('rhynd', 'NT11111111'),\
                ('riach', 'RK11111111'), ('rice', 'RK11111111'),\
                ('rich', 'RK11111111'), ('richard', 'RKT1111111'),\
                ('richardd', 'RKT1111111'), ('richards', 'RKTS111111'),\
                ('richardso', 'RKTSA11111'), ('richardson', 'RKTSN11111'),\
                ('richdale', 'RKTA111111'), ('riches', 'RKS1111111'),\
                ('richmond', 'RKMNT11111'), ('rickard', 'RKT1111111'),\
                ('ridd', 'RT11111111'), ('riddell', 'RTA1111111'),\
                ('riddick', 'RTK1111111'), ('ridding', 'RTNK111111'),\
                ('riddle', 'RTA1111111'), ('riddoch', 'RTK1111111'),\
                ('riddock', 'RTK1111111'), ('rideout', 'RTT1111111'),\
                ('ridgeon', 'RKN1111111'), ('ridgewell', 'RKWA111111'),\
                ('ridgwell', 'RKWA111111'), ('ridland', 'RTLNT11111'),\
                ('ridler', 'RTLA111111'), ('ridley', 'RTLA111111'),\
                ('riederer', 'RTRA111111'), ('riedle', 'RTA1111111'),\
                ('riely', 'RLA1111111'), ('rigby', 'RKPA111111'),\
                ('rigger', 'RKA1111111'), ('riggs', 'RKS1111111'),\
                ('riley', 'RLA1111111'), ('rillstone', 'RSTN111111'),\
                ('rilly', 'RLA1111111'), ('rimeiman', 'RMMN111111'),\
                ('rimmer', 'RMA1111111'), ('rimmington', 'RMNKTN1111'),\
                ('ringer', 'RNKA111111'), ('ringrose', 'RNKRS11111'),\
                ('riorden', 'RTN1111111'), ('ripley', 'RPLA111111'),\
                ('ripp', 'RP11111111'), ('rippin', 'RPN1111111'),\
                ('risk', 'RSK1111111'), ('rissman', 'RSMN111111'),\
                ('ritcbie', 'RTKPA11111'), ('ritchie', 'RKA1111111'),\
                ('ritchle', 'RKA1111111'), ('rittenberg', 'RTNPK11111'),\
                ('rive', 'RF11111111'), ('rivers', 'RFS1111111'),\
                ('rivett', 'RFT1111111'), ('rix', 'RK11111111'),\
                ('rixon', 'RKN1111111'), ('roach', 'RK11111111'),\
                ('roache', 'RK11111111'), ('roan', 'RN11111111'),\
                ('robb', 'RP11111111'), ('robbs', 'RPS1111111'),\
                ('roberston', 'RPSTN11111'), ('robert', 'RPT1111111'),\
                ('roberts', 'RPTS111111'), ('robertsan', 'RPTSN11111'),\
                ('robertshaw', 'RPTSA11111'), ('robertsn', 'RPTSN11111'),\
                ('robertson', 'RPTSN11111'), ('robetrson', 'RPTSN11111'),\
                ('robilliard', 'RPLT111111'), ('robins', 'RPNS111111'),\
                ('robinson', 'RPNSN11111'), ('robjohns', 'RPNS111111'),\
                ('robortson', 'RPTSN11111'), ('robson', 'RPSN111111'),\
                ('rocard', 'RKT1111111'), ('roche', 'RK11111111'),\
                ('rockliff', 'RKLF111111'), ('rodden', 'RTN1111111'),\
                ('roddick', 'RTK1111111'), ('roderique', 'RTRKA11111'),\
                ('rodger', 'RKA1111111'), ('rodgers', 'RKS1111111'),\
                ('rodgerson', 'RKSN111111'), ('rodgrer', 'RKRA111111'),\
                ('rodman', 'RTMN111111'), ('roe', 'RA11111111'),\
                ('roebuck', 'RPK1111111'), ('rogan', 'RKN1111111'),\
                ('rogen', 'RKN1111111'), ('roger', 'RKA1111111'),\
                ('rogers', 'RKS1111111'), ('rogersion', 'RKSN111111'),\
                ('rogerson', 'RKSN111111'), ('roggers', 'RKS1111111'),\
                ('rohan', 'RN11111111'), ('rohertson', 'RTSN111111'),\
                ('roland', 'RLNT111111'), ('rolfe', 'RF11111111'),\
                ('rolinson', 'RLNSN11111'), ('rolland', 'RLNT111111'),\
                ('rollins', 'RLNS111111'), ('rollinson', 'RLNSN11111'),\
                ('rollo', 'RLA1111111'), ('rolson', 'RSN1111111'),\
                ('rolton', 'RTN1111111'), ('romeril', 'RMRA111111'),\
                ('ronald', 'RNT1111111'), ('ronaldson', 'RNTSN11111'),\
                ('rooney', 'RNA1111111'), ('rorley', 'RLA1111111'),\
                ('rosavear', 'RSFA111111'), ('roscow', 'RSKA111111'),\
                ('rose', 'RS11111111'), ('rosenbroc', 'RSNPRK1111'),\
                ('rosenbrock', 'RSNPRK1111'), ('rosenbrook', 'RSNPRK1111'),\
                ('rosenlrock', 'RSNRK11111'), ('rosetta', 'RSTA111111'),\
                ('rosevear', 'RSFA111111'), ('roseveare', 'RSFA111111'),\
                ('rosewarne', 'RSWN111111'), ('rosie', 'RSA1111111'),\
                ('roskilley', 'RSKLA11111'), ('ross', 'RS11111111'),\
                ('rossbotham', 'RSPTM11111'), ('rosser', 'RSA1111111'),\
                ('rossiter', 'RSTA111111'), ('rosson', 'RSN1111111'),\
                ('rothwell', 'RTWA111111'), ('rotting', 'RTNK111111'),\
                ('rough', 'RF11111111'), ('roughan', 'RFN1111111'),\
                ('roulston', 'RSTN111111'), ('round', 'RNT1111111'),\
                ('rourke', 'RK11111111'), ('rousc', 'RSK1111111'),\
                ('rouse', 'RS11111111'), ('rout', 'RT11111111'),\
                ('routledge', 'RTLK111111'), ('routlege', 'RTLK111111'),\
                ('rowan', 'RWN1111111'), ('rowden', 'RTN1111111'),\
                ('rowe', 'RA11111111'), ('rowell', 'RWA1111111'),\
                ('rowland', 'RLNT111111'), ('rowlands', 'RLNTS11111'),\
                ('rowlatt', 'RLT1111111'), ('rowley', 'RLA1111111'),\
                ('rowse', 'RS11111111'), ('roxburgh', 'RKPA111111'),\
                ('roy', 'RA11111111'), ('royal', 'RA11111111'),\
                ('roydhouse', 'RTS1111111'), ('rubinson', 'RPNSN11111'),\
                ('ruck', 'RK11111111'), ('rudd', 'RT11111111'),\
                ('ruddiman', 'RTMN111111'), ('ruddle', 'RTA1111111'),\
                ('ruddy', 'RTA1111111'), ('rudhall', 'RTA1111111'),\
                ('rudkin', 'RTKN111111'), ('rudland', 'RTLNT11111'),\
                ('ruff', 'RF11111111'), ('ruffell', 'RFA1111111'),\
                ('ruhen', 'RN11111111'), ('rule', 'RA11111111'),\
                ('rumble', 'RMPA111111'), ('rumley', 'RMLA111111'),\
                ('rump', 'RMP1111111'), ('rumsey', 'RMSA111111'),\
                ('runcie', 'RNSA111111'), ('runciman', 'RNSMN11111'),\
                ('rundle', 'RNTA111111'), ('rusbatch', 'RSPK111111'),\
                ('rush-munro', 'RSMNRA1111'), ('rush', 'RS11111111'),\
                ('rushton', 'RSTN111111'), ('rushworth', 'RSWT111111'),\
                ('russell', 'RSA1111111'), ('rust', 'RST1111111'),\
                ('ruston', 'RSTN111111'), ('ruth', 'RT11111111'),\
                ('rutherfor', 'RTFA111111'), ('rutherforcl', 'RTFKA11111'),\
                ('rutherford', 'RTFT111111'), ('ruthsatz', 'RTSTS11111'),\
                ('ruthven', 'RTFN111111'), ('rutland', 'RTLNT11111'),\
                ('rutledge', 'RTLK111111'), ('rutter', 'RTA1111111'),\
                ('ruttledge', 'RTLK111111'), ('ryall', 'RA11111111'),\
                ('ryan', 'RN11111111'), ('ryburn', 'RPN1111111'),\
                ('ryder', 'RTA1111111'), ('rylance', 'RLNK111111'),\
                ('rylatt', 'RLT1111111'), ('sabiston', 'SPSTN11111'),\
                ('sachtler', 'SKTLA11111'), ('sadd', 'ST11111111'),\
                ('sadler', 'STLA111111'), ('safey', 'SFA1111111'),\
                ('sagar', 'SKA1111111'), ('sage', 'SK11111111'),\
                ('saggers', 'SKS1111111'), ('saimond', 'SMNT111111'),\
                ('sainsbury', 'SNSPRA1111'), ('salinger', 'SLNKA11111'),\
                ('salisbury', 'SLSPRA1111'), ('sallderson', 'STSN111111'),\
                ('salmon', 'SMN1111111'), ('salmond', 'SMNT111111'),\
                ('salt', 'ST11111111'), ('salter', 'STA1111111'),\
                ('sampson', 'SMPSN11111'), ('samson', 'SMSN111111'),\
                ('samuda', 'SMTA111111'), ('samuel', 'SMA1111111'),\
                ('samuels', 'SMS1111111'), ('sanaway', 'SNWA111111'),\
                ('sand', 'SNT1111111'), ('sanders', 'SNTS111111'),\
                ('sanderson', 'SNTSN11111'), ('sandes', 'SNTS111111'),\
                ('sandey', 'SNTA111111'), ('sandilands', 'SNTLNTS111'),\
                ('sandland', 'SNTLNT1111'), ('sandle', 'SNTA111111'),\
                ('sando', 'SNTA111111'), ('sandom', 'SNTM111111'),\
                ('sandrey', 'SNTRA11111'), ('sandry', 'SNTRA11111'),\
                ('sands', 'SNTS111111'), ('sandys', 'SNTS111111'),\
                ('sangster', 'SNKSTA1111'), ('sansom', 'SNSM111111'),\
                ('sanson', 'SNSN111111'), ('sapsford', 'SPSFT11111'),\
                ('sapwell', 'SPWA111111'), ('sargeant', 'SKNT111111'),\
                ('sarginson', 'SKNSN11111'), ('sarkies', 'SKS1111111'),\
                ('satterthwaite', 'STTWT11111'), ('saul', 'SA11111111'),\
                ('saunders', 'SNTS111111'), ('saunderson', 'SNTSN11111'),\
                ('savage', 'SFK1111111'), ('savigny', 'SFKNA11111'),\
                ('savory', 'SFRA111111'), ('sawers', 'SWS1111111'),\
                ('sawyer', 'SWA1111111'), ('saxby', 'SKPA111111'),\
                ('saxon', 'SKN1111111'), ('saxton', 'SKTN111111'),\
                ('say', 'SA11111111'), ('sayer', 'SA11111111'),\
                ('sayers', 'SS11111111'), ('scager', 'SKKA111111'),\
                ('scaife', 'SKF1111111'), ('scales', 'SKLS111111'),\
                ('scammell', 'SKMA111111'), ('scandrett', 'SKNTRT1111'),\
                ('scanlan', 'SKNLN11111'), ('scanlon', 'SKNLN11111'),\
                ('scannell', 'SKNA111111'), ('scarfe', 'SKF1111111'),\
                ('schapansk', 'SKPNSK1111'), ('schapanski', 'SKPNSKA111'),\
                ('schaper', 'SKPA111111'), ('schaumann', 'SKMN111111'),\
                ('scherek', 'SKRK111111'), ('schlaadt', 'SKLT111111'),\
                ('schluter', 'SKLTA11111'), ('schmaltz', 'SKMTS11111'),\
                ('schmeltz', 'SKMTS11111'), ('schmelz', 'SKMS111111'),\
                ('schmetz', 'SKMTS11111'), ('schmidt', 'SKMT111111'),\
                ('schofield', 'SKFT111111'), ('scholes', 'SKLS111111'),\
                ('schollar', 'SKLA111111'), ('scholtz', 'SKTS111111'),\
                ('schrick', 'SKRK111111'), ('schroeder', 'SKRTA11111'),\
                ('schruffer', 'SKRFA11111'), ('schulenbe', 'SKLNP11111'),\
                ('schulenberg', 'SKLNPK1111'), ('schulenbur', 'SKLNPA1111'),\
                ('schulenburg', 'SKLNPK1111'), ('schultz', 'SKTS111111'),\
                ('schultze', 'SKTS111111'), ('schwartfeger', 'SKWTFKA111'),\
                ('scobie', 'SKPA111111'), ('scoble', 'SKPA111111'),\
                ('scoffeld', 'SKFT111111'), ('scofieid', 'SKFT111111'),\
                ('scofield', 'SKFT111111'), ('scohle', 'SKA1111111'),\
                ('scoles', 'SKLS111111'), ('scollay', 'SKLA111111'),\
                ('scolon', 'SKLN111111'), ('scoones', 'SKNS111111'),\
                ('scores', 'SKRS111111'), ('scorgie', 'SKKA111111'),\
                ('scott', 'SKT1111111'), ('scoular', 'SKLA111111'),\
                ('scouler', 'SKLA111111'), ('scoullar', 'SKLA111111'),\
                ('scrivener', 'SKRFNA1111'), ('scrymgeour', 'SKRMKA1111'),\
                ('scudamore', 'SKTMA11111'), ('scully', 'SKLA111111'),\
                ('sculpher', 'SKFA111111'), ('scurr', 'SKA1111111'),\
                ('seager', 'SKA1111111'), ('seal', 'SA11111111'),\
                ('seales', 'SLS1111111'), ('seaman', 'SMN1111111'),\
                ('seamer', 'SMA1111111'), ('searchfield', 'SKFT111111'),\
                ('searchileld', 'SKLT111111'), ('searl', 'SA11111111'),\
                ('searle', 'SA11111111'), ('season', 'SSN1111111'),\
                ('seath', 'ST11111111'), ('seaton', 'STN1111111'),\
                ('seatree', 'STRA111111'), ('sedal', 'STA1111111'),\
                ('seddon', 'STN1111111'), ('seed', 'ST11111111'),\
                ('seehof', 'SF11111111'), ('seelen', 'SLN1111111'),\
                ('seguin', 'SKN1111111'), ('seherek', 'SRK1111111'),\
                ('seidelin', 'STLN111111'), ('seigle', 'SKA1111111'),\
                ('selby', 'SPA1111111'), ('self', 'SF11111111'),\
                ('selige', 'SLK1111111'), ('sell', 'SA11111111'),\
                ('sellar', 'SLA1111111'), ('sellars', 'SLS1111111'),\
                ('seller', 'SLA1111111'), ('semple', 'SMPA111111'),\
                ('senior', 'SNA1111111'), ('seott', 'ST11111111'),\
                ('seque', 'SKA1111111'), ('service', 'SFK1111111'),\
                ('setter', 'STA1111111'), ('sevenson', 'SFNSN11111'),\
                ('sew hoy', 'SWA1111111'), ('sewart', 'SWT1111111'),\
                ('sewell', 'SWA1111111'), ('sewhoy', 'SWA1111111'),\
                ('sexton', 'SKTN111111'), ('seymour', 'SMA1111111'),\
                ('shackell', 'SKA1111111'), ('shackleton', 'SKLTN11111'),\
                ('shacklock', 'SKLK111111'), ('shadbolt', 'STPT111111'),\
                ('shallcrass', 'SKRS111111'), ('shallish', 'SLS1111111'),\
                ('shalpe', 'SP11111111'), ('shanahan', 'SNN1111111'),\
                ('shand', 'SNT1111111'), ('shankland', 'SNKLNT1111'),\
                ('shanks', 'SNKS111111'), ('shann', 'SN11111111'),\
                ('shannahan', 'SNN1111111'), ('shannon', 'SNN1111111'),\
                ('shardlow', 'STLA111111'), ('sharkey', 'SKA1111111'),\
                ('sharkie', 'SKA1111111'), ('sharp', 'SP11111111'),\
                ('sharpe', 'SP11111111'), ('shaw', 'SA11111111'),\
                ('shea-lawlo', 'SLLA111111'), ('shea-lawlor', 'SLLA111111'),\
                ('shea', 'SA11111111'), ('shearer', 'SRA1111111'),\
                ('shearing', 'SRNK111111'), ('shears', 'SS11111111'),\
                ('shearsby', 'SSPA111111'), ('sheath', 'ST11111111'),\
                ('sheddan', 'STN1111111'), ('sheed', 'ST11111111'),\
                ('sheehan', 'SN11111111'), ('sheehy', 'SA11111111'),\
                ('sheen', 'SN11111111'), ('sheenan', 'SNN1111111'),\
                ('sheldrake', 'STRK111111'), ('shelton', 'STN1111111'),\
                ('shelverton', 'SFTN111111'), ('shene', 'SN11111111'),\
                ('shenken', 'SNKN111111'), ('shennan', 'SNN1111111'),\
                ('shephard', 'SFT1111111'), ('shepherd', 'SFT1111111'),\
                ('shepparcl', 'SPKA111111'), ('sheppard', 'SPT1111111'),\
                ('shepperd', 'SPT1111111'), ('shepphard', 'SPFT111111'),\
                ('sherburd', 'SPT1111111'), ('sherer', 'SRA1111111'),\
                ('sheridan', 'SRTN111111'), ('sheridian', 'SRTN111111'),\
                ('sheriff', 'SRF1111111'), ('sherlaw', 'SLA1111111'),\
                ('sherlock', 'SLK1111111'), ('sherriff', 'SRF1111111'),\
                ('sherwill', 'SWA1111111'), ('sherwood', 'SWT1111111'),\
                ('shieffelbien', 'SFPN111111'), ('shiel', 'SA11111111'),\
                ('shields', 'STS1111111'), ('shiels', 'SS11111111'),\
                ('shier', 'SA11111111'), ('shierlaw', 'SLA1111111'),\
                ('shiffington', 'SFNKTN1111'), ('shilcock', 'SKK1111111'),\
                ('shillum', 'SLM1111111'), ('shilton', 'STN1111111'),\
                ('shine', 'SN11111111'), ('shing', 'SNK1111111'),\
                ('shipman', 'SPMN111111'), ('shirer', 'SRA1111111'),\
                ('shires', 'SRS1111111'), ('shirley', 'SLA1111111'),\
                ('shirreffs', 'SRFS111111'), ('shore', 'SA11111111'),\
                ('shorney', 'SNA1111111'), ('short', 'ST11111111'),\
                ('shortt', 'ST11111111'), ('shrimpton', 'SRMPTN1111'),\
                ('shrubsole', 'SRPSA11111'), ('shuffill', 'SFA1111111'),\
                ('shugar', 'SKA1111111'), ('shutt', 'ST11111111'),\
                ('sibbald', 'SPT1111111'), ('sibley', 'SPLA111111'),\
                ('sickels', 'SKS1111111'), ('sidell', 'STA1111111'),\
                ('sidey', 'STA1111111'), ('sidon', 'STN1111111'),\
                ('sidoy', 'STA1111111'), ('sievwright', 'SFRT111111'),\
                ('silk', 'SK11111111'), ('silken', 'SKN1111111'),\
                ('silsby', 'SSPA111111'), ('silva', 'SFA1111111'),\
                ('silver', 'SFA1111111'), ('silverstone', 'SFSTN11111'),\
                ('silvertsen', 'SFTSN11111'), ('silvester', 'SFSTA11111'),\
                ('silvi', 'SFA1111111'), ('sim', 'SM11111111'),\
                ('sime', 'SM11111111'), ('simeon', 'SMN1111111'),\
                ('simes', 'SMS1111111'), ('simkin', 'SMKN111111'),\
                ('simm', 'SM11111111'), ('simmonds', 'SMNTS11111'),\
                ('simmons', 'SMNS111111'), ('simms', 'SMS1111111'),\
                ('simnons', 'SMNNS11111'), ('simon', 'SMN1111111'),\
                ('simons', 'SMNS111111'), ('simonsen', 'SMNSN11111'),\
                ('simpkins', 'SMPKNS1111'), ('simpson', 'SMPSN11111'),\
                ('sims', 'SMS1111111'), ('simson', 'SMSN111111'),\
                ('sinclair', 'SNKLA11111'), ('sinclait', 'SNKLT11111'),\
                ('sinclar', 'SNKLA11111'), ('sincock', 'SNKK111111'),\
                ('sincok', 'SNKK111111'), ('sing', 'SNK1111111'),\
                ('singleton', 'SNKLTN1111'), ('sings', 'SNKS111111'),\
                ('sinith', 'SNT1111111'), ('sinnamon', 'SNMN111111'),\
                ('sinton', 'SNTN111111'), ('sirnmonds', 'SNMNTS1111'),\
                ('sise', 'SS11111111'), ('sitley', 'STLA111111'),\
                ('sitopson', 'STPSN11111'), ('sivell', 'SFA1111111'),\
                ('sivertsen', 'SFTSN11111'), ('sivewright', 'SFRT111111'),\
                ('sixton', 'SKTN111111'), ('sizen', 'SSN1111111'),\
                ('sizer', 'SSA1111111'), ('skeane', 'SKN1111111'),\
                ('skeels', 'SKS1111111'), ('skeen', 'SKN1111111'),\
                ('skeene', 'SKN1111111'), ('skeet', 'SKT1111111'),\
                ('skelton', 'SKTN111111'), ('skene', 'SKN1111111'),\
                ('skeoch', 'SKK1111111'), ('skerrett', 'SKRT111111'),\
                ('skiffington', 'SKFNKTN111'), ('skilton', 'SKTN111111'),\
                ('skimer', 'SKMA111111'), ('skinner', 'SKNA111111'),\
                ('skipworth', 'SKPWT11111'), ('skirving', 'SKFNK11111'),\
                ('skow', 'SKA1111111'), ('skrimpton', 'SKRMPTN111'),\
                ('skuse', 'SKS1111111'), ('slack', 'SLK1111111'),\
                ('slade', 'SLT1111111'), ('slater', 'SLTA111111'),\
                ('slatter', 'SLTA111111'), ('slattery', 'SLTRA11111'),\
                ('slaughter', 'SLTA111111'), ('slee', 'SLA1111111'),\
                ('sleeman', 'SLMN111111'), ('slemint', 'SLMNT11111'),\
                ('slent', 'SLNT111111'), ('slight', 'SLT1111111'),\
                ('sligo', 'SLKA111111'), ('slinner', 'SLNA111111'),\
                ('sloan', 'SLN1111111'), ('sloper', 'SLPA111111'),\
                ('slovley', 'SLFLA11111'), ('slowey', 'SLWA111111'),\
                ('slowley', 'SLLA111111'), ('slowly', 'SLLA111111'),\
                ('slyfield', 'SLFT111111'), ('smail', 'SMA1111111'),\
                ('smaill', 'SMA1111111'), ('smales', 'SMLS111111'),\
                ('small', 'SMA1111111'), ('smalley', 'SMLA111111'),\
                ('smallman', 'SMMN111111'), ('smart', 'SMT1111111'),\
                ('smea]', 'SMA1111111'), ('smeal', 'SMA1111111'),\
                ('smear', 'SMA1111111'), ('smeaton', 'SMTN111111'),\
                ('smedley', 'SMTLA11111'), ('smellie', 'SMLA111111'),\
                ('smethurst', 'SMTST11111'), ('smiley', 'SMLA111111'),\
                ('smitb', 'SMTP111111'), ('smith-palmer', 'SMTPMA1111'),\
                ('smith', 'SMT1111111'), ('smither', 'SMTA111111'),\
                ('smithpalmer', 'SMTPMA1111'), ('smithson', 'SMTSN11111'),\
                ('smitl', 'SMTA111111'), ('smolenski', 'SMLNSKA111'),\
                ('smyth', 'SMT1111111'), ('smythe', 'SMT1111111'),\
                ('sneade', 'SNT1111111'), ('sneddon', 'SNTN111111'),\
                ('snell', 'SNA1111111'), ('snelleksz', 'SNLKS11111'),\
                ('snook', 'SNK1111111'), ('snow', 'SNA1111111'),\
                ('snowball', 'SNPA111111'), ('snowden', 'SNTN111111'),\
                ('snowdon', 'SNTN111111'), ('soden', 'STN1111111'),\
                ('solomon', 'SLMN111111'), ('somerviile', 'SMFA111111'),\
                ('somervill', 'SMFA111111'), ('somerville', 'SMFA111111'),\
                ('somes', 'SMS1111111'), ('sommerfield', 'SMFT111111'),\
                ('sommerville', 'SMFA111111'), ('sonntag', 'SNTK111111'),\
                ('sontag', 'SNTK111111'), ('soper', 'SPA1111111'),\
                ('sorenson', 'SRNSN11111'), ('soulsby', 'SSPA111111'),\
                ('soundy', 'SNTA111111'), ('souness', 'SNS1111111'),\
                ('sourdon', 'STN1111111'), ('souter', 'STA1111111'),\
                ('south', 'ST11111111'), ('southall', 'STA1111111'),\
                ('southam', 'STM1111111'), ('southberg', 'STPK111111'),\
                ('southern', 'STN1111111'), ('southey', 'STA1111111'),\
                ('southorn', 'STN1111111'), ('soutter', 'STA1111111'),\
                ('spain', 'SPN1111111'), ('spalding', 'SPTNK11111'),\
                ('spargo', 'SPKA111111'), ('sparks', 'SPKS111111'),\
                ('sparnon', 'SPNN111111'), ('sparrow', 'SPRA111111'),\
                ('spatz', 'SPTS111111'), ('spaul', 'SPA1111111'),\
                ('spavin', 'SPFN111111'), ('spear', 'SPA1111111'),\
                ('spedding', 'SPTNK11111'), ('speden', 'SPTN111111'),\
                ('speid', 'SPT1111111'), ('speight', 'SPT1111111'),\
                ('speir', 'SPA1111111'), ('speirs', 'SPS1111111'),\
                ('spell', 'SPA1111111'), ('spellman', 'SPMN111111'),\
                ('spence', 'SPNK111111'), ('spencer', 'SPNSA11111'),\
                ('spiers', 'SPS1111111'), ('spillane', 'SPLN111111'),\
                ('spinks', 'SPNKS11111'), ('spinner', 'SPNA111111'),\
                ('spiro', 'SPRA111111'), ('spong', 'SPNK111111'),\
                ('spooner', 'SPNA111111'), ('spowart', 'SPWT111111'),\
                ('spragg', 'SPRK111111'), ('spraggon', 'SPRKN11111'),\
                ('sprague', 'SPRKA11111'), ('spratt', 'SPRT111111'),\
                ('spray', 'SPRA111111'), ('spring', 'SPRNK11111'),\
                ('springhall', 'SPRNA11111'), ('sproat', 'SPRT111111'),\
                ('sprott', 'SPRT111111'), ('sproule', 'SPRA111111'),\
                ('sproull', 'SPRA111111'), ('spurden', 'SPTN111111'),\
                ('sputter', 'SPTA111111'), ('squiness', 'SKNS111111'),\
                ('squire', 'SKA1111111'), ('squires', 'SKRS111111'),\
                ('st george', 'STKK111111'), ('stabb', 'STP1111111'),\
                ('stables', 'STPLS11111'), ('stackhouse', 'STKS111111'),\
                ('stade', 'STT1111111'), ('stafford', 'STFT111111'),\
                ('stagpoole', 'STKPA11111'), ('staines', 'STNS111111'),\
                ('stainton', 'STNTN11111'), ('staite', 'STT1111111'),\
                ('stakey', 'STKA111111'), ('stalker', 'STKA111111'),\
                ('stallard', 'STLT111111'), ('stammers', 'STMS111111'),\
                ('stamper', 'STMPA11111'), ('stanafield', 'STNFT11111'),\
                ('stanaway', 'STNWA11111'), ('stanbrook', 'STNPRK1111'),\
                ('standen', 'STNTN11111'), ('standfield', 'STNTFT1111'),\
                ('standring', 'STNTRNK111'), ('stanford', 'STNFT11111'),\
                ('staniford', 'STNFT11111'), ('stanley', 'STNLA11111'),\
                ('stannens', 'STNNS11111'), ('stanners', 'STNS111111'),\
                ('stanton', 'STNTN11111'), ('staples', 'STPLS11111'),\
                ('stapleton', 'STPLTN1111'), ('starham', 'STM1111111'),\
                ('stark', 'STK1111111'), ('starkey', 'STKA111111'),\
                ('starr', 'STA1111111'), ('statham', 'STTM111111'),\
                ('staunton', 'STNTN11111'), ('stead', 'STT1111111'),\
                ('steadman', 'STTMN11111'), ('stedman', 'STTMN11111'),\
                ('stedward', 'STTWT11111'), ('steedman', 'STTMN11111'),\
                ('steeds', 'STTS111111'), ('steel', 'STA1111111'),\
                ('steele', 'STA1111111'), ('steen', 'STN1111111'),\
                ('steensoll', 'STNSA11111'), ('steenson', 'STNSN11111'),\
                ('steffens', 'STFNS11111'), ('steinman', 'STNMN11111'),\
                ('stella', 'STLA111111'), ('stem', 'STM1111111'),\
                ('stempa', 'STMPA11111'), ('stenhouse', 'STNS111111'),\
                ('stennouse', 'STNS111111'), ('stent', 'STNT111111'),\
                ('stentiford', 'STNTFT1111'), ('stepbenson', 'STPNSN1111'),\
                ('stephen', 'STFN111111'), ('stephens', 'STFNS11111'),\
                ('stephenso', 'STFNSA1111'), ('stephenson', 'STFNSN1111'),\
                ('sterart', 'STRT111111'), ('sterling', 'STLNK11111'),\
                ('stesvart', 'STSFT11111'), ('stevart', 'STFT111111'),\
                ('steven', 'STFN111111'), ('stevens', 'STFNS11111'),\
                ('stevenson', 'STFNSN1111'), ('steward', 'STWT111111'),\
                ('stewart', 'STWT111111'), ('stgeorge', 'STKK111111'),\
                ('stichann', 'STKN111111'), ('stichmann', 'STKMN11111'),\
                ('stickman', 'STKMN11111'), ('stiglish', 'STKLS11111'),\
                ('stiles', 'STLS111111'), ('still', 'STA1111111'),\
                ('stinso', 'STNSA11111'), ('stinson', 'STNSN11111'),\
                ('stirling', 'STLNK11111'), ('stiven', 'STFN111111'),\
                ('stobie', 'STPA111111'), ('stock', 'STK1111111'),\
                ('stockdale', 'STKTA11111'), ('stocker', 'STKA111111'),\
                ('stoddart', 'STTT111111'), ('stohr', 'STA1111111'),\
                ('stoke', 'STK1111111'), ('stokes', 'STKS111111'),\
                ('stone', 'STN1111111'), ('stonebrid', 'STNPRT1111'),\
                ('stonebridge', 'STNPRK1111'), ('stoneham', 'STNM111111'),\
                ('stook', 'STK1111111'), ('storer', 'STRA111111'),\
                ('storey', 'STRA111111'), ('storie', 'STRA111111'),\
                ('storm', 'STM1111111'), ('storrie', 'STRA111111'),\
                ('storry', 'STRA111111'), ('stort', 'STT1111111'),\
                ('story', 'STRA111111'), ('stothart', 'STTT111111'),\
                ('stott', 'STT1111111'), ('stout', 'STT1111111'),\
                ('stowell', 'STWA111111'), ('stozepanski', 'STSPNSKA11'),\
                ('strachan', 'STRKN11111'), ('strack', 'STRK111111'),\
                ('strafford', 'STRFT11111'), ('strain', 'STRN111111'),\
                ('strang', 'STRNK11111'), ('strange', 'STRNK11111'),\
                ('stratford', 'STRTFT1111'), ('strathern', 'STRTN11111'),\
                ('stratton', 'STRTN11111'), ('straw', 'STRA111111'),\
                ('strawbridge', 'STRPRK1111'), ('street', 'STRT111111'),\
                ('strickett', 'STRKT11111'), ('stright', 'STRT111111'),\
                ('stringer', 'STRNKA1111'), ('stronach', 'STRNK11111'),\
                ('strong', 'STRNK11111'), ('stroud', 'STRT111111'),\
                ('strouts', 'STRTS11111'), ('struckett', 'STRKT11111'),\
                ('struthers', 'STRTS11111'), ('stuart-miller', 'STTMLA1111'),\
                ('stuart', 'STT1111111'), ('stubbs', 'STPS111111'),\
                ('stubley', 'STPLA11111'), ('stuckey', 'STKA111111'),\
                ('stumbles', 'STMPLS1111'), ('sturgeon', 'STKN111111'),\
                ('sturtevan', 'STTFN11111'), ('styche', 'STK1111111'),\
                ('styles', 'STLS111111'), ('sudden', 'STN1111111'),\
                ('suddens', 'STNS111111'), ('sugden', 'SKTN111111'),\
                ('suilivan', 'SLFN111111'), ('sullivan', 'SLFN111111'),\
                ('sullivar', 'SLFA111111'), ('summerell', 'SMRA111111'),\
                ('summerfield', 'SMFT111111'), ('summers', 'SMS1111111'),\
                ('sumner', 'SMNA111111'), ('sunderland', 'SNTLNT1111'),\
                ('sutcliffe', 'STKLF11111'), ('suter', 'STA1111111'),\
                ('suters', 'STS1111111'), ('sutherlan', 'STLN111111'),\
                ('sutherland', 'STLNT11111'), ('sutherlard', 'STLT111111'),\
                ('sutton', 'STN1111111'), ('swale', 'SWA1111111'),\
                ('swan', 'SWN1111111'), ('swanerton', 'SWNTN11111'),\
                ('swanger', 'SWNKA11111'), ('swann', 'SWN1111111'),\
                ('swanson', 'SWNSN11111'), ('swanston', 'SWNSTN1111'),\
                ('swanwick', 'SWNWK11111'), ('sweeney', 'SWNA111111'),\
                ('sweetman', 'SWTMN11111'), ('sweetnam', 'SWTNM11111'),\
                ('swell', 'SWA1111111'), ('swete', 'SWT1111111'),\
                ('swift', 'SWFT111111'), ('swinburne', 'SWNPN11111'),\
                ('swindley', 'SWNTLA1111'), ('swinley', 'SWNLA11111'),\
                ('swinney', 'SWNA111111'), ('swinton', 'SWNTN11111'),\
                ('switalla', 'SWTLA11111'), ('switalli', 'SWTLA11111'),\
                ('switzer', 'SWTSA11111'), ('syder', 'STA1111111'),\
                ('sydney', 'STNA111111'), ('sykes', 'SKS1111111'),\
                ('syme', 'SM11111111'), ('symes', 'SMS1111111'),\
                ('symington', 'SMNKTN1111'), ('symon', 'SMN1111111'),\
                ('symonds', 'SMNTS11111'), ('syndercombe', 'SNTKM11111'),\
                ('sythes', 'STS1111111'), ('tabor', 'TPA1111111'),\
                ('tackson', 'TKSN111111'), ('taggart', 'TKT1111111'),\
                ('taine', 'TN11111111'), ('tait', 'TT11111111'),\
                ('talbot', 'TPT1111111'), ('talboys', 'TPS1111111'),\
                ('tall', 'TA11111111'), ('tallant', 'TLNT111111'),\
                ('tamblyn', 'TMPLN11111'), ('tanner', 'TNA1111111'),\
                ('tansey', 'TNSA111111'), ('tansleiy', 'TNSLA11111'),\
                ('tansley', 'TNSLA11111'), ('tapley', 'TPLA111111'),\
                ('taplin', 'TPLN111111'), ('tapper', 'TPA1111111'),\
                ('tapson', 'TPSN111111'), ('tarbutt', 'TPT1111111'),\
                ('tarleton', 'TLTN111111'), ('tarlton', 'TTN1111111'),\
                ('tarrant', 'TRNT111111'), ('tartakover', 'TTKFA11111'),\
                ('tarves', 'TFS1111111'), ('tasker', 'TSKA111111'),\
                ('tate', 'TT11111111'), ('tattersal', 'TTSA111111'),\
                ('tattersall', 'TTSA111111'), ('tattersfield', 'TTSFT11111'),\
                ('taunt', 'TNT1111111'), ('tavendale', 'TFNTA11111'),\
                ('taverner', 'TFNA111111'), ('tavlor', 'TFLA111111'),\
                ('tayior', 'TA11111111'), ('tayler', 'TLA1111111'),\
                ('tayles', 'TLS1111111'), ('taylor', 'TLA1111111'),\
                ('teague', 'TKA1111111'), ('teale', 'TA11111111'),\
                ('tearle', 'TA11111111'), ('teasdale', 'TSTA111111'),\
                ('tebbett', 'TPT1111111'), ('teer', 'TA11111111'),\
                ('teesdale', 'TSTA111111'), ('tegg', 'TK11111111'),\
                ('telfer', 'TFA1111111'), ('telford', 'TFT1111111'),\
                ('teller', 'TLA1111111'), ('tempero', 'TMPRA11111'),\
                ('temperton', 'TMPTN11111'), ('templcton', 'TMPKTN1111'),\
                ('temple', 'TMPA111111'), ('templeton', 'TMPLTN1111'),\
                ('tenbeth', 'TNPT111111'), ('tennant', 'TNNT111111'),\
                ('tennent', 'TNNT111111'), ('tennet', 'TNT1111111'),\
                ('tepene', 'TPN1111111'), ('terry', 'TRA1111111'),\
                ('teschner', 'TSKNA11111'), ('teviotdale', 'TFTA111111'),\
                ('thackwel', 'TKWA111111'), ('thiele', 'TA11111111'),\
                ('thin', 'TN11111111'), ('thinn', 'TN11111111'),\
                ('third', 'TT11111111'), ('thom', 'TM11111111'),\
                ('thomas', 'TMS1111111'), ('thomason', 'TMSN111111'),\
                ('thomlinson', 'TMLNSN1111'), ('thompson', 'TMPSN11111'),\
                ('thomson', 'TMSN111111'), ('thonas', 'TNS1111111'),\
                ('thora', 'TRA1111111'), ('thorapson', 'TRPSN11111'),\
                ('thorburn', 'TPN1111111'), ('thorley', 'TLA1111111'),\
                ('thorn', 'TN11111111'), ('thornburg', 'TNPK111111'),\
                ('thornburgh', 'TNPA111111'), ('thornhill', 'TNA1111111'),\
                ('thornicroft', 'TNKRFT1111'), ('thornley', 'TNLA111111'),\
                ('thornton', 'TNTN111111'), ('thorp', 'TP11111111'),\
                ('thotnpson', 'TTNPSN1111'), ('thow', 'TA11111111'),\
                ('throp', 'TRP1111111'), ('thurlow', 'TLA1111111'),\
                ('thurston', 'TSTN111111'), ('thwaites', 'TWTS111111'),\
                ('tibbles', 'TPLS111111'), ('tibbs', 'TPS1111111'),\
                ('tidey', 'TTA1111111'), ('tierney', 'TNA1111111'),\
                ('tighe umbers', 'TKMPS11111'), ('tighe-umbers', 'TKMPS11111'),\
                ('tighe', 'TA11111111'), ('tigheumbers', 'TKMPS11111'),\
                ('tilburn', 'TPN1111111'), ('tilbury', 'TPRA111111'),\
                ('tilley', 'TLA1111111'), ('tilleyshor', 'TLSA111111'),\
                ('tilleyshort', 'TLST111111'), ('tillie', 'TLA1111111'),\
                ('tillyshort', 'TLST111111'), ('tilson', 'TSN1111111'),\
                ('tiltman', 'TTMN111111'), ('tily', 'TLA1111111'),\
                ('timlin', 'TMLN111111'), ('timmings', 'TMNKS11111'),\
                ('timmins', 'TMNS111111'), ('timms', 'TMS1111111'),\
                ('tims', 'TMS1111111'), ('tinnock', 'TNK1111111'),\
                ('tinson', 'TNSN111111'), ('tipa', 'TPA1111111'),\
                ('tippet', 'TPT1111111'), ('tippett', 'TPT1111111'),\
                ('tisdall', 'TSTA111111'), ('titchener', 'TKNA111111'),\
                ('titchner', 'TKNA111111'), ('titclhener', 'TTKNA11111'),\
                ('tither', 'TTA1111111'), ('titohener', 'TTNA111111'),\
                ('tiverner', 'TFNA111111'), ('tizard', 'TST1111111'),\
                ('tlimlin', 'TLMLN11111'), ('tlomson', 'TLMSN11111'),\
                ('tnlley', 'TNLA111111'), ('toal', 'TA11111111'),\
                ('toase', 'TS11111111'), ('tobin', 'TPN1111111'),\
                ('tod', 'TT11111111'), ('toda', 'TTA1111111'),\
                ('todd', 'TT11111111'), ('tofield', 'TFT1111111'),\
                ('tohill', 'TA11111111'), ('tointon', 'TNTN111111'),\
                ('tolley', 'TLA1111111'), ('tolmie', 'TMA1111111'),\
                ('tombs', 'TMPS111111'), ('tomkins', 'TMKNS11111'),\
                ('tomkinson', 'TMKNSN1111'), ('tomlinson', 'TMLNSN1111'),\
                ('tompkins', 'TMPKNS1111'), ('toms', 'TMS1111111'),\
                ('tonar', 'TNA1111111'), ('toner', 'TNA1111111'),\
                ('tones', 'TNS1111111'), ('toneycliffe', 'TNKLF11111'),\
                ('tonkin', 'TNKN111111'), ('tonkinson', 'TNKNSN1111'),\
                ('tonner', 'TNA1111111'), ('tonnor', 'TNA1111111'),\
                ('toohey', 'TA11111111'), ('toohill', 'TA11111111'),\
                ('toohoy', 'TA11111111'), ('tooman', 'TMN1111111'),\
                ('toomer', 'TMA1111111'), ('toomey', 'TMA1111111'),\
                ('tooner', 'TNA1111111'), ('tootell', 'TTA1111111'),\
                ('topp', 'TP11111111'), ('torpey', 'TPA1111111'),\
                ('torrance', 'TRNK111111'), ('torrie', 'TRA1111111'),\
                ('tosh', 'TS11111111'), ('toshack', 'TSK1111111'),\
                ('tosswill', 'TSWA111111'), ('tough', 'TF11111111'),\
                ('tourell', 'TRA1111111'), ('tout', 'TT11111111'),\
                ('towart', 'TWT1111111'), ('towle', 'TA11111111'),\
                ('towler', 'TLA1111111'), ('town', 'TN11111111'),\
                ('towniey', 'TNA1111111'), ('townley', 'TNLA111111'),\
                ('townrow', 'TNRA111111'), ('townsend', 'TNSNT11111'),\
                ('townshend', 'TNSNT11111'), ('towsey', 'TSA1111111'),\
                ('towson', 'TSN1111111'), ('toy', 'TA11111111'),\
                ('toye', 'TA11111111'), ('tracey', 'TRSA111111'),\
                ('tracy', 'TRSA111111'), ('traherne', 'TRN1111111'),\
                ('trail', 'TRA1111111'), ('traill', 'TRA1111111'),\
                ('trainor', 'TRNA111111'), ('tranter', 'TRNTA11111'),\
                ('trapski', 'TRPSKA1111'), ('travena', 'TRFNA11111'),\
                ('traves', 'TRFS111111'), ('travis', 'TRFS111111'),\
                ('traynor', 'TRNA111111'), ('treacy', 'TRSA111111'),\
                ('treadwell', 'TRTWA11111'), ('trebilcock', 'TRPKK11111'),\
                ('tree', 'TRA1111111'), ('treeweek', 'TRWK111111'),\
                ('tregea', 'TRKA111111'), ('tregear', 'TRKA111111'),\
                ('tregilgus', 'TRKKS11111'), ('tregoning', 'TRKNNK1111'),\
                ('tregonning', 'TRKNNK1111'), ('treleaven', 'TRLFN11111'),\
                ('treloar', 'TRLA111111'), ('tremaine', 'TRMN111111'),\
                ('trench', 'TRNK111111'), ('trencll', 'TRNKA11111'),\
                ('trengrove', 'TRNKRF1111'), ('trenwith', 'TRNWT11111'),\
                ('trerise', 'TRRS111111'), ('tressider', 'TRSTA11111'),\
                ('tressler', 'TRSLA11111'), ('trestrail', 'TRSTRA1111'),\
                ('tretheway', 'TRTWA11111'), ('trevarthan', 'TRFTN11111'),\
                ('trevathan', 'TRFTN11111'), ('trevena', 'TRFNA11111'),\
                ('trevenna', 'TRFNA11111'), ('treves', 'TRFS111111'),\
                ('treweek', 'TRWK111111'), ('trewera', 'TRWRA11111'),\
                ('trewern', 'TRWN111111'), ('trewhellar', 'TRWLA11111'),\
                ('trewick', 'TRWK111111'), ('trezise', 'TRSS111111'),\
                ('triggs', 'TRKS111111'), ('trim', 'TRM1111111'),\
                ('trimble', 'TRMPA11111'), ('trimnell', 'TRMNA11111'),\
                ('trinder', 'TRNTA11111'), ('tripp', 'TRP1111111'),\
                ('trnbull', 'TNPA111111'), ('troadic', 'TRTK111111'),\
                ('troomer', 'TRMA111111'), ('troon', 'TRN1111111'),\
                ('trotman', 'TRTMN11111'), ('trott', 'TRT1111111'),\
                ('trotter', 'TRTA111111'), ('trounce', 'TRNK111111'),\
                ('troup', 'TRP1111111'), ('trow', 'TRA1111111'),\
                ('trower', 'TRWA111111'), ('truesdale', 'TRSTA11111'),\
                ('truscott', 'TRSKT11111'), ('try', 'TRA1111111'),\
                ('trythall', 'TRTA111111'), ('tubman', 'TPMN111111'),\
                ('tubmar', 'TPMA111111'), ('tuck', 'TK11111111'),\
                ('tucker', 'TKA1111111'), ('tuckey', 'TKA1111111'),\
                ('tudor', 'TTA1111111'), ('tuite', 'TT11111111'),\
                ('tull', 'TA11111111'), ('tulley', 'TLA1111111'),\
                ('tulloch', 'TLK1111111'), ('tully', 'TLA1111111'),\
                ('tunam', 'TNM1111111'), ('tunnell', 'TNA1111111'),\
                ('tunnicliffe', 'TNKLF11111'), ('tunzelman', 'TNSMN11111'),\
                ('tuohy', 'TA11111111'), ('turley', 'TLA1111111'),\
                ('turlington', 'TLNKTN1111'), ('turllbull', 'TPA1111111'),\
                ('turnbull', 'TNPA111111'), ('turner', 'TNA1111111'),\
                ('turpin', 'TPN1111111'), ('turton', 'TTN1111111'),\
                ('turvey', 'TFA1111111'), ('tustain', 'TSTN111111'),\
                ('tutty', 'TTA1111111'), ('tuxford', 'TKFT111111'),\
                ('tvlee', 'TFLA111111'), ('twaddell', 'TWTA111111'),\
                ('twaddle', 'TWTA111111'), ('tweed', 'TWT1111111'),\
                ('tweedale', 'TWTA111111'), ('tweedie', 'TWTA111111'),\
                ('tweedle', 'TWTA111111'), ('tweedy', 'TWTA111111'),\
                ('twelftree', 'TWFTRA1111'), ('twemlow', 'TWMLA11111'),\
                ('twhigg', 'TWK1111111'), ('twining', 'TWNNK11111'),\
                ('twist', 'TWST111111'), ('twose', 'TWS1111111'),\
                ('tye', 'TA11111111'), ('tylee', 'TLA1111111'),\
                ('tyler', 'TLA1111111'), ('tynan', 'TNN1111111'),\
                ('tyre', 'TA11111111'), ('tyree', 'TRA1111111'),\
                ('tyrie', 'TRA1111111'), ('tyrrell-baxter', 'TRPKTA1111'),\
                ('tyrrell', 'TRA1111111'), ('tysoll', 'TSA1111111'),\
                ('tyson', 'TSN1111111'), ('udy', 'ATA1111111'),\
                ('ufton', 'AFTN111111'), ('umbers', 'AMPS111111'),\
                ('underwood', 'ANTWT11111'), ('unwin', 'ANWN111111'),\
                ('uphill', 'AFA1111111'), ('upson', 'APSN111111'),\
                ('ure', 'AA11111111'), ('uren', 'ARN1111111'),\
                ('urquhart', 'AKT1111111'), ('usher', 'ASA1111111'),\
                ('usherwood', 'ASWT111111'), ('ussher', 'ASA1111111'),\
                ('ussherwood', 'ASWT111111'), ('utteridge', 'ATRK111111'),\
                ('uttley', 'ATLA111111'), ('vaidya', 'FTA1111111'),\
                ('vaile', 'FA11111111'), ('valentine', 'FLNTN11111'),\
                ('valli', 'FLA1111111'), ('valpy', 'FPA1111111'),\
                ('vance', 'FNK1111111'), ('vanes', 'FNS1111111'),\
                ('vann', 'FN11111111'), ('varcoe', 'FKA1111111'),\
                ('varian', 'FRN1111111'), ('varney', 'FNA1111111'),\
                ('vartha', 'FTA1111111'), ('vaughan', 'FKN1111111'),\
                ('veal', 'FA11111111'), ('vedder', 'FTA1111111'),\
                ('veint', 'FNT1111111'), ('veitch', 'FK11111111'),\
                ('ven our', 'FNA1111111'), ('venn', 'FN11111111'),\
                ('venning', 'FNNK111111'), ('venour', 'FNA1111111'),\
                ('vercoe', 'FKA1111111'), ('vere', 'FA11111111'),\
                ('verey', 'FRA1111111'), ('verity', 'FRTA111111'),\
                ('verngreen', 'FNKRN11111'), ('vernon', 'FNN1111111'),\
                ('vette', 'FT11111111'), ('vezey', 'FSA1111111'),\
                ('vial', 'FA11111111'), ('vickers', 'FKS1111111'),\
                ('vickery', 'FKRA111111'), ('vik', 'FK11111111'),\
                ('vile', 'FA11111111'), ('vince', 'FNK1111111'),\
                ('vincent', 'FNSNT11111'), ('vine', 'FN11111111'),\
                ('viney', 'FNA1111111'), ('vintiner', 'FNTNA11111'),\
                ('vintinner', 'FNTNA11111'), ('vintinuer', 'FNTNA11111'),\
                ('virtue', 'FTA1111111'), ('vitharson', 'FTSN111111'),\
                ('vivian', 'FFN1111111'), ('vlietstra', 'FLTSTRA111'),\
                ('voight', 'FT11111111'), ('voigt', 'FKT1111111'),\
                ('voiler', 'FLA1111111'), ('voisey', 'FSA1111111'),\
                ('voller', 'FLA1111111'), ('vosper', 'FSPA111111'),\
                ('voyce', 'FK11111111'), ('voysey', 'FSA1111111'),\
                ('vyner', 'FNA1111111'), ('waby', 'WPA1111111'),\
                ('wacher', 'WKA1111111'), ('wackeldin', 'WKTN111111'),\
                ('wackeldine', 'WKTN111111'), ('wackier', 'WKA1111111'),\
                ('wackilden', 'WKTN111111'), ('wackildene', 'WKTN111111'),\
                ('waddel', 'WTA1111111'), ('waddell', 'WTA1111111'),\
                ('waddle', 'WTA1111111'), ('wade', 'WT11111111'),\
                ('wadie', 'WTA1111111'), ('wadsworth', 'WTSWT11111'),\
                ('waghorn', 'WKN1111111'), ('waghorne', 'WKN1111111'),\
                ('waghornee', 'WKNA111111'), ('wagner', 'WKNA111111'),\
                ('wah', 'WA11111111'), ('wahren', 'WRN1111111'),\
                ('wahrlich', 'WLK1111111'), ('waide', 'WT11111111'),\
                ('waigth', 'WKT1111111'), ('wain', 'WN11111111'),\
                ('wainhouse', 'WNS1111111'), ('waite', 'WT11111111'),\
                ('wakefield', 'WKFT111111'), ('wakelin', 'WKLN111111'),\
                ('wakeling', 'WKLNK11111'), ('walden', 'WTN1111111'),\
                ('waldie', 'WTA1111111'), ('waldren', 'WTRN111111'),\
                ('waldron', 'WTRN111111'), ('wales', 'WLS1111111'),\
                ('wali', 'WLA1111111'), ('walkem', 'WKM1111111'),\
                ('walker', 'WKA1111111'), ('walkern', 'WKN1111111'),\
                ('walkinshaw', 'WKNSA11111'), ('walks', 'WKS1111111'),\
                ('wall', 'WA11111111'), ('wallace', 'WLK1111111'),\
                ('wallen', 'WLN1111111'), ('waller', 'WLA1111111'),\
                ('wallin', 'WLN1111111'), ('walling-jones', 'WLNKNS1111'),\
                ('wallinger', 'WLNKA11111'), ('wallis', 'WLS1111111'),\
                ('walls', 'WS11111111'), ('walmeley', 'WMLA111111'),\
                ('walmsey', 'WMSA111111'), ('walmsley', 'WMSLA11111'),\
                ('walmslsey', 'WMSSA11111'), ('walquest', 'WKST111111'),\
                ('walquist', 'WKST111111'), ('walscott', 'WSKT111111'),\
                ('walsh', 'WS11111111'), ('walter', 'WTA1111111'),\
                ('walters', 'WTS1111111'), ('walton', 'WTN1111111'),\
                ('ward', 'WT11111111'), ('warden', 'WTN1111111'),\
                ('wardrop', 'WTRP111111'), ('wards', 'WTS1111111'),\
                ('ware', 'WA11111111'), ('wares', 'WRS1111111'),\
                ('wark', 'WK11111111'), ('warne', 'WN11111111'),\
                ('warner', 'WNA1111111'), ('warnock', 'WNK1111111'),\
                ('warreil', 'WRA1111111'), ('warrell', 'WRA1111111'),\
                ('warren', 'WRN1111111'), ('warrington', 'WRNKTN1111'),\
                ('warwick', 'WWK1111111'), ('warwood', 'WWT1111111'),\
                ('washer', 'WSA1111111'), ('wason', 'WSN1111111'),\
                ('wassell', 'WSA1111111'), ('waterfield', 'WTFT111111'),\
                ('waterhous', 'WTS1111111'), ('waters', 'WTS1111111'),\
                ('waterson', 'WTSN111111'), ('waterston', 'WTSTN11111'),\
                ('wates', 'WTS1111111'), ('watkins', 'WTKNS11111'),\
                ('watler', 'WTLA111111'), ('watling', 'WTLNK11111'),\
                ('watmough', 'WTMA111111'), ('watsan', 'WTSN111111'),\
                ('watsol1', 'WTSA111111'), ('watson', 'WTSN111111'),\
                ('watt', 'WT11111111'), ('watters', 'WTS1111111'),\
                ('watterson', 'WTSN111111'), ('watts', 'WTS1111111'),\
                ('wattson', 'WTSN111111'), ('waugh', 'WA11111111'),\
                ('way', 'WA11111111'), ('wcatherston', 'KTSTN11111'),\
                ('weaherburn', 'WPN1111111'), ('wealherston', 'WSTN111111'),\
                ('weatherall', 'WTRA111111'), ('weatherbur', 'WTPA111111'),\
                ('weatherburn', 'WTPN111111'), ('weatherell', 'WTRA111111'),\
                ('weatheret', 'WTRT111111'), ('weatherst', 'WTST111111'),\
                ('weathersto', 'WTSTA11111'), ('weatherston', 'WTSTN11111'),\
                ('weatherstone', 'WTSTN11111'), ('weaver', 'WFA1111111'),\
                ('weavers', 'WFS1111111'), ('webb', 'WP11111111'),\
                ('webber', 'WPA1111111'), ('webh', 'WP11111111'),\
                ('webling', 'WPLNK11111'), ('webster', 'WPSTA11111'),\
                ('weddell', 'WTA1111111'), ('wedderspo', 'WTSPA11111'),\
                ('wedderspoo', 'WTSPA11111'), ('wedderspoon', 'WTSPN11111'),\
                ('wedgwood', 'WKWT111111'), ('wedlake', 'WTLK111111'),\
                ('wedlock', 'WTLK111111'), ('weedon', 'WTN1111111'),\
                ('weight', 'WT11111111'), ('weightman', 'WTMN111111'),\
                ('weir', 'WA11111111'), ('welbourn', 'WPN1111111'),\
                ('welch', 'WK11111111'), ('weldon', 'WTN1111111'),\
                ('welham', 'WM11111111'), ('wellard', 'WLT1111111'),\
                ('wellbourn', 'WPN1111111'), ('wellbrock', 'WPRK111111'),\
                ('wellburn', 'WPN1111111'), ('weller', 'WLA1111111'),\
                ('wellesley', 'WLSLA11111'), ('wellington', 'WLNKTN1111'),\
                ('wellman', 'WMN1111111'), ('wells', 'WS11111111'),\
                ('wellsted', 'WSTT111111'), ('welnoski', 'WNSKA11111'),\
                ('welply', 'WPLA111111'), ('welsford', 'WSFT111111'),\
                ('welsh', 'WS11111111'), ('welstead', 'WSTT111111'),\
                ('wenborn', 'WNPN111111'), ('wendelken', 'WNTKN11111'),\
                ('wenlock', 'WNLK111111'), ('wenthersto', 'WNTSTA1111'),\
                ('wentworth', 'WNTWT11111'), ('werner', 'WNA1111111'),\
                ('wesney', 'WSNA111111'), ('wessman', 'WSMN111111'),\
                ('west', 'WST1111111'), ('westake', 'WSTK111111'),\
                ('westbrook', 'WSTPRK1111'), ('westcott', 'WSTKT11111'),\
                ('western', 'WSTN111111'), ('westfield', 'WSTFT11111'),\
                ('westfold', 'WSTFT11111'), ('westlake', 'WSTLK11111'),\
                ('westland', 'WSTLNT1111'), ('weston', 'WSTN111111'),\
                ('westwood', 'WSTWT11111'), ('wetherilt', 'WTRT111111'),\
                ('wethersto', 'WTSTA11111'), ('wetherstone', 'WTSTN11111'),\
                ('wethey', 'WTA1111111'), ('wetney', 'WTNA111111'),\
                ('weyland', 'WLNT111111'), ('weymouth', 'WMT1111111'),\
                ('whaley', 'WLA1111111'), ('wharin', 'WRN1111111'),\
                ('wheatley', 'WTLA111111'), ('wheeier', 'WA11111111'),\
                ('wheelan', 'WLN1111111'), ('wheelel', 'WLA1111111'),\
                ('wheeler', 'WLA1111111'), ('wheeley', 'WLA1111111'),\
                ('wheelwright', 'WRT1111111'), ('whelan', 'WLN1111111'),\
                ('whetter', 'WTA1111111'), ('whibe', 'WP11111111'),\
                ('whileley', 'WLLA111111'), ('whineray', 'WNRA111111'),\
                ('whinray', 'WNRA111111'), ('whipp', 'WP11111111'),\
                ('whiston', 'WSTN111111'), ('whitaker', 'WTKA111111'),\
                ('whitburn', 'WTPN111111'), ('whitcombe', 'WTKM111111'),\
                ('white-pars', 'WTPS111111'), ('white-parsons', 'WTPSNS1111'),\
                ('white', 'WT11111111'), ('whitefield', 'WTFT111111'),\
                ('whitehead', 'WTT1111111'), ('whitehorl', 'WTA1111111'),\
                ('whitehorn', 'WTN1111111'), ('whiteley', 'WTLA111111'),\
                ('whiteside', 'WTST111111'), ('whitfield', 'WTFT111111'),\
                ('whiting', 'WTNK111111'), ('whitley', 'WTLA111111'),\
                ('whitlow', 'WTLA111111'), ('whitney', 'WTNA111111'),\
                ('whito', 'WTA1111111'), ('whitson', 'WTSN111111'),\
                ('whittaker', 'WTKA111111'), ('whittall', 'WTA1111111'),\
                ('whittet', 'WTT1111111'), ('whitticase', 'WTKS111111'),\
                ('whittington', 'WTNKTN1111'), ('whittleston', 'WTLSTN1111'),\
                ('whittlestone', 'WTLSTN1111'), ('whitton', 'WTN1111111'),\
                ('whitty', 'WTA1111111'), ('whvte', 'FT11111111'),\
                ('whyman', 'WMN1111111'), ('whyte', 'WT11111111'),\
                ('wiberg', 'WPK1111111'), ('wicks', 'WKS1111111'),\
                ('wicksteed', 'WKSTT11111'), ('widdowson', 'WTSN111111'),\
                ('wide', 'WT11111111'), ('widhart', 'WTT1111111'),\
                ('wigg', 'WK11111111'), ('wiggins', 'WKNS111111'),\
                ('wight', 'WT11111111'), ('wightman', 'WTMN111111'),\
                ('wiikinson', 'WKNSN11111'), ('wikland', 'WKLNT11111'),\
                ('wilberfoss', 'WPFS111111'), ('wilby', 'WPA1111111'),\
                ('wilcox', 'WKK1111111'), ('wilde', 'WT11111111'),\
                ('wilden', 'WTN1111111'), ('wilder', 'WTA1111111'),\
                ('wildey', 'WTA1111111'), ('wildgoose', 'WKS1111111'),\
                ('wildie', 'WTA1111111'), ('wilding', 'WTNK111111'),\
                ('wildoy', 'WTA1111111'), ('wiles', 'WLS1111111'),\
                ('wiley', 'WLA1111111'), ('wilhelmsen', 'WMSN111111'),\
                ('wilhelmson', 'WMSN111111'), ('wilkeison', 'WKSN111111'),\
                ('wilkerson', 'WKSN111111'), ('wilkie', 'WKA1111111'),\
                ('wilkin', 'WKN1111111'), ('wilkinon', 'WKNN111111'),\
                ('wilkins', 'WKNS111111'), ('wilkinson', 'WKNSN11111'),\
                ('will', 'WA11111111'), ('willcocks', 'WKKS111111'),\
                ('willers', 'WLS1111111'), ('willett', 'WLT1111111'),\
                ('william', 'WLM1111111'), ('williame', 'WLM1111111'),\
                ('williams', 'WLMS111111'), ('williamso', 'WLMSA11111'),\
                ('williamson', 'WLMSN11111'), ('willianson', 'WLNSN11111'),\
                ('williarns', 'WLNS111111'), ('williden', 'WLTN111111'),\
                ('willis', 'WLS1111111'), ('willocks', 'WLKS111111'),\
                ('willon', 'WLN1111111'), ('willox', 'WLK1111111'),\
                ('wills', 'WS11111111'), ('willson', 'WSN1111111'),\
                ('wilmot', 'WMT1111111'), ('wiloy', 'WLA1111111'),\
                ('wilson-brown', 'WSNPRN1111'), ('wilson-pyne', 'WSNPN11111'),\
                ('wilson', 'WSN1111111'), ('wilton', 'WTN1111111'),\
                ('wimpellny', 'WMPNA11111'), ('wimpenny', 'WMPNA11111'),\
                ('winchester', 'WNKSTA1111'), ('winchestor', 'WNKSTA1111'),\
                ('windelburn', 'WNTPN11111'), ('windeler', 'WNTLA11111'),\
                ('winder', 'WNTA111111'), ('winders', 'WNTS111111'),\
                ('windsor', 'WNTSA11111'), ('windus', 'WNTS111111'),\
                ('wine', 'WN11111111'), ('winefield', 'WNFT111111'),\
                ('winepress', 'WNPRS11111'), ('wing', 'WNK1111111'),\
                ('wingfield', 'WNKFT11111'), ('wingham', 'WNM1111111'),\
                ('winkfield', 'WNKFT11111'), ('winn', 'WN11111111'),\
                ('winslade', 'WNSLT11111'), ('winter', 'WNTA111111'),\
                ('winterr', 'WNTA111111'), ('winton', 'WNTN111111'),\
                ('wintrup', 'WNTRP11111'), ('wise', 'WS11111111'),\
                ('wisely', 'WSLA111111'), ('wiseman', 'WSMN111111'),\
                ('wishart', 'WST1111111'), ('wisnesky', 'WSNSKA1111'),\
                ('witchall', 'WKA1111111'), ('witchalls', 'WKS1111111'),\
                ('withecomb', 'WTKM111111'), ('withecombe', 'WTKM111111'),\
                ('witheford', 'WTFT111111'), ('withell', 'WTA1111111'),\
                ('withelmsen', 'WTMSN11111'), ('witherford', 'WTFT111111'),\
                ('withers', 'WTS1111111'), ('withey', 'WTA1111111'),\
                ('withington', 'WTNKTN1111'), ('withnell', 'WTNA111111'),\
                ('withy', 'WTA1111111'), ('witley', 'WTLA111111'),\
                ('witt', 'WT11111111'), ('wix', 'WK11111111'),\
                ('wkitty', 'KTA1111111'), ('wlight', 'LT11111111'),\
                ('wlitticase', 'LTKS111111'), ('woadhead', 'WTT1111111'),\
                ('wohlers', 'WLS1111111'), ('wohlmann', 'WMN1111111'),\
                ('wolf', 'WF11111111'), ('wolfe', 'WF11111111'),\
                ('wolfenden', 'WFNTN11111'), ('wolfinden', 'WFNTN11111'),\
                ('wolgast', 'WKST111111'), ('wolstenhol', 'WSTNA11111'),\
                ('wolstenholme', 'WSTNM11111'), ('wood', 'WT11111111'),\
                ('woodberry', 'WTPRA11111'), ('woodbury', 'WTPRA11111'),\
                ('woodfield', 'WTFT111111'), ('woodford', 'WTFT111111'),\
                ('woodger', 'WKA1111111'), ('woodham', 'WTM1111111'),\
                ('woodhead', 'WTT1111111'), ('woodhill', 'WTA1111111'),\
                ('woodhouse', 'WTS1111111'), ('woodifiel', 'WTFA111111'),\
                ('woodifield', 'WTFT111111'), ('wooding', 'WTNK111111'),\
                ('woodley', 'WTLA111111'), ('woodrow', 'WTRA111111'),\
                ('woods', 'WTS1111111'), ('woodside', 'WTST111111'),\
                ('woodward', 'WTWT111111'), ('wooldridge', 'WTRK111111'),\
                ('woolf', 'WF11111111'), ('woolland', 'WLNT111111'),\
                ('woolley', 'WLA1111111'), ('woolliams', 'WLMS111111'),\
                ('woolnough', 'WNA1111111'), ('wooster', 'WSTA111111'),\
                ('wooton', 'WTN1111111'), ('wootten', 'WTN1111111'),\
                ('wootton', 'WTN1111111'), ('worger', 'WKA1111111'),\
                ('work', 'WK11111111'), ('workman', 'WKMN111111'),\
                ('workn1an', 'WKNN111111'), ('worrall', 'WRA1111111'),\
                ('worsdell', 'WSTA111111'), ('worth', 'WT11111111'),\
                ('worthingt', 'WTNKT11111'), ('worthingto', 'WTNKTA1111'),\
                ('worthington', 'WTNKTN1111'), ('wortley', 'WTLA111111'),\
                ('wotherspoon', 'WTSPN11111'), ('wragge', 'RK11111111'),\
                ('wraggo', 'RKA1111111'), ('wraight', 'RT11111111'),\
                ('wrathall', 'RTA1111111'), ('wrather', 'RTA1111111'),\
                ('wray', 'RA11111111'), ('wreathall', 'RTA1111111'),\
                ('wregglesworth', 'RKLSWT1111'), ('wren', 'RN11111111'),\
                ('wrenn', 'RN11111111'), ('wrght', 'T111111111'),\
                ('wrigglesworth', 'RKLSWT1111'), ('wright', 'RT11111111'),\
                ('wrightson', 'RTSN111111'), ('wrignt', 'RKNT111111'),\
                ('wroblenski', 'RPLNSKA111'), ('wward', 'WT11111111'),\
                ('wyatt', 'WT11111111'), ('wyber', 'WPA1111111'),\
                ('wyborn', 'WPN1111111'), ('wycherley', 'WKLA111111'),\
                ('wyinks', 'WNKS111111'), ('wylie', 'WLA1111111'),\
                ('wyllie', 'WLA1111111'), ('wyman', 'WMN1111111'),\
                ('wyness', 'WNS1111111'), ('wynks', 'WNKS111111'),\
                ('wynn', 'WN11111111'), ('wynne', 'WN11111111'),\
                ('wyse', 'WS11111111'), ('yamm', 'YM11111111'),\
                ('yardley', 'YTLA111111'), ('yarlett', 'YLT1111111'),\
                ('yates', 'YTS1111111'), ('yelds', 'YTS1111111'),\
                ('yelland', 'YLNT111111'), ('yemm', 'YM11111111'),\
                ('yeoman', 'YMN1111111'), ('yerex', 'YRK1111111'),\
                ('yet', 'YT11111111'), ('yip', 'YP11111111'),\
                ('york', 'YK11111111'), ('yorstan', 'YSTN111111'),\
                ('yorston', 'YSTN111111'), ('youds', 'YTS1111111'),\
                ('young kwong', 'YNKWNK1111'), ('young', 'YNK1111111'),\
                ('youngman', 'YNKMN11111'), ('youngson', 'YNKSN11111'),\
                ('yuill', 'YA11111111'), ('zelland', 'SLNT111111'),\
                ('zeller', 'SLA1111111'), ('zimmerman', 'SMMN111111'),\
                ('zouch', 'SK11111111'), ('zwimpfer', 'SWMPFA1111'))
        for w, c in testset:
            self.assertEquals(caverphone(w), c)

    def test_caverphone2_caversham_testset(self):
        # caversham.otago.ac.nz/files/variantNames.csv
        self.assertEquals(caverphone('abernathy'), 'APNTA11111')
        self.assertEquals(caverphone('abernethie'), 'APNTA11111')
        self.assertEquals(caverphone('abernethy'), 'APNTA11111')
        self.assertEquals(caverphone('ailen'), 'ALN1111111')
        self.assertEquals(caverphone('aldridge'), 'ATRK111111')
        self.assertEquals(caverphone('allan'), 'ALN1111111')
        self.assertEquals(caverphone('allen'), 'ALN1111111')
        self.assertEquals(caverphone('andersen'), 'ANTSN11111')
        self.assertEquals(caverphone('anderson'), 'ANTSN11111')
        self.assertEquals(caverphone('andorson'), 'ANTSN11111')
        self.assertEquals(caverphone('applegart'), 'APLKT11111')
        self.assertEquals(caverphone('applegarth'), 'APLKT11111')
        self.assertEquals(caverphone('arnal'), 'ANA1111111')
        self.assertEquals(caverphone('arnel'), 'ANA1111111')
        self.assertEquals(caverphone('bailer'), 'PLA1111111')
        self.assertEquals(caverphone('bailey'), 'PLA1111111')
        self.assertEquals(caverphone('bail'), 'PA11111111')
        self.assertEquals(caverphone('bain'), 'PN11111111')
        self.assertEquals(caverphone('baley'), 'PLA1111111')
        self.assertEquals(caverphone('ball'), 'PA11111111')
        self.assertEquals(caverphone('barclay'), 'PKLA111111')
        self.assertEquals(caverphone('barkla'), 'PKLA111111')
        self.assertEquals(caverphone('barlthrop'), 'PTRP111111')
        self.assertEquals(caverphone('barltrop'), 'PTRP111111')
        self.assertEquals(caverphone('barnett'), 'PNT1111111')
        self.assertEquals(caverphone('barratt'), 'PRT1111111')
        self.assertEquals(caverphone('barrett'), 'PRT1111111')
        self.assertEquals(caverphone('barrie'), 'PRA1111111')
        self.assertEquals(caverphone('barwick'), 'PWK1111111')
        self.assertEquals(caverphone('baylee'), 'PLA1111111')
        self.assertEquals(caverphone('bellet'), 'PLT1111111')
        self.assertEquals(caverphone('bellett'), 'PLT1111111')
        self.assertEquals(caverphone('bell'), 'PA11111111')
        self.assertEquals(caverphone('bennet'), 'PNT1111111')
        self.assertEquals(caverphone('bennett'), 'PNT1111111')
        self.assertEquals(caverphone('bennie'), 'PNA1111111')
        self.assertEquals(caverphone('bernie'), 'PNA1111111')
        self.assertEquals(caverphone('berry'), 'PRA1111111')
        self.assertEquals(caverphone('berwick'), 'PWK1111111')
        self.assertEquals(caverphone('beven'), 'PFN1111111')
        self.assertEquals(caverphone('bevin'), 'PFN1111111')
        self.assertEquals(caverphone('binnie'), 'PNA1111111')
        self.assertEquals(caverphone('birrell'), 'PRA1111111')
        self.assertEquals(caverphone('black'), 'PLK1111111')
        self.assertEquals(caverphone('blakeley'), 'PLKLA11111')
        self.assertEquals(caverphone('blakely'), 'PLKLA11111')
        self.assertEquals(caverphone('blake'), 'PLK1111111')
        self.assertEquals(caverphone('bouchor'), 'PKA1111111')
        self.assertEquals(caverphone('boutcher'), 'PKA1111111')
        self.assertEquals(caverphone('brand'), 'PRNT111111')
        self.assertEquals(caverphone('brandt'), 'PRNT111111')
        self.assertEquals(caverphone('brockie'), 'PRKA111111')
        self.assertEquals(caverphone('brock'), 'PRK1111111')
        self.assertEquals(caverphone('brooke'), 'PRK1111111')
        self.assertEquals(caverphone('brook'), 'PRK1111111')
        self.assertEquals(caverphone('browne'), 'PRN1111111')
        self.assertEquals(caverphone('brown'), 'PRN1111111')
        self.assertEquals(caverphone('bruten'), 'PRTN111111')
        self.assertEquals(caverphone('bruton'), 'PRTN111111')
        self.assertEquals(caverphone('bulger'), 'PKA1111111')
        self.assertEquals(caverphone('bull'), 'PA11111111')
        self.assertEquals(caverphone('burger'), 'PKA1111111')
        self.assertEquals(caverphone('burgess'), 'PKS1111111')
        self.assertEquals(caverphone('burnett'), 'PNT1111111')
        self.assertEquals(caverphone('buttermore'), 'PTMA111111')
        self.assertEquals(caverphone('buttimore'), 'PTMA111111')
        self.assertEquals(caverphone('calder'), 'KTA1111111')
        self.assertEquals(caverphone('caley'), 'KLA1111111')
        self.assertEquals(caverphone('callaghan'), 'KLKN111111')
        self.assertEquals(caverphone('callander'), 'KLNTA11111')
        self.assertEquals(caverphone('callender'), 'KLNTA11111')
        self.assertEquals(caverphone('callighan'), 'KLKN111111')
        self.assertEquals(caverphone('carder'), 'KTA1111111')
        self.assertEquals(caverphone('carley'), 'KLA1111111')
        self.assertEquals(caverphone('carruthers'), 'KRTS111111')
        self.assertEquals(caverphone('carside'), 'KST1111111')
        self.assertEquals(caverphone('caruthers'), 'KRTS111111')
        self.assertEquals(caverphone('case'), 'KS11111111')
        self.assertEquals(caverphone('casey'), 'KSA1111111')
        self.assertEquals(caverphone('cassells'), 'KSS1111111')
        self.assertEquals(caverphone('cassels'), 'KSS1111111')
        self.assertEquals(caverphone('cassidy'), 'KSTA111111')
        self.assertEquals(caverphone('chaplain'), 'KPLN111111')
        self.assertEquals(caverphone('chaplin'), 'KPLN111111')
        self.assertEquals(caverphone('chrisp'), 'KRSP111111')
        self.assertEquals(caverphone('chronican'), 'KRNKN11111')
        self.assertEquals(caverphone('chronichan'), 'KRNKN11111')
        self.assertEquals(caverphone('clarke'), 'KLK1111111')
        self.assertEquals(caverphone('clark'), 'KLK1111111')
        self.assertEquals(caverphone('clent'), 'KLNT111111')
        self.assertEquals(caverphone('clint'), 'KLNT111111')
        self.assertEquals(caverphone('coates'), 'KTS1111111')
        self.assertEquals(caverphone('coats'), 'KTS1111111')
        self.assertEquals(caverphone('conheady'), 'KNTA111111')
        self.assertEquals(caverphone('connell'), 'KNA1111111')
        self.assertEquals(caverphone('connolly'), 'KNLA111111')
        self.assertEquals(caverphone('conolly'), 'KNLA111111')
        self.assertEquals(caverphone('cooke'), 'KK11111111')
        self.assertEquals(caverphone('cook'), 'KK11111111')
        self.assertEquals(caverphone('corcoran'), 'KKRN111111')
        self.assertEquals(caverphone('corkran'), 'KKRN111111')
        self.assertEquals(caverphone('cornell'), 'KNA1111111')
        self.assertEquals(caverphone('cosegrove'), 'KSKRF11111')
        self.assertEquals(caverphone('cosgrove'), 'KSKRF11111')
        self.assertEquals(caverphone('coulter'), 'KTA1111111')
        self.assertEquals(caverphone('coupar'), 'KPA1111111')
        self.assertEquals(caverphone('couper'), 'KPA1111111')
        self.assertEquals(caverphone('courter'), 'KTA1111111')
        self.assertEquals(caverphone('craig'), 'KRK1111111')
        self.assertEquals(caverphone('craik'), 'KRK1111111')
        self.assertEquals(caverphone('crammond'), 'KRMNT11111')
        self.assertEquals(caverphone('cramond'), 'KRMNT11111')
        self.assertEquals(caverphone('crawford'), 'KRFT111111')
        self.assertEquals(caverphone('crawfurd'), 'KRFT111111')
        self.assertEquals(caverphone('cress'), 'KRS1111111')
        self.assertEquals(caverphone('crisp'), 'KRSP111111')
        self.assertEquals(caverphone('crosbie'), 'KRSPA11111')
        self.assertEquals(caverphone('crosby'), 'KRSPA11111')
        self.assertEquals(caverphone('crossan'), 'KRSN111111')
        self.assertEquals(caverphone('crossian'), 'KRSN111111')
        self.assertEquals(caverphone('cruse'), 'KRS1111111')
        self.assertEquals(caverphone('cubbins'), 'KPNS111111')
        self.assertEquals(caverphone('culsey'), 'KSA1111111')
        self.assertEquals(caverphone('cunhingham'), 'KNNM111111')
        self.assertEquals(caverphone('cunningham'), 'KNNM111111')
        self.assertEquals(caverphone('curran'), 'KRN1111111')
        self.assertEquals(caverphone('curren'), 'KRN1111111')
        self.assertEquals(caverphone('cursey'), 'KSA1111111')
        self.assertEquals(caverphone('daly'), 'TLA1111111')
        self.assertEquals(caverphone('davany'), 'TFNA111111')
        self.assertEquals(caverphone('daveis'), 'TFS1111111')
        self.assertEquals(caverphone('davies'), 'TFS1111111')
        self.assertEquals(caverphone('davis'), 'TFS1111111')
        self.assertEquals(caverphone('davys'), 'TFS1111111')
        self.assertEquals(caverphone('delaney'), 'TLNA111111')
        self.assertEquals(caverphone('delany'), 'TLNA111111')
        self.assertEquals(caverphone('delargey'), 'TLKA111111')
        self.assertEquals(caverphone('delargy'), 'TLKA111111')
        self.assertEquals(caverphone('dely'), 'TLA1111111')
        self.assertEquals(caverphone('denfold'), 'TNFT111111')
        self.assertEquals(caverphone('denford'), 'TNFT111111')
        self.assertEquals(caverphone('devaney'), 'TFNA111111')
        self.assertEquals(caverphone('dickison'), 'TKSN111111')
        self.assertEquals(caverphone('dickson'), 'TKSN111111')
        self.assertEquals(caverphone('dillan'), 'TLN1111111')
        self.assertEquals(caverphone('dillon'), 'TLN1111111')
        self.assertEquals(caverphone('dockworth'), 'TKWT111111')
        self.assertEquals(caverphone('dodd'), 'TT11111111')
        self.assertEquals(caverphone('donne'), 'TN11111111')
        self.assertEquals(caverphone('dougall'), 'TKA1111111')
        self.assertEquals(caverphone('dougal'), 'TKA1111111')
        self.assertEquals(caverphone('douglass'), 'TKLS111111')
        self.assertEquals(caverphone('douglas'), 'TKLS111111')
        self.assertEquals(caverphone('dreaver'), 'TRFA111111')
        self.assertEquals(caverphone('dreavor'), 'TRFA111111')
        self.assertEquals(caverphone('droaver'), 'TRFA111111')
        self.assertEquals(caverphone('duckworth'), 'TKWT111111')
        self.assertEquals(caverphone('dunne'), 'TN11111111')
        self.assertEquals(caverphone('dunn'), 'TN11111111')
        self.assertEquals(caverphone('eagan'), 'AKN1111111')
        self.assertEquals(caverphone('eagar'), 'AKA1111111')
        self.assertEquals(caverphone('eager'), 'AKA1111111')
        self.assertEquals(caverphone('easson'), 'ASN1111111')
        self.assertEquals(caverphone('egan'), 'AKN1111111')
        self.assertEquals(caverphone('eldridge'), 'ATRK111111')
        self.assertEquals(caverphone('elliis'), 'ALS1111111')
        self.assertEquals(caverphone('ellis'), 'ALS1111111')
        self.assertEquals(caverphone('emerson'), 'AMSN111111')
        self.assertEquals(caverphone('emmerson'), 'AMSN111111')
        self.assertEquals(caverphone('essson'), 'ASN1111111')
        self.assertEquals(caverphone('fahey'), 'FA11111111')
        self.assertEquals(caverphone('fahy'), 'FA11111111')
        self.assertEquals(caverphone('fail'), 'FA11111111')
        self.assertEquals(caverphone('fairbairn'), 'FPN1111111')
        self.assertEquals(caverphone('fairburn'), 'FPN1111111')
        self.assertEquals(caverphone('faithful'), 'FTFA111111')
        self.assertEquals(caverphone('faithfull'), 'FTFA111111')
        self.assertEquals(caverphone('fall'), 'FA11111111')
        self.assertEquals(caverphone('farminger'), 'FMNKA11111')
        self.assertEquals(caverphone('farry'), 'FRA1111111')
        self.assertEquals(caverphone('feil'), 'FA11111111')
        self.assertEquals(caverphone('fell'), 'FA11111111')
        self.assertEquals(caverphone('fennessey'), 'FNSA111111')
        self.assertEquals(caverphone('fennessy'), 'FNSA111111')
        self.assertEquals(caverphone('ferry'), 'FRA1111111')
        self.assertEquals(caverphone('fiddes'), 'FTS1111111')
        self.assertEquals(caverphone('fiddis'), 'FTS1111111')
        self.assertEquals(caverphone('fielden'), 'FTN1111111')
        self.assertEquals(caverphone('fielder'), 'FTA1111111')
        self.assertEquals(caverphone('findlay'), 'FNTLA11111')
        self.assertEquals(caverphone('findley'), 'FNTLA11111')
        self.assertEquals(caverphone('fitzpatric'), 'FTSPTRK111')
        self.assertEquals(caverphone('fitzpatrick'), 'FTSPTRK111')
        self.assertEquals(caverphone('fraer'), 'FRA1111111')
        self.assertEquals(caverphone('fraher'), 'FRA1111111')
        self.assertEquals(caverphone('fullarton'), 'FLTN111111')
        self.assertEquals(caverphone('fullerton'), 'FLTN111111')
        self.assertEquals(caverphone('furminger'), 'FMNKA11111')
        self.assertEquals(caverphone('gailichan'), 'KLKN111111')
        self.assertEquals(caverphone('galbraith'), 'KPRT111111')
        self.assertEquals(caverphone('gallanders'), 'KLNTS11111')
        self.assertEquals(caverphone('gallaway'), 'KLWA111111')
        self.assertEquals(caverphone('gallbraith'), 'KPRT111111')
        self.assertEquals(caverphone('gallichan'), 'KLKN111111')
        self.assertEquals(caverphone('galloway'), 'KLWA111111')
        self.assertEquals(caverphone('garcho'), 'KKA1111111')
        self.assertEquals(caverphone('garchow'), 'KKA1111111')
        self.assertEquals(caverphone('garret'), 'KRT1111111')
        self.assertEquals(caverphone('garrett'), 'KRT1111111')
        self.assertEquals(caverphone('garside'), 'KST1111111')
        self.assertEquals(caverphone('geddes'), 'KTS1111111')
        self.assertEquals(caverphone('geddis'), 'KTS1111111')
        self.assertEquals(caverphone('georgeison'), 'KKSN111111')
        self.assertEquals(caverphone('george'), 'KK11111111')
        self.assertEquals(caverphone('georgeson'), 'KKSN111111')
        self.assertEquals(caverphone('gillanders'), 'KLNTS11111')
        self.assertEquals(caverphone('gillespie'), 'KLSPA11111')
        self.assertEquals(caverphone('gillispie'), 'KLSPA11111')
        self.assertEquals(caverphone('gilmore'), 'KMA1111111')
        self.assertEquals(caverphone('gilmour'), 'KMA1111111')
        self.assertEquals(caverphone('glendining'), 'KLNTNNK111')
        self.assertEquals(caverphone('glendinning'), 'KLNTNNK111')
        self.assertEquals(caverphone('glendinnin'), 'KLNTNN1111')
        self.assertEquals(caverphone('gorge'), 'KK11111111')
        self.assertEquals(caverphone('graig'), 'KRK1111111')
        self.assertEquals(caverphone('gray'), 'KRA1111111')
        self.assertEquals(caverphone('greeves'), 'KRFS111111')
        self.assertEquals(caverphone('greig'), 'KRK1111111')
        self.assertEquals(caverphone('greves'), 'KRFS111111')
        self.assertEquals(caverphone('grey'), 'KRA1111111')
        self.assertEquals(caverphone('griffiths'), 'KRFTS11111')
        self.assertEquals(caverphone('griffths'), 'KRFTS11111')
        self.assertEquals(caverphone('grigg'), 'KRK1111111')
        self.assertEquals(caverphone('grig'), 'KRK1111111')
        self.assertEquals(caverphone('gubbins'), 'KPNS111111')
        self.assertEquals(caverphone('gulbins'), 'KPNS111111')
        self.assertEquals(caverphone('haddon'), 'ATN1111111')
        self.assertEquals(caverphone('hal'), 'AA11111111')
        self.assertEquals(caverphone('hall'), 'AA11111111')
        self.assertEquals(caverphone('hanley'), 'ANLA111111')
        self.assertEquals(caverphone('hanly'), 'ANLA111111')
        self.assertEquals(caverphone('hannagan'), 'ANKN111111')
        self.assertEquals(caverphone('hannan'), 'ANN1111111')
        self.assertEquals(caverphone('hannigan'), 'ANKN111111')
        self.assertEquals(caverphone('hanon'), 'ANN1111111')
        self.assertEquals(caverphone('harman'), 'AMN1111111')
        self.assertEquals(caverphone('hart'), 'AT11111111')
        self.assertEquals(caverphone('harty'), 'ATA1111111')
        self.assertEquals(caverphone('hatton'), 'ATN1111111')
        self.assertEquals(caverphone('hay'), 'AA11111111')
        self.assertEquals(caverphone('hayden'), 'ATN1111111')
        self.assertEquals(caverphone('healey'), 'ALA1111111')
        self.assertEquals(caverphone('healy'), 'ALA1111111')
        self.assertEquals(caverphone('helleyer'), 'ALA1111111')
        self.assertEquals(caverphone('hellyer'), 'ALA1111111')
        self.assertEquals(caverphone('henaghan'), 'ANKN111111')
        self.assertEquals(caverphone('heneghan'), 'ANKN111111')
        self.assertEquals(caverphone('herman'), 'AMN1111111')
        self.assertEquals(caverphone('hey'), 'AA11111111')
        self.assertEquals(caverphone('hill'), 'AA11111111')
        self.assertEquals(caverphone('hinde'), 'ANT1111111')
        self.assertEquals(caverphone('hobcraft'), 'APKRFT1111')
        self.assertEquals(caverphone('hobcroft'), 'APKRFT1111')
        self.assertEquals(caverphone('hocking'), 'AKNK111111')
        self.assertEquals(caverphone('hoeking'), 'AKNK111111')
        self.assertEquals(caverphone('holander'), 'ALNTA11111')
        self.assertEquals(caverphone('holdgate'), 'AKT1111111')
        self.assertEquals(caverphone('holgate'), 'AKT1111111')
        self.assertEquals(caverphone('hollander'), 'ALNTA11111')
        self.assertEquals(caverphone('home'), 'AM11111111')
        self.assertEquals(caverphone('horn'), 'AN11111111')
        self.assertEquals(caverphone('horne'), 'AN11111111')
        self.assertEquals(caverphone('howarth'), 'AWT1111111')
        self.assertEquals(caverphone('howe'), 'AA11111111')
        self.assertEquals(caverphone('howie'), 'AWA1111111')
        self.assertEquals(caverphone('howorth'), 'AWT1111111')
        self.assertEquals(caverphone('hoy'), 'AA11111111')
        self.assertEquals(caverphone('huddleston'), 'ATLSTN1111')
        self.assertEquals(caverphone('huddlestone'), 'ATLSTN1111')
        self.assertEquals(caverphone('hugget'), 'AKT1111111')
        self.assertEquals(caverphone('huggett'), 'AKT1111111')
        self.assertEquals(caverphone('hume'), 'AM11111111')
        self.assertEquals(caverphone('hunt'), 'ANT1111111')
        self.assertEquals(caverphone('hurt'), 'AT11111111')
        self.assertEquals(caverphone('hutcheson'), 'AKSN111111')
        self.assertEquals(caverphone('hutchison'), 'AKSN111111')
        self.assertEquals(caverphone('hutt'), 'AT11111111')
        self.assertEquals(caverphone('hutton'), 'ATN1111111')
        self.assertEquals(caverphone('jacobsen'), 'YKPSN11111')
        self.assertEquals(caverphone('jacobson'), 'YKPSN11111')
        self.assertEquals(caverphone('jacobs'), 'YKPS111111')
        self.assertEquals(caverphone('jaicobs'), 'YKPS111111')
        self.assertEquals(caverphone('jamieson'), 'YMSN111111')
        self.assertEquals(caverphone('jamison'), 'YMSN111111')
        self.assertEquals(caverphone('jansen'), 'YNSN111111')
        self.assertEquals(caverphone('janson'), 'YNSN111111')
        self.assertEquals(caverphone('jardine'), 'YTN1111111')
        self.assertEquals(caverphone('jeannings'), 'YNNKS11111')
        self.assertEquals(caverphone('jeffery'), 'YFRA111111')
        self.assertEquals(caverphone('jeffrey'), 'YFRA111111')
        self.assertEquals(caverphone('jelly'), 'YLA1111111')
        self.assertEquals(caverphone('jennings'), 'YNNKS11111')
        self.assertEquals(caverphone('johnstone'), 'YNSTN11111')
        self.assertEquals(caverphone('johnston'), 'YNSTN11111')
        self.assertEquals(caverphone('johns'), 'YNS1111111')
        self.assertEquals(caverphone('jolly'), 'YLA1111111')
        self.assertEquals(caverphone('jones'), 'YNS1111111')
        self.assertEquals(caverphone('jurdine'), 'YTN1111111')
        self.assertEquals(caverphone('kean'), 'KN11111111')
        self.assertEquals(caverphone('keen'), 'KN11111111')
        self.assertEquals(caverphone('keennelly'), 'KNLA111111')
        self.assertEquals(caverphone('kellan'), 'KLN1111111')
        self.assertEquals(caverphone('kennard'), 'KNT1111111')
        self.assertEquals(caverphone('kennealy'), 'KNLA111111')
        self.assertEquals(caverphone('kennedy'), 'KNTA111111')
        self.assertEquals(caverphone('kenn'), 'KN11111111')
        self.assertEquals(caverphone('killin'), 'KLN1111111')
        self.assertEquals(caverphone('kirkaldie'), 'KKTA111111')
        self.assertEquals(caverphone('kirkcaldie'), 'KKTA111111')
        self.assertEquals(caverphone('kirke'), 'KK11111111')
        self.assertEquals(caverphone('kirk'), 'KK11111111')
        self.assertEquals(caverphone('kitchen'), 'KKN1111111')
        self.assertEquals(caverphone('kitchin'), 'KKN1111111')
        self.assertEquals(caverphone('krause'), 'KRS1111111')
        self.assertEquals(caverphone('kraus'), 'KRS1111111')
        self.assertEquals(caverphone('langham'), 'LNM1111111')
        self.assertEquals(caverphone('lanham'), 'LNM1111111')
        self.assertEquals(caverphone('larson'), 'LSN1111111')
        self.assertEquals(caverphone('laughlin'), 'LLN1111111')
        self.assertEquals(caverphone('laurie'), 'LRA1111111')
        self.assertEquals(caverphone('lawrie'), 'LRA1111111')
        self.assertEquals(caverphone('lawson'), 'LSN1111111')
        self.assertEquals(caverphone('leary'), 'LRA1111111')
        self.assertEquals(caverphone('leech'), 'LK11111111')
        self.assertEquals(caverphone('leery'), 'LRA1111111')
        self.assertEquals(caverphone('leitch'), 'LK11111111')
        self.assertEquals(caverphone('lemin'), 'LMN1111111')
        self.assertEquals(caverphone('lemon'), 'LMN1111111')
        self.assertEquals(caverphone('lenihan'), 'LNN1111111')
        self.assertEquals(caverphone('lennon'), 'LNN1111111')
        self.assertEquals(caverphone('leyden'), 'LTN1111111')
        self.assertEquals(caverphone('leydon'), 'LTN1111111')
        self.assertEquals(caverphone('lister'), 'LSTA111111')
        self.assertEquals(caverphone('list'), 'LST1111111')
        self.assertEquals(caverphone('livingstone'), 'LFNKSTN111')
        self.assertEquals(caverphone('livingston'), 'LFNKSTN111')
        self.assertEquals(caverphone('lochhead'), 'LKT1111111')
        self.assertEquals(caverphone('lockhead'), 'LKT1111111')
        self.assertEquals(caverphone('loughlin'), 'LLN1111111')
        self.assertEquals(caverphone('macallum'), 'MKLM111111')
        self.assertEquals(caverphone('macaskill'), 'MKSKA11111')
        self.assertEquals(caverphone('macaulay'), 'MKLA111111')
        self.assertEquals(caverphone('macauley'), 'MKLA111111')
        self.assertEquals(caverphone('macbeath'), 'MKPT111111')
        self.assertEquals(caverphone('macdonald'), 'MKTNT11111')
        self.assertEquals(caverphone('maceewan'), 'MSWN111111')
        self.assertEquals(caverphone('macewan'), 'MSWN111111')
        self.assertEquals(caverphone('macfarlane'), 'MKFLN11111')
        self.assertEquals(caverphone('macintosh'), 'MSNTS11111')
        self.assertEquals(caverphone('mackechnie'), 'MKKNA11111')
        self.assertEquals(caverphone('mackenzie'), 'MKNSA11111')
        self.assertEquals(caverphone('mackersey'), 'MKSA111111')
        self.assertEquals(caverphone('mackersy'), 'MKSA111111')
        self.assertEquals(caverphone('maclean'), 'MKLN111111')
        self.assertEquals(caverphone('macnee'), 'MKNA111111')
        self.assertEquals(caverphone('macpherson'), 'MKFSN11111')
        self.assertEquals(caverphone('main'), 'MN11111111')
        self.assertEquals(caverphone('maley'), 'MLA1111111')
        self.assertEquals(caverphone('malladew'), 'MLTA111111')
        self.assertEquals(caverphone('maloney'), 'MLNA111111')
        self.assertEquals(caverphone('mann'), 'MN11111111')
        self.assertEquals(caverphone('marchant'), 'MKNT111111')
        self.assertEquals(caverphone('marett'), 'MRT1111111')
        self.assertEquals(caverphone('marrett'), 'MRT1111111')
        self.assertEquals(caverphone('mason'), 'MSN1111111')
        self.assertEquals(caverphone('matheson'), 'MTSN111111')
        self.assertEquals(caverphone('mathieson'), 'MTSN111111')
        self.assertEquals(caverphone('mattingle'), 'MTNKA11111')
        self.assertEquals(caverphone('mattingly'), 'MTNKLA1111')
        self.assertEquals(caverphone('mawson'), 'MSN1111111')
        self.assertEquals(caverphone('mcaulay'), 'MKLA111111')
        self.assertEquals(caverphone('mcauley'), 'MKLA111111')
        self.assertEquals(caverphone('mcauliffe'), 'MKLF111111')
        self.assertEquals(caverphone('mcauliff'), 'MKLF111111')
        self.assertEquals(caverphone('mcbeath'), 'MKPT111111')
        self.assertEquals(caverphone('mccallum'), 'MKLM111111')
        self.assertEquals(caverphone('mccarthy'), 'MKTA111111')
        self.assertEquals(caverphone('mccarty'), 'MKTA111111')
        self.assertEquals(caverphone('mccaskill'), 'MKSKA11111')
        self.assertEquals(caverphone('mccay'), 'MKA1111111')
        self.assertEquals(caverphone('mcclintock'), 'MKLNTK1111')
        self.assertEquals(caverphone('mccluskey'), 'MKLSKA1111')
        self.assertEquals(caverphone('mcclusky'), 'MKLSKA1111')
        self.assertEquals(caverphone('mccormack'), 'MKMK111111')
        self.assertEquals(caverphone('mccormacl'), 'MKMKA11111')
        self.assertEquals(caverphone('mccrorie'), 'MKRRA11111')
        self.assertEquals(caverphone('mccrory'), 'MKRRA11111')
        self.assertEquals(caverphone('mccrossan'), 'MKRSN11111')
        self.assertEquals(caverphone('mccrossin'), 'MKRSN11111')
        self.assertEquals(caverphone('mcdermott'), 'MKTMT11111')
        self.assertEquals(caverphone('mcdiarmid'), 'MKTMT11111')
        self.assertEquals(caverphone('mcdonald'), 'MKTNT11111')
        self.assertEquals(caverphone('mcdonell'), 'MKTNA11111')
        self.assertEquals(caverphone('mcdonnell'), 'MKTNA11111')
        self.assertEquals(caverphone('mcdowall'), 'MKTWA11111')
        self.assertEquals(caverphone('mcdowell'), 'MKTWA11111')
        self.assertEquals(caverphone('mcewan'), 'MSWN111111')
        self.assertEquals(caverphone('mcewen'), 'MSWN111111')
        self.assertEquals(caverphone('mcfarlane'), 'MKFLN11111')
        self.assertEquals(caverphone('mcfaull'), 'MKFA111111')
        self.assertEquals(caverphone('mcgill'), 'MKA1111111')
        self.assertEquals(caverphone('mciintyre'), 'MSNTA11111')
        self.assertEquals(caverphone('mcintosh'), 'MSNTS11111')
        self.assertEquals(caverphone('mcintyre'), 'MSNTA11111')
        self.assertEquals(caverphone('mciver'), 'MSFA111111')
        self.assertEquals(caverphone('mcivor'), 'MSFA111111')
        self.assertEquals(caverphone('mckay'), 'MKA1111111')
        self.assertEquals(caverphone('mckechnie'), 'MKKNA11111')
        self.assertEquals(caverphone('mckecknie'), 'MKKNA11111')
        self.assertEquals(caverphone('mckellar'), 'MKLA111111')
        self.assertEquals(caverphone('mckenzie'), 'MKNSA11111')
        self.assertEquals(caverphone('mcketterick'), 'MKTRK11111')
        self.assertEquals(caverphone('mckey'), 'MKA1111111')
        self.assertEquals(caverphone('mckinlay'), 'MKNLA11111')
        self.assertEquals(caverphone('mckinley'), 'MKNLA11111')
        self.assertEquals(caverphone('mckitterick'), 'MKTRK11111')
        self.assertEquals(caverphone('mclachlan'), 'MKLKLN1111')
        self.assertEquals(caverphone('mclauchlan'), 'MKLKLN1111')
        self.assertEquals(caverphone('mclauchlin'), 'MKLKLN1111')
        self.assertEquals(caverphone('mclaughlan'), 'MKLLN11111')
        self.assertEquals(caverphone('mclaughlin'), 'MKLLN11111')
        self.assertEquals(caverphone('mclean'), 'MKLN111111')
        self.assertEquals(caverphone('mcledd'), 'MKLT111111')
        self.assertEquals(caverphone('mcledowne'), 'MKLTN11111')
        self.assertEquals(caverphone('mcledowney'), 'MKLTNA1111')
        self.assertEquals(caverphone('mclellan'), 'MKLLN11111')
        self.assertEquals(caverphone('mcleod'), 'MKLT111111')
        self.assertEquals(caverphone('mclintock'), 'MKLNTK1111')
        self.assertEquals(caverphone('mcloud'), 'MKLT111111')
        self.assertEquals(caverphone('mcloughlin'), 'MKLLN11111')
        self.assertEquals(caverphone('mcmillan'), 'MKMLN11111')
        self.assertEquals(caverphone('mcmullan'), 'MKMLN11111')
        self.assertEquals(caverphone('mcmullen'), 'MKMLN11111')
        self.assertEquals(caverphone('mcnair'), 'MKNA111111')
        self.assertEquals(caverphone('mcnalty'), 'MKNTA11111')
        self.assertEquals(caverphone('mcnatty'), 'MKNTA11111')
        self.assertEquals(caverphone('mcnee'), 'MKNA111111')
        self.assertEquals(caverphone('mcneill'), 'MKNA111111')
        self.assertEquals(caverphone('mcneil'), 'MKNA111111')
        self.assertEquals(caverphone('mcnicoll'), 'MKNKA11111')
        self.assertEquals(caverphone('mcnicol'), 'MKNKA11111')
        self.assertEquals(caverphone('mcnie'), 'MKNA111111')
        self.assertEquals(caverphone('mcphail'), 'MKFA111111')
        self.assertEquals(caverphone('mcphee'), 'MKFA111111')
        self.assertEquals(caverphone('mcpherson'), 'MKFSN11111')
        self.assertEquals(caverphone('mcsweeney'), 'MKSWNA1111')
        self.assertEquals(caverphone('mcsweeny'), 'MKSWNA1111')
        self.assertEquals(caverphone('mctague'), 'MKTKA11111')
        self.assertEquals(caverphone('mctigue'), 'MKTKA11111')
        self.assertEquals(caverphone('mcvicar'), 'MKFKA11111')
        self.assertEquals(caverphone('mcvickar'), 'MKFKA11111')
        self.assertEquals(caverphone('mcvie'), 'MKFA111111')
        self.assertEquals(caverphone('meade'), 'MT11111111')
        self.assertEquals(caverphone('mead'), 'MT11111111')
        self.assertEquals(caverphone('meder'), 'MTA1111111')
        self.assertEquals(caverphone('meekin'), 'MKN1111111')
        self.assertEquals(caverphone('meighan'), 'MKN1111111')
        self.assertEquals(caverphone('melladew'), 'MLTA111111')
        self.assertEquals(caverphone('merchant'), 'MKNT111111')
        self.assertEquals(caverphone('metcalfe'), 'MTKF111111')
        self.assertEquals(caverphone('metcalf'), 'MTKF111111')
        self.assertEquals(caverphone('millar'), 'MLA1111111')
        self.assertEquals(caverphone('millea'), 'MLA1111111')
        self.assertEquals(caverphone('miller'), 'MLA1111111')
        self.assertEquals(caverphone('millie'), 'MLA1111111')
        self.assertEquals(caverphone('moffat'), 'MFT1111111')
        self.assertEquals(caverphone('moffitt'), 'MFT1111111')
        self.assertEquals(caverphone('moirison'), 'MRSN111111')
        self.assertEquals(caverphone('mokenzie'), 'MKNSA11111')
        self.assertEquals(caverphone('moloney'), 'MLNA111111')
        self.assertEquals(caverphone('molonoy'), 'MLNA111111')
        self.assertEquals(caverphone('monaghan'), 'MNKN111111')
        self.assertEquals(caverphone('monagon'), 'MNKN111111')
        self.assertEquals(caverphone('moodie'), 'MTA1111111')
        self.assertEquals(caverphone('moody'), 'MTA1111111')
        self.assertEquals(caverphone('morell'), 'MRA1111111')
        self.assertEquals(caverphone('morice'), 'MRK1111111')
        self.assertEquals(caverphone('morrell'), 'MRA1111111')
        self.assertEquals(caverphone('morrisey'), 'MRSA111111')
        self.assertEquals(caverphone('morris'), 'MRS1111111')
        self.assertEquals(caverphone('morrison'), 'MRSN111111')
        self.assertEquals(caverphone('morrissey'), 'MRSA111111')
        self.assertEquals(caverphone('muiorhead'), 'MT11111111')
        self.assertEquals(caverphone('muirhead'), 'MT11111111')
        self.assertEquals(caverphone('mulch'), 'MK11111111')
        self.assertEquals(caverphone('mulholland'), 'MLNT111111')
        self.assertEquals(caverphone('mullay'), 'MLA1111111')
        self.assertEquals(caverphone('mullholland'), 'MLNT111111')
        self.assertEquals(caverphone('mulloy'), 'MLA1111111')
        self.assertEquals(caverphone('mulqueen'), 'MKN1111111')
        self.assertEquals(caverphone('mulquin'), 'MKN1111111')
        self.assertEquals(caverphone('murdoch'), 'MTK1111111')
        self.assertEquals(caverphone('murdock'), 'MTK1111111')
        self.assertEquals(caverphone('mutch'), 'MK11111111')
        self.assertEquals(caverphone('naughton'), 'NTN1111111')
        self.assertEquals(caverphone('naumann'), 'NMN1111111')
        self.assertEquals(caverphone('neason'), 'NSN1111111')
        self.assertEquals(caverphone('nelsion'), 'NSN1111111')
        self.assertEquals(caverphone('nelson'), 'NSN1111111')
        self.assertEquals(caverphone('nesbitt'), 'NSPT111111')
        self.assertEquals(caverphone('neumann'), 'NMN1111111')
        self.assertEquals(caverphone('newall'), 'NWA1111111')
        self.assertEquals(caverphone('newell'), 'NWA1111111')
        self.assertEquals(caverphone('newlands'), 'NLNTS11111')
        self.assertEquals(caverphone('neylan'), 'NLN1111111')
        self.assertEquals(caverphone('neylon'), 'NLN1111111')
        self.assertEquals(caverphone('nichol'), 'NKA1111111')
        self.assertEquals(caverphone('nicoll'), 'NKA1111111')
        self.assertEquals(caverphone('nicol'), 'NKA1111111')
        self.assertEquals(caverphone('nisbet'), 'NSPT111111')
        self.assertEquals(caverphone('norton'), 'NTN1111111')
        self.assertEquals(caverphone('nowlands'), 'NLNTS11111')
        self.assertEquals(caverphone('o\'brian'), 'APRN111111')
        self.assertEquals(caverphone('o\'brien'), 'APRN111111')
        self.assertEquals(caverphone('ockwell'), 'AKWA111111')
        self.assertEquals(caverphone('o\'connell'), 'AKNA111111')
        self.assertEquals(caverphone('o\'connor'), 'AKNA111111')
        self.assertEquals(caverphone('ocwell'), 'AKWA111111')
        self.assertEquals(caverphone('odham'), 'ATM1111111')
        self.assertEquals(caverphone('ogilvie'), 'AKFA111111')
        self.assertEquals(caverphone('ogivie'), 'AKFA111111')
        self.assertEquals(caverphone('o\'keefe'), 'AKF1111111')
        self.assertEquals(caverphone('o\'keeffe'), 'AKF1111111')
        self.assertEquals(caverphone('oldham'), 'ATM1111111')
        self.assertEquals(caverphone('olsen'), 'ASN1111111')
        self.assertEquals(caverphone('olsien'), 'ASN1111111')
        self.assertEquals(caverphone('osmand'), 'ASMNT11111')
        self.assertEquals(caverphone('osmond'), 'ASMNT11111')
        self.assertEquals(caverphone('page'), 'PK11111111')
        self.assertEquals(caverphone('paine'), 'PN11111111')
        self.assertEquals(caverphone('pascoe'), 'PSKA111111')
        self.assertEquals(caverphone('pasco'), 'PSKA111111')
        self.assertEquals(caverphone('paterson'), 'PTSN111111')
        self.assertEquals(caverphone('patrick'), 'PTRK111111')
        self.assertEquals(caverphone('patterson'), 'PTSN111111')
        self.assertEquals(caverphone('pattison'), 'PTSN111111')
        self.assertEquals(caverphone('pattrick'), 'PTRK111111')
        self.assertEquals(caverphone('payne'), 'PN11111111')
        self.assertEquals(caverphone('peace'), 'PK11111111')
        self.assertEquals(caverphone('pearce'), 'PK11111111')
        self.assertEquals(caverphone('peebles'), 'PPLS111111')
        self.assertEquals(caverphone('pegg'), 'PK11111111')
        self.assertEquals(caverphone('peoples'), 'PPLS111111')
        self.assertEquals(caverphone('pepperell'), 'PPRA111111')
        self.assertEquals(caverphone('pepperill'), 'PPRA111111')
        self.assertEquals(caverphone('perry'), 'PRA1111111')
        self.assertEquals(caverphone('petersen'), 'PTSN111111')
        self.assertEquals(caverphone('peterson'), 'PTSN111111')
        self.assertEquals(caverphone('phimester'), 'FMSTA11111')
        self.assertEquals(caverphone('phimister'), 'FMSTA11111')
        self.assertEquals(caverphone('picket'), 'PKT1111111')
        self.assertEquals(caverphone('pickett'), 'PKT1111111')
        self.assertEquals(caverphone('pickles'), 'PKLS111111')
        self.assertEquals(caverphone('picklis'), 'PKLS111111')
        self.assertEquals(caverphone('pollock'), 'PLK1111111')
        self.assertEquals(caverphone('polloek'), 'PLK1111111')
        self.assertEquals(caverphone('polwarth'), 'PWT1111111')
        self.assertEquals(caverphone('polworth'), 'PWT1111111')
        self.assertEquals(caverphone('popperell'), 'PPRA111111')
        self.assertEquals(caverphone('powell'), 'PWA1111111')
        self.assertEquals(caverphone('power'), 'PWA1111111')
        self.assertEquals(caverphone('preston'), 'PRSTN11111')
        self.assertEquals(caverphone('priston'), 'PRSTN11111')
        self.assertEquals(caverphone('procter'), 'PRKTA11111')
        self.assertEquals(caverphone('proctor'), 'PRKTA11111')
        self.assertEquals(caverphone('pullar'), 'PLA1111111')
        self.assertEquals(caverphone('puller'), 'PLA1111111')
        self.assertEquals(caverphone('purches'), 'PKS1111111')
        self.assertEquals(caverphone('rae'), 'RA11111111')
        self.assertEquals(caverphone('ramsay'), 'RMSA111111')
        self.assertEquals(caverphone('ramsey'), 'RMSA111111')
        self.assertEquals(caverphone('ray'), 'RA11111111')
        self.assertEquals(caverphone('redder'), 'RTA1111111')
        self.assertEquals(caverphone('reed'), 'RT11111111')
        self.assertEquals(caverphone('reider'), 'RTA1111111')
        self.assertEquals(caverphone('reidle'), 'RTA1111111')
        self.assertEquals(caverphone('reid'), 'RT11111111')
        self.assertEquals(caverphone('rendel'), 'RNTA111111')
        self.assertEquals(caverphone('render'), 'RNTA111111')
        self.assertEquals(caverphone('renfree'), 'RNFRA11111')
        self.assertEquals(caverphone('renfrew'), 'RNFRA11111')
        self.assertEquals(caverphone('riddoch'), 'RTK1111111')
        self.assertEquals(caverphone('riddock'), 'RTK1111111')
        self.assertEquals(caverphone('riedle'), 'RTA1111111')
        self.assertEquals(caverphone('riley'), 'RLA1111111')
        self.assertEquals(caverphone('rilly'), 'RLA1111111')
        self.assertEquals(caverphone('robertsan'), 'RPTSN11111')
        self.assertEquals(caverphone('robertson'), 'RPTSN11111')
        self.assertEquals(caverphone('rodgerson'), 'RKSN111111')
        self.assertEquals(caverphone('rodgers'), 'RKS1111111')
        self.assertEquals(caverphone('rogerson'), 'RKSN111111')
        self.assertEquals(caverphone('rogers'), 'RKS1111111')
        self.assertEquals(caverphone('rorley'), 'RLA1111111')
        self.assertEquals(caverphone('rosenbrock'), 'RSNPRK1111')
        self.assertEquals(caverphone('rosenbrook'), 'RSNPRK1111')
        self.assertEquals(caverphone('rose'), 'RS11111111')
        self.assertEquals(caverphone('ross'), 'RS11111111')
        self.assertEquals(caverphone('routledge'), 'RTLK111111')
        self.assertEquals(caverphone('routlege'), 'RTLK111111')
        self.assertEquals(caverphone('rowley'), 'RLA1111111')
        self.assertEquals(caverphone('russell'), 'RSA1111111')
        self.assertEquals(caverphone('sanders'), 'SNTS111111')
        self.assertEquals(caverphone('sandes'), 'SNTS111111')
        self.assertEquals(caverphone('sandrey'), 'SNTRA11111')
        self.assertEquals(caverphone('sandry'), 'SNTRA11111')
        self.assertEquals(caverphone('saunders'), 'SNTS111111')
        self.assertEquals(caverphone('saxton'), 'SKTN111111')
        self.assertEquals(caverphone('scaife'), 'SKF1111111')
        self.assertEquals(caverphone('scanlan'), 'SKNLN11111')
        self.assertEquals(caverphone('scanlon'), 'SKNLN11111')
        self.assertEquals(caverphone('scarfe'), 'SKF1111111')
        self.assertEquals(caverphone('scoffeld'), 'SKFT111111')
        self.assertEquals(caverphone('scofield'), 'SKFT111111')
        self.assertEquals(caverphone('seamer'), 'SMA1111111')
        self.assertEquals(caverphone('sellar'), 'SLA1111111')
        self.assertEquals(caverphone('seller'), 'SLA1111111')
        self.assertEquals(caverphone('sexton'), 'SKTN111111')
        self.assertEquals(caverphone('seymour'), 'SMA1111111')
        self.assertEquals(caverphone('sharpe'), 'SP11111111')
        self.assertEquals(caverphone('sharp'), 'SP11111111')
        self.assertEquals(caverphone('shaw'), 'SA11111111')
        self.assertEquals(caverphone('shea'), 'SA11111111')
        self.assertEquals(caverphone('shephard'), 'SFT1111111')
        self.assertEquals(caverphone('shepherd'), 'SFT1111111')
        self.assertEquals(caverphone('sheppard'), 'SPT1111111')
        self.assertEquals(caverphone('shepperd'), 'SPT1111111')
        self.assertEquals(caverphone('sheriff'), 'SRF1111111')
        self.assertEquals(caverphone('sherriff'), 'SRF1111111')
        self.assertEquals(caverphone('sidey'), 'STA1111111')
        self.assertEquals(caverphone('sidoy'), 'STA1111111')
        self.assertEquals(caverphone('silvertsen'), 'SFTSN11111')
        self.assertEquals(caverphone('sincock'), 'SNKK111111')
        self.assertEquals(caverphone('sincok'), 'SNKK111111')
        self.assertEquals(caverphone('sivertsen'), 'SFTSN11111')
        self.assertEquals(caverphone('skeene'), 'SKN1111111')
        self.assertEquals(caverphone('skene'), 'SKN1111111')
        self.assertEquals(caverphone('slowley'), 'SLLA111111')
        self.assertEquals(caverphone('slowly'), 'SLLA111111')
        self.assertEquals(caverphone('smith'), 'SMT1111111')
        self.assertEquals(caverphone('smythe'), 'SMT1111111')
        self.assertEquals(caverphone('smyth'), 'SMT1111111')
        self.assertEquals(caverphone('spencer'), 'SPNSA11111')
        self.assertEquals(caverphone('spence'), 'SPNK111111')
        self.assertEquals(caverphone('steadman'), 'STTMN11111')
        self.assertEquals(caverphone('stedman'), 'STTMN11111')
        self.assertEquals(caverphone('stenhouse'), 'STNS111111')
        self.assertEquals(caverphone('stennouse'), 'STNS111111')
        self.assertEquals(caverphone('stephenson'), 'STFNSN1111')
        self.assertEquals(caverphone('stevenson'), 'STFNSN1111')
        self.assertEquals(caverphone('stichmann'), 'STKMN11111')
        self.assertEquals(caverphone('stickman'), 'STKMN11111')
        self.assertEquals(caverphone('stock'), 'STK1111111')
        self.assertEquals(caverphone('stook'), 'STK1111111')
        self.assertEquals(caverphone('strang'), 'STRNK11111')
        self.assertEquals(caverphone('strong'), 'STRNK11111')
        self.assertEquals(caverphone('summerell'), 'SMRA111111')
        self.assertEquals(caverphone('taverner'), 'TFNA111111')
        self.assertEquals(caverphone('tillie'), 'TLA1111111')
        self.assertEquals(caverphone('tiverner'), 'TFNA111111')
        self.assertEquals(caverphone('todd'), 'TT11111111')
        self.assertEquals(caverphone('tonar'), 'TNA1111111')
        self.assertEquals(caverphone('toner'), 'TNA1111111')
        self.assertEquals(caverphone('tonner'), 'TNA1111111')
        self.assertEquals(caverphone('tonnor'), 'TNA1111111')
        self.assertEquals(caverphone('townsend'), 'TNSNT11111')
        self.assertEquals(caverphone('townshend'), 'TNSNT11111')
        self.assertEquals(caverphone('treeweek'), 'TRWK111111')
        self.assertEquals(caverphone('tregoning'), 'TRKNNK1111')
        self.assertEquals(caverphone('tregonning'), 'TRKNNK1111')
        self.assertEquals(caverphone('trevena'), 'TRFNA11111')
        self.assertEquals(caverphone('trevenna'), 'TRFNA11111')
        self.assertEquals(caverphone('trewick'), 'TRWK111111')
        self.assertEquals(caverphone('turley'), 'TLA1111111')
        self.assertEquals(caverphone('vial'), 'FA11111111')
        self.assertEquals(caverphone('vintinner'), 'FNTNA11111')
        self.assertEquals(caverphone('vintinuer'), 'FNTNA11111')
        self.assertEquals(caverphone('wackeldine'), 'WKTN111111')
        self.assertEquals(caverphone('wackildene'), 'WKTN111111')
        self.assertEquals(caverphone('wackilden'), 'WKTN111111')
        self.assertEquals(caverphone('waghornee'), 'WKNA111111')
        self.assertEquals(caverphone('waghorne'), 'WKN1111111')
        self.assertEquals(caverphone('wallace'), 'WLK1111111')
        self.assertEquals(caverphone('wallin'), 'WLN1111111')
        self.assertEquals(caverphone('walquest'), 'WKST111111')
        self.assertEquals(caverphone('walquist'), 'WKST111111')
        self.assertEquals(caverphone('walsh'), 'WS11111111')
        self.assertEquals(caverphone('warreil'), 'WRA1111111')
        self.assertEquals(caverphone('warrell'), 'WRA1111111')
        self.assertEquals(caverphone('watsan'), 'WTSN111111')
        self.assertEquals(caverphone('watson'), 'WTSN111111')
        self.assertEquals(caverphone('welbourn'), 'WPN1111111')
        self.assertEquals(caverphone('weldon'), 'WTN1111111')
        self.assertEquals(caverphone('wellbourn'), 'WPN1111111')
        self.assertEquals(caverphone('wells'), 'WS11111111')
        self.assertEquals(caverphone('welsh'), 'WS11111111')
        self.assertEquals(caverphone('wheelan'), 'WLN1111111')
        self.assertEquals(caverphone('wheeler'), 'WLA1111111')
        self.assertEquals(caverphone('whelan'), 'WLN1111111')
        self.assertEquals(caverphone('white'), 'WT11111111')
        self.assertEquals(caverphone('whyte'), 'WT11111111')
        self.assertEquals(caverphone('wilden'), 'WTN1111111')
        self.assertEquals(caverphone('wildey'), 'WTA1111111')
        self.assertEquals(caverphone('wildoy'), 'WTA1111111')
        self.assertEquals(caverphone('willis'), 'WLS1111111')
        self.assertEquals(caverphone('willon'), 'WLN1111111')
        self.assertEquals(caverphone('willson'), 'WSN1111111')
        self.assertEquals(caverphone('wills'), 'WS11111111')
        self.assertEquals(caverphone('wilson'), 'WSN1111111')
        self.assertEquals(caverphone('wilton'), 'WTN1111111')
        self.assertEquals(caverphone('winders'), 'WNTS111111')
        self.assertEquals(caverphone('windus'), 'WNTS111111')
        self.assertEquals(caverphone('wine'), 'WN11111111')
        self.assertEquals(caverphone('winn'), 'WN11111111')
        self.assertEquals(caverphone('wooton'), 'WTN1111111')
        self.assertEquals(caverphone('wootten'), 'WTN1111111')
        self.assertEquals(caverphone('wootton'), 'WTN1111111')
        self.assertEquals(caverphone('wraight'), 'RT11111111')
        self.assertEquals(caverphone('wright'), 'RT11111111')

    def test_caverphone1(self):
        self.assertEquals(caverphone('', 1), '111111')
        self.assertEquals(caverphone('', version=1), '111111')

        # http://caversham.otago.ac.nz/files/working/ctp060902.pdf
        self.assertEquals(caverphone('David', version=1), 'TFT111')
        self.assertEquals(caverphone('Whittle', version=1), 'WTL111')

class alpha_sis_test_cases(unittest.TestCase):
    def test_alpha_sis(self):
        self.assertEquals(alpha_sis('')[0], '00000000000000')

        self.assertEquals(alpha_sis('Rodgers')[0], '04740000000000')
        self.assertEquals(alpha_sis('Rogers')[0], '04740000000000')
        self.assertEquals(alpha_sis('Kant')[0], '07210000000000')
        self.assertEquals(alpha_sis('Knuth')[0], '02100000000000')
        self.assertEquals(alpha_sis('Harper')[0], '24940000000000')
        self.assertEquals(alpha_sis('Collier')[0], '07540000000000')
        self.assertEquals(alpha_sis('Schultz')[0], '06500000000000')
        self.assertEquals(alpha_sis('Livingston')[0], '05827012000000')

        # tests of repeated letters
        self.assertEquals(alpha_sis('Colllier')[0], '07554000000000')
        self.assertEquals(alpha_sis('Collllier')[0], '07554000000000')
        self.assertEquals(alpha_sis('Colllllier')[0], '07555400000000')
        self.assertEquals(alpha_sis('Collllllier')[0], '07555400000000')
        self.assertEquals(alpha_sis('Colalalier')[0], '07555400000000')

if __name__ == '__main__':
    unittest.main()
