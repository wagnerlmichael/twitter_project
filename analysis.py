import pandas as pd
from textblob import TextBlob

df = pd.read_csv("/Users/michaelwagner/Dropbox/proj/data.csv")
df.head()

#need to figure out how to filter our non - text blobbable words, biasing by providing too many neutrals
df['sentiment'] = df['clean_tweets'].apply(lambda x: TextBlob(x).sentiment)
df['sentiment'].head(10)

# get avg polarity across tweets
polarity_scores = []
for i in df['clean_tweets']:
    unit = TextBlob(i).sentiment[0]  # selects polarity
    polarity_scores.append(unit)

polarity_score = sum(polarity_scores) / len(df)
print(polarity_score)

# get avg subjectivity across tweets
subjectivity_scores = []
for i in df['clean_tweets']:
    unit = TextBlob(i).sentiment[1]  # selects polarity
    subjectivity_scores.append(unit)

subjectivity_score = sum(subjectivity_scores) / len(df)
print(subjectivity_score)

"""
Polarity is float which lies in the range of [-1,1] where 1 means positive
statement and -1 means a negative statement.
Subjective sentences generally refer to personal opinion, emotion or judgment
whereas objective refers to factual information.
Subjectivity is also a float which lies in the range of [0,1]
where 0.0 is very objective and 1.0 is very subjective.
"""
