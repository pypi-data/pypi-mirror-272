from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def tokenize_features(train_features, val_features, test_features, sequence_length=200):
    """
    Tokenizes the given features using a pre-loaded tokenizer and returns the tokenized features.
    """
    # Initialize tokenizer
    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(train_features + val_features + test_features)

    # Tokenize and pad sequences
    x_train = pad_sequences(tokenizer.texts_to_sequences(train_features), maxlen=sequence_length)
    x_val = pad_sequences(tokenizer.texts_to_sequences(val_features), maxlen=sequence_length)
    x_test = pad_sequences(tokenizer.texts_to_sequences(test_features), maxlen=sequence_length)

    return x_train, x_val, x_test, tokenizer

def tokenize_url(tokenizer, url, sequence_length=200):
    """
    Tokenizes the given url using a pre-loaded tokenizer and returns the tokenized sequence.
    """
    return pad_sequences(tokenizer.texts_to_sequences([url]), maxlen=sequence_length)

