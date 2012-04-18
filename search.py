#!/usr/bin/env python
#
# search.py
# Nick Loadholtes nick@ironboundsoftware.com
# April 17 2012
#
# Searches twitter, stores results for later analysis

from load_tweets import loadTweets

def retrieveTweetSearch(topic):
    output = []

    return output

def saveTweets(tweets):
    return


if __name__ == '__main__':
    if len(sys.arg) < 2:
        print("A search query is needed")
        exit(-1)

    tweets = retrieveTweetsSearch(sys.arg)
    saveTweets(tweets)
