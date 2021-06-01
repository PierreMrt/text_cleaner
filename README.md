# Text cleaning with Natural Language Processing

:yellow_circle: in progress

Python library using Natural Language Processing (NLP) to easily and quickly clean text.

Automaticaly tokenize text, remove punctuation and special characters, normalize the case, remove stopwords in various languages, stem words... with this simple yet customizable library.

## Usage

<u>Install</u>  :

`pip install pytext_cleaner`

<u>Example</u> : 

```
from pytext_cleaner import TextCleaner

cleaner = TextCleaner()
cleaner.settings['rm_stopwords']['activate'] = True
cleaner.lang_setting['french']['activate'] = True
clean_text = cleaner.clean_text(string_to_clean, tokenize=True)
```