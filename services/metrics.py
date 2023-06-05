import re
from joblib import load
import nltk
from collections import Counter
from lexicalrichness import LexicalRichness

# Tokens = Words
# Types = Different Words


class Metrics():

    def __init__(self, text):
        self.text = text
        self.lex = LexicalRichness(text.replace("\n", " "))
        self.pos_tagger = load("./services/tagger/POS_tagger_brill.pkl")
        self.tagger_words = dict(self.pos_tagger.tag(
            nltk.word_tokenize(self.text.lower())))

    # Use python's method Counter() to get the word frequency.
    def wordFrequency(self, text):
        # Select only the alphanumerics
        text = re.sub(r'[^\w\d\s]', ' ', text)

        # Convert the text to lowercase
        text = text.lower()

        # Separate words in an array
        result = re.split("[^\w]+", text)

        if (result[-1] == ''):
            result.pop()
        return Counter(result)

    # Counts the number of tokens.
    def numberOfTokens(self):
        return self.lex.words

    # Counts the number of different words in the text.
    def numberOfTypes(self):
        return self.lex.terms

    # Counts the number of lines in the text based on how many "\n" the text has.
    def numberOfLines(self):
        lines = 1
        for char in self.text:
            if char == '\n':
                lines += 1
        return lines

    # Calculates the lexical density value based on Ure's method.
    def calculateUre(self):
        pos = self.pos_tagger.tag(nltk.word_tokenize(self.text))
        lexitems = 0

        for item in pos:
            if (item[1] == 'ADJ') or (item[1] == 'VAUX') or (item[1] == 'N') or \
                    (item[1] == 'NPROP') or (item[1] == 'V'):
                lexitems += 1

        tokens = self.numberOfTokens()

        return lexitems*100/tokens

    # Calculates the lexical density value based on Halliday's method.
    def calculateHalliday(self):
        pos = self.pos_tagger.tag(nltk.word_tokenize(self.text))
        lexitems = 0

        for item in pos:
            if (item[1] == 'ADJ') or (item[1] == 'VAUX') or (item[1] == 'N') or \
                (item[1] == 'NPROP') or (item[1] == 'V') or (item[1] == 'ADV') or \
                    (item[1] == 'ADV-KS') or (item[1] == 'ADV-KS-REL'):
                lexitems += 1

        tokens = self.numberOfTokens()

        return lexitems*100/tokens

    # Counts the occurrences of each of the lexical items extracted from the text
    # pos_dict = Pos-Tagger Object
    # freq_dict = wordFrequency() Object
    def countLexicalItems(self):
        pos_dict = dict(self.pos_tagger.tag(
            nltk.word_tokenize(self.text.lower())))
        freq_dict = self.wordFrequency(self.text)

        pos_subs = 0
        pos_verbs = 0
        pos_adj = 0
        pos_adv = 0

        for wd in freq_dict:
            if (pos_dict[wd] == 'N' or pos_dict[wd] == 'NPROP'):
                pos_subs += freq_dict[wd]
            elif (pos_dict[wd] == 'V' or pos_dict[wd] == 'VAUX'):
                pos_verbs += freq_dict[wd]
            elif (pos_dict[wd] == 'ADJ'):
                pos_adj += freq_dict[wd]
            elif (pos_dict[wd] == 'ADV' or pos_dict[wd] == 'ADV-KS' or pos_dict[wd] == 'ADV-KS-REL'):
                pos_adv += freq_dict[wd]

        return pos_subs, pos_verbs, pos_adj, pos_adv

    # Counts the occurrences of each of the non-lexical items extracted from the text
    # pos_dict = Pos-Tagger Object
    # freq_dict = wordFrequency() Object
    def countNonLexicalItems(self):
        pos_dict = dict(self.pos_tagger.tag(
            nltk.word_tokenize(self.text.lower())))
        freq_dict = self.wordFrequency(self.text)

        pos_pro = 0
        pos_art = 0
        pos_others = 0

        for wd in freq_dict:
            if (pos_dict[wd] != 'N' and pos_dict[wd] != 'NPROP' and pos_dict[wd] != 'V' and pos_dict[wd] != 'VAUX' and pos_dict[wd] != 'ADJ' and pos_dict[wd] != 'ADV' and pos_dict[wd] != 'ADV-KS' and pos_dict[wd] != 'ADV-KS-REL'):
                if (pos_dict[wd] == 'PROADJ' or pos_dict[wd] == 'PROPESS' or pos_dict[wd] == 'PROSUB' or pos_dict[wd] == 'PRO-KS' or pos_dict[wd] == 'PRO-KS-REL'):
                    pos_pro += freq_dict[wd]
                elif (pos_dict[wd] == 'ART'):
                    pos_art += freq_dict[wd]
                else:
                    pos_others += freq_dict[wd]
        print("done:", pos_pro, pos_art, pos_others)
        return pos_pro, pos_art, pos_others

    # Calculates the lexical diversity value based on TTR's method.
    def calculateTTR(self):
        return self.lex.ttr

    # Calculates the lexical diversity value based on RTTR's method.
    def calculateRTTR(self):
        return self.lex.rttr

    # Calculates the lexical diversity value based on CTTR's method.
    def calculateCTTR(self):
        return self.lex.cttr

    # Calculates the lexical diversity value based on MSTTR's method.
    def calculateMSTTR(self):
        return self.lex.msttr(segment_window=25)

    # Calculates the lexical diversity value based on MATTR's method.
    def calculateMATTR(self):
        return self.lex.mattr(window_size=25)

    # Calculates the lexical diversity value based on MTLD's method.
    def calculateMTLD(self):
        return self.lex.mtld(threshold=0.72)

    # Calculates the lexical diversity value based on HDD's method.
    def calculateHDD(self):
        return self.lex.hdd(draws=42)

    # Calculates the lexical diversity value based on VOCD's method.
    def calculateVOCD(self):
        return self.lex.vocd()

    # Calculates the lexical diversity value based on Herdan's method.
    def calculateHerdan(self):
        return self.lex.Herdan

    # Calculates the lexical diversity value based on Summer's method.
    def calculateSummer(self):
        return self.lex.Summer

    # Calculates the lexical diversity value based on Dugast's method.
    def calculateDugast(self):
        return self.lex.Dugast

    # Calculates the lexical diversity value based on Maas's method.
    def calculateMaas(self):
        return self.lex.Maas
