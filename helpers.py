# -*- coding: utf-8 -*-

import re

from pybo import SylComponents


class Agreement:
    def __init__(self):
        self.sc = SylComponents()
        self.cases = []
        data = {"particles":
            {
                "dreldra": ["གི", "ཀྱི", "གྱི", "ཡི"],
                "jedra": ["གིས", "ཀྱིས", "གྱིས", "ཡིས"],
                "ladon": ["སུ", "ཏུ", "དུ", "རུ"],
                "lhakce": ["སྟེ", "ཏེ", "དེ"],
                "gyendu": ["ཀྱང", "ཡང", "འང"],
                "jedu": ["གམ", "ངམ", "དམ", "ནམ", "བམ", "མམ", "འམ", "རམ", "ལམ", "སམ", "ཏམ"],
                "dagdra_pa": ["པ", "བ"],
                "dagdra_po": ["པོ", "བོ"],
                "lardu": ["གོ", "ངོ", "དོ", "ནོ", "བོ", "མོ", "འོ", "རོ", "ལོ", "སོ", "ཏོ"],
                "cing": ["ཅིང", "ཤིང", "ཞིང"],
                "ces": ["ཅེས", "ཞེས"],
                "ceo": ["ཅེའོ", "ཤེའོ", "ཞེའོ"],
                "cena": ["ཅེ་ན", "ཤེ་ན", "ཞེ་ན"],
                "cig": ["ཅིག", "ཤིག", "ཞིག"],
                "gin": ["ཀྱིན", "གིན", "གྱིན"]
            },
            "corrections":
                {
                    "dreldra": {"ད": "ཀྱི", "བ": "ཀྱི", "ས": "ཀྱི", "ག": "གི", "ང": "གི", "ན": "གྱི", "མ": "གྱི",
                                "ར": "གྱི", "ལ": "གྱི", "འ": "ཡི", "མཐའ་མེད": "ཡི", "ད་དྲག": "གྱི"},
                    "jedra": {"ད": "ཀྱིས", "བ": "ཀྱིས", "ས": "ཀྱིས", "ག": "གིས", "ང": "གིས", "ན": "གྱིས", "མ": "གྱིས",
                              "ར": "གྱིས", "ལ": "གྱིས", "འ": "ཡིས", "མཐའ་མེད": "ཡིས", "ད་དྲག": "གྱིས"},
                    "ladon": {"ག": "ཏུ", "བ": "ཏུ", "ང": "དུ", "ད": "དུ", "ན": "དུ", "མ": "དུ", "ར": "དུ", "ལ": "དུ",
                              "འ": "རུ", "ས": "སུ", "མཐའ་མེད": "རུ", "ད་དྲག": "ཏུ"},
                    "lhakce": {"ན": "ཏེ", "ར": "ཏེ", "ལ": "ཏེ", "ས": "ཏེ", "ད": "དེ", "ག": "སྟེ", "ང": "སྟེ",
                               "བ": "སྟེ", "མ": "སྟེ", "འ": "སྟེ", "མཐའ་མེད": "སྟེ", "ད་དྲག": "ཏེ"},
                    "gyendu": {"ག": "ཀྱང", "ད": "ཀྱང", "བ": "ཀྱང", "ས": "ཀྱང", "འ": "ཡང", "ང": "ཡང", "ན": "ཡང",
                               "མ": "ཡང", "ར": "ཡང", "ལ": "ཡང", "མཐའ་མེད": "ཡང", "ད་དྲག": "ཀྱང"},
                    "jedu": {"ག": "གམ", "ང": "ངམ", "ད་དྲག": "ཏམ", "ད": "དམ", "ན": "ནམ", "བ": "བམ", "མ": "མམ", "འ": "འམ",
                             "ར": "རམ", "ལ": "ལམ", "ས": "སམ", "མཐའ་མེད": "འམ"},
                    "dagdra_pa": {"ག": "པ", "ད": "པ", "བ": "པ", "ས": "པ", "ན": "པ", "མ": "པ", "ང": "བ", "འ": "བ",
                                  "ར": "བ", "ལ": "བ", "མཐའ་མེད": "བ", "ད་དྲག": "པ"},
                    "dagdra_po": {"ག": "པོ", "ད": "པོ", "བ": "པོ", "ས": "པོ", "ན": "པོ", "མ": "པོ", "ང": "བོ",
                                  "འ": "བོ", "ར": "བོ", "ལ": "བོ", "མཐའ་མེད": "བོ", "ད་དྲག": "པོ"},
                    "lardu": {"ག": "གོ", "ང": "ངོ", "ད": "དོ", "ན": "ནོ", "བ": "བོ", "མ": "མོ", "འ": "འོ", "ར": "རོ",
                              "ལ": "ལོ", "ས": "སོ", "མཐའ་མེད": "འོ", "ད་དྲག": "ཏོ"},
                    "cing": {"ག": "ཅིང", "ད": "ཅིང", "བ": "ཅིང", "ང": "ཞིང", "ན": "ཞིང", "མ": "ཞིང", "འ": "ཞིང",
                             "ར": "ཞིང", "ལ": "ཞིང", "ས": "ཤིང", "མཐའ་མེད": "ཞིང", "ད་དྲག": "ཅིང"},
                    "ces": {"ག": "ཅེས", "ད": "ཅེས", "བ": "ཅེས", "ང": "ཞེས", "ན": "ཞེས", "མ": "ཞེས", "འ": "ཞེས",
                            "ར": "ཞེས", "ལ": "ཞེས", "ས": "ཞེས", "མཐའ་མེད": "ཞེས", "ད་དྲག": "ཅེས"},
                    "ceo": {"ག": "ཅེའོ", "ད": "ཅེའོ", "བ": "ཅེའོ", "ང": "ཞེའོ", "ན": "ཞེའོ", "མ": "ཞེའོ", "འ": "ཞེའོ",
                            "ར": "ཞེའོ", "ལ": "ཞེའོ", "ས": "ཤེའོ", "མཐའ་མེད": "ཞེའོ", "ད་དྲག": "ཅེའོ"},
                    "cena": {"ག": "ཅེ་ན", "ད": "ཅེ་ན", "བ": "ཅེ་ན", "ང": "ཞེ་ན", "ན": "ཞེ་ན", "མ": "ཞེ་ན", "འ": "ཞེ་ན",
                             "ར": "ཞེ་ན", "ལ": "ཞེ་ན", "ས": "ཤེ་ན", "མཐའ་མེད": "ཞེ་ན", "ད་དྲག": "ཅེ་ན"},
                    "cig": {"ག": "ཅིག", "ད": "ཅིག", "བ": "ཅིག", "ང": "ཞིག", "ན": "ཞིག", "མ": "ཞིག", "འ": "ཞིག",
                            "ར": "ཞིག", "ལ": "ཞིག", "ས": "ཤིག", "མཐའ་མེད": "ཞིག", "ད་དྲག": "ཅིག"},
                    "gin": {"ད": "ཀྱིན", "བ": "ཀྱིན", "ས": "ཀྱིན", "ག": "གིན", "ང": "གིན", "ན": "གྱིན", "མ": "གྱིན",
                            "ར": "གྱིན", "ལ": "གྱིན", "ད་དྲག": "ཀྱིན"}
                }
        }

        for part in data['particles']:
            self.cases.append((data['particles'][part], data['corrections'][part]))

    def part_agreement(self, previous_syl, particle):
        """
        proposes the right particle according to the previous syllable.
            In case of an invalid previous syllable, returns the particle preceded by *
            limitation : particle needs to be a separate syllabes. (the problems with wrong merged agreement will be flagged by get_mingzhi )
            input : previous syllable, particle
        :param previous_syl: preceding syllable
        :param particle: particle at hand
        :return: the correct agreement for the preceding syllable
        """
        previous = self.sc.get_info(previous_syl)
        mingzhi = self.sc.get_mingzhi(previous_syl)

        if previous == 'dadrag':
            final = 'ད་དྲག'
        elif previous == 'thame':
            # the agreement of thame syllable often depend on their ending and not on their mingzhi
            # a thame syllable can end this way : [ྱྲླྭྷ]?[ིེོུ]?(འ[ིོུ]|ར|ས)
            ssyl = re.sub(r'[ིེོུ]$', '', previous_syl)  # removes vowels occurring after འ
            if ssyl[-1] == mingzhi:  # if the mingzhi was only followed by a vowel
                final = 'མཐའ་མེད'
            elif ssyl.endswith('འ'):  # if the syllable ended either by འི, འུ or འོ
                final = 'འ'
            elif ssyl.endswith('ར'):  # if the syllable ended with a ར
                final = 'ར'
            elif ssyl.endswith('ས'):  # if the syllable ended with a ས
                final = 'ས'
            elif ssyl[-2] == mingzhi:  # if the syllable ended with [ྱྲླྭྷ] plus a vowel
                final = 'མཐའ་མེད'
            else:  # catch all other cases
                final = None
        else:
            final = previous[-1]
            if final not in ['ག', 'ང', 'ད', 'ན', 'བ', 'མ', 'འ', 'ར', 'ལ', 'ས']:
                final = None

        if final:
            # added the ད་དྲག་ for all and the མཐའ་མེད་ for all in provision of all cases
            # where an extra syllable is needed in verses
            # dadrag added according to Élie’s rules.

            correction = ''
            for case in self.cases:
                if particle in case[0]:
                    correction = case[1][final]
            return correction
        else:
            return '*' + particle


