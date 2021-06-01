import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextCleaner:
    def __init__(self):
        self.settings = self.get_settings()
        self.lang_settings = {
            'english': {'active': True, 'words': set(stopwords.words('english'))},
            'french' : {'active': True, 'words': set(stopwords.words('french'))},
            'italian': {'active': True, 'words': set(stopwords.words('italian'))},
            'spanish': {'active': True, 'words': set(stopwords.words('spanish'))}}
        
        self.white_list = []
        self.black_list = []

    def get_settings(self):
        return {
            'remove_punctuation': {'active': True, 'action': self.remove_punctuation},
            'lower_case':         {'active': True, 'action': self.lowerize},
            'remove_stopword':    {'active': True, 'action': self.remove_stopwords},
            'stemming':           {'active': False, 'action': self.stemming},
            'too_long':           {'active': True, 'action': self.too_long}
        }

    def clean_text(self, to_clean, **kwargs):
        tokens = self.tokenize(to_clean)

        for k, params in self.settings.items():

            if params['active']:
                tokens = params['action'](tokens)

        if 'stringify' in kwargs:
            if kwargs['stringify']:
                return ' '.join(tokens)
        else:  
            return tokens

    @staticmethod
    def tokenize(text):
        return word_tokenize(text)

    @staticmethod
    def remove_punctuation(tokens):
        future_tokens = []
        whitelist = string.ascii_letters + ' ' + "'" + 'éèàçùëê'
        for text in tokens:      
            try:
                future_tokens.append(''.join(character for character in text if character in whitelist))
            except TypeError as e:
                print(f'Error removing punctuation from token:\n{e}')
        return future_tokens

    @staticmethod
    def lowerize(tokens):
        return [w.lower() for w in tokens]

    def remove_stopwords(self, tokens):
        return [w for w in tokens if w not in self.create_stopwords()]

    @staticmethod
    def stemming(tokens):
        porter = PorterStemmer()
        return [porter.stem(word) for word in tokens]

    @staticmethod
    def too_long(tokens):
        return [w for w in tokens if len(w) < 13]

    def create_stopwords(self):
        stop_words = set(self.black_list)
        for v in self.lang_settings.values():
            if v['active']:
                stop_words = set.union(stop_words, v['words'])
        stop_words = [w for w in stop_words if w not in self.white_list]
        return stop_words

if __name__ == '__main__':
    cleaner = TextCleaner()
    text = "Today we're going to clean a lot of text easily!"
    cleaner.white_list = []
    cleaner.black_list = []

    cleaner.lang_settings['french']['active'] = False
    cleaner.settings['lower_case']['active'] = False
    cleaned_text = cleaner.clean_text(text)
    print(cleaned_text)

