from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class Preprocessing:
    def __init__(self):
        self.tokenizer = None
        self.encoder = None
        self.char_index = None
        

    def transform_input(self, url, sequence_length):
        """Transforms new url data using the fitted tokenizer."""
        if not self.tokenizer:
            raise ValueError("The tokenizer is not fitted yet. Please initialize or fit the tokenizer before transforming data.")
        return pad_sequences(self.tokenizer.texts_to_sequences(url), maxlen=sequence_length)

    def transform_labels(self, raw_y):
        """Transforms new label data using the fitted encoder."""
        if not self.encoder:
            raise ValueError("The encoder is not fitted yet. Please initialize or fit the encoder before transforming data.")
        return self.encoder.transform(raw_y)

    def fit_transform(self, train, test, val, sequence_length=200):
        """Fits the tokenizer and encoder on the training data and transforms all datasets."""
        raw_x_train = [line.split("\t")[1] for line in train]
        raw_y_train = [line.split("\t")[0] for line in train]

        raw_x_test = [line.split("\t")[1] for line in test]
        raw_y_test = [line.split("\t")[0] for line in test]

        raw_x_val=[line.split("\t")[1] for line in val]
        raw_y_val=[line.split("\t")[0] for line in val]

        self.tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
        self.tokenizer.fit_on_texts(raw_x_train + raw_x_val + raw_x_test)
        self.char_index = self.tokenizer.word_index

        x_train = self.transform_input(raw_x_train, sequence_length)
        x_val = self.transform_input(raw_x_val, sequence_length)
        x_test = self.transform_input(raw_x_test, sequence_length)

        self.encoder = LabelEncoder()
        y_train = self.encoder.fit_transform(raw_y_train)
        y_val = self.encoder.transform(raw_y_val)
        y_test = self.encoder.transform(raw_y_test)

        return x_train, y_train, x_val, y_val, x_test, y_test
    
    def get_tokenizer(self):
        """Returns the fitted tokenizer."""
        return self.tokenizer
    
    def get_char_index(self):
        """Returns the char index of the fitted tokenizer."""
        return self.char_index
    
    def get_encoder(self):
        """Returns the fitted encoder."""
        return self.encoder
    
    def set_tokenizer(self, tokenizer):
        """Sets the tokenizer to the provided tokenizer."""
        self.tokenizer = tokenizer

    def set_encoder(self, encoder):
        """Sets the encoder to the provided encoder."""
        self.encoder = encoder
