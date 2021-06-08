import unittest

from src.pytext_cleaner.text_cleaner import TextCleaner

class TestTextTransformation(unittest.TestCase):
    
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.text_cleaner = TextCleaner()

    def test_tokenization(self):
        text = 'Text 2clean.'
        tokens = self.text_cleaner.tokenize(text)
        self.assertEqual(tokens, ['Text', '2', 'clean', '.'])
    
    def test_rm_punctuation(self):
        tokens = ['Text', '2', 'clean', '.']
        tokens = self.text_cleaner.remove_punctuation(tokens)
        self.assertEqual(tokens, ['Text', '2', 'clean'])

    def test_lowerize(self):
        tokens = ['TexT', 'To', 'lower']
        tokens = self.text_cleaner.lowerize(tokens)
        self.assertEqual(tokens, ['text', 'to', 'lower'])

    def test_rm_empty(self):
        tokens = ['text', '', 'with', 'empty', '']
        tokens = self.text_cleaner.rm_empty_tokens(tokens)
        self.assertEqual(tokens, ['text', 'with', 'empty'])

    def test_rm_numeric(self):
        tokens = ['remove', '15', 'digits', '1']
        tokens = self.text_cleaner.remove_numeric(tokens)
        self.assertEqual(tokens, ['remove', 'digits'])

    def test_rm_long_words(self):
        tokens = ['removethislongwords', 'ok?']
        tokens = self.text_cleaner.remove_long_words(tokens)
        self.assertEqual(tokens, ['ok?'])

    def test_remove_stopwords(self):
        self.text_cleaner.black_list = ['common']
        self.text_cleaner.white_list = ['be']
        tokens = ['remove', 'common', 'words', 'to', 'be']
        tokens = self.text_cleaner.remove_stopwords(tokens)
        self.assertEqual(tokens, ['remove', 'words', 'be'])

    def test_stemming(self):
        tokens = ['words', 'for', 'stemming', 'examples']
        tokens = self.text_cleaner.stemming(tokens)
        self.assertEqual(tokens, ['word', 'for', 'stem', 'exampl'])


if __name__ == '__main__':
    unittest.main()
