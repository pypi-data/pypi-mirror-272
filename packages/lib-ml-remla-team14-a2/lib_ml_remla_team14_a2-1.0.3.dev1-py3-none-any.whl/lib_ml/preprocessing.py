from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

class TextPreprocessor:
    DEFAULT_CONFIG = {
        'lower': True,
        'char_level': True,
        'oov_token': '-n-',
        'sequence_length': 200
    }

    def __init__(self, config={}):
        config = {**self.DEFAULT_CONFIG, **config}
        self.tokenizer = Tokenizer(
            lower=config['lower'],
            char_level=config['char_level'],
            oov_token=config['oov_token']
        )
        self.sequence_length = config['sequence_length']

    def fit_text(self, text_list):
        self.tokenizer.fit_on_texts(text_list)
        self.char_index = self.tokenizer.word_index
        return self.char_index

    def transform_text(self, text_list):
        sequences = self.tokenizer.texts_to_sequences(text_list)
        padded_sequences = pad_sequences(sequences, maxlen=self.sequence_length)
        return padded_sequences