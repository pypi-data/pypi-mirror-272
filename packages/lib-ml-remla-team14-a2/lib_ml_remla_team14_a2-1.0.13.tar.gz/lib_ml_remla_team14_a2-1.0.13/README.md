# lib_ml_remla_team14_a2

lib_ml_remla_team14_a2 contains pre-processing logic for data used in our ML training pipeline.

## Features

- Tokenization of text data at a character level.
- Padding of text sequences to uniform lengths.

## Installation

Install lib_ml_remla_team14_a2 using pip:

```bash
pip install lib_ml_remla_team14_a2
```

## Usage

### Importing the Class

```bash
from lib_ml.preprocessing import TextPreprocessor

```

### Initializing the Preprocessor'

You can customize the behavior of the `TextPreprocessor` by adjusting its configuration. Here's how to initialize it with the default settings:

```bash
preprocessor = TextPreprocessor()

```

Or customize its behavior:

```bash
config = {
    'lower': True,
    'char_level': True,
    'oov_token': '-n-',  # Token used for out-of-vocabulary characters
    'sequence_length': 150  # Adjust sequence length as needed
}
preprocessor = TextPreprocessor(config=config)

```

### Preprocessing Text Data

Use the `fit_text` method to fit the tokenizer on your text data, and `transform_text` to convert text data into padded sequences:

```bash
texts = ["hello", "world"]
preprocessor.fit_text(texts)
processed_texts = preprocessor.transform_text(texts)

```


### Output

The `transform_text` method returns an array of tokenized and padded sequences, ready for use in training or inference:

```bash
print(processed_texts)  # Output will be a NumPy array of processed text data

```