def pre_process(raw_string, mode='words'):
    """
    Splits a raw Tibetan orig_list by the punctuation and syllables or words
    :param raw_string:
    :param mode: words for splitting on words, syls for splitting in syllables. Default value is words
    :return: a list with the elements separated from the punctuation
    """
    # replace all underscore if the string contains any
    if '_' in raw_string:
        raw_string = raw_string.replace('_', ' ')

    def is_punct(string):
        # put in common
        if '༄' in string or '༅' in string or '༆' in string or '༇' in string or '༈' in string or \
            '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or \
            '༔' in string or ';' in string or ':' in string:
            return True
        else:
            return False

    def trim_punct(l):
        i = 0
        while i < len(l) - 1:
            if is_punct(l[i]) and is_punct(l[i + 1]):
                del l[i + 1]
            i += 1

    yigo = r'((༄༅+|༆|༇|༈)།?༎? ?།?༎?)'
    text_punct = r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)'
    splitted = []
    # replace unbreakable tsek and tabs
    raw_string = raw_string.replace('༌', '་').replace('   ', ' ')
    # split the raw orig_list by the yigos,
    for text in re.split(yigo, raw_string):
        # add the yigos to the list
        if re.match(yigo, text):
            splitted.append(text.replace(' ', '_'))
        elif text != '':
            # split the orig_list between yigos by the text pre_process
            for par in re.split(text_punct, text):
                # add the pre_process to the list
                if is_punct(par):
                    splitted.append(par.replace(' ', '_'))
                elif par != '':
                    # add the segmented text split on words
                    if mode == 'words':
                        splitted.extend(par.split(' '))
                    # add the non-segmented text by splitting it on syllables.
                    elif mode == 'syls':
                        temp = []
                        for chunk in par.split(' '):
                            if '་' in chunk:
                                word = ''
                                for c in chunk:
                                    if c == '་':
                                        word += c
                                        temp.append(word)
                                        word = ''
                                    else:
                                        word += c
                                # adding the last word in temp[]
                                if word != '':
                                    temp.append(word)
                            else:
                                temp.append(chunk)
                        splitted.extend(temp)
                    else:
                        print('non-valid splitting mode. choose either "words" or "syls".')
                        break
    # trim the extra pre_process
    trim_punct(splitted)
    return splitted


