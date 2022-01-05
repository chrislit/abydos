# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.phones._phones.

The phones module implements phonetic feature coding, decoding, and comparison
functions.
"""

from typing import Dict, List, Optional, Sequence, Union
from unicodedata import normalize

__all__ = ['cmp_features', 'get_feature', 'ipa_to_features']


_PHONETIC_FEATURES = {
    't': 2783230754502126250,
    't͇': 2783230754502126250,
    't̪': 2783230479624219306,
    't̠': 2783231579135847082,
    'd': 2783230754501864106,
    'd͇': 2783230754501864106,
    'd̪': 2783230479623957162,
    'd̠': 2783231579135584938,
    's': 2783230754502125978,
    's͇': 2783230754502125978,
    's̪': 2783230479624219034,
    's̟': 2783230479624219034,
    'z': 2783230754501863834,
    'z͇': 2783230754501863834,
    'z̪': 2783230479623956890,
    'z̟': 2783230479623956890,
    'θ̱': 2783230754502125994,
    'θ͇': 2783230754502125994,
    'ɹ̝̊': 2783230754502125994,
    'ð̠': 2783230754501863850,
    'ð͇': 2783230754501863850,
    'ɹ̝': 2783230754501863850,
    'ɬ': 2783230754502060454,
    'ɮ': 2783230754501863846,
    'θ': 2783230479624219050,
    's̄': 2783230479624219034,
    'ð': 2783230479623956906,
    'ð̞': 2693158487076546986,
    'ʃ': 2783231556184615322,
    'ʃʲ': 2783231556184615322,
    'š': 2783231556184615322,
    'ɹ̠̊˔': 2783231579135846826,
    'ʒ': 2783231556184353178,
    'ʒʲ': 2783231556184353178,
    'ž': 2783231556184353178,
    'ɹ̠˔': 2783231579135584682,
    'c': 2783233463150095018,
    'ɟ': 2783233463149832874,
    'ç': 2783233463150094762,
    'ʝ': 2783233463149832618,
    'p': 2781720575281375914,
    'p̪': 2781702983095331498,
    'p͆': 2781702983095331498,
    'b': 2781720575281113770,
    'b̪': 2781702983095069354,
    'b͆': 2781702983095069354,
    'f': 2781702983095331242,
    'v': 2781702983095069098,
    'ɸ': 2781720575281375658,
    'ɸ̞': 2691648582733965738,
    'β': 2781720575281113514,
    'β̞': 2691648582733703594,
    'k': 2783233462881659562,
    'ɡ': 2783233462881397418,
    'g': 2783233462881397418,
    'x': 2783233462881659306,
    'x̞': 2981391846485961130,
    'ɣ': 2783233462881397162,
    'ɰ': 2981391846485698986,
    'ɣ̞': 2981391846485698986,
    'ɣ˕': 2981391846485698986,
    'q': 2783233480061528746,
    'ɢ': 2783233480061266602,
    'χ': 2783233480061528490,
    'x̣': 2783233480061528490,
    'χ̞': 2693161487514118570,
    'ʁ': 2783233480061266346,
    'ʁ̝': 2783233480061266346,
    'ʁ̞': 2693161487513856426,
    'ħ': 2783233503273855402,
    'ħ̞': 2693161510726445482,
    'ʕ': 2783233503273593258,
    'ʕ̝': 2783233503273593258,
    'ʕ̞': 2693161510726183338,
    'ɑ̯': 2693161510726183338,
    'h': 2783233503281129898,
    'h̃': 2693161510733719914,
    'ɦ': 2783233503280867754,
    'ʔ': 2783233503281179306,
    'm': 2709662981243185770,
    'm̥': 2709662981243447914,
    'ɱ': 2709645389057141354,
    'm̪': 2709645389057141354,
    'n': 2711173160463936106,
    'n̪': 2711172885586029162,
    'n̥': 2711173160464198250,
    'n̊': 2711173160464198250,
    'n̪̊': 2711172885586291306,
    'ɳ': 2711174259975563882,
    'ɳ̊': 2711174259975826026,
    'ɳ̥': 2711174259975826026,
    'ɲ': 2711175869111904874,
    'ñ': 2711175869111904874,
    'n̠ʲ': 2711173944966556266,
    'ɲ̟': 2711173944966556266,
    'ɲ̊': 2711175869112167018,
    'ɲ̥': 2711175869112167018,
    'ŋ': 2711175868843469418,
    'ŋ̊': 2711175868843731562,
    'ɴ': 2711175886023338602,
    'l': 2693158761954453926,
    'l̠': 2693159586588174758,
    'l̪': 2693158487076546982,
    'ɫ': 2693158721554917798,
    'lˠ': 2693158721554917798,
    'lˤ': 2693158721554917798,
    'l̴': 2693158721554917798,
    'ɫ̪': 2693158446677010854,
    'l̪ˠ': 2693158446677010854,
    'l̪ˤ': 2693158446677010854,
    'l̴̪': 2693158446677010854,
    'l̥': 2693158761954716070,
    'ʎ': 2693161470602422694,
    'l̠ʲ': 2693159546457074086,
    'ʎ̟': 2693159546457074086,
    'ʟ': 2693161470333987238,
    'r': 2711173160463936170,
    'r̥': 2711173160464198314,
    'ɹ': 2693158761954453930,
    'ð̠˕': 2693158761954453930,
    'ʀ': 2711175886023338666,
    'ʀ̥': 2711175886023600810,
    'j': 2981391846754134442,
    'i̯': 2981391846754134442,
    'j̊': 2981391846754396586,
    'w': 2978753018579036586,
    'u̯': 2978753018579036586,
    'ɰʷ': 2978753018579036586,
    'ʍ': 2978753018579298730,
    'w̥': 2978753018579298730,
    'ɰᵝ': 2978682649834858922,
    'wᵝ': 2978682649834858922,
    'ɥ': 2978753018847472042,
    'jʷ': 2978753018847472042,
    'ʡ': 2783233503274904234,
    'ʜ': 2783233503274903978,
    'ʢ': 2783233503274641834,
    'ʢ̝': 2783233503274641834,
    'ʢ̞': 2693161510727231914,
    'ᴙ': 2711175909236714154,
    'ʙ': 2709662981243185834,
    'ʋ': 2691630990547659178,
    'ɕ': 2783231539004746138,
    'ʑ': 2783231539004483994,
    'ɾ': 2711173160463935914,
    'ᴅ': 2711173160463935914,
    'ɾ̥': 2711173160464198058,
    'ɾ̊': 2711173160464198058,
    'ᴅ̥': 2711173160464198058,
    'ᴅ̊': 2711173160464198058,
    'ɾ̃': 2711173160463935850,
    'n̆': 2711173160463935850,
    'ⱱ': 2709645389057141162,
    'ⱱ̟': 2709662981243185578,
    'w̆': 2709662981243185578,
    'b̆': 2709662981243185578,
    'ɢ̆': 2711175886023338410,
    'ʀ̆': 2711175886023338410,
    'ʡ̯': 2711175909236713898,
    'ɺ': 2711173160463935910,
    'ʎ̯': 2711175869111904678,
    'ʟ̆': 2711175868843469222,
    'ʈ': 2783231854013754026,
    'ɖ': 2783231854013491882,
    'ʂ': 2783231854013753754,
    'ʐ': 2783231854013491610,
    'ɻ': 2693159861466081706,
    'ɽ': 2711174259975563690,
    'ɽ͡r': 2711174259975563946,
    'ɭ': 2693159861466081702,
    'ɭ̆': 2711174259975563686,
    'ɺ˞': 2711174259975563686,
    'ɺ̢': 2711174259975563686,
    'ꞎ': 2783231854013688230,
    'ʎ̝̊': 2783233463150094758,
    'ʟ̝̊': 2783233462881659302,
    'ʟ̝': 2783233462881397158,
    # affricates & co-articulated
    't͡ʃ': 2783231556184615833,
    'ʧ': 2783231556184615833,
    't͜ʃ': 2783231556184615833,
    't̠ʲʃ': 2783231556184615833,
    'č': 2783231556184615833,
    'd͡ʒ': 2783231556184353689,
    'ʤ': 2783231556184353689,
    'd͜ʒ': 2783231556184353689,
    'd̠ʲʒ': 2783231556184353689,
    'ǯ': 2783231556184353689,
    't͡s': 2783230754502126489,
    'ʦ': 2783230754502126489,
    't͜s': 2783230754502126489,
    't̪͡s̪': 2783230479624219545,
    't͡s̪': 2783230479624219545,
    't̟͡s̟': 2783230479624219545,
    't͡s̟': 2783230479624219545,
    'ʦ̪': 2783230479624219545,
    'ʦ̟': 2783230479624219545,
    't͡θ̠': 2783230754502126505,
    't͡θ͇': 2783230754502126505,
    't͡θ': 2783230479624219561,
    't͜θ': 2783230479624219561,
    't̪͡θ': 2783230479624219561,
    't̟͡θ': 2783230479624219561,
    'd͡z': 2783230754501864345,
    'ʣ': 2783230754501864345,
    'd͜z': 2783230754501864345,
    'd̪͡z̪': 2783230479623957401,
    'd͡z̪': 2783230479623957401,
    'd̟͡z̟': 2783230479623957401,
    'd͡z̟': 2783230479623957401,
    'ʣ̪': 2783230479623957401,
    'ʣ̟': 2783230479623957401,
    'd͡ð̠': 2783230754501864361,
    'd͡ð̳': 2783230754501864361,
    'd͡ð': 2783230479623957417,
    'd͜ð': 2783230479623957417,
    'd̪͡ð': 2783230479623957417,
    'd̟͡ð': 2783230479623957417,
    'k͡x': 2783233462881659817,
    'ɡ͡ɣ': 2783233462881397673,
    'g͡ɣ': 2783233462881397673,
    'p͡f': 2781738167467420585,
    'p̪͡f': 2781702983095331753,
    'b͡v': 2781738167467158441,
    'b̪͡v': 2781702983095069609,
    'b̪͜v': 2781702983095069609,
    't͡ɕ': 2783231539004746649,
    't͜ɕ': 2783231539004746649,
    'ʨ': 2783231539004746649,
    'd͡ʑ': 2783231539004484505,
    'd͜ʑ': 2783231539004484505,
    'ʥ': 2783231539004484505,
    'ʈ͡ʂ': 2783231854013754265,
    't͡ʂ': 2783231854013754265,
    'ɖ͡ʐ': 2783231854013492121,
    'd͡ʐ': 2783231854013492121,
    't͡ɬ': 2783230754502060965,
    't͜ɬ': 2783230754502060965,
    'ƛ': 2783230754502060965,
    'd͡ɮ': 2783230754501864357,
    'c͡ç': 2783233463150095273,
    'c͜ç': 2783233463150095273,
    'ɟ͡ʝ': 2783233463149833129,
    'c͡ʎ̝̥': 2783233463150095269,
    'k͡ʟ̝̊': 2783233462881659813,
    'ɡ͡ʟ̝': 2783233462881397669,
    'q͡χ': 2783233480061529001,
    'ɢ͡ʁ': 2783233480061266857,
    'ɢ͜ʁ': 2783233480061266857,
    'ɧ': 2783231813614217626,
    'k͡p': 2781720534881839786,
    'k͜p': 2781720534881839786,
    'ɡ͡b': 2781720534881577642,
    'kʷ': 2780594634974997162,
    'k͡w': 2780594634974997162,
    'k͜w': 2780594634974997162,
    'kʷh': 2780594634974931626,
    'gʷ': 2780594634974735018,
    'g͡w': 2780594634974735018,
    'gʷh': 2780594634974669482,
    # implosives
    'ɓ̥': 2781720575281355434,
    'ƥ': 2781720575281355434,
    'pʼ↓': 2781720575281355434,
    'ɓ': 2781720575281093290,
    'ɗ̥': 2783230754502105770,
    'ƭ': 2783230754502105770,
    'tʼ↓': 2783230754502105770,
    'ɗ': 2783230754501843626,
    'ᶑ': 2783231854013471402,
    'ʄ̊': 2783233463150074538,
    'ƈ': 2783233463150074538,
    'cʼ↓': 2783233463150074538,
    'ʄ': 2783233463149812394,
    'ɠ': 2783233462881376938,
    'ʛ': 2783233480061246122,
    # clicks
    'ʘ': 2781720575281374890,
    'ʘʰ': 2781720575281309354,
    'ʘ̬': 2781720575281112746,
    'ᶢʘ': 2781720575281112746,
    'ʘ̃': 2781720575281112682,
    'ᵑʘ': 2781720575281112682,
    'ᵐʘ': 2781720575281112682,
    'ʘ̥̃ʰ': 2781720575281309290,
    'ᵑ̊ʘʰ': 2781720575281309290,
    'ʘ̃ˀ': 2781720575281358442,
    'ᵑʘˀ': 2781720575281358442,
    'ʘ̃͜ʔ': 2781720575281358442,
    'ᵑ̊ʘˀ': 2781720575281358442,
    'ǀ': 2783230479624218282,
    'ʇ': 2783230479624218282,
    'ǀ̬': 2783230479623956138,
    'ʇ̬': 2783230479623956138,
    'ᶢǀ': 2783230479623956138,
    'ᶢʇ': 2783230479623956138,
    'ǀ̃': 2783230479623956074,
    'ʇ̃': 2783230479623956074,
    'ᵑǀ': 2783230479623956074,
    'ⁿǀ': 2783230479623956074,
    'ᵑʇ': 2783230479623956074,
    'ǀ̥̃ʰ': 2783230479624152682,
    'ʇ̥̃ʰ': 2783230479624152682,
    'ᵑ̊ǀʰ': 2783230479624152682,
    'ᵑ̊ʇʰ': 2783230479624152682,
    'ǀ̃ˀ': 2783230479624201834,
    'ʇ̃ˀ': 2783230479624201834,
    'ᵑǀˀ': 2783230479624201834,
    'ᵑʇˀ': 2783230479624201834,
    'ᵑ̊ǀˀ': 2783230479624201834,
    'ᵑ̊ʇˀ': 2783230479624201834,
    'ǃ': 2783230754502125226,
    'ʗ': 2783230754502125226,
    'ǃʰ': 2783230754502059690,
    'ʗʰ': 2783230754502059690,
    'ǃ̬': 2783230754501863082,
    'ʗ̬': 2783230754501863082,
    'ᶢǃ': 2783230754501863082,
    'ᶢʗ': 2783230754501863082,
    'ǃ̃': 2783230754501863018,
    'ᵑǃ': 2783230754501863018,
    'ʗ̃': 2783230754501863018,
    'ᵑʗ': 2783230754501863018,
    'ǃ̥̃ʰ': 2783230754502059626,
    'ʗ̃̊ʰ': 2783230754502059626,
    'ᵑ̊ǃʰ': 2783230754502059626,
    'ᵑ̊ʗʰ': 2783230754502059626,
    'ǃ̃ˀ': 2783230754502108778,
    'ʗ̃ˀ': 2783230754502108778,
    'ᵑǃˀ': 2783230754502108778,
    'ᵑʗˀ': 2783230754502108778,
    'ǂ': 2783233463150093994,
    'ʄ̵': 2783233463150093994,
    '⨎': 2783233463150093994,
    'ǂʰ': 2783233463150028458,
    'ǂ̬': 2783233463149831850,
    'ᶢǂ': 2783233463149831850,
    'ǂ̃': 2783233463149831786,
    'ᵑǂ': 2783233463149831786,
    'ǂ̥̃ʰ': 2783233463150028394,
    'ᵑ̊ǂʰ': 2783233463150028394,
    'ǂ̃ˀ': 2783233463150077546,
    'ᵑǂˀ': 2783233463150077546,
    'ᵑǂ͡ʔ': 2783233463150077546,
    'ᵑ̊ǂˀ': 2783233463150077546,
    'ǃ͡s': 2783233463150093978,
    'ǂᶴ': 2783233463150093978,
    'ǁ': 2783230754502125222,
    'ʖ': 2783230754502125222,
    'ǁʰ': 2783230754502059686,
    'ʖʰ': 2783230754502059686,
    'ǁ̬': 2783230754501863078,
    'ʖ̬': 2783230754501863078,
    'ᶢǁ': 2783230754501863078,
    'ᶢʖ': 2783230754501863078,
    'ǁ̃': 2783230754501863014,
    'ʖ̃': 2783230754501863014,
    'ᵑǁ': 2783230754501863014,
    'ᵑʖ': 2783230754501863014,
    'ǁ̥̃ʰ': 2783230754502059622,
    'ʖ̥̃ʰ': 2783230754502059622,
    'ᵑ̊ǁʰ': 2783230754502059622,
    'ᵑ̊ʖʰ': 2783230754502059622,
    'ǁ̃ˀ': 2783230754502108774,
    'ʖ̃ˀ': 2783230754502108774,
    'ᵑǁˀ': 2783230754502108774,
    'ᵑʖˀ': 2783230754502108774,
    'ᵑǁ͡ʔ': 2783230754502108774,
    'ʖ̃͜ʔ': 2783230754502108774,
    'ǃ˞': 2783231854013753002,
    'ǃǁ': 2783231854013753002,
    '‼': 2783231854013753002,
    '!!': 2783231854013753002,
    'ǃ˞ʰ': 2783231854013687466,
    '‼ʰ': 2783231854013687466,
    '!!ʰ': 2783231854013687466,
    'ǃ̬˞': 2783231854013490858,
    'ᶢǃ˞': 2783231854013490858,
    '‼̬': 2783231854013490858,
    '!!̬': 2783231854013490858,
    'ᶢ‼': 2783231854013490858,
    'ᶢ!!': 2783231854013490858,
    'ǃ̃˞': 2783231854013490794,
    'ᵑǃ˞': 2783231854013490794,
    '‼̃': 2783231854013490794,
    '!!̃': 2783231854013490794,
    'ᵑ‼': 2783231854013490794,
    'ᵑ!!': 2783231854013490794,
    'ǃ̥̃˞ʰ': 2783231854013687402,
    'ᵑ̊ǃ˞ʰ': 2783231854013687402,
    '‼̥̃ʰ': 2783231854013687402,
    '!!̥̃ʰ': 2783231854013687402,
    'ᵑ̊‼ʰ': 2783231854013687402,
    'ᵑ̊!!ʰ': 2783231854013687402,
    'ǃ̃˞ˀ': 2783231854013736554,
    'ᵑǃ˞͜ʔ': 2783231854013736554,
    'ᵑ̊‼ˀ': 2783231854013736554,
    'ᵑ‼ˀ': 2783231854013736554,
    '‼̃ˀ': 2783231854013736554,
    'ᵑ̊!!ˀ': 2783231854013736554,
    'ᵑ!!ˀ': 2783231854013736554,
    '!!̃ˀ': 2783231854013736554,
    # vowels
    'i': 1826957412996131242,
    'ɪ': 1826957413067434410,
    'ɩ': 1826957413067434410,
    'u': 1825831513894594986,
    'ʊ': 1825831513965898154,
    'ɷ': 1825831513965898154,
    'ᴜ': 1825831513965898154,
    'ɯ̽': 1826957413872740778,
    'ʊ̜': 2115187790024452522,
    'e': 1826957430176000426,
    'ɛ': 1826957430247303594,
    'o': 1825831531074464170,
    'ɤ': 1826957430981306794,
    'ɔ': 1825831531145767338,
    'ʌ': 1826957431052609962,
    'a': 1826957425952336298,
    'a̟': 1826957425952336298,
    'æ̞': 1826957425952336298,
    'ɶ': 1825831526045493674,
    'æ': 1826957425885227434,
    'y': 1825831513089288618,
    'ʏ': 1825831513160591786,
    'ø': 1825831530269157802,
    'œ': 1825831530340460970,
    'ə': 1828083331160779178,
    'ɵ̞': 1825831531347093930,
    'ə̹': 1825831531347093930,
    'ɞ̝': 1825831531347093930,
    'ɘ̞': 1826957431253936554,
    'ɯ': 1826957413805631914,
    'ɒ': 1825831526850800042,
    'ɑ': 1826957426757642666,
    'ɨ': 1826957414069873066,
    'ï': 1826957414069873066,
    'ʉ': 1825831514163030442,
    'ü': 1825831514163030442,
    'ɘ': 1826957431249742250,
    'ë': 1826957431249742250,
    'ɵ': 1825831531342899626,
    'ö': 1825831531342899626,
    'ɜ': 1826957431316851114,
    'ɛ̈': 1826957431316851114,
    'ɞ': 1825831531410008490,
    'ɔ̈': 1825831531410008490,
    'ä': 1826957427026078122,
    'a̠': 1826957427026078122,
    'ɑ̈': 1826957427026078122,
    'ɐ̞': 1826957427026078122,
    'ɐ': 1828083326865811882,
    'ɜ̞': 1826957426958969258,
    'ɞ̞': 1825831527052126634,
    'ɪ̟': 1826957413063240106,
    'ʏ̟': 1825831513156397482,
    'ʏ̫': 1825550038183881130,
    'ʏʷ': 1825550038183881130,
    'ɪʷ': 1825550038183881130,
    'y̫': 1825550038112577962,
    'yʷ': 1825550038112577962,
    'iʷ': 1825550038112577962,
    'u͍': 1825761145150417322,
    'ɯᵝ': 1825761145150417322,
    'ɯ͡β̞': 1825761145150417322,
    'ʉ͍': 1825761145418852778,
    'ɨᵝ': 1825761145418852778,
    'ɨ͡β̞': 1825761145418852778,
    'ɪ̈': 1826957414136981930,
    'ɨ̞': 1826957414136981930,
    'ɘ̝': 1826957414136981930,
    'ʊ̈': 1825831514230139306,
    'ʉ̞': 1825831514230139306,
    'ø̫': 1825550055292447146,
    'øʷ': 1825550055292447146,
    'eʷ': 1825550055292447146,
    'e̞': 1826957430180194730,
    'ɛ̝': 1826957430180194730,
    'ø̞': 1825831530273352106,
    'œ̝': 1825831530273352106,
    'o̞': 1825831531078658474,
    'ɔ̝': 1825831531078658474,
    'ɤ̞': 1826957430985501098,
    'ʌ̝': 1826957430985501098,
    # feature diacritics
    'ʰ': 65536,
    'ʱ': 327680,
    '̤': 327680,
    'ʼ': 16384,
    '̚': 131072,
    '̬': 262144,
    '̌': 262144,
    '̥': 524288,
    '̊': 524288,
    'ʷ': 6737807255011328,
    'ʲ': 103012106240,
    '̰': 278528,
    '̩': 1152921504606846976,
    '̯': 2305843009213693952,
    '̃': 64,
    '̨': 64,
    '͊': 128,
    'ˠ': 98180268032,
    '̴': 98180268032,
    'ˤ': 32505856,
    '̘': 23068672,
    '̙': 26214400,
    '˭': 688256,
}

_FEATURE_MASK = {
    'syllabic': 3458764513820540928,
    'consonantal': 864691128455135232,
    'sonorant': 216172782113783808,
    'approximant': 54043195528445952,
    'labial': 13510798882111488,
    'round': 3377699720527872,
    'protruded': 844424930131968,
    'compressed': 211106232532992,
    'labiodental': 52776558133248,
    'coronal': 13194139533312,
    'anterior': 3298534883328,
    'distributed': 824633720832,
    'dorsal': 206158430208,
    'high': 51539607552,
    'low': 12884901888,
    'front': 3221225472,
    'back': 805306368,
    'tense': 201326592,
    'pharyngeal': 50331648,
    'atr': 12582912,
    'rtr': 3145728,
    'voice': 786432,
    'spread_glottis': 196608,
    'constricted_glottis': 49152,
    'glottalic_suction': 12288,
    'velaric_suction': 3072,
    'continuant': 768,
    'nasal': 192,
    'strident': 48,
    'lateral': 12,
    'delayed_release': 3,
}


def ipa_to_features(ipa: str) -> List[int]:
    """Convert IPA to features.

    This translates an IPA string of one or more phones to a list of ints
    representing the features of the string.

    Parameters
    ----------
    ipa : str
        The IPA representation of a phone or series of phones

    Returns
    -------
    list of ints
        A representation of the features of the input string

    Examples
    --------
    >>> ipa_to_features('mut')
    [2709662981243185770, 1825831513894594986, 2783230754502126250]
    >>> ipa_to_features('fon')
    [2781702983095331242, 1825831531074464170, 2711173160463936106]
    >>> ipa_to_features('telz')
    [2783230754502126250, 1826957430176000426, 2693158761954453926,
    2783230754501863834]

    .. versionadded:: 0.1.0

    """
    features = []
    pos = 0
    ipa = normalize('NFD', ipa.lower())

    maxsymlen = max(len(_) for _ in _PHONETIC_FEATURES)

    while pos < len(ipa):
        found_match = False
        for i in range(maxsymlen, 0, -1):
            if (
                pos + i - 1 <= len(ipa)
                and ipa[pos : pos + i] in _PHONETIC_FEATURES
            ):
                features.append(_PHONETIC_FEATURES[ipa[pos : pos + i]])
                pos += i
                found_match = True

        if not found_match:
            features.append(-1)
            pos += 1

    return features


def ipa_to_feature_dicts(ipa: str) -> List[Dict[str, str]]:
    """Convert IPA to a feature dict list.

    This translates an IPA string of one or more phones to a list of dicts
    representing the features of the string.

    Parameters
    ----------
    ipa : str
        The IPA representation of a phone or series of phones

    Returns
    -------
    list of dicts
        A representation of the features of the input string

    Examples
    --------
    >>> ipa_to_feature_dicts('mut')
    [{'syllabic': '-',
      'consonantal': '+',
      'sonorant': '+',
      'approximant': '-',
      'labial': '+',
      'round': '-',
      'protruded': '-',
      'compressed': '-',
      'labiodental': '-',
      'coronal': '-',
      'anterior': '0',
      'distributed': '0',
      'dorsal': '-',
      'high': '0',
      'low': '0',
      'front': '0',
      'back': '0',
      'tense': '0',
      'pharyngeal': '-',
      'atr': '0',
      'rtr': '0',
      'voice': '+',
      'spread_glottis': '-',
      'constricted_glottis': '-',
      'glottalic_suction': '-',
      'velaric_suction': '-',
      'continuant': '-',
      'nasal': '+',
      'strident': '-',
      'lateral': '-',
      'delayed_release': '-'},
     {'syllabic': '+',
      'consonantal': '-',
      'sonorant': '+',
      'approximant': '+',
      'labial': '+',
      'round': '+',
      'protruded': '-',
      'compressed': '-',
      'labiodental': '-',
      'coronal': '-',
      'anterior': '0',
      'distributed': '0',
      'dorsal': '+',
      'high': '+',
      'low': '-',
      'front': '-',
      'back': '+',
      'tense': '+',
      'pharyngeal': '+',
      'atr': '+',
      'rtr': '-',
      'voice': '+',
      'spread_glottis': '-',
      'constricted_glottis': '-',
      'glottalic_suction': '-',
      'velaric_suction': '-',
      'continuant': '+',
      'nasal': '-',
      'strident': '-',
      'lateral': '-',
      'delayed_release': '-'},
     {'syllabic': '-',
      'consonantal': '+',
      'sonorant': '-',
      'approximant': '-',
      'labial': '-',
      'round': '0',
      'protruded': '0',
      'compressed': '0',
      'labiodental': '0',
      'coronal': '+',
      'anterior': '+',
      'distributed': '-',
      'dorsal': '-',
      'high': '0',
      'low': '0',
      'front': '0',
      'back': '0',
      'tense': '0',
      'pharyngeal': '-',
      'atr': '0',
      'rtr': '0',
      'voice': '-',
      'spread_glottis': '-',
      'constricted_glottis': '-',
      'glottalic_suction': '-',
      'velaric_suction': '-',
      'continuant': '-',
      'nasal': '-',
      'strident': '-',
      'lateral': '-',
      'delayed_release': '-'}]

    .. versionadded:: 0.4.1

    """
    features = []
    pos = 0
    ipa = normalize('NFD', ipa.lower())

    maxsymlen = max(len(_) for _ in _PHONETIC_FEATURES)

    while pos < len(ipa):
        found_match = False
        for i in range(maxsymlen, 0, -1):
            if (
                pos + i - 1 <= len(ipa)
                and ipa[pos : pos + i] in _PHONETIC_FEATURES
            ):
                feature_int = _PHONETIC_FEATURES[ipa[pos : pos + i]]
                feature_dict = {}
                for feature in _FEATURE_MASK.keys():
                    # each feature mask contains two bits, one each for - and +
                    mask = _FEATURE_MASK[feature]
                    # the lower bit represents +
                    pos_mask = mask >> 1

                    masked = feature_int & mask
                    if masked == 0:
                        feature_dict[feature] = '0'  # 0
                    elif masked == mask:
                        feature_dict[feature] = '+/-'  # +/-
                    elif masked & pos_mask:
                        feature_dict[feature] = '+'  # +
                    else:
                        feature_dict[feature] = '-'  # -
                features.append(feature_dict)
                pos += i
                found_match = True

        if not found_match:
            features.append({})
            pos += 1

    return features


def get_feature(vector: List[int], feature: str) -> List[Union[int, float]]:
    """Get a feature vector.

    This returns a list of ints, equal in length to the vector input,
        representing presence/absence/neutrality with respect to a particular
        phonetic feature.

    Parameters
    ----------
    vector : list
        A tuple or list of ints representing the phonetic features of a phone
        or series of phones (such as is returned by the ipa_to_features
        function)
    feature : str
        A feature name from the set:

            - ``syllabic``
            - ``consonantal``
            - ``sonorant``
            - ``approximant``
            - ``labial``
            - ``round``
            - ``protruded``
            - ``compressed``
            - ``labiodental``
            - ``coronal``
            - ``anterior``
            - ``distributed``
            - ``dorsal``
            - ``high``
            - ``low``
            - ``front``
            - ``back``
            - ``tense``
            - ``pharyngeal``
            - ``atr``
            - ``rtr``
            - ``voice``
            - ``spread_glottis``
            - ``constricted_glottis``
            - ``glottalic_suction``
            - ``velaric_suction``
            - ``continuant``
            - ``nasal``
            - ``strident``
            - ``lateral``
            - ``delayed_release``

    Returns
    -------
    list of ints
        A list indicating presence/absence/neutrality with respect to the
        feature

    Raises
    ------
    AttributeError
        feature must be one of ...

    Examples
    --------
    >>> tails = ipa_to_features('telz')
    >>> get_feature(tails, 'consonantal')
    [1, -1, 1, 1]
    >>> get_feature(tails, 'sonorant')
    [-1, 1, 1, -1]
    >>> get_feature(tails, 'nasal')
    [-1, -1, -1, -1]
    >>> get_feature(tails, 'coronal')
    [1, -1, 1, 1]

    .. versionadded:: 0.1.0

    """
    # :param bool binary: if False, -1, 0, & 1 represent -, 0, & +
    #           if True, only binary oppositions are allowed:
    #           0 & 1 represent - & + and 0s are mapped to -

    if feature not in _FEATURE_MASK:
        raise AttributeError(
            "feature must be one of: '{}'".format(  # noqa: SFS201
                "', '".join(_FEATURE_MASK.keys())
            )
        )

    # each feature mask contains two bits, one each for - and +
    mask = _FEATURE_MASK[feature]
    # the lower bit represents +
    pos_mask = mask >> 1
    retvec = []
    for char in vector:
        if char < 0:
            retvec.append(float('NaN'))
        else:
            masked = char & mask
            if masked == 0:
                retvec.append(0)  # 0
            elif masked == mask:
                retvec.append(2)  # +/-
            elif masked & pos_mask:
                retvec.append(1)  # +
            else:
                retvec.append(-1)  # -

    return retvec


def cmp_features(
    feat1: int,
    feat2: int,
    weights: Optional[
        Union[Sequence[Union[int, float]], Dict[str, Union[int, float]]]
    ] = None,
) -> float:
    """Compare features.

    This returns a number in the range [0, 1] representing a comparison of two
    feature bundles.

    If one of the bundles is negative, -1 is returned (for unknown values)

    If the bundles are identical, 1 is returned.

    If they are inverses of one another, 0 is returned.

    Otherwise, a float representing their similarity is returned.

    Parameters
    ----------
    feat1 : int
        A feature bundle
    feat2 : int
        A feature bundle
    weights : None or list or tuple or dict
        If None, all features are of equal significance and a simple normalized
        hamming distance of the features is calculated. If a list or tuple
        of numeric values is supplied, the values are inferred as the weights
        for each feature, in order of the features listed in _FEATURE_MASK.
        If a dict is supplied, its key values should match keys in
        _FEATURE_MASK to which each weight (value) should be assigned. Missing
        values in all cases are assigned a weight of 0 and will be omitted from
        the comparison.

    Returns
    -------
    float
        A comparison of the feature bundles

    Examples
    --------
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('l')[0])
    1.0
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('n')[0])
    0.8709677419354839
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('z')[0])
    0.8709677419354839
    >>> cmp_features(ipa_to_features('l')[0], ipa_to_features('i')[0])
    0.564516129032258

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.4.1
        Added weights parameter for modifiable feature weighting

    """
    if feat1 < 0 or feat2 < 0:
        return 0.0
    if feat1 == feat2:
        return 1.0

    # This should be handled some other way since this will take a long time
    # when done repeatedly. Maybe convert to a class & save the weights list.
    if weights is not None:
        if isinstance(weights, dict):
            weights = [
                weights[feature] if feature in weights else 0
                for feature in sorted(
                    _FEATURE_MASK, key=_FEATURE_MASK.get, reverse=True
                )
            ]
        elif isinstance(weights, (list, tuple)):
            weights = list(weights) + [0] * (len(_FEATURE_MASK) - len(weights))
        else:
            raise TypeError('weights must be a dist, list, or tuple.')

    magnitude = sum(weights) if weights else len(_FEATURE_MASK)

    """
    # Alternate implementation
    diff_feats = 0
    i = 0
    while feat1 or feat2:
        f1 = feat1 & 0b11
        f2 = feat2 & 0b11
        if (not (0b11 in {f1, f2} and (f1 in {0b01, 0b10} or
            f2 in {0b01, 0b10}))) and (f1 != f2):
            diff_feats += weights[i] if weights else 1

        feat1 >>= 2
        feat2 >>= 2
        i += 1

    return 1 - (diff_feats / magnitude)
    """

    featxor = feat1 ^ feat2
    diffbits = 0.0
    i = 0
    while featxor:
        if featxor & 0b1:
            diffbits += weights[i] if weights else 1
        featxor >>= 1
        if featxor & 0b1:
            diffbits += weights[i] if weights else 1
        featxor >>= 1
        i += 1
    return 1 - (0 if not diffbits else (diffbits / (2 * magnitude)))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
