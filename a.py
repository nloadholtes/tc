#
# a.py
# April 19, 2012
# Nick Loadholtes <nick@ironboundsoftware.com>
#
# Analysis of tweets
#
import sys
from classifiers.classify_tweets import Emotion
from load_tweets import loadTweets
import json

def scoreTweet(tweet, classifier):
    """Looks at the tweet and gives it a score based on
    the type of classifier we are dealing with."""
    return classifier.classify(tweet)

def saveScore(tweet, score, collection, lt):
    tweet.score = score
    lt.update_tweet(tweet, collection)

def getTweets(collection, lt):
    tweets = lt.get_stored_tweets(collection)
    return tweets

if __name__ == '__main__':
    print("Examining tweets (Emotion)")
    if len(sys.argv) < 2:
        print("A search query is needed")
        exit(-1)

    lt = loadTweets()
    collectionname = sys.argv[1]
    tweets_cursor = getTweets(collectionname, lt)
    tweets = []
    for t in tweets_cursor:
        tweets.append(t)
    f = open(collectionname +".json", "w")
    f.write(str(tweets))
    f.close()
