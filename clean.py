import tweepy as tw
import pandas as pd
import matplotlib.pyplot as plt
import re
import spacy
nlp = spacy.load('en_core_web_lg')
import seaborn as sns
from nltk.stem.snowball import SnowballStemmer
import preprocessor as p
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from pathlib import Path

# import API credentials
from credentials import api_credentials

my_api_key = api_credentials.get('my_api_key')
my_api_secret = api_credentials.get('my_api_secret')
bearer_token = api_credentials.get('bearer_token')
access_token = api_credentials.get('access_token')
access_token_secret = api_credentials.get('access_token_secret')

auth = tw.OAuthHandler(my_api_key, my_api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

number_of_tweets = 200
tweets = []
likes = []
time = []

for i in tw.Cursor(api.user_timeline, id='MichaelWagger', tweet_mode='extended').items(number_of_tweets):
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)

df = pd.DataFrame({'tweets': tweets, 'clean_tweets': tweets, 'likes': likes, 'time': time})

# to lower
df['clean_tweets'] = df.clean_tweets.str.lower()

# remove URLs
df.clean_tweets = df.clean_tweets.apply(lambda x: re.sub(r'https?:\/\/\S+', '', x))
df.clean_tweets = df.clean_tweets.apply(
    lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', x))

# remove RTs
df = df[~df.clean_tweets.str.contains('rt')]

# removing mentions -- confirmed works
df.clean_tweets = df.clean_tweets.apply(lambda x: re.sub(r'@[A-Za-z0-9]+', '', x))

# trying to delete the long tokenized thing -- pretty sure this works
df.clean_tweets = df.clean_tweets.apply(lambda x: re.sub(r'\w{41,}', '', x))

# remove non-letter --- need to run something that clears token thing before this
df.clean_tweets = df.clean_tweets.apply(lambda x: re.sub(r"[^a-z\s\(\-:\)\\\/\];='#]", '', x))

# strip white space
df['clean_tweets'] = df['clean_tweets'].str.strip()

# replace empty string values to NA so we can then drop them
df = df.replace(r'^s*$', float('NaN'), regex=True)
df.dropna(inplace=True)

df.shape

# view just tweets and clean tweets
df[df.columns[0:2]].head(10)

# used this to write my data to csv
"""filepath = Path(
    '/Users/michaelwagner/Dropbox/proj/data.csv')
df.to_csv(filepath, index=False)"""

# check
the_list = []
for i in df.clean_tweets:
    the_list.append(i)

# convert all twitter data into a list of words
clean_words = []
for sentence in clean_sentences:
    words = sentence.split()
    for w in words:
        clean_words.append(w)


# https://www.youtube.com/watch?v=bNDRiaFyLrs
"""
Website Resources:
https://towardsdatascience.com/how-to-easily-run-python-scripts-on-website-inputs-d5167bd4eb4b
https://towardsdatascience.com/build-a-web-data-dashboard-in-just-minutes-with-python-d722076aee2b
"""
