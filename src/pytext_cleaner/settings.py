from types import SimpleNamespace

class Settings:
    def __init__(self) -> None:
        pass

class CleanerSettings(Settings):
    def __init__(self) -> None:
        super().__init__()
        self.remove_punctuation = SimpleNamespace({'active': True, 'action': self.remove_punctuation})
        self.remove_numeric = {'active': True, 'action': self.remove_numeric}
        self.lower_case = {'active': True, 'action': self.lowerize}
        self.remove_stopword = SimpleNamespace({'active': True, 'action': self.remove_stopwords})
        self.stemming = {'active': False, 'action': self.stemming}
        self.too_long = {'active': True, 'action': self.too_long}

class LangSettings(Settings):
    def __init__(self) -> None:
        super().__init__()