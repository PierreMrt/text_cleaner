# Text cleaning with Natural Language Processing

:yellow_circle: _in progress_

Python library using Natural Language Processing (NLP) to easily and quickly clean text.

Automaticaly tokenize text, remove punctuation and special characters, normalize the case, remove stopwords in various languages, stem words... with this simple yet customizable library.

## Usage

**Install**  :

> pip install pytext_cleaner

**Example** : 

```
from pytext_cleaner import TextCleaner

cleaner = TextCleaner()
cleaner.settings = ['rm_punctuation', 'rm_numeric', 'lowerize']
cleaner.lang_setting = ['italian', 'french']
clean_text = cleaner.clean_text(string_to_clean)
```

## Customize

**Default settings**: `['rm_punctuation', 'rm_numeric', 'lowerize', 'rm_stopwords']`

**Available settings** are : 

 * rm_punctuation
 * rm_numeric
 * lowerize
 * rm_stopwords
 * stem_words
 * rm_long_words

**Default language settings**: `['english']`

**To include or exclude stopwords**:
```
cleaner.white_list = ['words', 'to', 'include']
cleaner.black_list = ['words', 'to', 'exclude']
```

**Change return type**:

By default, text_cleaner return a modified string.

To return of list of tokens, add tokenize=True:

`cleaner.clean_text(string_to_clean, tokenize=True)`
