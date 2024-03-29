# -*- coding: utf-8 -*-
"""IMDB dataset classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KAllYMJzmVoeQLdKpI8SWPK7V0X-OyRU

# **Sentiment Analysis on IMDB Movie Reviews**

# Kaggle API Setup and Dataset Download in Google Colab

This guide provides detailed instructions on how to set up the Kaggle API and download datasets directly into a Google Colab notebook. These steps are essential for accessing Kaggle's vast repository of datasets for data science and machine learning projects.

## Prerequisites

Before beginning, ensure you have a Kaggle account. If you do not have one, sign up at [Kaggle](https://www.kaggle.com).


### Step 1: Install Kaggle Library

First, we install the Kaggle library using pip. This library is essential for interacting with Kaggle's API to download datasets and participate in competitions.

```python
!pip install -q kaggle
```
"""

!pip install -q kaggle

"""Step 2: Upload Kaggle API Key
-----------------------------

To use Kaggle's API, you need an API key, which is a JSON file (`kaggle.json`) obtained from your Kaggle account. To download this file:

1.  Go to your Kaggle account settings.
2.  Scroll to the "API" section and click "Create New API Token".
3.  This will download the `kaggle.json` file to your computer.

Once you have the `kaggle.json` file, you need to upload it to Colab:
"""

from google.colab import files

files.upload()

"""Step 3: Set Up Kaggle API Key
-----------------------------

After uploading the API key, set it up by moving it to the `.kaggle` directory in your home folder. This step ensures that the Kaggle API can access the key for authentication:
"""

! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

"""Step 4: Download Dataset
------------------------

With the Kaggle API set up, you can now download datasets. In this example, we'll download the IMDB Dataset of 50K Movie Reviews, a dataset useful for natural language processing and sentiment analysis tasks:
"""

!kaggle datasets download -d lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re

"""Download `punkt` and `stopwords` models using nltk library"""

nltk.download('punkt')
nltk.download('stopwords')

pd.set_option('display.max_colwidth', None)

"""Step 5: Data Preprocessing
------------------

*   **Reading the Dataset**: Load the dataset into a pandas DataFrame for manipulation.
*   **Exploratory Data Analysis (EDA)**: Analyze the dataset to understand its structure, checking for class imbalance, and identifying any missing values.
*   **Text Preprocessing**: Clean and preprocess the review texts by converting to lowercase, removing special characters, and filtering out stopwords.

"""

df = pd.read_csv("/content/imdb-dataset-of-50k-movie-reviews.zip")

df.columns

df['sentiment'].value_counts()

df.shape

df.isna().sum()

df['review'] = df['review'].str.lower()

"""### Step 6: Text Preprocessing

Normalize text data by converting to lowercase, removing special characters, and filtering out stopwords.
"""

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return ' '.join(words)

df['processed_review'] = df['review'].apply(preprocess_text)

X_train, X_test, y_train, y_test = train_test_split(df['processed_review'], df['sentiment'], test_size=0.3, random_state=42)

X_train.shape, X_test.shape, y_train.shape, y_test.shape


"""Step 7.3: Feature Extraction and Model Training
--------------------------

### Neural Network Model
> Indented block Build a neural network model with Keras, incorporating embedding layers for text data. Train the model, and evaluate its performance on the test data.
"""

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping

max_words = 1000
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train)

tokenizer

train_sequences = tokenizer.texts_to_sequences(X_train)
test_sequences = tokenizer.texts_to_sequences(X_test)

all_sequences = train_sequences + test_sequences
# Calculate the lengths of all sequences
sequence_lengths = [len(seq) for seq in all_sequences]

# Plotting the histogram
plt.hist(sequence_lengths, bins=50, edgecolor='black')
plt.title('Distribution of Sequence Lengths')
plt.xlabel('Sequence Length')
plt.ylabel('Frequency')

# Calculate and display the mean and median lengths
mean_length = np.mean(sequence_lengths)
median_length = np.median(sequence_lengths)

plt.axvline(mean_length, color='red', linestyle='dashed', linewidth=2, label=f'Mean Length: {mean_length:.2f}')
plt.axvline(median_length, color='green', linestyle='dashed', linewidth=2, label=f'Median Length: {median_length}')

plt.legend()
plt.show()

max_sequence_length = max(len(seq) for seq in train_sequences + test_sequences)
max_sequence_length

max_sequence_length = 130
X_train = pad_sequences(train_sequences, maxlen=max_sequence_length)
X_test = pad_sequences(test_sequences, maxlen=max_sequence_length)

embedding_dim = 512

model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(Flatten())
# model.add(Dense(512, activation='relu'))  # Increase number of neurons
# model.add(Dropout(0.3))  # Add dropout for regularization
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))  # Add dropout for regularization
model.add(Dense(128, activation='relu'))  # Increase number of neurons
model.add(Dropout(0.4))  # Add dropout for regularization
model.add(Dense(64, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

# Train the model
model.fit(X_train, (y_train == 'positive').astype(int),
          epochs=10, batch_size=16, validation_split=0.2)
# , callbacks=[early_stopping])

loss, accuracy = model.evaluate(X_test, (y_test == 'positive').astype(int))
print(f"Test Accuracy: {accuracy*100:.2f}%")

"""Conclusion

Below are the test accruacy for all models

1.   BOW & NB : 85.88%
2.   TF-IDF & NB : 86.62%
3.   Neural Net: 81.18%


"""