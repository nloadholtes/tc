#!/usr/bin/env python
#
# search.py
# Nick Loadholtes nick@ironboundsoftware.com
# April 17 2012
#
# Searches twitter, stores results for later analysis

import sys
from load_tweets import loadTweets

def retrieveTweetSearch(lt, topic):
    output = lt.retrieve_search_results(topic)
    return output


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("A search query is needed")
        exit(-1)

    collectionname = ''.join(sys.argv[1:][0].split(' '))
    lt = loadTweets()
    tweets = retrieveTweetSearch(lt, sys.argv[1:][0])
    lt.save_tweet(tweets, collectionname)
