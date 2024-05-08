def practical7():
    print('''
!pip install nltk

import numpy as np
import pandas as pd
import math
from collections import Counter
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

from nltk import pos_tag
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

from sklearn.feature_extraction.text import TfidfVectorizer

document=""" The sun rises in the east and sets in the west. Birds chirp in the morning, signaling the start of a new day. People wake up, drink coffee, and prepare for work or school. Traffic fills the streets, and life carries on amidst the hustle and bustle of the city."""

words=word_tokenize(document)
print("Original Words :",words)

pos = pos_tag(words)
print('pos_tagging :',pos)

stop_words=set(stopwords.words('english'))
filtered_token=[word for word in words if word.lower() not in stop_words and word not in string.punctuation]
print('stop words removed: ',filtered_token)

stemmer = PorterStemmer()
stemmed_token = [stemmer.stem(word) for word in filtered_token]
print("Stemmed token: ",stemmed_token)

lemmatizer = WordNetLemmatizer()
lemmatized_words=[lemmatizer.lemmatize(word) for word in filtered_token]
print("Lemamatization: ",lemmatized_words)

documents=[document]
tfidf_vectorizer=TfidfVectorizer()
tfidf_matrix=tfidf_vectorizer.fit_transform(documents)
terms=tfidf_vectorizer.get_feature_names_out()
print("TF-IDF Matrix: ")
print(tfidf_matrix.toarray())
print("Terms: ",terms)

''')
practical7()