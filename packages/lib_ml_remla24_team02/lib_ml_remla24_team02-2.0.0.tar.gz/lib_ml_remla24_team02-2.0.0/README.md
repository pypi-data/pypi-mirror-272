# lib_ml_remla24_team02

This Python package provides data pre-processing tools for the [phishing machine learning model](https://github.com/remla24-02/model-training) of team 2 of the REMLA course taught at the TU Delft. The package is available on [PyPI](https://pypi.org/project/lib_ml_remla24_team02/).

## Installation

To install this package, run `poetry add lib_ml_remla24_team02`.

## Usage

After installation, the package can be used as follows:

```
from lib_ml_remla24_team02 import data_preprocessing


example_url = "www.test.com"
preprocessed_url = data_preprocessing.preprocess_single(example_url) # Returns a tokenized URL

data_dir = 'path/to/your/data' # Path to training data
output_dir = 'path/to/save/processed/data' # Path for joblib output
data_preprocessing.preprocess(data_dir, output_dir) # Pre-processes the whole dataset

```