"""
Preprocess the data to be trained by the learning algorithm.
"""
import os, sys, logging
import importlib.resources as pkg_resources
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer  # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences  # type: ignore
from joblib import dump, load


def load_data(data_dir):
    """
    Loading the dataset.
    """
    paths = {
        'train': os.path.join(data_dir, 'train.txt'),
        'test': os.path.join(data_dir, 'test.txt'),
        'val': os.path.join(data_dir, 'val.txt')
    }
    data = {}

    for key, path in paths.items():
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            data[f'raw_x_{key}'] = [line.split("\t")[1].strip() for line in lines]
            data[f'raw_y_{key}'] = [line.split("\t")[0].strip() for line in lines]

    raw_x = [data["raw_x_train"], data["raw_x_test"], data["raw_x_val"]]
    raw_y = [data["raw_y_train"], data["raw_y_test"], data["raw_y_val"]]

    return raw_x, raw_y


def tokenize_data(raw_x):
    """
    Tokenizing the data for training.
    """
    raw_x_train, raw_x_test, raw_x_val = raw_x

    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(raw_x_train + raw_x_val + raw_x_test)

    char_index = tokenizer.word_index
    sequence_length = 200

    x_train = pad_sequences(tokenizer.texts_to_sequences(
        raw_x_train), maxlen=sequence_length)
    x_val = pad_sequences(tokenizer.texts_to_sequences(
        raw_x_val), maxlen=sequence_length)
    x_test = pad_sequences(tokenizer.texts_to_sequences(
        raw_x_test), maxlen=sequence_length)

    return x_train, x_val, x_test, char_index


def encode_data(raw_y):
    """
    Encoding the data for training.
    """
    raw_y_train, raw_y_test, raw_y_val = raw_y

    encoder = LabelEncoder()

    y_train = encoder.fit_transform(raw_y_train)
    y_val = encoder.transform(raw_y_val)
    y_test = encoder.transform(raw_y_test)

    return y_train, y_val, y_test, encoder


def preprocess(data_dir, output_dir):
    """
    Preprocessing the data for training.
    """
    raw_x, raw_y = load_data(data_dir)
    x_train, x_val, x_test, char_index = tokenize_data(raw_x)
    y_train, y_val, y_test, encoder = encode_data(raw_y)

    os.makedirs(output_dir, exist_ok=True)

    # Dumping the data
    dump(x_train, os.path.join(output_dir, 'preprocessed_x_train.joblib'))
    dump(x_val, os.path.join(output_dir, 'preprocessed_x_val.joblib'))
    dump(x_test, os.path.join(output_dir, 'preprocessed_x_test.joblib'))
    dump(char_index, os.path.join(output_dir, 'char_index.joblib'))

    dump(y_train, os.path.join(output_dir, 'preprocessed_y_train.joblib'))
    dump(y_val, os.path.join(output_dir, 'preprocessed_y_val.joblib'))
    dump(y_test, os.path.join(output_dir, 'preprocessed_y_test.joblib'))
    dump(encoder, os.path.join(output_dir, 'label_encoder.joblib'))


def preprocess_single(url):
    """
    Preprocess a single URL.
    """
    sequence_length = 200
    with pkg_resources.path('lib_ml_remla24_team02.data', 'char_index.joblib') as model_path:
        char_index = load(model_path)

        sequence = []
        for char in url:
            sequence.append(char_index.get(char, char_index.get('-n-', 1)))

        return pad_sequences([sequence], maxlen=sequence_length)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Incorrect arguments. Usage: python data_preprocessing.py <data_dir> <output_dir>")
        sys.exit(1)

    data_dir, output_dir = sys.argv[1], sys.argv[2]
    preprocess(data_dir, output_dir)
