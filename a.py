#
# a.py
# April 19, 2012
# Nick Loadholtes <nick@ironboundsoftware.com>
#
# Analysis of tweets
#

from classifiers.classify_tweets import Emotion
from load_tweets import loadTweets

def scoreTweet(tweet, classifier):
    """Looks at the tweet and gives it a score based on
    the type of classifier we are dealing with."""
    return classifier.classify(tweet)

def saveScore(tweet, score, collection, lt):
    tweet.score = score
    lt.update_tweet(tweet, collection)

if __name__ == '__main__':
    print("Examining tweets (Emotion)")

