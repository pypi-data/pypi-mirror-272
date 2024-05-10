# lib-ml
Contains the pre-processing logic for data that is used for training or queries.

## Methods
- `fit_transform(train, test, val, sequence_length=200)`: Fits the tokenizer and encoder on the training data and transforms all datasets.
- `transform_input(url, sequence_length)`: Transforms new url data using the fitted tokenizer.
- `transform_labels(raw_y)`: Transforms new label data using the fitted encoder.
- `get_tokenizer()`: Returns the fitted tokenizer.
- `get_char_index()`: Returns the char index of the fitted tokenizer.
- `get_encoder()`: Returns the fitted encoder.
- `set_tokenizer(tokenizer)`: Sets the tokenizer to the provided tokenizer.
- `set_encoder(encoder)`: Sets the encoder to the provided encoder.

## Installation
```bash
pip install lib-ml-team11
```

## Usage
```python
from lib_ml_team11 import Preprocessing

# Create an instance of the Preprocessing class
preprocessing = Preprocessing()

...

# Transform the data
x_train, y_train, x_val, y_val, x_test, y_test = preprocessing.fit_transform(train, test, val, sequence_length=200)
```

## Releasing
Create a new git tag and push it to the repository. The CI/CD pipeline will automatically publish the new version to PyPi.

```bash
git tag v0.1.0
git push origin v0.1.0
```

Note: The version number should follow the semantic versioning format, i.e., `vX.Y.Z` where `X`, `Y`, and `Z` are non-negative integers. Note that the version number should be prefixed with a `v`.

