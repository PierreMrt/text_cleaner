# Standard libraries
import contractions
import re
import string
from types import SimpleNamespace

# Nltk download
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
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
        settings = {
            'remove_punctuation': {'active': True, 'action': self.remove_punctuation},
            'remove_numeric'    : {'active': True, 'action': self.remove_numeric},
            'lower_case'        : {'active': True, 'action': self.lowerize},
            'remove_stopword'   : {'active': True, 'action': self.remove_stopwords},
            'stemming'          : {'active': False, 'action': self.stemming},
            'too_long'          : {'active': True, 'action': self.too_long}
        }
        return RecursiveNamespace(**settings)


    def clean_text(self, to_clean, **kwargs):
        to_clean = contractions.fix(to_clean) # Expand contractions
        tokens = self.tokenize(to_clean)

        for params in self.settings.values():
            if params['active']:
                tokens = params['action'](tokens)

        [tokens.remove(w) for w in tokens if w == ''] # Remove empty tokens

        if 'stringify' in kwargs:
            if kwargs['stringify']:
                return ' '.join(tokens)
        else:  
            return tokens

    @staticmethod
    def tokenize(text):
        tokens = word_tokenize(text)
        splitted = []
        for w in tokens:
            splitted += re.split(r'(\d+)', w)
        return splitted

    @staticmethod
    def remove_punctuation(tokens):
        future_tokens = []
        for text in tokens: 
            try:
                future_tokens.append(''.join(character for character in text if character not in string.punctuation))
            except TypeError as e:
                print(f'Error removing punctuation from token:\n{e}')
        return future_tokens
        
    @staticmethod
    def remove_numeric(tokens):
        return [w for w in tokens if not w.isdigit()]

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


class RecursiveNamespace(SimpleNamespace):

  @staticmethod
  def map_entry(entry):
    if isinstance(entry, dict):
      return RecursiveNamespace(**entry)

    return entry

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    for key, val in kwargs.items():
      if type(val) == dict:
        setattr(self, key, RecursiveNamespace(**val))
      elif type(val) == list:
        setattr(self, key, list(map(self.map_entry, val)))


if __name__ == '__main__':
    cleaner = TextCleaner()
    text = '''I'll be there within 5min. Shouldn't you be there too?
            I'd love to see u there my dear. It's awesome to meet new friends.
            We've been waiting for this day hélas for so long.'''
    cleaner.white_list = []
    cleaner.black_list = []

    print(cleaner.settings.lower_case.active)
    cleaner.lang_settings['french']['active'] = False
    cleaner.settings.remove_stopword
    cleaned_text = cleaner.clean_text(text)
    print(cleaned_text)

