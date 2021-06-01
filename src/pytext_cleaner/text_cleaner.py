# Standard libraries
import contractions
import re
import string
import enum

# Nltk download
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextCleaner:
    def __init__(self):
        self.settings = ['rm_punctuation', 'rm_numeric', 'lowerize', 'rm_stopwords']
               
        self.white_list = []
        self.black_list = []
        self.lang_settings = ['english']

    def lang_stopwords(self):
        stop_words = set()
        [stop_words.update(set(stopwords.words(lang.lower()))) for lang in self.lang_settings]
        return stop_words

    def action_settings(self):
        """ map settings to their respective actions. """
        settings = {
            'rm_punctuation': self.remove_punctuation,
            'rm_numeric'    : self.remove_numeric,
            'lowerize'      : self.lowerize,
            'rm_stopwords'  : self.remove_stopwords,
            'stem_words'    : self.stemming,
            'rm_long_words' : self.remove_long_words
        }
        return settings


    def clean_text(self, to_clean, **kwargs):
        to_clean = contractions.fix(to_clean) # Expand contractions
        tokens = self.tokenize(to_clean)

        for param in self.settings:
            tokens = self.action_settings()[param](tokens)
            
        [tokens.remove(w) for w in tokens if w == ''] # Remove empty tokens

        if 'tokenize' in kwargs:
            if kwargs['tokenize']:
                return tokens
        else:  
            return ' '.join(tokens)

    @staticmethod
    def tokenize(text):
        """ Tokenize string and split numeric and alpha characters 
        
            :return: list of tokens
        """
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
    def remove_long_words(tokens):
        return [w for w in tokens if len(w) < 13]

    def create_stopwords(self):
        stop_words = set(self.black_list)
        stop_words.update(self.lang_stopwords())
        stop_words = [w for w in stop_words if w not in self.white_list]
        return stop_words


if __name__ == '__main__':
    cleaner = TextCleaner()
    text = '''I'll be there within 5min. Shouldn't you be there too?
            I'd love to see u there my dear. It's awesome to meet new friends.
            We've been waiting for this day hélas for so long.'''
    cleaner.white_list = []
    cleaner.black_list = []
    cleaned_text = cleaner.clean_text(text)
    print(cleaned_text)