def tib_sort(l):
    """
    sorts a list according to the Tibetan order
    code from https://github.com/eroux/tibetan-collation/blob/master/implementations/Unicode/rules-icu52.txt
    :param l: list to sort
    :return: sorted list
    """
    from icu import RuleBasedCollator
    rules = '\n# Rules for Sanskrit ordering\n# From Bod rgya tshig mdzod chen mo pages 9 - 11, 347, 1153, 1615, 1619, 1711, 1827, 2055, 2061, 2840, 2920, 3136 and 3137\n# Example: ཀར་ལུགས།  < ཀརྐ་ཊ།\n&ཀར=ཀར\n&ཀལ=ཀལ\n&ཀས=ཀས\n&གཉྫ=གཉྫ\n&ཐར=ཐར\n&པུས=པུས\n&ཕལ=ཕལ\n&བིལ=བིལ\n&མཉྫ=མཉྫ\n&མར=མར\n&ཤས=ཤས\n&སར=སར\n&ཨར=ཨར\n&ཨས=ཨས\n# Marks (seconadry different, with low equal primary weight after Lao)\n&[before 1]ཀ<།<<༎<<༏<<༐<<༑<<༔<<༴<་=༌\n&ཀ<<ྈྐ<ཫ<དཀ<བཀ<རྐ<ལྐ<སྐ<བརྐ<བསྐ\n&ཁ<<ྈྑ<མཁ<འཁ\n&ག<དགག<དགང<དགད<དགན<དགབ<དགཝ<དགའ<དགར<དགལ<དགས<དགི<དགུ<དགེ<དགོ<དགྭ<དགྱ<དགྲ<བགག<བགང<བགད<བགབ<བགམ<<<བགཾ<བགཝ<བགའ\n		<བགར<བགལ<བགི<བགུ<བགེ<བགོ<བགྭ<བགྱ<བགྲ<བགླ<མགག<མགང<མགད<མགབ<མགའ<མགར<མགལ<མགི<མགུ<མགེ<མགོ<མགྭ<མགྱ<མགྲ<འགག<འགང<འགད<འགན<འགབ<འགམ<<<འགཾ\n		<འགའ<འགར<འགལ<འགས<འགི<འགུ<འགེ<འགོ<འགྭ<འགྱ<འགྲ<རྒ<ལྒ<སྒ<བརྒ<བསྒ\n&ང<<<ྂ<<<ྃ<དངག<དངང<དངད<དངན<དངབ<དངའ<དངར<དངལ<དངི<དངུ<དངེ<དངོ<མངག<མངང<མངད<མངན<མངབ<མངའ<མངར<མངལ<མངི<མངུ<མངེ<མངོ<རྔ<ལྔ<སྔ<བརྔ<བསྔ\n&ཅ<གཅ<བཅ<ལྕ<བལྕ\n&ཆ<མཆ<འཆ\n&ཇ<མཇ<འཇ<རྗ<ལྗ<བརྗ\n&ཉ<<ྋྙ<གཉ<མཉ<རྙ=ཪྙ<སྙ<བརྙ=བཪྙ<བསྙ\n&ཏ<ཊ<ཏྭ<ཏྲ<གཏ<བཏ<རྟ<ལྟ<སྟ<བརྟ<བལྟ<བསྟ\n&ཐ<ཋ<མཐ<འཐ\n&ད<ཌ<གདག<གདང<གདད<གདན<གདབ<གདམ<<<གདཾ<གདའ<གདར<གདལ<གདས<གདི<གདུ<གདེ<གདོ<གདྭ<བདག<བདང<བདད<བདབ<བདམ<<<བདཾ<བདའ\n		<བདར<བདལ<བདས<བདི<བདུ<བདེ<བདོ<བདྭ<མདག<མདང<མདད<མདན<མདབ<མདའ<མདར<མདལ<མདས<མདི<མདུ<མདེ<མདོ<མདྭ<འདག<འདང<འདད<འདན<འདབ<འདམ<<<འདཾ\n		<འདཝ<འདའ<འདར<འདལ<འདས<འདི<འདུ<འདེ<འདོ<འདྭ<འདྲ<རྡ<ལྡ<སྡ<བརྡ<བལྡ<བསྡ\n&ན<ཎ<གནག<གནང<གནད<གནན<གནབ<གནམ<<<གནཾ<གནཝ<གནའ<གནར<གནལ<གནས<གནི<གནུ<གནེ<གནོ<གནྭ<མནག<མནང<མནད<མནན<མནབ<མནམ<<<མནཾ<མནའ\n		<མནར<མནལ<མནས<མནི<མནུ<མནེ<མནོ<མནྭ<རྣ<སྣ<བརྣ<བསྣ\n&པ<<ྉྤ<དཔག<དཔང<དཔད<དཔབ<དཔའ<དཔར<དཔལ<དཔས<དཔི<དཔུ<དཔེ<དཔོ<དཔྱ<དཔྲ<ལྤ<སྤ\n&ཕ<<ྉྥ<འཕ\n&བ<དབག<དབང<དབད<དབན<དབབ<དབའ<དབར<དབལ<དབས<དབི<དབུ<དབེ<དབོ<དབྱ<དབྲ<འབག<འབང<འབད<འབན<འབབ<འབམ\n	<<<འབཾ<འབའ<འབར<འབལ<འབས<འབི<འབུ<འབེ<འབོ<འབྱ<འབྲ<རྦ<ལྦ<སྦ\n&མ<<<ཾ<དམག<དམང<དམད<དམན<དམབ<དམཝ<དམའ<དམར<དམལ<དམས<དམི<དམུ<དམེ<དམོ<དམྭ<དམྱ<རྨ<སྨ\n&ཙ<གཙ<བཙ<རྩ<སྩ<བརྩ<བསྩ\n&ཚ<མཚ<འཚ\n&ཛ<མཛ<འཛ<རྫ<བརྫ\n# &ཝ\n&ཞ<གཞ<བཞ\n&ཟ<གཟ<བཟ\n# &འ\n&ཡ<གཡ\n&ར<<<ཪ<ཬ<བརླ=བཪླ\n# &ལ\n&ཤ<ཥ<གཤ<བཤ\n&ས<གསག<གསང<གསད<གསན<གསབ<གསའ<གསར<གསལ<གསས<གསི<གསུ<གསེ<གསོ<གསྭ<བསག<བསང<བསད<བསབ<བསམ<<<བསཾ<བསའ<བསར\n		<བསལ<བསས<བསི<བསུ<བསེ<བསོ<བསྭ<བསྲ<བསླ\n&ཧ<ལྷ\n&ཨ\n# Explicit vowels\n<ཱ<ི<ཱི<ྀ<ཱྀ<ུ<ཱུ<ེ<ཻ=ེེ<ོ<ཽ=ོོ\n# Post-radicals\n	<ྐ<ྑ<ྒ<ྔ<ྕ<ྖ<ྗ<ྙ<ྟ<ྚ<ྠ<ྛ<ྡ<ྜ<ྣ<ྞ<ྤ<ྥ<ྦ<ྨ<ྩ<ྪ<ྫ<ྭ<<<ྺ<ྮ<ྯ<ྰ<ྱ<<<ྻ<ྲ<<<ྼ<ླ<ྴ\n	<ྵ<ྶ<ྷ<ྸ\n# Combining marks and signs (secondary weight)\n&༹<<྄<<ཿ<<྅<<ྈ<<ྉ<<ྊ<<ྋ<<ྌ<<ྍ<<ྎ<<ྏ\n# Treatༀ,  ཷand ,ཹ as decomposed\n&ཨོཾ=ༀ\n&ྲཱྀ=ཷ\n&ླཱྀ=ཹ'
    collator = RuleBasedCollator('[normalization on]\n' + rules)
    return sorted(l, key=collator.getSortKey)
