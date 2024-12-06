import pandas as pd
import numpy as np
import re
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud, STOPWORDS
import demoji
import string
from textblob import TextBlob

import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector

from collections import Counter
import string
import wordcloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.base import BaseEstimator, TransformerMixin
from string import punctuation
PUNCTUATION = string.punctuation

nltk.download('punkt_tab')  # If `punkt_tab` is required
nltk.download('punkt')  # Regular Punkt tokenizer


class SegmentFeaturizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.future_words = ["tomorrow", "future", "futures"]
        
    @staticmethod
    def getCharCount(doc):
#         print(len(doc.text))
        return len(doc.text)
    
    @staticmethod
    def getWordsInSen(doc):
        res = sum([i.strip(string.punctuation).isalpha() for i in doc.text.split()])
        return res
    
    @staticmethod
    def noSen(doc):
        return len(nltk.sent_tokenize(doc.text))
    
    @staticmethod
    def noUniqueWord(doc):
        return len(set(doc.text.split()))
    
    @staticmethod
    def avgWordLenInSen(doc):
        words = [word for word in doc.text.split() if word]
        if (len(words) != 0):
            avg = sum(map(len, words))/len(words)
            return avg
        else:
            return 0
        
    @staticmethod
    def avgSenLen(doc):
        if (SegmentFeaturizer.noSen(doc) != 0):
            return (SegmentFeaturizer.getWordsInSen(doc) / SegmentFeaturizer.noSen(doc))
        else:
            return 0

    @staticmethod
    def count_pronouns(doc):
        segment = doc.text.lower().split()
        counter = {"1sg": 0, "1pl": 0}
        for pronoun in FIRST_SINGULAR:
            counter["1sg"] += segment.count(pronoun)
        for pronoun in FIRST_PLURAL:
            counter["1pl"] += segment.count(pronoun)
        return counter

    @staticmethod
    def getWordInDoubleQuote(doc):
        return len(re.findall(r'["][\w\s]+["]', doc.text))
    
    @staticmethod
    def getNoStopWords(doc):
        return len([x for x in nltk.word_tokenize(doc.text) if x in STOPWORDS])


    @staticmethod
    def getPunctuationcount(doc):
        return len("".join(x for x in doc.text if x in PUNCTUATION))
    
    @staticmethod
    def getNoPositiveWords(doc):
        return len([i for i in doc.text.split() if TextBlob(i).sentiment.polarity >= 0.5])
    
    @staticmethod
    def getNoNegativeWords(doc):
        return len([i for i in doc.text.split() if TextBlob(i).sentiment.polarity >= 0.5])

    @staticmethod
    def get_n_words_before_main_verb(doc):
        numbers = [0]
        for sent in doc.sents:
            main = [t for t in sent if t.dep_ == "ROOT"][0]
            if main.pos_ == "VERB":
                dist_to_init = main.i - sent[0].i
                numbers.append(dist_to_init)
        return np.mean(numbers)

    @staticmethod
    def get_n_complex_clauses(doc):
        embedded_elements_count = []
        for sent in doc.sents:
            n_embedded = len(
                [t for t in sent if t.dep_ in {"ccomp", "xcomp", "advcl", "dative"}]
            )
            embedded_elements_count.append(n_embedded)
        return np.mean(embedded_elements_count)
    
    # putting it all together!
    def featurize(self, segments):
        feature_dicts = []
        docs = self.nlp.pipe(segments)
        for doc in docs:
            feature_dict = {
                'charCount': self.getCharCount(doc),
                'getWordsInSen': self.getWordsInSen(doc),
                'noSen': self.noSen(doc),
                'noUniqueWord': self.noUniqueWord(doc),
                'avgWordLenInSen': self.avgWordLenInSen(doc),
                'avgSenLen': self.avgSenLen(doc),
                "n_complex_clauses": self.get_n_complex_clauses(doc),
                "n_words_before_main_verb": self.get_n_words_before_main_verb(doc),
                'getNoNegativeWords': self.getNoNegativeWords(doc),
                'getNoPositiveWords': self.getNoPositiveWords(doc),
                'getPunctuationcount': self.getPunctuationcount(doc),
                'getNoStopWords': self.getNoStopWords(doc),
                'getWordInDoubleQuote': self.getWordInDoubleQuote(doc),
                
            }
            feature_dicts.append(feature_dict)
        return feature_dicts

segment_featurizer = SegmentFeaturizer()  # more on this below
class CustomLinguisticFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.l = 1
    def fit(self, x, y=None):
        return self
    def transform(self, data):
        return segment_featurizer.featurize(data)