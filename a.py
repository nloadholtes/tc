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
import simplejson as json
import datetime

def scoreTweet(tweet, classifier):
    """Looks at the tweet and gives it a score based on
    the type of classifier we are dealing with."""
    return classifier.classify(tweet['text'])

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

    # lt = loadTweets()
    collectionname = sys.argv[1]
    # tweets_cursor = getTweets(collectionname, lt)
    tweets = []
    # for t in tweets_cursor:
    #     tweets.append(t)
    # f = open(collectionname +".json", "w")
    # dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    # f.write(json.dumps(tweets,default=dthandler))
    # f.close()

    #Load from the test file
    f = open(collectionname+".json", "r")
    data = f.read()
    #print(data)
    tweets = json.loads(data)
    f.close()
    print("Number of tweets:" + str(len(tweets)))
    emotion = Emotion()
    avg = 0.0
    total = len(tweets)
    bad = 0
    good = 0
    neutral = 0
    n_tweets = []
    for t in tweets:
        if ' -- ' in t['text']:
            continue
        score = scoreTweet(t, emotion)
        if score >0:
            good += 1
        if score == 0:
            neutral += 1
            n_tweets.append(t['text'])
        if score < 0:
            bad += 1
        avg += score

    print("Average: " + str(avg/total))
    print("G,b,n: %d,%d,%d" %(good, bad, neutral))
    for x in range(141,155):
        print(n_tweets[x]+"\n")
