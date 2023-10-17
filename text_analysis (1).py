# -*- coding: utf-8 -*-
"""Text Analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u-9ExBBNXVkO_xhCeA7nJnoqERH4BLJP
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read input Excel file
input_df = pd.read_excel("Input (1).xlsx")

# Function to extract article text from URL
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract article title and text (modify these selectors based on the structure of the website)
    title_element = soup.find("h1")
    article_text_elements = soup.find_all("p")

    # Check if title and article_text_elements exist
    if title_element:
        title = title_element.text.strip()
    else:
        title = "No Title Found"  # or whatever default title you want

    if article_text_elements:
        article_text = "\n".join([p.text for p in article_text_elements])
    else:
        article_text = "No Article Text Found"  # or whatever default text you want

    return title, article_text

# Extract article data and store it in a list of dictionaries
article_data_list = []
for index, row in input_df.iterrows():
    url = row["URL"]
    title, article_text = extract_article_text(url)
    article_data_list.append({
        "URL": url,
        "Title": title,
        "ArticleText": article_text
    })

# Convert the list of dictionaries to a Pandas DataFrame
article_df = pd.DataFrame(article_data_list)

# Save the extracted data to a new Excel file (optional)
article_df.to_excel("ExtractedData.xlsx", index=False)

print("Textual data extraction completed.")

df = pd.read_excel("ExtractedData.xlsx")

df

df.isnull().sum()

df.shape

df.nunique()

!pip install tqdm
import re
import string
from tqdm.notebook import tqdm
import dateutil.parser
!pip install pyspellchecker i
from datetime import datetime

import nltk
from spellchecker import SpellChecker
from nltk.sentiment.vader import  SentimentIntensityAnalyzer as SIA

from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords
import random

nltk.download('vader_lexicon')
nltk.download('stopwords')

languages=stopwords.fileids()
print("number of supported languages:",len(languages))
print("support language",languages)

nltk.download('punkt')
nltk.download('stopwords')

import re
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string

english_stopwords = set(stopwords.words('english'))
hinglish_stopwords = set(stopwords.words('hinglish'))

def clean_title(Title):
    # Remove URL, hashtag, mention, and special characters
    Title = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", Title)
    Title = re.sub(r"[^\w\s]", "", Title)

    # Tokenize the tweet
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    tokens = tokenizer.tokenize(Title)

    # Remove stopwords for English and Hinglish
    tokens = [token for token in tokens if token not in english_stopwords and token not in hinglish_stopwords]

    # Remove punctuation and convert to lowercase
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]
    tokens = [token.lower() for token in tokens]

    # Join tokens back into a string
    cleaned_title = ' '.join(tokens)
    return cleaned_title

df['cleaned_title'] = df['Title'].apply(clean_title)

df.head()

df.tail()

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove leading and trailing whitespaces
    cleaned_text = text.strip()
    return cleaned_text

df.cleaned_title=df.cleaned_title.apply(lambda x:clean_text(x))

df.head()

def clean_Article(ArticleText):
    # Remove URL, hashtag, mention, and special characters
    ArticleText = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", ArticleText)
    ArticleText = re.sub(r"[^\w\s]", "", ArticleText)

    # Tokenize the article text
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    tokens = tokenizer.tokenize(ArticleText)

    # Remove stopwords for English and Hinglish
    tokens = [token for token in tokens if token not in english_stopwords and token not in hinglish_stopwords]

    # Remove punctuation and convert to lowercase
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]
    tokens = [token.lower() for token in tokens]

    # Join tokens back into a string
    cleaned_Article = ' '.join(tokens)
    return cleaned_Article

df['cleaned_Article'] = df['ArticleText'].apply(clean_Article)

df

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove leading and trailing whitespaces
    cleaned_Article = text.strip()
    return cleaned_Article

df.cleaned_Article=df.cleaned_Article.apply(lambda x:clean_text(x))

df.head()

def tokenizatio(text):
  tokens=re.split('W+',text)
  return tokens

df.cleaned_title=df.cleaned_title.apply(lambda x:tokenizatio(x))

df.cleaned_title

df.cleaned_Article=df.cleaned_Article.apply(lambda x:tokenizatio(x))

df.cleaned_Article

nltk.download('wordnet')
nltk.download('omw-1.4')

def lemmatizer(telemmatizerxt):
  lemm_text="".join([wordnet_lemmatizer.lemmatize(word) for word in text])
  return lemm_text

from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

def lemmatizer(text):
    lemm_text = "".join([wordnet_lemmatizer.lemmatize(word) for word in text])
    return lemm_text

!pip install langdetect

from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None

df['language'] = df['cleaned_title'].apply(detect_language)

df.head()

df['language'].value_counts()

# Import pandas library if not already imported
import pandas as pd

# Assuming 'cleaned_title' column contains lists
# Explode the lists into separate rows
exploded_df = df.explode('cleaned_title')

# Get unique values from the exploded column
unique_titles = exploded_df['cleaned_title'].unique()

# Print or use unique_titles as needed
print(unique_titles)

spell=SpellChecker()

def label_sentiment(x:float):
  if x<-0.05: return 'negative'
  if x>0.35: return 'pasitive'
  return 'natural'

sia=SIA()

# Convert all elements to strings
df['cleaned_title'] = df['cleaned_title'].astype(str)

# Now apply the sentiment analysis
df['sentiment'] = [sia.polarity_scores(x)['compound'] for x in tqdm(df['cleaned_title'])]
df['overall_sentiment'] = df['sentiment'].apply(label_sentiment)

df

df['overall_sentiment'].unique()

df['overall_sentiment'].value_counts()

df1=df[['overall_sentiment','cleaned_title']]

df1

from nltk.tokenize import word_tokenize
# Sample financial text
financial_text = "Your financial text goes here."

# Sample positive and negative dictionaries
positive_words = ["positive", "good", "profit", ...]  # Add positive words to the list
negative_words = ["negative", "loss", "bad", ...]  # Add negative words to the list

# Step 1: Text Preparation
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(financial_text.lower())  # Tokenize and convert to lowercase
cleaned_words = [word for word in word_tokens if word.isalpha() and word not in stop_words]

# Step 2: Positive and Negative Dictionaries
positive_score = sum(1 for word in cleaned_words if word in positive_words)
negative_score = sum(1 for word in cleaned_words if word in negative_words)

# Step 3: Polarity Score Calculation
polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

# Step 4: Subjectivity Score Calculation
subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)

# Results
print("Positive Score:", positive_score)
print("Negative Score:", negative_score)
print("Polarity Score:", polarity_score)
print("Subjectivity Score:", subjectivity_score)

!pip install nltk
!pip install syllable

import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict, stopwords

# Download NLTK resources (if not already downloaded)

nltk.download('cmudict')

# Sample financial text
financial_text = "Your financial text goes here."

# Step 1: Text Preparation
stop_words = set(stopwords.words('english'))
sentences = sent_tokenize(financial_text)
word_tokens = word_tokenize(financial_text.lower())  # Tokenize and convert to lowercase
cleaned_words = [word for word in word_tokens if word.isalpha() and word not in stop_words]

# Step 2: Average Number of Words Per Sentence
average_words_per_sentence = len(cleaned_words) / len(sentences)

# Step 3: Complex Word Count (words with more than two syllables)
pronouncing_dict = cmudict.dict()
complex_words = [word for word in cleaned_words if len(pronouncing_dict.get(word, [])) > 2]
complex_word_count = len(complex_words)

complex_word_count

# Step 4: Word Count
word_count = len(cleaned_words)

# Step 5: Syllable Count Per Word
def count_syllables(word):
    return max([len(list(y for y in x if y[-1].isdigit())) for x in pronouncing_dict[word.lower()]])

syllable_count_per_word = [count_syllables(word) for word in cleaned_words]

# Step 6: Personal Pronouns Count
personal_pronouns = ['i', 'we', 'my', 'ours', 'us']
personal_pronoun_count = sum(1 for word in cleaned_words if word in personal_pronouns)

# Step 7: Average Word Length
average_word_length = sum(len(word) for word in cleaned_words) / len(cleaned_words)

# Results
print("Average Number of Words Per Sentence:", average_words_per_sentence)
print("Complex Word Count:", complex_word_count)
print("Word Count:", word_count)
print("Syllable Count Per Word:", syllable_count_per_word)
print("Personal Pronouns Count:", personal_pronoun_count)
print("Average Word Length:", average_word_length)

import wordcloud
import matplotlib.pyplot as plt

from wordcloud import WordCloud
data=df['cleaned_title']
plt.figure(figsize=[10,7])
wc=WordCloud(max_words=1000,width=1600,height=800,
             collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

data=df1[df1['overall_sentiment']=='pasitive']['cleaned_title']
plt.figure(figsize=[10,7])
wc=WordCloud(max_words=1000,width=1600,height=800,
             collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

data=df1[df1['overall_sentiment']=='negative']['cleaned_title']
plt.figure(figsize=[10,7])
wc=WordCloud(max_words=1000,width=1600,height=800,
             collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

data=df1[df1['overall_sentiment']=='natural']['cleaned_title']
plt.figure(figsize=[10,7])
wc=WordCloud(max_words=1000,width=1600,height=800,
             collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

import matplotlib.pyplot as plt
from wordcloud import WordCloud

if not data.empty:
    plt.figure(figsize=[10, 7])
    wc = WordCloud(max_words=1000, width=1600, height=800, collocations=False).generate(" ".join(data))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
else:
    print("NO data for 'neutral' sentiment. Unable to generate WordCloud.")

df1

X=df1['cleaned_title']
y=df1['overall_sentiment']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=101)

from sklearn.feature_extraction.text import CountVectorizer
vect=CountVectorizer()
vect.fit(X_train)

X_train_dtm=vect.transform(X_train)
X_test_dtm=vect.transform(X_test)

vect_tunned = CountVectorizer(stop_words='english', ngram_range=(1, 2), min_df=0.1, max_df=0.7, max_features=100)

vect_tunned

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer=TfidfTransformer()
tfidf_transformer.fit(X_train_dtm)
X_train_tfidf=tfidf_transformer.transform(X_train_dtm)

X_train_tfidf

texts=df1['cleaned_title']
target=df1['overall_sentiment']

from keras.preprocessing.text import Tokenizer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
vocab_length = len(tokenizer.word_index) + 1
vocab_length

!pip install tensorflow

import tensorflow as tf
 from tensorflow.keras.preprocessing.sequence import pad_sequences
 from nltk.tokenize import word_tokenize

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def embed(corpus):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    return tokenizer.texts_to_sequences(corpus)

# Assuming df1 is your DataFrame containing 'cleaned_english_tweets' column
texts = df1["cleaned_title"]

# Use your 'embed' function to convert text sequences to integer sequences
train_padded_sentences = pad_sequences(
    embed(texts),
    padding='post'
)

train_padded_sentences

embeddings_dictionary=dict()
embedding_dim=100
#load Slove 100d embeddings
with open('glove.6B.100d.txt',encoding='utf8') as fp:
  for line in fp.reaadlines():
    records=liine.split()
    word=records[0]
    vector_dimensions=np.asarray(records[1:],dtype='float32')
    embeddings_dictionary [word]=vector_dimensions

import numpy as np

embeddings_dictionary = dict()
embedding_dim = 100
glove_file = 'glove.6B.100d.txt'

with open(glove_file, encoding='utf8') as fp:
    for line in fp.readlines():
        records = line.split()
        word = records[0]
        vector_dimensions = np.asarray(records[1:], dtype='float32')
        embeddings_dictionary[word] = vector_dimensions

from sklearn.naive_bayes import MultinomialNB
nb=MultinomialNB()

nb.fit(X_train_dtm,y_train)

y_pred_class=nb.predict(X_test_dtm)
y_pred_prob=nb.predict_proba(X_test_dtm)[:,1]

from sklearn import metrics
print(metrics.accuracy_score(y_test,y_pred_class))

from sklearn .feature_extraction.text import TfidfTransformer,CountVectorizer

from sklearn.pipeline import Pipeline
pipe=Pipeline([
               ('bow',CountVectorizer()),
               ('tfid',TfidfTransformer()),
               ('model',MultinomialNB())
])

pipe.fit(X_train,y_train)
y_pred_class=pipe.predict(X_test)
print(metrics.accuracy_score(y_test,y_pred_class))

from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()
y_encoded=le.fit_transform(y)

X_train,X_test,y_train,y_test=train_test_split(X,y_encoded,test_size=0.2,random_state=101)

import xgboost as xgb

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb

pipe = Pipeline([
    ('bow', CountVectorizer()),  # Bag-of-words representation
    ('tfidf', TfidfTransformer()),  # TF-IDF transformation
    ('model', xgb.XGBClassifier(
        learning_rate=0.1,
        max_depth=7,
        n_estimators=80,
        use_label_encoder=False,
        eval_metric='auc'  # Corrected 'evel_metrics' to 'eval_metric'
    ))
])

pipe.fit(X_train,y_train)

y_pred=pipe.predict(X_test)

from sklearn.metrics import accuracy_score

acc=accuracy_score(y_test,y_pred)
print('Test accuracy',acc)

