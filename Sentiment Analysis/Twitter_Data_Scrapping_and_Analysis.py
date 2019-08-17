# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 08:39:26 2019

@author: abhil
"""
# Importing the Required Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from twitterscraper import query_tweets
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Specifying the start and end date till which you want to scrap the twitter data.
begin_date = dt.date(2019,8,4)
end_date = dt.date(2019,8,17)

# This command will query the data based on the hashtag '#Article370'
#The limit is used to state the number of max number tweets that you want to scrap.
tweets = query_tweets("#Article370", begindate= begin_date, enddate= end_date, limit = 1000000, lang= 'eng')
                
                      
# Here we are Converting first the tweets into Dictionary then we are converting it into a DataFrame:                   
tweet_data = pd.DataFrame(t.__dict__ for t in tweets)

#Here we are saving the scraped data into a csv file:
tweet_data.to_csv('D:\Practice Datasets\Twitter_Practice\Tweets_370A')        

# When we scrap the tweets we get the tweets of many different languages for the same hashstag.
# The Below defined function is used to detect the language in which a particular tweet is written in.
from langdetect import detect
def detector(x):
    try:
        return detect(x)
    except:
        None
 
#Here we apply the above function on the text column of the tweets and hence it will give the lang type for each tweet.
tweet_data['lang'] = tweet_data['text'].apply(lambda x: detector(x))

# Here we are filtering out the tweets which are written in english language:
tweet_data_1 = tweet_data[tweet_data['lang'] == 'en']

# Creating the Object of SentimentIntensityAnalyzer Class.
analyzer = SentimentIntensityAnalyzer()


# Here apply the polarity_scores function of SentimentIntensityAnalyzer class.
# it will giev the following Sentiment Metric for the tweets:
#  1. Positive
#  2. Neutral
#  3. Negative
#  4. Compound 

# The Positive, Negative and Neutral scores represent the proportion of text that falls in these categories.
# The Compound score is a metric that calculates the sum of all the lexicon ratings which have been normalized
# between -1(most extreme negative) and +1 (most extreme positive).
sentiments = tweet_data_1['text'].apply(lambda x :analyzer.polarity_scores(x))


# Here we concat the above discovered sentiment metrics into the old tweet_data_1 dataframe.
tweet_data_1 = pd.concat([tweet_data_1,sentiments.apply(pd.Series)],1)

# This will remove the duplicates tweets(eg: retweeted tweets, sponsored tweets)
tweet_data_1.drop_duplicates(subset = 'text', inplace = True)

# This will cretat a histogram:
plt.hist(tweet_data_1['compound'])
plt.xlabel('Compound Scores')
plt.ylabel('Number of Tweets')


# Based on the compound score calculated we categorize each tweet into the following 3 categories:
# 1. Positive Sentiment : compound score >= 0.05
# 2. Neutral Sentiment : compound score > - 0.05 and compound score < - 0.05
# 3. Negative Sentiment : compound score <= -0.05 
def sentiments(x):
    if x >= 0.05:
        return "Positive"
    elif x > -0.05 and x < 0.05:
        return "Neutral"
    else:
        return "Negative"
    
tweet_data_1['Sentiments']  =  tweet_data_1['compound'].apply(sentiments)


# This will create a  Pie Chart which will show the sentiments of the data on the issue:
plt.figure(figsize = (7,7))
tweet_data_1['Sentiments'].value_counts().plot(kind = 'pie', autopct = '%0.1f')
plt.ylabel("")
plt.title("Peoples Sentiments on the Revocation of 350A based on 98k Tweets")

# Saving the final data into a csv format:
tweet_data_1.to_csv('D:\Practice Datasets\Twitter_Practice\Twitter_Sentiments')